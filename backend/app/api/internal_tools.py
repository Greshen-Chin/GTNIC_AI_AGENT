import logging
from fastapi import APIRouter, Depends, status

from app.auth import verify_internal_token
from app.schemas.tools import (
    IpIn,
    SearchAlertsIn,
    SearchAlertsResponse,
    LoginHistoryResponse,
    RagQueryIn,
    RagResponse,
    WebAttackIn,
    InspectWebAttackResponse,
)
from app.schemas.incident import (
    AgentInvestigateRequest,
    AgentInvestigateResponse,
)
from app.services.wazuh_service import search_alerts_by_ip, fetch_login_history, inspect_web_attack
from app.services.rag_service import search_mitre_owasp_rag
from app.services.agent_service import investigate_alert

logger = logging.getLogger("soar-api.internal")

router = APIRouter(
    prefix="/internal",
    tags=["Internal Tools (Agent / n8n)"],
    dependencies=[Depends(verify_internal_token)]
)


@router.post(
    "/tools/search_alerts_by_ip",
    response_model=SearchAlertsResponse,
    summary="Tool 1: Query Wazuh Indexer for recent alerts by IP",
    description="Queries Wazuh Indexer (OpenSearch) for alerts matching the srcip within the last 24h. Returns deterministic facts."
)
def api_search_alerts_by_ip(payload: SearchAlertsIn):
    logger.info(f"Tool search_alerts_by_ip called for {payload.srcip}")
    result = search_alerts_by_ip(
        srcip=payload.srcip,
        time_window=payload.time_window,
        max_alerts=payload.max_alerts
    )
    return result


@router.post(
    "/tools/get_login_history",
    response_model=LoginHistoryResponse,
    summary="Tool 2: Query login history aggregations by IP",
    description="Aggregates Wazuh rule 100100 (failed) vs 100103 (success) in the last 24h. Returns deterministic facts."
)
def api_get_login_history(payload: IpIn):
    logger.info(f"Tool get_login_history called for {payload.srcip}")
    result = fetch_login_history(srcip=payload.srcip)
    return result


@router.post(
    "/tools/mitre_owasp_rag",
    response_model=RagResponse,
    summary="Tool 3: RAG lookup over MITRE ATT&CK & OWASP Top 10 with Vertex AI Embeddings",
    description="Generates embedding using Google Cloud Vertex AI (text-embedding-004) and performs pgvector cosine similarity search."
)
def api_mitre_owasp_rag(payload: RagQueryIn):
    logger.info(f"Tool mitre_owasp_rag called with query: '{payload.query}' (top_k={payload.top_k})")
    result = search_mitre_owasp_rag(query=payload.query, top_k=payload.top_k)
    return result


@router.post(
    "/tools/inspect_web_attack",
    response_model=InspectWebAttackResponse,
    summary="Tool 4: Deep inspection for SQL Injection (SQLi) & Cross-Site Scripting (XSS)",
    description="Inspects web alerts for SQLi & XSS payloads, target parameters, HTTP status (500=DB error, 403=WAF, 200=served) and defensive headers."
)
def api_inspect_web_attack(payload: WebAttackIn):
    logger.info(f"Tool inspect_web_attack called for {payload.srcip} (type={payload.attack_type})")
    result = inspect_web_attack(
        srcip=payload.srcip,
        attack_type=payload.attack_type,
        time_window=payload.time_window
    )
    return result


@router.post(
    "/agent/investigate",
    response_model=AgentInvestigateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Autonomous AI Agent Triage using Vertex AI Gemini Tool Calling",
    description="Full agent pipeline: invokes Gemini on Vertex AI with tools, runs deterministic validator & scorer, and creates an incident record."
)
def api_agent_investigate(payload: AgentInvestigateRequest):
    logger.info("Executing autonomous AI Agent investigation pipeline via Vertex AI")
    result = investigate_alert(alert=payload.alert, dedup_key=payload.dedup_key)
    return result
