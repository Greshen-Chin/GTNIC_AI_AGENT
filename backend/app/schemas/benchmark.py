from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class BenchmarkRunItem(BaseModel):
    id: Optional[str] = None
    run_id: str
    scenario_name: str
    expected_verdict: str
    detected: bool = True
    agent_verdict: str
    baseline_verdict: Optional[str] = None
    agent_time_ms: int
    baseline_time_ms: Optional[int] = None
    agent_tokens: Optional[int] = 0
    baseline_tokens: Optional[int] = 0
    evidence_valid_ratio: Optional[float] = 1.0
    evidence_completeness: Optional[float] = 1.0
    created_at: Optional[datetime] = None


class BenchmarkSummary(BaseModel):
    total_scenarios: int
    agent_accuracy: float
    baseline_accuracy: float
    false_positive_rate: float
    false_negative_rate: float
    avg_evidence_validity: float
    avg_agent_time_ms: float
    runs: List[BenchmarkRunItem] = Field(default_factory=list)
