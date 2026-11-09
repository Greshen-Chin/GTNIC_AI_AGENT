"""
Discord Alert Service for GTNIC SOAR AI Agent.
Dispatches real-time, rich embed security incident notifications to Discord via the REST API v10.
"""

import logging
import threading
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import json

try:
    import httpx
except ImportError:
    httpx = None

import urllib.request
import ssl

try:
    from app.config import settings
except Exception:
    settings = None

logger = logging.getLogger("soar-api.discord")

# Color mapping by severity (integer hex for Discord embed)
SEVERITY_COLORS = {
    "critical": 0x990000,  # Dark Crimson
    "high": 0xE74C3C,      # Red
    "medium": 0xE67E22,    # Amber
    "low": 0x3498DB,       # Blue
}

SEVERITY_EMOJIS = {
    "critical": "🚨",
    "high": "⚠️",
    "medium": "🟡",
    "low": "ℹ️",
}


def build_incident_embed(incident: Dict[str, Any], incident_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Constructs a structured Discord Embed object representing the security incident.
    """
    inc_id = incident_id or incident.get("id") or "N/A"
    raw_alert = incident.get("raw_alert") or {}
    if isinstance(raw_alert, str):
        try:
            raw_alert = json.loads(raw_alert)
        except Exception:
            raw_alert = {}
    if not isinstance(raw_alert, dict):
        raw_alert = {}

    alert_data = raw_alert.get("data") or {}
    if not isinstance(alert_data, dict):
        alert_data = {}

    severity_label = str(incident.get("severity_label", "medium")).lower()
    severity_score = incident.get("severity_score", 50)
    confidence_score = incident.get("confidence_score", 50)
    status = incident.get("status", "likely")
    title = incident.get("title") or "Security Alert Incident"
    source_ip = incident.get("source_ip") or alert_data.get("srcip") or "Unknown"

    color = SEVERITY_COLORS.get(severity_label, 0x95A5A6)
    emoji = SEVERITY_EMOJIS.get(severity_label, "🛡️")

    # Extract target and payload details
    target = alert_data.get("threat_location") or raw_alert.get("agent", {}).get("name") or "System / Host"
    threat_type = alert_data.get("threat_type") or incident.get("flags", ["unknown"])[0]
    payload = alert_data.get("payload") or alert_data.get("url") or ""

    # Truncate payload safely for Discord embed field limit (1024 chars)
    payload_display = str(payload).strip()
    if len(payload_display) > 500:
        payload_display = payload_display[:497] + "..."

    timestamp = (
        incident.get("created_at")
        or alert_data.get("timestamp")
        or datetime.now(timezone.utc).isoformat()
    )

    fields = [
        {"name": "🎯 Threat Type", "value": f"`{threat_type}`", "inline": True},
        {"name": "🌐 Attacker IP", "value": f"`{source_ip}`", "inline": True},
        {"name": "📍 Location / Target", "value": f"`{target}`", "inline": True},
        {
            "name": "📊 Severity & Confidence",
            "value": f"**{severity_label.upper()}** (Score: {severity_score}/100) • **{confidence_score}%** Confidence",
            "inline": True,
        },
        {"name": "⚖️ Triage Verdict", "value": f"`{status}`", "inline": True},
        {"name": "🎫 Incident ID", "value": f"`{inc_id}`", "inline": True},
    ]

    if payload_display:
        fields.append({
            "name": "🔍 Observed Payload / Evidence",
            "value": f"```{payload_display}```",
            "inline": False,
        })

    # Add attack story preview if present
    attack_story = incident.get("attack_story") or []
    if attack_story and isinstance(attack_story, list) and len(attack_story) > 0:
        step1 = attack_story[0]
        event_desc = step1.get("event") or step1.get("title") or ""
        if event_desc:
            fields.append({
                "name": "📖 Attack Summary",
                "value": str(event_desc)[:300],
                "inline": False,
            })

    embed = {
        "title": f"{emoji} [{severity_label.upper()}] {title}",
        "description": f"A new security event has been logged and correlated by the **GTNIC SOAR Agent**.",
        "color": color,
        "fields": fields,
        "footer": {
            "text": f"GTNIC AI Defense Engine • {incident.get('llm_model', 'SOAR')}",
        },
        "timestamp": timestamp,
    }

    return embed


def send_discord_alert(incident: Dict[str, Any], incident_id: Optional[str] = None) -> bool:
    """
    Synchronously posts the incident embed to the configured Discord channel using Discord REST API v10.
    """
    if settings is None or not getattr(settings, "DISCORD_ENABLED", False):
        logger.debug("Discord alert skipped: DISCORD_ENABLED is false or settings missing")
        return False

    token = getattr(settings, "DISCORD_BOT_TOKEN", None)
    channel_id = getattr(settings, "DISCORD_CHANNEL_ID", None)

    if not token or not channel_id:
        logger.warning("Discord alert skipped: DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID is not configured")
        return False

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "GTNIC-SOAR-Agent (https://gtnic.internal, 2.0)",
    }

    embed = build_incident_embed(incident, incident_id=incident_id)
    payload = {
        "content": "🚨 **New Security Attack Detected**",
        "embeds": [embed],
    }

    try:
        if httpx is not None:
            with httpx.Client(timeout=6.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                resp.raise_for_status()
        else:
            ctx = ssl.create_default_context()
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data_bytes, headers=headers)
            with urllib.request.urlopen(req, timeout=6.0, context=ctx) as r:
                if r.status >= 400:
                    raise RuntimeError(f"HTTP {r.status}")
        logger.info("Discord alert dispatched successfully for incident %s", incident_id or incident.get("id"))
        return True
    except Exception as e:
        logger.exception("Failed to dispatch Discord alert: %s", e)
        return False


def dispatch_discord_alert_async(incident: Dict[str, Any], incident_id: Optional[str] = None) -> None:
    """
    Non-blocking worker that dispatches the Discord alert in a background daemon thread.
    Ensures that ingestion and database operations return instantly without waiting for Discord.
    """
    thread = threading.Thread(
        target=send_discord_alert,
        args=(incident, incident_id),
        name=f"discord-alert-{incident_id or 'bg'}",
        daemon=True,
    )
    thread.start()
