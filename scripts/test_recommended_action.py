import sys
sys.path.insert(0, "backend")

from app.schemas.incident import IncidentResponse
from app.services.agent_service import resolve_recommended_action, investigate_alert
from app.database import db_insert_incident, db_fetch_incidents, db_fetch_incident_by_id

print("=== 1. Testing resolve_recommended_action ===")
sqli_rec = resolve_recommended_action("SQL Injection attempt", "192.168.1.10", flags=["sql_injection"])
print(f"SQLi Playbook: {sqli_rec}")
assert "Prepared Statements" in sqli_rec

xss_rec = resolve_recommended_action("Reflected XSS script tag", "192.168.1.20", flags=["cross_site_scripting"])
print(f"XSS Playbook: {xss_rec}")
assert "Content Security Policy" in xss_rec

brute_rec = resolve_recommended_action("Failed login attempts", "192.168.1.30", flags=["brute-force"])
print(f"Brute Force Playbook: {brute_rec}")
assert "rate-limiting" in brute_rec

print("\n=== 2. Testing Database Insert & Fetch with recommended_action ===")
test_inc = {
    "title": "[HIGH] Test SQLi Injection Incident",
    "source_ip": "203.0.113.99",
    "status": "confirmed",
    "severity_label": "high",
    "severity_score": 75,
    "confidence_score": 90,
    "summary": "Investigasi serangan SQL Injection pada parameter search.",
    "recommended_action": "Terapkan Prepared Statements (parameterized queries) dan blokir IP 203.0.113.99 pada WAF.",
    "raw_alert": {
        "rule": {"description": "SQL Injection attempt"},
        "data": {"srcip": "203.0.113.99"}
    }
}

inc_id = db_insert_incident(test_inc)
print(f"Inserted incident id: {inc_id}")

fetched = db_fetch_incident_by_id(inc_id)
print(f"Fetched incident recommended_action: {fetched.get('recommended_action')}")
assert fetched.get("recommended_action") == test_inc["recommended_action"]
assert fetched.get("summary") == test_inc["summary"]

print("\n=== 3. Testing IncidentResponse Schema Serialization ===")
response_obj = IncidentResponse.model_validate(fetched)
response_dict = response_obj.model_dump(mode="json")
print(f"Serialized recommended_action: {response_dict.get('recommended_action')}")
assert response_dict.get("recommended_action") == test_inc["recommended_action"]
assert response_dict.get("summary") == test_inc["summary"]

print("\nALL RECOMMENDATION PLAYBOOK TESTS PASSED SUCCESSFULLY! ✅")

