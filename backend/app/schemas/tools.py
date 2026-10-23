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


class LoginHistoryResponse(BaseModel):
    srcip: str
    failed_count: int
    success_count: int
    window: str = "24h"
    facts: List[str] = Field(
        ...,
        description="Deterministic factual strings referenced by the AI Agent (e.g. failed_count=10, success_count=0)"
    )


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
