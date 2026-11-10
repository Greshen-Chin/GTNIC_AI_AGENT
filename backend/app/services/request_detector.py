"""Context-aware request signatures. A match proves a pattern, never exploitation."""
import json
import re
from urllib.parse import unquote, parse_qsl, urlsplit

DETECTOR_VERSION = "context-signatures-v1"

PATTERNS = {
    "command_injection": re.compile(r"(?:[;|]\s*(?:cat|ls|id|whoami|curl|wget|bash|sh|powershell)\b|`[^`]+`|\$\([^)]+\))", re.I),
    "sql_injection": re.compile(r"(?:\bunion\s+(?:all\s+)?select\b|\bselect\b.+\bfrom\b|\b(?:or|and)\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+|['\"]\s*(?:--|#|/\*)|;\s*(?:drop|delete|update|insert)\b|\b(?:sleep|benchmark|pg_sleep)\s*\()", re.I),
    "path_traversal": re.compile(r"(?:\.\.[/\\]|/etc/(?:passwd|shadow)\b|\b(?:boot|win)\.ini\b)", re.I),
    "cross_site_scripting": re.compile(r"<\s*script\b|javascript\s*:|\bonerror\s*=|\bonload\s*=|<\s*svg\b", re.I),
}


def decode(value):
    value = str(value)
    for _ in range(2):
        decoded = unquote(value)
        if decoded == value:
            break
        value = decoded
    return value


def request_inputs(uri, body):
    """Keep input fields separate and recognize Juice Shop's challenge telemetry."""
    uri, body = str(uri or "")[:8000], str(body or "")[:16000]
    try:
        parsed = urlsplit(uri)
    except ValueError:
        parsed = urlsplit("/")
    if parsed.path.startswith("/socket.io/") and body:
        frames = body.split("\x1e")
        try:
            events = [json.loads(frame[2:]) for frame in frames if frame.startswith("42")]
            if len(events) == len(frames) and all(
                isinstance(event, list) and event and event[0] in
                {"verifyLocalXssChallenge", "verifySvgInjectionChallenge"} for event in events
            ):
                return []
        except (ValueError, TypeError):
            pass
    inputs = [("URL", decode(parsed.path))]
    inputs += [("URL", decode(value)) for _, value in parse_qsl(parsed.query, keep_blank_values=True)]

    def values(value):
        if isinstance(value, dict):
            return [text for child in value.values() for text in values(child)]
        if isinstance(value, list):
            return [text for child in value for text in values(child)]
        return [str(value)] if isinstance(value, (str, int, float)) else []

    if body:
        try:
            texts = values(json.loads(body))
        except (ValueError, TypeError):
            texts = ([value for _, value in parse_qsl(body, keep_blank_values=True)]
                     if re.match(r"^[\w.\[\]-]+=", body) else [body])
        inputs += [("Request Body", decode(text)) for text in texts]
    return inputs


def detect_request(event):
    inputs = request_inputs(event.get("uri"), event.get("body"))
    for threat_type, pattern in PATTERNS.items():
        for location, text in inputs:
            match = pattern.search(text)
            if match:
                return {"threat_type": threat_type, "threat_location": location,
                        "payload": text[:2000], "matched_pattern": match.group(0)[:500]}
    return None


def inspect_current_request(alert):
    data = alert.get("data") or {}
    result = detect_request({"uri": data.get("url"), "body": data.get("body")})
    facts = ["pattern_detected=" + str(bool(result)).lower()]
    if result:
        facts += [f"threat_type={result['threat_type']}", f"matched_pattern={result['matched_pattern']}"]
    return {"facts": facts, "detection": result, "provenance": {"source": "recorded-request"},
            "limitation": "Pattern evidence only; exploitation outcome is not verified."}
