"""One background investigator; persisted pending incidents survive API restarts."""

import json
import logging
from threading import Event, Thread

from app.database import db_next_pending_investigation, db_update_incident_analysis
from app.services.agent_service import investigate_alert

logger = logging.getLogger("soar-api.investigation-worker")


def process_next_investigation():
    incident = db_next_pending_investigation()
    if not incident:
        return False
    incident_id = str(incident["id"])
    try:
        alert = incident["raw_alert"]
        if isinstance(alert, str):
            alert = json.loads(alert)
        investigate_alert(alert=alert, dedup_key=incident.get("dedup_key"),
                          incident_id=incident_id)
    except Exception:
        logger.exception("Investigation failed for %s; keeping signature evidence", incident_id)
        # A failed AI call must not turn into another endless investigation loop.
        db_update_incident_analysis(incident_id, {"llm_model": "signature-fallback"})
    return True


def start_investigation_worker():
    stop = Event()

    def run():
        while not stop.is_set():
            try:
                if process_next_investigation():
                    continue
            except Exception:
                logger.exception("Investigation queue unavailable")
            stop.wait(0.5)

    thread = Thread(target=run, name="juice-investigator", daemon=True)
    thread.start()
    return stop, thread
