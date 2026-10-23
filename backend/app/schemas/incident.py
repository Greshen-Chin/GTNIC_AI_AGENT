from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


StatusType = Literal["confirmed", "likely", "uncertain", "false_positive"]
SeverityLabelType = Literal["low", "medium", "high", "critical"]
HumanDecisionType = Literal["pending", "approved", "rejected"]


class EvidenceItem(BaseModel):
    claim: str
    tool: str  # e.g. "get_login_history", "search_alerts_by_ip", "mitre_owasp_rag", or "alert"
    evidence_ref: str  # e.g. "failed_count=10", "level=5", "rule_id=100100"
    source: Optional[str] = None
    confidence: Optional[str] = "High"


class AttackStoryStep(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    step: int = Field(default=1, alias="stepNumber")
    event: str = Field(..., alias="description")
    title: Optional[str] = None
    timestamp: Optional[str] = None
    phase: Optional[str] = "Initial Access"


class ToolTraceStep(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = None
    tool: str = Field(..., alias="toolName")
    facts: List[str] = Field(default_factory=list)
    duration_ms: Optional[int] = Field(default=0, alias="durationMs")
    executed_at: Optional[str] = Field(default=None, alias="executedAt")
    status: Optional[str] = "success"
    input: Optional[Dict[str, Any]] = Field(default_factory=dict)
    output: Optional[Dict[str, Any]] = Field(default_factory=dict)


class MitreItem(BaseModel):
    id: str  # e.g. "T1110"
    name: str
    tactic: Optional[str] = "Initial Access"
    doc_ref: Optional[str] = None
    description: Optional[str] = None
    mitigationAdvice: Optional[str] = None


class OwaspItem(BaseModel):
    id: str  # e.g. "A03:2021"
    name: str
    description: Optional[str] = None
    remediation: Optional[str] = None


class IncidentCreate(BaseModel):
    dedup_key: Optional[str] = None
    suppressed_count: int = 0
    wazuh_rule_id: Optional[str] = None
    title: str
    source_ip: Optional[str] = None
    raw_alert: Optional[Dict[str, Any]] = None
    status: StatusType = "uncertain"
    flags: List[str] = Field(default_factory=list)
    severity_score: int = Field(default=50, ge=10, le=100)
    severity_label: SeverityLabelType = "medium"
    confidence_score: int = Field(default=50, ge=0, le=100)
    attack_story: List[Dict[str, Any]] = Field(default_factory=list)
    pro_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    contra_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    invalid_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    tool_trace: List[Dict[str, Any]] = Field(default_factory=list)
    mitre_context: List[Dict[str, Any]] = Field(default_factory=list)
    llm_model: Optional[str] = None
    prompt_version: Optional[str] = "v2.0"
    tokens_in: Optional[int] = 0
    tokens_out: Optional[int] = 0
    latency_ms: Optional[int] = 0


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: Optional[datetime] = None
    dedup_key: Optional[str] = None
    suppressed_count: int = 0
    wazuh_rule_id: Optional[str] = None
    title: str
    source_ip: Optional[str] = None
    raw_alert: Optional[Dict[str, Any]] = None
    status: StatusType
    flags: List[str] = Field(default_factory=list)
    severity_score: int
    severity_label: SeverityLabelType
    confidence_score: int
    attack_story: List[Dict[str, Any]] = Field(default_factory=list)
    pro_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    contra_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    invalid_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    tool_trace: List[Dict[str, Any]] = Field(default_factory=list)
    mitre_context: List[Dict[str, Any]] = Field(default_factory=list)
    llm_model: Optional[str] = None
    prompt_version: Optional[str] = None
    tokens_in: Optional[int] = 0
    tokens_out: Optional[int] = 0
    latency_ms: Optional[int] = 0
    human_decision: HumanDecisionType = "pending"
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None


class DecisionRequest(BaseModel):
    decision: Literal["approved", "rejected", "Approved", "Rejected"]
    decided_by: Optional[str] = Field(default="soc-analyst", description="Name or ID of reviewer")


class DecisionResponse(BaseModel):
    id: str
    human_decision: HumanDecisionType
    decided_by: str
    decided_at: datetime
    message: str


class IncidentSummaryStats(BaseModel):
    totalIncidents: int
    criticalCount: int
    highCount: int
    activeCount: int
    mitigatedCount: int
    aiAverageConfidence: float


class AgentInvestigateRequest(BaseModel):
    alert: Dict[str, Any] = Field(..., description="Raw Wazuh alert JSON")
    dedup_key: Optional[str] = None


class AgentInvestigateResponse(BaseModel):
    incident_id: Optional[str] = None
    status: StatusType
    severity_score: int
    severity_label: SeverityLabelType
    confidence_score: int
    flags: List[str]
    attack_story: List[Dict[str, Any]]
    pro_evidence: List[Dict[str, Any]]
    contra_evidence: List[Dict[str, Any]]
    invalid_evidence: List[Dict[str, Any]]
    tool_trace: List[Dict[str, Any]]
    mitre: List[Dict[str, Any]]
    summary: str
    recommended_action: str
    llm_model: str
    latency_ms: int
