"""Regression coverage for one slow investigation causing repeated log delivery."""

import json
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import httpx
import pytest

from app import database
from app.api import ingest
from app.config import settings
from app.services import juice_log_forwarder as forwarder


@pytest.fixture
def investigation(monkeypatch):
    monkeypatch.setattr(database, "_IN_MEMORY_INCIDENTS", [])
    monkeypatch.setattr(database, "get_db", lambda: None)
    monkeypatch.setattr(settings, "DISCORD_ENABLED", False)
    monkeypatch.setattr(settings, "WEBHOOK_URL", None)

    def investigate(*, alert, dedup_key):
        incident_id = database.db_insert_incident({
            "dedup_key": dedup_key, "raw_alert": alert,
        })
        return {"incident_id": incident_id, "status": "likely"}

    spy = Mock(side_effect=investigate)
    monkeypatch.setattr(ingest, "investigate_alert", spy)
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
    first = ingest.ingest_juice_shop_access_log(event)
    for _ in range(5):
        repeated = ingest.ingest_juice_shop_access_log(dict(event))
        assert repeated["duplicate"] is True
        assert repeated["incident_id"] == first["incident_id"]
    assert investigation.call_count == 1
    assert len(database._IN_MEMORY_INCIDENTS) == 1


def test_new_event_from_same_ip_and_rule_is_investigated(event, investigation):
    first = ingest.ingest_juice_shop_access_log(event)
    second = ingest.ingest_juice_shop_access_log({
        **event, "time": "2026-11-10T14:31:49+00:00",
    })
    assert second["incident_id"] != first["incident_id"]
    assert investigation.call_count == 2


def test_distinct_log_entries_in_same_second_are_not_suppressed(event, investigation):
    first = ingest.ingest_juice_shop_access_log({**event, "event_id": "entry-1"})
    second = ingest.ingest_juice_shop_access_log({**event, "event_id": "entry-2"})
    assert second["incident_id"] != first["incident_id"]
    assert investigation.call_count == 2


def test_simultaneous_retries_do_not_start_parallel_investigations(event, investigation):
    original = investigation.side_effect

    def slow_investigation(**kwargs):
        time.sleep(0.05)
        return original(**kwargs)

    investigation.side_effect = slow_investigation
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(ingest.ingest_juice_shop_access_log, [event] * 4))
    assert len({r["incident_id"] for r in results}) == 1
    assert investigation.call_count == 1


@pytest.mark.parametrize("uri", ["/", "/rest/products/search?q=apple", "/assets/public/images/apple.jpg"])
def test_normal_traffic_does_not_investigate(event, investigation, uri):
    for _ in range(3):
        result = ingest.ingest_juice_shop_access_log({**event, "uri": uri, "status": 200})
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
        # A slow AI response must not hit the old five-second read deadline.
        assert timeout.read is None
        assert timeout.connect == 5.0
        delivered_ids.append(json["event_id"])
        result = ingest.ingest_juice_shop_access_log(json)
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
