import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


IP_REGEX = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


class IpIn(BaseModel):
    srcip: str = Field(
        ...,
        description="IPv4 address to query in Wazuh Indexer",
        json_schema_extra={"example": "203.0.113.10"}
    )

    @field_validator("srcip")
    @classmethod
    def validate_ipv4(cls, v: str) -> str:
        clean_ip = v.strip()
        if not IP_REGEX.match(clean_ip):
            raise ValueError(f"Invalid IPv4 format: {clean_ip}")
        parts = clean_ip.split(".")
        if any(not (0 <= int(p) <= 255) for p in parts):
            raise ValueError(f"IPv4 octets out of range (0-255): {clean_ip}")
        return clean_ip


class SearchAlertsIn(IpIn):
    time_window: str = Field(default="now-24h", description="Time window for OpenSearch query")
    max_alerts: int = Field(default=20, ge=1, le=50, description="Max alerts to retrieve")


class SearchAlertsResponse(BaseModel):
    srcip: str
    facts: List[str] = Field(
        ...,
        description="Deterministic factual strings referenced by the AI Agent (e.g. alert_count=12, distinct_rules=3)"
    )
    total_hits: int
    rule_ids: List[str]
    alerts: List[Dict[str, Any]] = Field(default_factory=list)
    provenance: Optional[Dict[str, Any]] = None


class LoginHistoryResponse(BaseModel):
    srcip: str
    failed_count: int
    success_count: int
    window: str = "24h"
    facts: List[str] = Field(
        ...,
        description="Deterministic factual strings referenced by the AI Agent (e.g. failed_count=10, success_count=0)"
    )
    provenance: Optional[Dict[str, Any]] = None


class RagQueryIn(BaseModel):
    query: str = Field(..., min_length=2, max_length=500, description="Cybersecurity attack query or alert summary")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of MITRE ATT&CK / OWASP context chunks to retrieve")


class RagMatchItem(BaseModel):
    id: int
    source: str
    content: str
    metadata: Dict[str, Any]
    similarity: float
    doc_ref: str
    mitre_id: Optional[str] = None
    owasp_id: Optional[str] = None


class RagResponse(BaseModel):
    query: str
    facts: List[str] = Field(
        ...,
        description="Deterministic factual strings referenced by the AI Agent (e.g. doc:42, mitre:T1110, owasp:A07)"
    )
    matches: List[RagMatchItem]


class WebAttackIn(IpIn):
    attack_type: str = Field(
        default="all",
        description="Filter by attack vector: 'all', 'sqli', or 'xss'"
    )
    time_window: str = Field(
        default="now-24h",
        description="Time window for OpenSearch query (e.g. 'now-24h', 'now-1h')"
    )


class SqlAttackDetail(BaseModel):
    detected: bool = False
    sqli_types: List[str] = Field(default_factory=list, description="e.g. union_based, boolean_based, error_based, time_based")
    sample_payloads: List[str] = Field(default_factory=list)
    targeted_parameters: List[str] = Field(default_factory=list)
    database_error_reflected: bool = False


class XssAttackDetail(BaseModel):
    detected: bool = False
    xss_types: List[str] = Field(default_factory=list, description="e.g. reflected_script_tag, event_handler_attribute, javascript_pseudo_protocol")
    sample_payloads: List[str] = Field(default_factory=list)
    targeted_parameters: List[str] = Field(default_factory=list)
    csp_enforced: bool = False
    httponly_protected: bool = False


class InspectWebAttackResponse(BaseModel):
    srcip: str
    total_web_alerts: int
    attack_type_queried: str
    status_breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="HTTP Response status counts, e.g. {'200': 5, '403': 12, '500': 3}"
    )
    endpoints_targeted: List[str] = Field(default_factory=list)
    sqli: SqlAttackDetail = Field(default_factory=SqlAttackDetail)
    xss: XssAttackDetail = Field(default_factory=XssAttackDetail)
    waf_mitigated: bool = False
    facts: List[str] = Field(
        ...,
        description="Deterministic factual strings referenced by the AI Agent (e.g. sqli_detected=true, http_500_count=3, target_param=id)"
    )
    provenance: Optional[Dict[str, Any]] = None

