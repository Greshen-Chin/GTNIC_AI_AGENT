"""Discord uses persisted dashboard rows; no real messages are sent by these tests."""
import json
from datetime import datetime, timezone

import httpx
import pytest

from app import database
from app.services import discord_service as discord


@pytest.fixture
def incident():
    return {
        "id": "incident-123", "title": "Juice Shop SQL injection attempt (Request Body)",
        "source_ip": "203.0.113.5", "severity_label": "high", "severity_score": 75,
        "status": "uncertain", "confidence_score": 0, "human_decision": "pending",
        "llm_model": "investigation-pending", "summary": "Recorded request contains a SQL pattern.",
        "raw_alert": {"timestamp": "2026-11-10T15:32:52+00:00", "agent": {"name": "juice-shop"},
                      "data": {"method": "POST", "url": "/rest/user/login", "threat_location": "Request Body"}},
        "pro_evidence": [{"claim": "Observed input", "evidence_ref": "pattern_detected=true"}],
        "contra_evidence": [], "tool_trace": [], "recommended_action": "Review the recorded request.",
    }


@pytest.fixture
def delivery(monkeypatch):
    monkeypatch.setattr(discord, "_tracked", {})
    monkeypatch.setattr(discord, "_retry_at", 0.0)
    monkeypatch.setattr(discord.settings, "DISCORD_ENABLED", True)
    monkeypatch.setattr(discord.settings, "DISCORD_BOT_TOKEN", "test-token")
    monkeypatch.setattr(discord.settings, "DISCORD_CHANNEL_ID", "123456")
    requests = []
    original_client = httpx.Client

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"id": "discord-message-1"})

    monkeypatch.setattr(discord.httpx, "Client", lambda **kwargs: original_client(
        transport=httpx.MockTransport(handler), **kwargs))
    return requests


def fields(embed):
    return {field["name"]: field["value"] for field in embed["fields"]}


def test_pending_embed_matches_dashboard_without_invented_values(incident):
    embed = discord.build_incident_embed(incident)
    data = fields(embed)
    assert embed["title"] == incident["title"]
    assert embed["description"] == incident["summary"]
    assert data["Verdict"] == "Under Review"
    assert data["Evidence Score"] == "Awaiting analysis"
    assert data["Status"] == "Active Threat"
    assert data["Target Asset"] == "juice-shop"  # not "Request Body"
    assert data["Target IP"] == "Unknown"
    assert embed["timestamp"] == incident["raw_alert"]["timestamp"]
    assert embed["url"] == "https://gtnic-hackwitgoh.vercel.app/incidents/incident-123"


@pytest.mark.parametrize("status,verdict", [("confirmed", "Malicious"), ("likely", "Suspicious"),
                                           ("uncertain", "Under Review"), ("false_positive", "Benign")])
def test_verdict_labels_follow_dashboard_mapping(incident, status, verdict):
    incident.update(status=status, llm_model="local-triage", confidence_score=0)
    data = fields(discord.build_incident_embed(incident))
    assert data["Verdict"] == verdict
    assert data["Evidence Score"] == "0%"


def test_approved_decision_does_not_claim_enforcement(incident):
    incident["human_decision"] = "approved"
    data = fields(discord.build_incident_embed(incident))
    assert data["Status"] == "Approved"
    assert "not verified" in data["Analyst Decision"]
    assert data["Suggested Mitigation"] == incident["recommended_action"]


def test_missing_and_serialized_fields_are_safe(incident):
    incident.update(raw_alert=json.dumps(incident["raw_alert"]), flags=[])
    assert fields(discord.build_incident_embed(incident))["Target Asset"] == "juice-shop"
    incident.update(raw_alert={"agent": None, "data": None}, created_at=datetime(2026, 11, 10, tzinfo=timezone.utc))
    assert discord.build_incident_embed(incident)["timestamp"] == "2026-11-10T00:00:00+00:00"
    incident.pop("created_at")
    assert "timestamp" not in discord.build_incident_embed(incident)


def test_embed_size_limits(incident):
    incident.update(title="x" * 5000, summary="x" * 8000, recommended_action="x" * 5000)
    incident["pro_evidence"] *= 100
    incident["contra_evidence"] = incident["pro_evidence"]
    embed = discord.build_incident_embed(incident)
    assert len(embed["title"]) <= 256
    assert len(embed["fields"]) <= 25
    assert all(len(field["value"]) <= 1024 for field in embed["fields"])
    length = len(embed["title"]) + len(embed["description"]) + len(embed["footer"]["text"])
    assert length + sum(len(f["name"]) + len(f["value"]) for f in embed["fields"]) <= 6000


def test_only_persisted_website_data_is_sent(incident, delivery, monkeypatch):
    monkeypatch.setattr(database, "db_fetch_incident_by_id", lambda _: incident)
    assert discord.send_discord_alert({"id": incident["id"], "title": "untrusted caller title"})
    payload = json.loads(delivery[0].content)
    assert payload["embeds"][0]["title"] == incident["title"]
    assert payload["allowed_mentions"] == {"parse": []}
    monkeypatch.setattr(database, "db_fetch_incident_by_id", lambda _: None)
    assert not discord.send_discord_alert({"id": "not-a-dashboard-record"})
    assert len(delivery) == 1


def test_one_message_is_updated_after_analysis_and_approval(incident, delivery, monkeypatch):
    monkeypatch.setattr(database, "db_fetch_incidents", lambda: [incident])
    discord._tracked[incident["id"]] = {"message_id": None, "fingerprint": None}
    discord._sync_once()
    discord._sync_once()
    assert len(delivery) == 1  # unchanged dashboard data is not sent again
    incident.update(llm_model="local-triage", status="likely", confidence_score=67)
    incident["summary"] = "Updated recorded investigation facts."
    discord._sync_once()
    incident["human_decision"] = "approved"
    discord._sync_once()
    assert [r.method for r in delivery] == ["POST", "PATCH", "PATCH"]
    assert str(delivery[-1].url).endswith("/messages/discord-message-1")
    data = fields(json.loads(delivery[-1].content)["embeds"][0])
    assert data["Evidence Score"] == "67%"
    assert data["Status"] == "Approved"


def test_rate_limit_is_respected_without_dropping_alert(incident, delivery, monkeypatch):
    clock = [100.0]
    monkeypatch.setattr(discord.time, "monotonic", lambda: clock[0])

    class Client:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def request(self, method, url, **kwargs):
            delivery.append(method)
            return httpx.Response(429 if len(delivery) == 1 else 200,
                                  json={"retry_after": 5} if len(delivery) == 1 else {"id": "message-1"},
                                  request=httpx.Request(method, url))

    monkeypatch.setattr(discord.httpx, "Client", lambda **kwargs: Client())
    assert not discord._upsert(incident, incident["id"])
    assert not discord._upsert(incident, incident["id"])
    assert len(delivery) == 1
    clock[0] = 106
    assert discord._upsert(incident, incident["id"])
    assert len(delivery) == 2


def test_temporary_empty_dashboard_read_retains_message_for_later_update(incident, delivery, monkeypatch):
    monkeypatch.setattr(database, "db_fetch_incidents", lambda: [incident])
    discord._tracked[incident["id"]] = {"message_id": None, "fingerprint": None}
    discord._sync_once()
    monkeypatch.setattr(database, "db_fetch_incidents", lambda: [])
    discord._sync_once()
    assert incident["id"] in discord._tracked
    incident.update(llm_model="local-triage", status="likely", confidence_score=70)
    monkeypatch.setattr(database, "db_fetch_incidents", lambda: [incident])
    discord._sync_once()
    assert [r.method for r in delivery] == ["POST", "PATCH"]


def test_auth_failure_is_reported_without_claiming_delivery(incident, delivery, monkeypatch, caplog):
    class Client:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def request(self, method, url, **kwargs):
            return httpx.Response(403, json={"code": 50013}, request=httpx.Request(method, url))

    monkeypatch.setattr(discord.httpx, "Client", lambda **kwargs: Client())
    assert not discord._upsert(incident, incident["id"])
    assert "Discord HTTP 403" in caplog.text
    assert discord._tracked[incident["id"]]["message_id"] is None
