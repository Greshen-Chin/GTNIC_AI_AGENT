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
                try:
                    cur.execute("ALTER TABLE incidents ADD COLUMN IF NOT EXISTS summary TEXT;")
                    cur.execute("ALTER TABLE incidents ADD COLUMN IF NOT EXISTS recommended_action TEXT;")
                except Exception as migration_err:
                    logger.debug(f"Could not auto-migrate incidents columns: {migration_err}")
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
                    try:
                        cur.execute(
                            """
                            SELECT id, created_at, dedup_key, suppressed_count, wazuh_rule_id,
                                   title, source_ip, raw_alert, status, flags, severity_score,
                                   severity_label, confidence_score, attack_story, pro_evidence,
                                   contra_evidence, invalid_evidence, tool_trace, mitre_context,
                                   llm_model, prompt_version, tokens_in, tokens_out, latency_ms,
                                   human_decision, decided_by, decided_at, summary, recommended_action
                            FROM incidents
                            ORDER BY created_at DESC
                            LIMIT 100;
                            """
                        )
                    except Exception:
                        conn.rollback()
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
                        raw_alert = row.get("raw_alert")
                        if isinstance(raw_alert, str):
                            try:
                                raw_alert = json.loads(raw_alert)
                                row["raw_alert"] = raw_alert
                            except Exception:
                                pass
                        if isinstance(raw_alert, dict):
                            if not row.get("summary"):
                                row["summary"] = raw_alert.get("summary")
                            if not row.get("recommended_action"):
                                row["recommended_action"] = raw_alert.get("recommended_action") or (raw_alert.get("data") or {}).get("recommended_action")
                    return rows
        except Exception as e:
            logger.error(f"Error querying incidents from DB: {e}")

    # Fallback in-memory
    for inc in _IN_MEMORY_INCIDENTS:
        raw_alert = inc.get("raw_alert")
        if isinstance(raw_alert, dict):
            if not inc.get("summary"):
                inc["summary"] = raw_alert.get("summary")
            if not inc.get("recommended_action"):
                inc["recommended_action"] = raw_alert.get("recommended_action") or (raw_alert.get("data") or {}).get("recommended_action")
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
                    try:
                        cur.execute(
                            """
                            SELECT id, created_at, dedup_key, suppressed_count, wazuh_rule_id,
                                   title, source_ip, raw_alert, status, flags, severity_score,
                                   severity_label, confidence_score, attack_story, pro_evidence,
                                   contra_evidence, invalid_evidence, tool_trace, mitre_context,
                                   llm_model, prompt_version, tokens_in, tokens_out, latency_ms,
                                   human_decision, decided_by, decided_at, summary, recommended_action
                            FROM incidents
                            WHERE id = %s;
                            """,
                            (incident_id,)
                        )
                    except Exception:
                        conn.rollback()
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
                    if row:
                        if isinstance(row.get("id"), uuid.UUID):
                            row["id"] = str(row["id"])
                        raw_alert = row.get("raw_alert")
                        if isinstance(raw_alert, str):
                            try:
                                raw_alert = json.loads(raw_alert)
                                row["raw_alert"] = raw_alert
                            except Exception:
                                pass
                        if isinstance(raw_alert, dict):
                            if not row.get("summary"):
                                row["summary"] = raw_alert.get("summary")
                            if not row.get("recommended_action"):
                                row["recommended_action"] = raw_alert.get("recommended_action") or (raw_alert.get("data") or {}).get("recommended_action")
                    return row
        except Exception as e:
            logger.error(f"Error fetching incident {incident_id}: {e}")

    for inc in _IN_MEMORY_INCIDENTS:
        if str(inc.get("id")) == str(incident_id):
            raw_alert = inc.get("raw_alert")
            if isinstance(raw_alert, dict):
                if not inc.get("summary"):
                    inc["summary"] = raw_alert.get("summary")
                if not inc.get("recommended_action"):
                    inc["recommended_action"] = raw_alert.get("recommended_action") or (raw_alert.get("data") or {}).get("recommended_action")
            return inc
    return None


def db_find_incident_by_dedup_key(dedup_key: str) -> Optional[str]:
    """Find a previously processed event, including after an API restart."""
    conn = get_db()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM incidents WHERE dedup_key = %s LIMIT 1;",
                    (dedup_key,),
                )
                row = cur.fetchone()
                return str(row["id"]) if row else None
    return next(
        (str(inc["id"]) for inc in _IN_MEMORY_INCIDENTS
         if inc.get("dedup_key") == dedup_key),
        None,
    )


def db_next_pending_investigation() -> Optional[Dict[str, Any]]:
    """The incident table doubles as a durable, oldest-first work queue."""
    conn = get_db()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, raw_alert, dedup_key FROM incidents "
                    "WHERE llm_model = 'investigation-pending' ORDER BY created_at LIMIT 1;"
                )
                return cur.fetchone()
    return next((inc for inc in reversed(_IN_MEMORY_INCIDENTS)
                 if inc.get("llm_model") == "investigation-pending"), None)


def db_update_incident_analysis(incident_id: str, analysis: Dict[str, Any]) -> None:
    """Enrich the same incident without overwriting analyst decisions or its time."""
    json_fields = {"raw_alert", "flags", "attack_story", "pro_evidence", "contra_evidence",
                   "invalid_evidence", "tool_trace", "mitre_context"}
    allowed = json_fields | {"title", "status", "severity_score", "severity_label",
                             "confidence_score", "llm_model", "prompt_version",
                             "tokens_in", "tokens_out", "latency_ms", "summary", "recommended_action"}
    updates = {key: value for key, value in analysis.items() if key in allowed}
    if not updates:
        return
    conn = get_db()
    if conn:
        with conn:
            with conn.cursor() as cur:
                assignments = ", ".join(
                    f"{key} = %s::jsonb" if key in json_fields else f"{key} = %s"
                    for key in updates
                )
                values = [json.dumps(value) if key in json_fields else value
                          for key, value in updates.items()]
                cur.execute(f"UPDATE incidents SET {assignments} WHERE id = %s;",
                            (*values, incident_id))
                if cur.rowcount != 1:
                    raise LookupError(f"Incident {incident_id} no longer exists")
        return
    for inc in _IN_MEMORY_INCIDENTS:
        if str(inc["id"]) == str(incident_id):
            inc.update(updates)
            return
    raise LookupError(f"Incident {incident_id} no longer exists")


def db_insert_incident(inc_data: Dict[str, Any]) -> str:
    inc_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    conn = get_db()

    raw_alert = inc_data.get("raw_alert", {})
    if isinstance(raw_alert, str):
        try:
            raw_alert = json.loads(raw_alert)
        except Exception:
            raw_alert = {}
    if isinstance(raw_alert, dict):
        if inc_data.get("summary") and "summary" not in raw_alert:
            raw_alert["summary"] = inc_data["summary"]
        if inc_data.get("recommended_action") and "recommended_action" not in raw_alert:
            raw_alert["recommended_action"] = inc_data["recommended_action"]

    summary_val = inc_data.get("summary") or (raw_alert.get("summary") if isinstance(raw_alert, dict) else None)
    rec_val = inc_data.get("recommended_action") or (raw_alert.get("recommended_action") if isinstance(raw_alert, dict) else None)

    if conn:
        try:
            with conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute(
                            """
                            INSERT INTO incidents (
                                id, created_at, dedup_key, suppressed_count, wazuh_rule_id,
                                title, source_ip, raw_alert, status, flags, severity_score,
                                severity_label, confidence_score, attack_story, pro_evidence,
                                contra_evidence, invalid_evidence, tool_trace, mitre_context,
                                llm_model, prompt_version, tokens_in, tokens_out, latency_ms,
                                human_decision, decided_by, decided_at, summary, recommended_action
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                                json.dumps(raw_alert),
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
                                inc_data.get("decided_at"),
                                summary_val,
                                rec_val
                            )
                        )
                    except Exception:
                        conn.rollback()
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
                                json.dumps(raw_alert),
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
                    # Dispatch real-time alert to Discord
                    try:
                        from app.services.discord_service import dispatch_discord_alert_async
                        dispatch_discord_alert_async({**inc_data, "summary": summary_val, "recommended_action": rec_val}, incident_id=str(created_id))
                    except Exception as discord_err:
                        logger.exception("Could not trigger Discord notification: %s", discord_err)
                    return str(created_id)
        except Exception as e:
            logger.error(f"Error inserting incident into Postgres: {e}")

    # Fallback in-memory
    inc_record = {
        **inc_data,
        "id": inc_id,
        "created_at": now.isoformat(),
        "human_decision": inc_data.get("human_decision", "pending"),
        "summary": summary_val,
        "recommended_action": rec_val,
        "raw_alert": raw_alert
    }
    _IN_MEMORY_INCIDENTS.insert(0, inc_record)
    # Dispatch real-time alert to Discord for in-memory record as well
    try:
        from app.services.discord_service import dispatch_discord_alert_async
        dispatch_discord_alert_async(inc_record, incident_id=inc_id)
    except Exception as discord_err:
        logger.exception("Could not trigger Discord notification: %s", discord_err)
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
