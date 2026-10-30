"""Lightweight detection and n8n reporting for requests reaching soar-api."""

import json
import logging
import re
from datetime import datetime, timezone

import httpx

from app.config import settings

logger = logging.getLogger("soar-api.security")

# Catch common SQLi probes, including the classic `' OR 1=1 --` example.
SQLI_PATTERN = re.compile(
    r"(?:\bunion\s+(?:all\s+)?select\b|\bselect\b.+\bfrom\b|"
    r"\bor\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+|"
    r"['\"]\s*or\s+['\"\w]+\s*=|--\s|;\s*(?:drop|delete|update|insert)\b|"
    r"\bsleep\s*\(|\bbenchmark\s*\()",
    re.IGNORECASE,
)
MAX_INSPECT_BYTES = 1_000_000
MAX_PAYLOAD_CHARS = 4_000


class AttackWebhookMiddleware:
    """Inspect incoming URL/body text and report likely SQL injection probes."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Buffer and replay the ASGI body so inspection does not consume it for FastAPI.
        messages = []
        body = bytearray()
        more_body = True
        while more_body:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            messages.append(message)
            body.extend(message.get("body", b""))
            more_body = message.get("more_body", False)

        async def replay_body():
            if messages:
                return messages.pop(0)
            return {"type": "http.request", "body": b"", "more_body": False}

        searchable = (
            scope.get("query_string", b"") + b"\n" + bytes(body[:MAX_INSPECT_BYTES])
        ).decode("utf-8", errors="replace")
        match = SQLI_PATTERN.search(searchable)
        if match:
            # Report the matched input context, not unrelated parts of the request.
            payload = searchable[max(0, match.start() - 100):match.end() + 300]
            await self._send_alert(scope, payload[:MAX_PAYLOAD_CHARS])

        await self.app(scope, replay_body, send)

    async def _send_alert(self, scope, payload):
        if not settings.WEBHOOK_URL:
            logger.warning("SQL injection-like request detected, but WEBHOOK_URL is not configured")
            return

        client = scope.get("client")
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "threat_type": "sql_injection",
            "ip": client[0] if client else "unknown",
            "payload": payload,
        }
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(settings.WEBHOOK_URL, json=event)
                response.raise_for_status()
        except httpx.HTTPError:
            # The application request should continue if n8n is temporarily unavailable.
            logger.exception("Failed to deliver security event to n8n webhook")
