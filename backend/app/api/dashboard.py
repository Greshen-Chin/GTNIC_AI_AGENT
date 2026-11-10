import logging
from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import verify_dashboard_api_key
from app.services.detection_evaluation import evaluate_detector
from app.schemas.incident import (
    IncidentResponse,
    DecisionRequest,
    DecisionResponse,
    IncidentSummaryStats,
)
from app.schemas.benchmark import (
    BenchmarkRunItem,
    BenchmarkSummary,
)
from app.database import (
    db_fetch_incidents,
    db_fetch_incident_by_id,
    db_update_incident_decision,
    db_fetch_stats,
    db_fetch_benchmarks,
)

logger = logging.getLogger("soar-api.dashboard")

router = APIRouter(
    prefix="/api",
    tags=["Dashboard & SOC Analyst API"],
    dependencies=[Depends(verify_dashboard_api_key)]
)


@router.get(
    "/incidents",
    response_model=List[IncidentResponse],
    summary="List all investigated incidents",
    description="Returns recorded incidents, including those awaiting investigation."
)
def get_incidents():
    incidents = db_fetch_incidents()
    return incidents


@router.get(
    "/incidents/{incident_id}",
    response_model=IncidentResponse,
    summary="Get single incident detail",
    description="Returns full incident details including Attack Story, Pro vs Contra Evidence, and Tool Traces."
)
def get_incident(incident_id: str):
    inc = db_fetch_incident_by_id(incident_id)
    if not inc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found"
        )
    return inc


@router.post(
    "/incidents/{incident_id}/decision",
    response_model=DecisionResponse,
    summary="Record human analyst decision (Approve / Reject)",
    description="Records human approval or rejection of AI recommended mitigation, saving decided_by and decided_at."
)
def record_decision(incident_id: str, payload: DecisionRequest):
    decided_by = payload.decided_by or "soc-analyst"
    clean_decision = payload.decision.lower()

    if clean_decision not in ("approved", "rejected"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Decision must be 'approved' or 'rejected'"
        )

    updated = db_update_incident_decision(
        incident_id=incident_id,
        decision=clean_decision,
        decided_by=decided_by
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with ID {incident_id} not found"
        )

    action_text = "mitigation approved" if clean_decision == "approved" else "marked as false positive"
    return DecisionResponse(
        id=updated["id"],
        human_decision=updated["human_decision"],
        decided_by=updated["decided_by"],
        decided_at=updated["decided_at"] if isinstance(updated["decided_at"], datetime) else datetime.now(timezone.utc),
        message=f"Incident successfully {action_text} by {decided_by}"
    )


@router.get(
    "/stats",
    response_model=IncidentSummaryStats,
    summary="Get summary metrics for SOC dashboard",
    description="Calculates total incidents, active count, critical count, high count, and average confidence score."
)
def get_stats():
    stats = db_fetch_stats()
    evaluation = evaluate_detector()
    stats.update(detectionAccuracy=evaluation["accuracy"] / 100, evaluationCases=evaluation["total_scenarios"], evaluationCorrect=evaluation["correct"], evaluationVersion=evaluation["dataset_version"])
    return stats


@router.get("/benchmark", summary="Measured request-detector lab evaluation")
def get_benchmark():
    return evaluate_detector()
