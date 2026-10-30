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
    r"\bor\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+|"
    r"['\"]\s*or\s+['\"\w]+\s*=|--\s|;\s*(?:drop|delete|update|insert)\b|"
    r"\bsleep\s*\(|\bbenchmark\s*\()",
    re.IGNORECASE,
)
XSS_PATTERN = re.compile(
    r"<\s*script\b|javascript\s*:|\bonerror\s*=|\bonload\s*=|<\s*svg\b",
    re.IGNORECASE,
)


@router.post("/juice-shop/access-log")
def ingest_juice_shop_access_log(
    event: Dict[str, Any],
    _: str = Depends(verify_internal_token),
):
    """Create a dashboard incident for suspicious Juice Shop URL requests."""
    raw_uri = str(event.get("uri", ""))[:8_000]
    decoded_uri = unquote_plus(raw_uri)
    match = SQLI_PATTERN.search(decoded_uri)
    threat_type = "sql_injection" if match else None
    if not threat_type and XSS_PATTERN.search(decoded_uri):
        threat_type = "cross_site_scripting"
    if not threat_type:
        return {"accepted": True, "detected": False}

    client_ip = str(event.get("remote_addr") or "unknown")[:128]
    timestamp = str(event.get("time") or datetime.now(timezone.utc).isoformat())
    payload = decoded_uri[:2_000]
    description = f"Juice Shop {threat_type.replace('_', ' ')} request detected by proxy access-log inspection"
    title = "Juice Shop SQL injection attempt" if threat_type == "sql_injection" else "Juice Shop XSS attempt"
    severity = "high" if threat_type == "sql_injection" else "medium"
    alert = {
        "timestamp": timestamp,
        "agent": {"name": "juice-shop"},
        "rule": {"id": "juice-proxy-1001", "description": description},
        "data": {
            "srcip": client_ip,
            "url": raw_uri,
            "method": str(event.get("method", ""))[:16],
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
        "flags": [threat_type, "juice-shop", "proxy-detected"],
        "severity_score": 75 if severity == "high" else 55,
        "severity_label": severity,
        "confidence_score": 80,
        "attack_story": [{
            "step": 1,
            "title": "Suspicious request observed",
            "event": f"Reverse proxy recorded a {threat_type.replace('_', ' ')} pattern in the request URI.",
            "timestamp": timestamp,
            "phase": "Initial Access",
        }],
        "pro_evidence": [{
            "claim": description,
            "tool": "nginx-access-log",
            "evidence_ref": f"uri={payload[:500]}",
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

    return {"accepted": True, "detected": True, "incident_id": incident_id, "threat_type": threat_type}
