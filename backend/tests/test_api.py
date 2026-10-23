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
async def test_health_endpoint(ac: AsyncClient):
    response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["embed_model"] == settings.EMBED_MODEL
    assert data["embed_dim"] == 768


@pytest.mark.anyio
async def test_internal_tools_auth_protection(ac: AsyncClient):
    # Calling without X-Internal-Token should return 401
    resp = await ac.post("/internal/tools/get_login_history", json={"srcip": "203.0.113.10"})
    assert resp.status_code == 401

    # Calling with invalid token should return 401
    resp = await ac.post(
        "/internal/tools/get_login_history",
        headers={"X-Internal-Token": "wrong-token"},
        json={"srcip": "203.0.113.10"}
    )
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_ip_validation(ac: AsyncClient):
    # Invalid IP regex
    resp = await ac.post(
        "/internal/tools/get_login_history",
        headers=INTERNAL_HEADERS,
        json={"srcip": "999.999.999.999"}
    )
    assert resp.status_code == 422

    resp = await ac.post(
        "/internal/tools/get_login_history",
        headers=INTERNAL_HEADERS,
        json={"srcip": "invalid_ip_injection'; DROP TABLE--"}
    )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_get_login_history_tool(ac: AsyncClient):
    resp = await ac.post(
        "/internal/tools/get_login_history",
        headers=INTERNAL_HEADERS,
        json={"srcip": "203.0.113.20"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["srcip"] == "203.0.113.20"
    assert "facts" in data
    assert any("failed_count=" in f for f in data["facts"])
    assert any("success_count=" in f for f in data["facts"])
    assert "window=24h" in data["facts"]


@pytest.mark.anyio
async def test_search_alerts_by_ip_tool(ac: AsyncClient):
    resp = await ac.post(
        "/internal/tools/search_alerts_by_ip",
        headers=INTERNAL_HEADERS,
        json={"srcip": "203.0.113.10", "max_alerts": 10}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["srcip"] == "203.0.113.10"
    assert "facts" in data
    assert any("alert_count=" in f for f in data["facts"])
    assert any("distinct_rules=" in f for f in data["facts"])


@pytest.mark.anyio
async def test_mitre_owasp_rag_tool(ac: AsyncClient):
    resp = await ac.post(
        "/internal/tools/mitre_owasp_rag",
        headers=INTERNAL_HEADERS,
        json={"query": "sql injection login bypass", "top_k": 4}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "facts" in data
    assert "matches" in data
    assert len(data["matches"]) > 0
    # Facts should have doc:<id> and mitre or owasp
    assert any(f.startswith("doc:") for f in data["facts"])


@pytest.mark.anyio
async def test_agent_investigate_and_deterministic_validator(ac: AsyncClient):
    alert_payload = {
        "rule": {
            "id": "100101",
            "level": 8,
            "description": "SQL Injection attempt detected on /rest/products/search"
        },
        "data": {
            "srcip": "203.0.113.10",
            "url": "/rest/products/search?q=' OR 1=1--"
        }
    }

    resp = await ac.post(
        "/internal/agent/investigate",
        headers=INTERNAL_HEADERS,
        json={"alert": alert_payload}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "incident_id" in data
    assert data["status"] in ("confirmed", "likely", "uncertain", "false_positive")
    assert 10 <= data["severity_score"] <= 100
    assert 0 <= data["confidence_score"] <= 100
    assert len(data["tool_trace"]) >= 2
    assert "attack_story" in data
    assert "pro_evidence" in data


@pytest.mark.anyio
async def test_dashboard_api_flow(ac: AsyncClient):
    # 1. Fetch incidents
    resp = await ac.get("/api/incidents", headers=DASHBOARD_HEADERS)
    assert resp.status_code == 200
    incidents = resp.json()
    assert isinstance(incidents, list)
    assert len(incidents) > 0

    first_id = incidents[0]["id"]

    # 2. Fetch single incident
    detail_resp = await ac.get(f"/api/incidents/{first_id}", headers=DASHBOARD_HEADERS)
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["id"] == first_id

    # 3. Submit Decision: Approve
    decision_resp = await ac.post(
        f"/api/incidents/{first_id}/decision",
        headers=DASHBOARD_HEADERS,
        json={"decision": "approved", "decided_by": "lead-analyst"}
    )
    assert decision_resp.status_code == 200
    dec_data = decision_resp.json()
    assert dec_data["human_decision"] == "approved"
    assert dec_data["decided_by"] == "lead-analyst"

    # 4. Fetch Stats
    stats_resp = await ac.get("/api/stats", headers=DASHBOARD_HEADERS)
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert "totalIncidents" in stats
    assert "mitigatedCount" in stats
    assert stats["mitigatedCount"] >= 1

    # 5. Fetch Benchmark
    bench_resp = await ac.get("/api/benchmark", headers=DASHBOARD_HEADERS)
    assert bench_resp.status_code == 200
    bench = bench_resp.json()
    assert "total_scenarios" in bench
    assert bench["agent_accuracy"] > bench["baseline_accuracy"]
