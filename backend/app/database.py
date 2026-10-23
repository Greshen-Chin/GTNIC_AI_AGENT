import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector

from app.config import settings

logger = logging.getLogger("soar-api.database")

# In-memory store fallback when PostgreSQL is unreachable (e.g. local unit tests or dry runs)
_IN_MEMORY_INCIDENTS: List[Dict[str, Any]] = []
_IN_MEMORY_BENCHMARKS: List[Dict[str, Any]] = []
_USE_FALLBACK = False


def get_connection_string() -> str:
    """
    Constructs PostgreSQL connection string directly from .env variables.
    """
    return (
        f"host={settings.POSTGRES_HOST} "
        f"port={settings.POSTGRES_PORT} "
        f"dbname={settings.POSTGRES_DB} "
        f"user={settings.POSTGRES_USER} "
        f"password={settings.POSTGRES_PASSWORD} "
        f"connect_timeout=3"
    )


def test_postgres_connection() -> bool:
    global _USE_FALLBACK
    try:
        with psycopg.connect(get_connection_string(), autocommit=True) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                res = cur.fetchone()
                if res and res[0] == 1:
                    _USE_FALLBACK = False
                    logger.info("Successfully connected to PostgreSQL (pgvector active)")
                    return True
    except Exception as e:
        logger.warning(
            f"PostgreSQL connection to {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT} ({settings.POSTGRES_DB}) failed: {e}. "
            "Activating local memory store fallback."
        )
        _USE_FALLBACK = True
        return False


def get_db():
    if _USE_FALLBACK:
        return None
    try:
        conn = psycopg.connect(get_connection_string(), row_factory=dict_row)
        register_vector(conn)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return None


# =========================================================================
# Incident Database Operations
# =========================================================================

def db_fetch_incidents() -> List[Dict[str, Any]]:
    conn = get_db()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, created_at, dedup_key, suppressed_count, wazuh_rule_id,
                               title, source_ip, raw_alert, status, flags, severity_score,
                               severity_label, confidence_score, attack_story, pro_evidence,
                               contra_evidence, invalid_evidence, tool_trace, mitre_context,
                               llm_model, prompt_version, tokens_in, tokens_out, latency_ms,
                               human_decision, decided_by, decided_at
                        FROM incidents
                        ORDER BY created_at DESC
                        LIMIT 100;
                        """
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        if isinstance(row.get("id"), uuid.UUID):
                            row["id"] = str(row["id"])
                    return rows
        except Exception as e:
            logger.error(f"Error querying incidents from DB: {e}")

    # Fallback in-memory
    return sorted(
        _IN_MEMORY_INCIDENTS,
        key=lambda x: str(x.get("created_at", "")),
        reverse=True
    )


def db_fetch_incident_by_id(incident_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, created_at, dedup_key, suppressed_count, wazuh_rule_id,
                               title, source_ip, raw_alert, status, flags, severity_score,
                               severity_label, confidence_score, attack_story, pro_evidence,
                               contra_evidence, invalid_evidence, tool_trace, mitre_context,
                               llm_model, prompt_version, tokens_in, tokens_out, latency_ms,
                               human_decision, decided_by, decided_at
                        FROM incidents
                        WHERE id = %s;
                        """,
                        (incident_id,)
                    )
                    row = cur.fetchone()
                    if row and isinstance(row.get("id"), uuid.UUID):
                        row["id"] = str(row["id"])
                    return row
        except Exception as e:
            logger.error(f"Error fetching incident {incident_id}: {e}")

    for inc in _IN_MEMORY_INCIDENTS:
        if str(inc.get("id")) == str(incident_id):
            return inc
    return None


def db_insert_incident(inc_data: Dict[str, Any]) -> str:
    inc_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    conn = get_db()

    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO incidents (
                            id, created_at, dedup_key, suppressed_count, wazuh_rule_id,
                            title, source_ip, raw_alert, status, flags, severity_score,
                            severity_label, confidence_score, attack_story, pro_evidence,
                            contra_evidence, invalid_evidence, tool_trace, mitre_context,
                            llm_model, prompt_version, tokens_in, tokens_out, latency_ms,
                            human_decision, decided_by, decided_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        ) RETURNING id;
                        """,
                        (
                            inc_id,
                            now,
                            inc_data.get("dedup_key"),
                            inc_data.get("suppressed_count", 0),
                            inc_data.get("wazuh_rule_id"),
                            inc_data.get("title", "Wazuh Alert Incident"),
                            inc_data.get("source_ip"),
                            json.dumps(inc_data.get("raw_alert", {})),
                            inc_data.get("status", "uncertain"),
                            json.dumps(inc_data.get("flags", [])),
                            inc_data.get("severity_score", 50),
                            inc_data.get("severity_label", "medium"),
                            inc_data.get("confidence_score", 50),
                            json.dumps(inc_data.get("attack_story", [])),
                            json.dumps(inc_data.get("pro_evidence", [])),
                            json.dumps(inc_data.get("contra_evidence", [])),
                            json.dumps(inc_data.get("invalid_evidence", [])),
                            json.dumps(inc_data.get("tool_trace", [])),
                            json.dumps(inc_data.get("mitre_context", [])),
                            inc_data.get("llm_model", settings.LLM_MODEL),
                            inc_data.get("prompt_version", "v2.0"),
                            inc_data.get("tokens_in", 0),
                            inc_data.get("tokens_out", 0),
                            inc_data.get("latency_ms", 0),
                            inc_data.get("human_decision", "pending"),
                            inc_data.get("decided_by"),
                            inc_data.get("decided_at")
                        )
                    )
                    created_id = cur.fetchone()["id"]
                    conn.commit()
                    return str(created_id)
        except Exception as e:
            logger.error(f"Error inserting incident into Postgres: {e}")

    # Fallback in-memory
    inc_record = {
        **inc_data,
        "id": inc_id,
        "created_at": now.isoformat(),
        "human_decision": inc_data.get("human_decision", "pending")
    }
    _IN_MEMORY_INCIDENTS.insert(0, inc_record)
    return inc_id


def db_update_incident_decision(incident_id: str, decision: str, decided_by: str) -> Optional[Dict[str, Any]]:
    clean_decision = decision.lower()
    now = datetime.now(timezone.utc)
    conn = get_db()

    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE incidents
                        SET human_decision = %s,
                            decided_by = %s,
                            decided_at = %s
                        WHERE id = %s
                        RETURNING id, human_decision, decided_by, decided_at;
                        """,
                        (clean_decision, decided_by, now, incident_id)
                    )
                    row = cur.fetchone()
                    conn.commit()
                    if row:
                        return {
                            "id": str(row["id"]),
                            "human_decision": row["human_decision"],
                            "decided_by": row["decided_by"],
                            "decided_at": row["decided_at"]
                        }
        except Exception as e:
            logger.error(f"Error updating incident decision in Postgres: {e}")

    # Fallback in-memory
    for inc in _IN_MEMORY_INCIDENTS:
        if str(inc.get("id")) == str(incident_id):
            inc["human_decision"] = clean_decision
            inc["decided_by"] = decided_by
            inc["decided_at"] = now.isoformat()
            return {
                "id": str(inc["id"]),
                "human_decision": clean_decision,
                "decided_by": decided_by,
                "decided_at": now
            }
    return None


def db_fetch_stats() -> Dict[str, Any]:
    conn = get_db()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT 
                            COUNT(*) as total,
                            COUNT(*) FILTER (WHERE severity_label = 'critical') as critical_count,
                            COUNT(*) FILTER (WHERE severity_label = 'high') as high_count,
                            COUNT(*) FILTER (WHERE human_decision = 'pending') as active_count,
                            COUNT(*) FILTER (WHERE human_decision = 'approved') as mitigated_count,
                            COALESCE(AVG(confidence_score), 0) as avg_confidence
                        FROM incidents;
                        """
                    )
                    r = cur.fetchone()
                    if r:
                        return {
                            "totalIncidents": r["total"],
                            "criticalCount": r["critical_count"],
                            "highCount": r["high_count"],
                            "activeCount": r["active_count"],
                            "mitigatedCount": r["mitigated_count"],
                            "aiAverageConfidence": float(r["avg_confidence"]) / 100.0
                        }
        except Exception as e:
            logger.error(f"Error computing incident stats: {e}")

    total = len(_IN_MEMORY_INCIDENTS)
    critical = sum(1 for i in _IN_MEMORY_INCIDENTS if i.get("severity_label") == "critical")
    high = sum(1 for i in _IN_MEMORY_INCIDENTS if i.get("severity_label") == "high")
    active = sum(1 for i in _IN_MEMORY_INCIDENTS if i.get("human_decision", "pending") == "pending")
    mitigated = sum(1 for i in _IN_MEMORY_INCIDENTS if i.get("human_decision") == "approved")
    total_conf = sum(i.get("confidence_score", 50) for i in _IN_MEMORY_INCIDENTS)
    avg_conf = (total_conf / total / 100.0) if total > 0 else 0.0

    return {
        "totalIncidents": total,
        "criticalCount": critical,
        "highCount": high,
        "activeCount": active,
        "mitigatedCount": mitigated,
        "aiAverageConfidence": round(avg_conf, 2)
    }


def db_fetch_benchmarks() -> List[Dict[str, Any]]:
    conn = get_db()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, run_id, scenario_name, expected_verdict, detected,
                               agent_verdict, baseline_verdict, agent_time_ms, baseline_time_ms,
                               agent_tokens, baseline_tokens, evidence_valid_ratio, evidence_completeness,
                               created_at
                        FROM benchmark_runs
                        ORDER BY created_at DESC
                        LIMIT 50;
                        """
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        if isinstance(row.get("id"), uuid.UUID):
                            row["id"] = str(row["id"])
                    return rows
        except Exception as e:
            logger.error(f"Error fetching benchmark runs: {e}")

    return _IN_MEMORY_BENCHMARKS


def db_search_rag_knowledge(query_vector: List[float], top_k: int = 4) -> List[Dict[str, Any]]:
    conn = get_db()
    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, source, content, metadata,
                               (1 - (embedding <=> %s::vector)) AS similarity
                        FROM security_knowledge
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s;
                        """,
                        (query_vector, query_vector, top_k)
                    )
                    rows = cur.fetchall()
                    return rows
        except Exception as e:
            logger.error(f"Error performing pgvector RAG search: {e}")
    return []
