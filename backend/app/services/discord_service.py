"""Discord notifications rendered from the same persisted incidents as the dashboard."""
import hashlib
import json
import logging
import threading
import time
from datetime import datetime
from urllib.parse import quote

import httpx

try:
    from app.config import settings
except Exception:
    settings = None

logger = logging.getLogger("soar-api.discord")
DASHBOARD_URL = "https://gtnic-hackwitgoh.vercel.app"
COLORS = {"critical": 0x990000, "high": 0xE74C3C, "medium": 0xE67E22, "low": 0x3498DB}
VERDICTS = {"confirmed": "Malicious", "likely": "Suspicious", "uncertain": "Under Review", "false_positive": "Benign"}
_tracked = {}
_lock = threading.Lock()
_wake = threading.Event()
_worker = None
_retry_at = 0.0


def _object(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return {}
    return value if isinstance(value, dict) else {}


def _text(value, limit=500):
    text = str(value if value is not None else "Unknown") or "Unknown"
    return text if len(text) <= limit else text[:limit - 1] + "…"


def build_incident_embed(incident, incident_id=None):
    """Mirror dashboard labels; do not infer attacks, confidence or enforcement."""
    inc_id = str(incident_id or incident.get("id") or "Unknown")
    raw = _object(incident.get("raw_alert"))
    data = _object(raw.get("data"))
    agent = _object(raw.get("agent"))
    severity = str(incident.get("severity_label") or "unknown").lower()
    title = incident.get("title") or "Unknown"
    summary = incident.get("summary") or raw.get("summary") or _object(raw.get("rule")).get("description") or title
    engine = incident.get("llm_model") or "autonomous-agent"
    pending = engine == "investigation-pending"
    decision = incident.get("human_decision")
    status = ("Approved" if decision == "approved" else "False Positive"
              if decision == "rejected" or incident.get("status") == "false_positive" else "Active Threat")
    score = incident.get("confidence_score")
    score_text = "Awaiting analysis" if pending else f"{score}%" if score is not None else "Not available"
    fields = []

    def field(name, value, limit=500, inline=True):
        fields.append({"name": name, "value": _text(value, limit), "inline": inline})

    field("Severity", severity.title(), 32)
    field("Verdict", VERDICTS.get(incident.get("status"), "Under Review"), 32)
    field("Status", status, 32)
    field("Evidence Score", score_text, 64)
    field("Engine", engine, 100)
    field("Source IP", incident.get("source_ip") or data.get("srcip"), 128)
    field("Target Asset", agent.get("name"), 128)
    field("Target IP", data.get("dstip"), 128)
    field("Incident ID", inc_id, 100)
    field("Request", f"{data.get('method') or 'Unknown'} {data.get('url') or 'Unknown'}", 500, False)
    if data.get("threat_location"):
        field("Input Location", data["threat_location"], 64)
    pro, contra = incident.get("pro_evidence") or [], incident.get("contra_evidence") or []
    field("Evidence / Tool Trace", f"Pro: {len(pro)} | Contra: {len(contra)} | Tool calls: {len(incident.get('tool_trace') or [])}", 100, False)
    for name, evidence in (("Pro Evidence", pro), ("Contra Evidence", contra)):
        if evidence:
            field(name, "\n".join(f"{item.get('claim', '')}: {item.get('evidence_ref', '')}" for item in evidence if isinstance(item, dict)), 500, False)
    story = incident.get("attack_story") or []
    if story:
        field("Attack Story", "\n".join(str(step.get("description") or step.get("event") or step.get("title") or "")
                                       for step in story[:3] if isinstance(step, dict)), 400, False)
    mitre = incident.get("mitre_context") or []
    if mitre:
        field("MITRE ATT&CK", "\n".join(f"{item.get('id', '')} {item.get('name', '')}"
                                        for item in mitre if isinstance(item, dict)), 400, False)
    action = incident.get("recommended_action") or raw.get("recommended_action") or data.get("recommended_action")
    if action and str(action).lower() != "no recommendation provided.":
        field("Suggested Mitigation", action, 600, False)
    if decision == "approved":
        field("Analyst Decision", "Mitigation approved. External execution is not verified.", 100, False)
    url = f"{DASHBOARD_URL}/incidents/{quote(inc_id, safe='')}"
    field("Dashboard", url, 300, False)
    embed = {"title": _text(title, 256), "description": _text(summary, 700), "url": url,
             "color": COLORS.get(severity, 0x95A5A6), "fields": fields,
             "footer": {"text": "GTNIC SOAR | Dashboard incident data | Evidence score is not accuracy"}}
    timestamp = raw.get("timestamp") or incident.get("created_at")
    if timestamp:
        try:
            parsed = timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
            if parsed.tzinfo is not None:
                embed["timestamp"] = parsed.isoformat()
        except (ValueError, TypeError):
            pass
    return embed


def _credentials():
    if settings is None or not getattr(settings, "DISCORD_ENABLED", False):
        return None
    token = str(getattr(settings, "DISCORD_BOT_TOKEN", None) or "").strip().removeprefix("Bot ").strip()
    channel = str(getattr(settings, "DISCORD_CHANNEL_ID", None) or "").strip()
    if not token or not channel:
        logger.warning("Discord requires DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID on the backend server")
        return None
    return token, channel


def _upsert(incident, inc_id):
    """Edit the original alert when the dashboard's analysis or decision changes."""
    global _retry_at
    credentials = _credentials()
    if not credentials or time.monotonic() < _retry_at:
        return False
    token, channel = credentials
    embed = build_incident_embed(incident, inc_id)
    fingerprint = hashlib.sha256(json.dumps(embed, sort_keys=True).encode()).hexdigest()
    with _lock:
        state = dict(_tracked.setdefault(inc_id, {"message_id": None, "fingerprint": None}))
    if state["fingerprint"] == fingerprint:
        return True
    url = f"https://discord.com/api/v10/channels/{channel}/messages"
    if state["message_id"]:
        url += "/" + state["message_id"]
    payload = {"embeds": [embed], "allowed_mentions": {"parse": []}}
    try:
        with httpx.Client(timeout=6.0) as client:
            response = client.request("PATCH" if state["message_id"] else "POST", url,
                                      headers={"Authorization": f"Bot {token}"}, json=payload)
        if response.status_code == 429:
            _retry_at = time.monotonic() + max(float(response.json().get("retry_after", 3)), 0.1)
            logger.warning("Discord rate limited; respecting retry_after")
            return False
        if response.status_code == 404 and state["message_id"]:
            with _lock:
                _tracked[inc_id] = {"message_id": None, "fingerprint": None}
            return False
        if response.status_code in (401, 403):
            _retry_at = time.monotonic() + 60
            logger.error("Discord HTTP %s: check bot token, channel access, Send Messages and Embed Links", response.status_code)
            return False
        response.raise_for_status()
        message_id = state["message_id"] or str(response.json()["id"])
        with _lock:
            _tracked[inc_id] = {"message_id": message_id, "fingerprint": fingerprint}
        return True
    except Exception:
        logger.exception("Discord delivery failed for incident %s; will retry", inc_id)
        return False


def send_discord_alert(incident, incident_id=None):
    """Send only a saved dashboard incident, never a caller-provided test payload."""
    from app.database import db_fetch_incident_by_id
    inc_id = str(incident_id or incident.get("id") or "")
    if not _credentials() or not inc_id:
        return False
    current = db_fetch_incident_by_id(inc_id)
    return _upsert(current, inc_id) if current else False


def _sync_once():
    from app.database import db_fetch_incidents, db_fetch_incident_by_id
    if not _credentials() or time.monotonic() < _retry_at:
        return
    rows = {str(row["id"]): row for row in db_fetch_incidents()}
    with _lock:
        tracked = list(_tracked.items())
    for inc_id, state in tracked:
        current = rows.get(inc_id)
        if current is None:
            if state["message_id"]:
                # Stop watching rows no longer in the dashboard's recent queue.
                # An empty response may be a temporary DB outage; retain state.
                if len(rows) >= 100:
                    with _lock:
                        _tracked.pop(inc_id, None)
                continue
            current = db_fetch_incident_by_id(inc_id)
        if current:
            _upsert(current, inc_id)
        if time.monotonic() < _retry_at:
            break


def dispatch_discord_alert_async(incident, incident_id=None):
    """One notifier thread; ingestion and investigation never wait for Discord."""
    global _worker
    if not _credentials():
        return
    inc_id = str(incident_id or incident.get("id") or "")
    if not inc_id:
        return
    with _lock:
        _tracked.setdefault(inc_id, {"message_id": None, "fingerprint": None})
        if _worker is None or not _worker.is_alive():
            def run():
                while True:
                    _wake.wait(3)
                    _wake.clear()
                    try:
                        _sync_once()
                    except Exception:
                        logger.exception("Discord dashboard synchronization failed; will retry")
            _worker = threading.Thread(target=run, name="discord-dashboard-sync", daemon=True)
            _worker.start()
    _wake.set()
