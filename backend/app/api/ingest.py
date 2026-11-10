"""Authenticated ingestion endpoint for Juice Shop reverse-proxy access logs."""

import logging
import re
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List
from urllib.parse import unquote_plus

import httpx
from fastapi import APIRouter, Depends

from app.auth import verify_internal_token
from app.config import settings
from app.database import db_insert_incident
from app.services.agent_service import investigate_alert

logger = logging.getLogger("soar-api.ingest")
router = APIRouter(prefix="/integrations", tags=["Security Event Ingestion"])

# Sliding window for brute force login detection: {client_ip: [timestamp1, timestamp2, ...]}
_FAILED_LOGINS: Dict[str, List[float]] = defaultdict(list)
BRUTE_FORCE_THRESHOLD = 5   # Alert when 5 failed login attempts occur
BRUTE_FORCE_WINDOW = 60     # Within a 60-second window
_LAST_BRUTE_FORCE_ALERT: Dict[str, float] = {}  # Cooldown per IP (30s) to prevent spamming

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
    """
    Ingest suspicious Juice Shop reverse-proxy access logs and trigger
    autonomous investigation via the AI Agent pipeline (Gemini / Local Triage).
    """
    raw_uri = str(event.get("uri", ""))[:8_000]
    raw_body = str(event.get("body", ""))[:16_000]
    decoded_uri = unquote_plus(raw_uri)
    decoded_body = unquote_plus(raw_body)

    # Extract true client IP: prioritize Cloudflare CF-Connecting-IP, then X-Forwarded-For, then remote_addr
    cf_ip = str(event.get("cf_connecting_ip") or "").strip()
    xff = str(event.get("x_forwarded_for") or "").strip()
    remote_ip = str(event.get("remote_addr") or "").strip()

    if cf_ip and cf_ip not in ("-", "null", "None", ""):
        client_ip = cf_ip
    elif xff and xff not in ("-", "null", "None", ""):
        # X-Forwarded-For can be comma-separated: "client, proxy1, proxy2"
        client_ip = xff.split(",")[0].strip()
    elif remote_ip and remote_ip not in ("-", "null", "None", ""):
        client_ip = remote_ip
    else:
        client_ip = "unknown"

    client_ip = client_ip[:128]
    method = str(event.get("method", ""))[:16].upper()
    status_code = str(event.get("status") or "")

    # Detect attack pattern in URI first, then in request body
    threat_type = None
    threat_location = None
    matched_payload = ""
    fail_count = 0

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

    # Priority 5: Brute Force Login Detection (Rate-based on HTTP 401 on login)
    is_login_endpoint = "/rest/user/login" in raw_uri or raw_uri.rstrip("/").endswith("/login")
    is_failed_login = method == "POST" and is_login_endpoint and status_code == "401"

    if not threat_type and is_failed_login:
        now_ts = time.time()
        # Clean older entries beyond sliding window (60s)
        _FAILED_LOGINS[client_ip] = [t for t in _FAILED_LOGINS[client_ip] if now_ts - t <= BRUTE_FORCE_WINDOW]
        _FAILED_LOGINS[client_ip].append(now_ts)

        fail_count = len(_FAILED_LOGINS[client_ip])
        last_alert = _LAST_BRUTE_FORCE_ALERT.get(client_ip, 0)
        # Alert if threshold is reached (e.g. 5 failed attempts in 60s) and not in cooldown
        if fail_count >= BRUTE_FORCE_THRESHOLD and (now_ts - last_alert > 30):
            _LAST_BRUTE_FORCE_ALERT[client_ip] = now_ts
            threat_type = "brute_force"
            threat_location = "Endpoint"
            matched_payload = f"{fail_count} failed login attempts within {BRUTE_FORCE_WINDOW}s"

    elif method == "POST" and is_login_endpoint and status_code == "200":
        # Clear tracker on successful login
        _FAILED_LOGINS.pop(client_ip, None)

    if not threat_type:
        return {"accepted": True, "detected": False}

    timestamp = str(event.get("time") or datetime.now(timezone.utc).isoformat())
    payload = matched_payload[:2_000]

    threat_names = {
        "sql_injection": "SQL injection",
        "cross_site_scripting": "XSS",
        "command_injection": "Command injection",
        "path_traversal": "Path traversal",
        "brute_force": "Brute force login",
    }
    threat_label = threat_names.get(threat_type, threat_type.replace('_', ' '))

    severity_map = {
        "command_injection": "critical",
        "sql_injection": "high",
        "path_traversal": "high",
        "brute_force": "high",
        "cross_site_scripting": "medium",
    }
    severity = severity_map.get(threat_type, "medium")
    severity_scores = {"critical": 90, "high": 75, "medium": 55, "low": 30}
    severity_score = severity_scores.get(severity, 55)

    rule_id_map = {
        "brute_force": "100101",
        "sql_injection": "100110",
        "cross_site_scripting": "100115",
        "command_injection": "100120",
        "path_traversal": "100118",
    }
    rule_id = rule_id_map.get(threat_type, "juice-proxy-1001")

    mitre_map = {
        "brute_force": ["T1110"],
        "sql_injection": ["T1190"],
        "cross_site_scripting": ["T1059.007"],
        "command_injection": ["T1059"],
        "path_traversal": ["T1083"],
    }
    mitre_ids = mitre_map.get(threat_type, ["T1190"])

    recommendations = {
        "command_injection": f"Isolasi container/host web, hentikan eksekusi command shell unauthorized, dan blokir IP {client_ip} di gateway edge firewall.",
        "sql_injection": f"Terapkan Prepared Statements (parameterized queries), blokir IP {client_ip} pada edge WAF/firewall, dan batasi verbose error database.",
        "path_traversal": f"Validasi dan normalkan path URI sebelum akses filesystem, tolak dot-dot-slash traversal, dan batasi direktori chroot dari {client_ip}.",
        "cross_site_scripting": "Aktifkan Content Security Policy (CSP), terapkan Context-aware HTML entity encoding, dan pasang flag HttpOnly pada semua session cookie.",
        "brute_force": f"Terapkan IP rate-limiting pada endpoint autentikasi, paksa tantangan MFA, dan tinjau potensi kompromi akun dari IP {client_ip}."
    }
    recommended_action = recommendations.get(
        threat_type,
        f"Blokir IP {client_ip} pada edge gateway firewall dan tinjau log request mencurigakan."
    )

    if threat_type == "brute_force":
        description = f"Juice Shop Brute force login detected: {matched_payload}"
        title = f"Juice Shop Brute force attempt (Frequency: {fail_count}/{BRUTE_FORCE_WINDOW}s)"
        attack_story = [{
            "step": 1,
            "title": "High-Frequency Authentication Failures",
            "event": f"Reverse proxy observed {matched_payload} targeting /rest/user/login from {client_ip}.",
            "timestamp": timestamp,
            "phase": "Credential Access",
        }]
        evidence_ref = f"failed_logins_count={fail_count}"
        mitre_context = [{
            "id": "T1110",
            "name": "Brute Force",
            "technique": "Password Guessing",
            "source": "mitre-rule"
        }]
    else:
        description = f"Juice Shop {threat_label} request detected in {threat_location} by proxy access-log inspection"
        title = f"Juice Shop {threat_label} attempt ({threat_location})"
        attack_story = [{
            "step": 1,
            "title": "Suspicious request observed",
            "event": f"Reverse proxy recorded a {threat_type.replace('_', ' ')} pattern in the request {threat_location}.",
            "timestamp": timestamp,
            "phase": "Initial Access",
        }]
        evidence_ref = f"{threat_location.lower().replace(' ', '_')}={payload[:500]}"
        mitre_context = [{"id": m, "name": threat_label, "source": "mitre-rule"} for m in mitre_ids]

    rule_level = 10 if severity == "critical" else (8 if severity == "high" else 5)
    alert = {
        "timestamp": timestamp,
        "agent": {"name": "juice-shop"},
        "rule": {
            "id": rule_id,
            "level": rule_level,
            "description": description,
            "mitre": {"id": mitre_ids}
        },
        "summary": description,
        "recommended_action": recommended_action,
        "data": {
            "srcip": client_ip,
            "url": raw_uri,
            "body": raw_body[:2_000] if raw_body else None,
            "threat_location": threat_location,
            "method": method,
            "status": str(status_code) if status_code else "400",
            "http_status": str(status_code) if status_code else "400",
            "user_agent": str(event.get("user_agent", ""))[:256],
            "threat_type": threat_type,
            "payload": payload,
            "summary": description,
            "recommended_action": recommended_action,
        },
        "full_log": f'{client_ip} - - [{timestamp}] "{method} {raw_uri} HTTP/1.1" {status_code or 400} {len(payload)} "-" "{event.get("user_agent", "")}"'
    }

    # Autonomous AI Investigation Pipeline
    # Runs Gemini tool calling or deterministic local triage fallback to produce real tool_trace
    incident_id = None
    investigation_result: Dict[str, Any] = {}
    dedup_key = f"juice_{client_ip}_{rule_id}"

    try:
        investigation_result = investigate_alert(alert=alert, dedup_key=dedup_key)
        incident_id = investigation_result.get("incident_id")
        logger.info(
            "Autonomous investigation completed for %s: Incident %s (Status: %s, Severity: %s, Engine: %s, ToolTraces: %d)",
            client_ip,
            incident_id,
            investigation_result.get("status"),
            investigation_result.get("severity_label"),
            investigation_result.get("llm_model"),
            len(investigation_result.get("tool_trace") or [])
        )
    except Exception as inv_err:
        logger.exception("AI agent investigation encountered error; falling back to direct persistence: %s", inv_err)
        incident = {
            "dedup_key": dedup_key,
            "wazuh_rule_id": rule_id,
            "title": title,
            "source_ip": client_ip,
            "raw_alert": alert,
            "status": "likely",
            "flags": [threat_type, "juice-shop", "proxy-detected", f"loc-{threat_location.lower().replace(' ', '-')}"] ,
            "severity_score": severity_score,
            "severity_label": severity,
            "confidence_score": 80,
            "summary": description,
            "recommended_action": recommended_action,
            "attack_story": attack_story,
            "pro_evidence": [{
                "claim": description,
                "tool": "nginx-access-log",
                "evidence_ref": evidence_ref,
                "source": "Juice Shop reverse proxy",
                "confidence": "High",
            }],
            "contra_evidence": [],
            "tool_trace": [],
            "mitre_context": mitre_context,
            "llm_model": "signature-fallback",
            "prompt_version": "proxy-v2",
            "human_decision": "pending",
        }
        incident_id = db_insert_incident(incident)

    notification = {
        "event": "security.alert",
        "incident_id": incident_id,
        "timestamp": timestamp,
        "threat_type": threat_type,
        "threat_location": threat_location,
        "severity": investigation_result.get("severity_label") or severity,
        "status": investigation_result.get("status") or "likely",
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
        "status": investigation_result.get("status") or "likely",
        "severity": investigation_result.get("severity_label") or severity,
        "llm_model": investigation_result.get("llm_model") or "signature-fallback",
    }
