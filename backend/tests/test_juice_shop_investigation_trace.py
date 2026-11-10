import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.config import settings

INTERNAL_HEADERS = {"X-Internal-Token": settings.INTERNAL_TOKEN}
DASHBOARD_HEADERS = {"X-Dashboard-API-Key": settings.DASHBOARD_API_KEY}


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.anyio
async def test_juice_shop_attack_triggers_investigation_and_populates_traces(ac: AsyncClient):
    """
    Regression Test:
    Ensures that Juice Shop proxy access logs containing attacks:
    1. Are ingested and automatically analyzed via investigate_alert()
    2. Contain genuine tool execution traces (tool_trace length >= 2)
    3. Include automated mitigation playbook recommendations (recommended_action)
    4. Populate MITRE ATT&CK & OWASP mapping
    5. Are retrievable from the SOC Dashboard API with consistent data
    """
    event = {
        "remote_addr": "198.51.100.77",
        "method": "POST",
        "uri": "/rest/user/login",
        "body": '{"email":"admin\' OR \'1\'=\'1\'--","password":"password123"}',
        "status": 500,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    # 1. Ingest access log event
    resp = await ac.post(
        "/integrations/juice-shop/access-log",
        headers=INTERNAL_HEADERS,
        json=event,
    )
    assert resp.status_code == 200, f"Ingest failed: {resp.text}"
    data = resp.json()

    assert data["accepted"] is True
    assert data["detected"] is True
    assert data["threat_type"] == "sql_injection"
    assert "incident_id" in data
    incident_id = data["incident_id"]
    assert incident_id, "Expected valid incident_id returned from investigation"

    # 2. Fetch the incident from SOC Dashboard API
    detail_resp = await ac.get(f"/api/incidents/{incident_id}", headers=DASHBOARD_HEADERS)
    assert detail_resp.status_code == 200, f"Detail fetch failed: {detail_resp.text}"
    incident = detail_resp.json()

    # 3. Assert tool traces are genuine and non-empty
    tool_trace = incident.get("tool_trace", [])
    assert len(tool_trace) >= 2, f"Expected at least 2 tool traces, got: {tool_trace}"
    tool_names = [t.get("tool") or t.get("toolName") for t in tool_trace]
    assert any(name in ("inspect_web_attack", "search_alerts_by_ip", "mitre_owasp_rag") for name in tool_names)

    # 4. Assert automated mitigation recommendation is present and not default empty
    rec_action = incident.get("recommended_action")
    assert rec_action is not None and len(rec_action.strip()) > 0
    assert "no recommendation provided" not in rec_action.lower()

    # 5. Assert MITRE context is mapped
    mitre_ctx = incident.get("mitre_context", [])
    assert len(mitre_ctx) > 0, "Expected MITRE ATT&CK techniques mapped"

    # 6. Assert LLM Model engine is labeled
    llm_model = incident.get("llm_model")
    assert llm_model in (settings.LLM_MODEL, "local-triage", "gemini-3.8-flash", "gemini-2.5-flash")
