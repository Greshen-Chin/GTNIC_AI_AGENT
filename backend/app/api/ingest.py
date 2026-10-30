"""Authenticated ingestion endpoint for Juice Shop reverse-proxy access logs."""

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.parse import unquote_plus

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.auth import verify_internal_token
from app.config import settings
from app.database import db_insert_incident

logger = logging.getLogger("soar-api.ingest")
router = APIRouter(prefix="/integrations", tags=["Security Event Ingestion"])

SQLI_PATTERN = re.compile(
    r"(?:\bunion\s+(?:all\s+)?select\b|\bselect\b.+\bfrom\b|"
    r"\bor\b\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w*['\"]?|"
    r"['\"]\s*or\s+['\"\w]+\s*=|--\s*|#|/\*|;\s*(?:drop|delete|update|insert)\b|"
    r"\bsleep\s*\(|\bbenchmark\s*\()",
    re.IGNORECASE,
)
XSS_PATTERN = re.compile(
    r"<\s*script\b|javascript\s*:|\bonerror\s*=|\bonload\s*=|<\s*svg\b",
    re.IGNORECASE,
)
PATH_TRAVERSAL_PATTERN = re.compile(
    r"(?:\.\./|\.\.\\|/etc/(?:passwd|shadow)|boot\.ini|win\.ini)",
    re.IGNORECASE,
)
COMMAND_INJECTION_PATTERN = re.compile(
    r"(?:;\s*(?:cat|ls|id|whoami|curl|wget|bash|sh|powershell)\b|"
    r"\|\s*(?:cat|ls|id|whoami|curl|wget|bash|sh)\b|"
    r"`[^`]+`|\$\([^)]+\))",
    re.IGNORECASE,
)


@router.post("/juice-shop/access-log")
def ingest_juice_shop_access_log(
    event: Dict[str, Any],
    _: str = Depends(verify_internal_token),
):
    """Create a dashboard incident for suspicious Juice Shop URL or request body payload."""
    raw_uri = str(event.get("uri", ""))[:8_000]
    raw_body = str(event.get("body", ""))[:16_000]
    decoded_uri = unquote_plus(raw_uri)
    decoded_body = unquote_plus(raw_body)

    # Detect attack pattern in URI first, then in request body
    threat_type = None
    threat_location = None
    matched_payload = ""

    # Priority 1: Command Injection
    if COMMAND_INJECTION_PATTERN.search(decoded_uri):
        threat_type = "command_injection"
        threat_location = "URL"
        matched_payload = decoded_uri
    elif COMMAND_INJECTION_PATTERN.search(decoded_body):
        threat_type = "command_injection"
        threat_location = "Request Body"
        matched_payload = decoded_body
    # Priority 2: SQL Injection
    elif SQLI_PATTERN.search(decoded_uri):
        threat_type = "sql_injection"
        threat_location = "URL"
        matched_payload = decoded_uri
    elif SQLI_PATTERN.search(decoded_body):
        threat_type = "sql_injection"
        threat_location = "Request Body"
        matched_payload = decoded_body
    # Priority 3: Path Traversal
    elif PATH_TRAVERSAL_PATTERN.search(decoded_uri):
        threat_type = "path_traversal"
        threat_location = "URL"
        matched_payload = decoded_uri
    elif PATH_TRAVERSAL_PATTERN.search(decoded_body):
        threat_type = "path_traversal"
        threat_location = "Request Body"
        matched_payload = decoded_body
    # Priority 4: Cross-Site Scripting (XSS)
    elif XSS_PATTERN.search(decoded_uri):
        threat_type = "cross_site_scripting"
        threat_location = "URL"
        matched_payload = decoded_uri
    elif XSS_PATTERN.search(decoded_body):
        threat_type = "cross_site_scripting"
        threat_location = "Request Body"
        matched_payload = decoded_body

    if not threat_type:
        return {"accepted": True, "detected": False}

    client_ip = str(event.get("remote_addr") or "unknown")[:128]
    timestamp = str(event.get("time") or datetime.now(timezone.utc).isoformat())
    payload = matched_payload[:2_000]
    method = str(event.get("method", ""))[:16]

    threat_names = {
        "sql_injection": "SQL injection",
        "cross_site_scripting": "XSS",
        "command_injection": "Command injection",
        "path_traversal": "Path traversal",
    }
    threat_label = threat_names.get(threat_type, threat_type.replace('_', ' '))

    severity_map = {
        "command_injection": "critical",
        "sql_injection": "high",
        "path_traversal": "high",
        "cross_site_scripting": "medium",
    }
    severity = severity_map.get(threat_type, "medium")
    severity_scores = {"critical": 90, "high": 75, "medium": 55, "low": 30}
    severity_score = severity_scores.get(severity, 55)

    description = f"Juice Shop {threat_label} request detected in {threat_location} by proxy access-log inspection"
    title = f"Juice Shop {threat_label} attempt ({threat_location})"
    alert = {
        "timestamp": timestamp,
        "agent": {"name": "juice-shop"},
        "rule": {"id": "juice-proxy-1001", "description": description},
        "data": {
            "srcip": client_ip,
            "url": raw_uri,
            "body": raw_body[:2_000] if raw_body else None,
            "threat_location": threat_location,
            "method": method,
            "http_status": event.get("status"),
            "user_agent": str(event.get("user_agent", ""))[:256],
            "threat_type": threat_type,
            "payload": payload,
        },
    }
    incident = {
        "dedup_key": None,
        "wazuh_rule_id": "juice-proxy-1001",
        "title": title,
        "source_ip": client_ip,
        "raw_alert": alert,
        "status": "likely",
        "flags": [threat_type, "juice-shop", "proxy-detected", f"loc-{threat_location.lower().replace(' ', '-')}"] ,
        "severity_score": severity_score,
        "severity_label": severity,
        "confidence_score": 80,
        "attack_story": [{
            "step": 1,
            "title": "Suspicious request observed",
            "event": f"Reverse proxy recorded a {threat_type.replace('_', ' ')} pattern in the request {threat_location}.",
            "timestamp": timestamp,
            "phase": "Initial Access",
        }],
        "pro_evidence": [{
            "claim": description,
            "tool": "nginx-access-log",
            "evidence_ref": f"{threat_location.lower().replace(' ', '_')}={payload[:500]}",
            "source": "Juice Shop reverse proxy",
            "confidence": "High",
        }],
        "contra_evidence": [],
        "tool_trace": [],
        "mitre_context": [],
        "llm_model": "signature-detection",
        "prompt_version": "proxy-v1",
        "human_decision": "pending",
    }
    incident_id = db_insert_incident(incident)

    notification = {
        "event": "security.alert",
        "incident_id": incident_id,
        "timestamp": timestamp,
        "threat_type": threat_type,
        "threat_location": threat_location,
        "severity": severity,
        "source_ip": client_ip,
        "target": "juice-shop",
        "payload": payload,
        "title": title,
        "dashboard_url": f"/incidents/{incident_id}",
    }
    if settings.WEBHOOK_URL:
        try:
            response = httpx.post(settings.WEBHOOK_URL, json=notification, timeout=5.0)
            response.raise_for_status()
        except httpx.HTTPError:
            # Incident persistence is independent from notification delivery.
            logger.exception("Incident %s stored, but n8n notification failed", incident_id)
    else:
        logger.warning("Incident %s stored; WEBHOOK_URL is not configured", incident_id)

    return {
        "accepted": True,
        "detected": True,
        "incident_id": incident_id,
        "threat_type": threat_type,
        "threat_location": threat_location,
    }
