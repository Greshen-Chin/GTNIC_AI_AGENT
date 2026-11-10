"""Regression coverage for one slow investigation causing repeated log delivery."""

import json
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from app import database
from app.api import ingest
from app.config import settings
from app.services import juice_log_forwarder as forwarder
from app.services import investigation_worker as worker
from fastapi import BackgroundTasks
from fastapi.testclient import TestClient
from app import main
from app.middleware import AttackWebhookMiddleware


def ingest_event(event):
    return ingest.ingest_juice_shop_access_log(event, BackgroundTasks())


@pytest.fixture
def investigation(monkeypatch):
    monkeypatch.setattr(database, "_IN_MEMORY_INCIDENTS", [])
    monkeypatch.setattr(database, "get_db", lambda: None)
    monkeypatch.setattr(settings, "DISCORD_ENABLED", False)
    monkeypatch.setattr(settings, "WEBHOOK_URL", None)
    monkeypatch.setattr(ingest, "_FAILED_LOGINS", ingest.defaultdict(list))
    monkeypatch.setattr(ingest, "_LAST_BRUTE_FORCE_ALERT", {})

    def investigate(*, alert, dedup_key, incident_id):
        database.db_update_incident_analysis(incident_id, {"llm_model": "local-triage"})
        return {"incident_id": incident_id, "status": "likely"}

    spy = Mock(side_effect=investigate)
    monkeypatch.setattr(worker, "investigate_alert", spy)
    return spy


@pytest.fixture
def event():
    # Same URI and HTTP status observed in the production incident records.
    return {
        "time": "2026-11-10T14:31:48+00:00",
        "remote_addr": "198.51.100.77",
        "method": "GET", "uri": "/etc/passwd", "body": "", "status": 304,
    }


def test_replayed_log_only_investigates_once(event, investigation):
    first = ingest_event(event)
    for _ in range(5):
        repeated = ingest_event(dict(event))
        assert repeated["duplicate"] is True
        assert repeated["incident_id"] == first["incident_id"]
    assert investigation.call_count == 0
    assert worker.process_next_investigation() is True
    assert worker.process_next_investigation() is False
    assert investigation.call_count == 1
    assert len(database._IN_MEMORY_INCIDENTS) == 1


def test_new_event_from_same_ip_and_rule_is_investigated(event, investigation):
    first = ingest_event(event)
    second = ingest_event({
        **event, "time": "2026-11-10T14:31:49+00:00",
    })
    assert second["incident_id"] != first["incident_id"]
    assert worker.process_next_investigation() is True
    assert worker.process_next_investigation() is True
    assert investigation.call_count == 2


def test_distinct_log_entries_in_same_second_are_not_suppressed(event, investigation):
    first = ingest_event({**event, "event_id": "entry-1"})
    second = ingest_event({**event, "event_id": "entry-2"})
    assert second["incident_id"] != first["incident_id"]
    assert worker.process_next_investigation() is True
    assert worker.process_next_investigation() is True
    assert investigation.call_count == 2


def test_simultaneous_retries_do_not_start_parallel_investigations(event, investigation):
    original = investigation.side_effect

    def slow_investigation(**kwargs):
        time.sleep(0.05)
        return original(**kwargs)

    investigation.side_effect = slow_investigation
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(ingest_event, [event] * 4))
    assert len({r["incident_id"] for r in results}) == 1
    assert investigation.call_count == 0
    assert worker.process_next_investigation() is True
    assert worker.process_next_investigation() is False
    assert investigation.call_count == 1


@pytest.mark.parametrize("uri", ["/", "/rest/products/search?q=apple", "/assets/public/images/apple.jpg"])
def test_normal_traffic_does_not_investigate(event, investigation, uri):
    for _ in range(3):
        result = ingest_event({**event, "uri": uri, "status": 200})
        assert result == {"accepted": True, "detected": False}
    investigation.assert_not_called()
    assert database._IN_MEMORY_INCIDENTS == []


def test_lost_response_retries_same_log_without_reinvestigation(
    event, investigation, tmp_path, monkeypatch,
):
    log_path = tmp_path / "access.jsonl"
    state_path = tmp_path / "cursor.json"
    log_path.write_text(json.dumps(event) + "\n", encoding="utf-8")
    monkeypatch.setattr(forwarder, "LOG_PATH", log_path)
    monkeypatch.setattr(forwarder, "STATE_PATH", state_path)
    monkeypatch.setattr(forwarder, "TOKEN", "test-token")
    delivered_ids = []

    def post(url, *, json, headers, timeout):
        # The response only waits for persistence; AI runs separately.
        assert timeout.read == 5.0
        assert timeout.connect == 5.0
        delivered_ids.append(json["event_id"])
        result = ingest_event(json)
        if len(delivered_ids) == 1:
            # The incident was saved, but the client lost the HTTP response.
            raise httpx.ReadError("response lost")
        assert result["duplicate"] is True
        return httpx.Response(200, request=httpx.Request("POST", url), json=result)

    def stop_after_delivery(_):
        if state_path.exists():
            raise RuntimeError("stop test loop")

    monkeypatch.setattr(forwarder.httpx, "post", post)
    monkeypatch.setattr(forwarder.time, "sleep", stop_after_delivery)
    with pytest.raises(RuntimeError, match="stop test loop"):
        forwarder.run()
    assert len(delivered_ids) == 2
    assert delivered_ids[0] == delivered_ids[1]
    assert investigation.call_count == 0
    assert worker.process_next_investigation() is True
    assert worker.process_next_investigation() is False
    assert investigation.call_count == 1
    assert json.loads(state_path.read_text())["offset"] == log_path.stat().st_size


def test_duplicate_lookup_uses_persisted_database(monkeypatch):
    conn = Mock()
    cursor = Mock()
    conn.__enter__ = Mock(return_value=conn)
    conn.__exit__ = Mock(return_value=False)
    cursor.__enter__ = Mock(return_value=cursor)
    cursor.__exit__ = Mock(return_value=False)
    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = {"id": "persisted-incident"}
    monkeypatch.setattr(database, "get_db", lambda: conn)
    assert database.db_find_incident_by_dedup_key("juice-event:123") == "persisted-incident"
    assert cursor.execute.call_args.args[1] == ("juice-event:123",)


def test_replayed_failed_login_does_not_become_brute_force(event, investigation):
    failed = {**event, "method": "POST", "uri": "/rest/user/login", "status": 401}
    for _ in range(8):
        assert ingest_event(failed)["detected"] is False
    assert len(ingest._FAILED_LOGINS[event["remote_addr"]]) == 1
    assert database._IN_MEMORY_INCIDENTS == []


def test_distinct_failed_logins_still_detect_brute_force(event, investigation):
    failed = {**event, "method": "POST", "uri": "/rest/user/login", "status": 401}
    for attempt in range(4):
        assert ingest_event({**failed, "event_id": str(attempt)})["detected"] is False
    result = ingest_event({**failed, "event_id": "4"})
    assert result["threat_type"] == "brute_force"
    assert result["llm_model"] == "investigation-pending"


def test_slow_ai_does_not_block_next_attack_or_duplicate_delivery(event, investigation):
    started, release = Event(), Event()
    original = investigation.side_effect

    def blocked_ai(**kwargs):
        started.set()
        assert release.wait(3), "test worker was not released"
        return original(**kwargs)

    investigation.side_effect = blocked_ai
    first = ingest_event({**event, "event_id": "slow-1"})
    with ThreadPoolExecutor(max_workers=1) as executor:
        work = executor.submit(worker.process_next_investigation)
        try:
            assert started.wait(1)
            second = ingest_event({**event, "event_id": "slow-2"})
            duplicate = ingest_event({**event, "event_id": "slow-1"})
            assert second["incident_id"] != first["incident_id"]
            assert duplicate["incident_id"] == first["incident_id"]
            assert len(database._IN_MEMORY_INCIDENTS) == 2
            assert not work.done()
        finally:
            release.set()
        assert work.result(timeout=1)


def test_ai_failure_keeps_evidence_and_does_not_retry_forever(event, investigation):
    first = ingest_event(event)
    investigation.side_effect = RuntimeError("AI unavailable")
    assert worker.process_next_investigation()
    assert not worker.process_next_investigation()
    record = database.db_fetch_incident_by_id(first["incident_id"])
    assert record["llm_model"] == "signature-fallback"
    assert record["pro_evidence"]
    assert investigation.call_count == 1


def test_enrichment_preserves_analyst_decision_and_creation_time(event, investigation):
    first = ingest_event(event)
    record = database.db_fetch_incident_by_id(first["incident_id"])
    created_at = record["created_at"]
    database.db_update_incident_decision(first["incident_id"], "rejected", "analyst")
    database.db_update_incident_analysis(first["incident_id"], {
        "title": "AI result", "human_decision": "pending", "created_at": "wrong-time",
    })
    assert record["human_decision"] == "rejected"
    assert record["created_at"] == created_at
    assert record["title"] == "AI result"


def test_http_ingestion_stays_fast_while_worker_investigates(event, investigation, monkeypatch):
    started, release = Event(), Event()
    original = investigation.side_effect

    def blocked_ai(**kwargs):
        started.set()
        assert release.wait(5)
        return original(**kwargs)

    investigation.side_effect = blocked_ai
    monkeypatch.setattr(main, "test_postgres_connection", lambda: True)
    monkeypatch.setattr(main, "get_vertex_client", lambda: None)
    headers = {"X-Internal-Token": settings.INTERNAL_TOKEN}
    try:
        with TestClient(main.app) as client:
            health = client.get("/health").json()
            assert health["ingestion_mode"] == "persist-first-background-investigation"
            assert health["investigation_worker_alive"] is True
            first = client.post("/integrations/juice-shop/access-log", headers=headers,
                                json={**event, "event_id": "http-path"})
            assert first.status_code == 200
            assert started.wait(2)
            sqli = {**event, "event_id": "http-sql", "method": "POST",
                    "uri": "/rest/user/login", "body": "{\"email\":\"' OR 1=1--\"}"}
            before = time.monotonic()
            response = client.post("/integrations/juice-shop/access-log", headers=headers, json=sqli)
            assert time.monotonic() - before < 1
            assert response.status_code == 200
            data = response.json()
            assert data["threat_type"] == "sql_injection"
            assert data["llm_model"] == "investigation-pending"
            detail = client.get(f"/api/incidents/{data['incident_id']}",
                                headers={"X-Dashboard-API-Key": settings.DASHBOARD_API_KEY})
            assert detail.status_code == 200
            assert detail.json()["raw_alert"]["data"]["threat_type"] == "sql_injection"
            assert investigation.call_count == 1  # the earlier path request is still blocked
            retry = client.post("/integrations/juice-shop/access-log", headers=headers, json=sqli)
            assert retry.json()["incident_id"] == data["incident_id"]
            assert len(database._IN_MEMORY_INCIDENTS) == 2
            release.set()
    finally:
        release.set()


def test_forwarded_sql_evidence_does_not_trigger_middleware_alert(event, investigation, monkeypatch):
    middleware_alert = AsyncMock()
    monkeypatch.setattr(AttackWebhookMiddleware, "_send_alert", middleware_alert)
    notification = Mock()
    monkeypatch.setattr(settings, "WEBHOOK_URL", "https://not-called.invalid/webhook")
    monkeypatch.setattr(ingest, "_send_notification", notification)
    with TestClient(main.app) as client:
        headers = {"X-Internal-Token": settings.INTERNAL_TOKEN}
        sql = {**event, "uri": "/rest/products/search?q=' OR 1=1--", "event_id": "sql-notify"}
        for _ in range(2):
            assert client.post("/integrations/juice-shop/access-log", headers=headers, json=sql).status_code == 200
    middleware_alert.assert_not_called()
    notification.assert_called_once()


@pytest.mark.parametrize("truncated", [False, True])
def test_forwarder_skips_corrupt_lines_and_waits_for_partial_line(
    event, tmp_path, monkeypatch, truncated,
):
    log_path, state_path = tmp_path / "access.jsonl", tmp_path / "cursor.json"
    prefix = 'broken-json\n[]\n' + json.dumps(event) + '\n'
    log_path.write_text(prefix + '{"unfinished":', encoding="utf-8", newline="")
    monkeypatch.setattr(forwarder, "LOG_PATH", log_path)
    monkeypatch.setattr(forwarder, "STATE_PATH", state_path)
    monkeypatch.setattr(forwarder, "TOKEN", "test-token")
    if truncated:
        state_path.write_text(json.dumps({"inode": log_path.stat().st_ino, "offset": 99999}))
    delivered = []

    def post(url, *, json, **kwargs):
        delivered.append(json)
        return httpx.Response(200, request=httpx.Request("POST", url))

    def stop(_):
        raise RuntimeError("stop test loop")

    monkeypatch.setattr(forwarder.httpx, "post", post)
    monkeypatch.setattr(forwarder.time, "sleep", stop)
    with pytest.raises(RuntimeError, match="stop test loop"):
        forwarder.run()
    assert len(delivered) == 1
    assert json.loads(state_path.read_text())["offset"] == len(prefix.encode("utf-8"))
