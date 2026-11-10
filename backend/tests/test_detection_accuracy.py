import json
import pytest

from app.services.request_detector import detect_request, inspect_current_request
from app.services.detection_evaluation import CASE_PATH, evaluate_detector
from app.services import agent_service, wazuh_service
from app import database

CASES = json.loads(CASE_PATH.read_bytes())["cases"]


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_labelled_request_classification(case):
    result = detect_request(case["event"])
    assert (result["threat_type"] if result else None) == case["expected"]


def test_evaluation_reports_actual_counts_and_scope():
    result = evaluate_detector()
    assert result["total_scenarios"] == len(CASES)
    assert result["correct"] == sum(r["correct"] for r in result["runs"])
    assert result["accuracy"] == round(100 * result["correct"] / len(CASES), 2)
    assert sum(result["confusion_matrix"].values()) == len(CASES)
    assert result["source"] == "labelled-lab-fixtures"


def test_empty_index_does_not_discard_valid_results(monkeypatch):
    monkeypatch.setattr(agent_service.settings, "ALLOW_SIMULATION", False)
    alert = {"agent": {"name": "juice-shop"}, "rule": {"id": "100110", "level": 8},
             "data": {"url": "/rest/user/login", "body": "{\"email\":\"' OR 1=1--\"}"}}
    traces = [
        {"tool": "search_alerts_by_ip", "status": "success", "facts": ["alert_count=0", "other_alert_count=0"], "output": {"provenance": {"source": "wazuh-indexer"}}},
        {"tool": "inspect_current_request", "status": "success", "facts": inspect_current_request(alert)["facts"], "output": {}},
    ]
    result = agent_service.validate_and_score({"status": "confirmed", "pro_evidence": [], "contra_evidence": [
        {"tool": "search_alerts_by_ip", "evidence_ref": "other_alert_count=0", "claim": "No indexed corroboration"}
    ]}, alert, traces)
    assert result["status"] == "likely"  # a request pattern cannot prove exploitation
    assert "tool_inconsistent" not in result["flags"]
    assert "min_tools_not_met" not in result["flags"]
    assert result["contra_evidence"]
    assert any(e["evidence_ref"] == "pattern_detected=true" for e in result["pro_evidence"])


def test_wazuh_inspection_includes_body_and_does_not_infer_firewall(monkeypatch):
    monkeypatch.setattr(wazuh_service, "query_indexer", lambda _: {"hits": {"hits": [{"_source": {
        "data": {"url": "/rest/user/login", "body": "{\"email\":\"' OR 1=1--\"}", "status": "403"}
    }}]}})
    result = wazuh_service.inspect_web_attack("203.0.113.10")
    assert result["sqli"]["detected"] is True
    assert result["waf_mitigated"] is None
    assert "block_observed=true" not in result["facts"]
    assert result["sqli"]["database_error_reflected"] is None


def test_pending_incidents_are_excluded_from_evidence_average(monkeypatch):
    monkeypatch.setattr(database, "_IN_MEMORY_INCIDENTS", [
        {"confidence_score": 60, "llm_model": "local-triage"},
        {"confidence_score": 0, "llm_model": "investigation-pending"},
    ])
    assert database.db_fetch_stats()["aiAverageConfidence"] == 0.6
    monkeypatch.setattr(database, "_IN_MEMORY_INCIDENTS", [])
    assert database.db_fetch_stats()["aiAverageConfidence"] is None


def test_reference_document_is_not_event_proof():
    result = agent_service.validate_and_score({"status": "likely", "pro_evidence": [
        {"tool": "mitre_owasp_rag", "evidence_ref": "doc:1", "claim": "This document proves an attack"}
    ]}, {"rule": {"level": 5}, "data": {"url": "/"}}, [
        {"tool": "mitre_owasp_rag", "status": "success", "facts": ["doc:1"], "output": {}}
    ])
    assert result["pro_evidence"] == []
    assert result["status"] == "uncertain"


def test_reset_requires_explicit_confirmation():
    from app.reset_lab import reset_lab
    with pytest.raises(ValueError, match="Explicit"):
        reset_lab("wrong")


def test_reset_archives_and_verifies_before_clearing(monkeypatch, tmp_path):
    from unittest.mock import MagicMock
    from app import reset_lab as reset
    path = tmp_path / "access.jsonl"
    path.write_text("old log\n")
    conn = MagicMock()
    cur = conn.__enter__.return_value.cursor.return_value.__enter__.return_value
    cur.fetchone.side_effect = [(27,), (27,)]
    monkeypatch.setattr(reset.psycopg, "connect", lambda _: conn)
    monkeypatch.setattr(reset, "LOG_PATH", path)
    saved = []
    monkeypatch.setattr(reset, "save_cursor", lambda *args: saved.append(args))
    reset.reset_lab("RESET_LAB")
    statements = [str(call.args[0]) for call in cur.execute.call_args_list]
    assert "CREATE TABLE" in statements[0]
    assert "TRUNCATE TABLE incidents" == statements[-1]
    assert saved == [(path.stat().st_ino, path.stat().st_size)]


def test_reset_does_not_clear_if_archive_count_disagrees(monkeypatch, tmp_path):
    from unittest.mock import MagicMock
    from app import reset_lab as reset
    path = tmp_path / "access.jsonl"
    path.write_text("old log\n")
    conn = MagicMock()
    cur = conn.__enter__.return_value.cursor.return_value.__enter__.return_value
    cur.fetchone.side_effect = [(26,), (27,)]
    monkeypatch.setattr(reset.psycopg, "connect", lambda _: conn)
    monkeypatch.setattr(reset, "LOG_PATH", path)
    with pytest.raises(RuntimeError, match="Archive verification"):
        reset.reset_lab("RESET_LAB")
    assert not any("TRUNCATE" in str(call.args[0]) for call in cur.execute.call_args_list)
