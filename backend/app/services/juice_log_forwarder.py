"""Forward Nginx JSON access logs to soar-api without mounting the Docker socket."""

import json
import hashlib
import logging
import os
import time
from pathlib import Path

import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("juice-log-forwarder")

LOG_PATH = Path(os.getenv("JUICE_ACCESS_LOG", "/var/log/nginx/access.jsonl"))
STATE_PATH = Path("/var/lib/juice-forwarder/cursor.json")
API_URL = os.getenv("SOAR_API_URL", "http://soar-api:8000").rstrip("/")
TOKEN = os.getenv("INTERNAL_TOKEN", "")


def load_cursor():
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"inode": None, "offset": 0}


def save_cursor(inode, offset):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps({"inode": inode, "offset": offset}), encoding="utf-8")
    temporary.replace(STATE_PATH)


def run():
    if not TOKEN:
        raise RuntimeError("INTERNAL_TOKEN must be set for authenticated log forwarding")

    cursor = load_cursor()
    headers = {"X-Internal-Token": TOKEN}
    logger.info("Watching %s and forwarding detections to %s", LOG_PATH, API_URL)

    while True:
        try:
            if not LOG_PATH.exists():
                time.sleep(1)
                continue

            stat = LOG_PATH.stat()
            inode = getattr(stat, "st_ino", 0)
            if cursor["inode"] != inode or stat.st_size < cursor["offset"]:
                cursor = {"inode": inode, "offset": 0}

            with LOG_PATH.open("r", encoding="utf-8", errors="replace") as log_file:
                log_file.seek(cursor["offset"])
                while line := log_file.readline():
                    # A writer may not have finished the last JSON line yet.
                    if not line.endswith("\n"):
                        break
                    next_offset = log_file.tell()
                    try:
                        event = json.loads(line)
                        if not isinstance(event, dict):
                            raise ValueError("access-log entry must be a JSON object")
                    except (json.JSONDecodeError, ValueError):
                        # One corrupt complete line must not hold up all later
                        # attacks. Incomplete trailing lines are retried above.
                        logger.warning("Skipping invalid access-log line at offset %s", cursor["offset"])
                        cursor["offset"] = next_offset
                        save_cursor(inode, next_offset)
                        continue
                    try:
                        # Keep the same identity when a delivery is retried or the
                        # forwarder restarts before saving its cursor.
                        event["event_id"] = hashlib.sha256(
                            f"{inode}:{cursor['offset']}:{line}".encode("utf-8")
                        ).hexdigest()
                        response = httpx.post(
                            f"{API_URL}/integrations/juice-shop/access-log",
                            json=event,
                            headers=headers,
                            # Ingestion acknowledges persistence, not AI completion.
                            # Retried deliveries retain the same event identity.
                            timeout=httpx.Timeout(5.0),
                        )
                        response.raise_for_status()
                    except httpx.HTTPError:
                        logger.exception("Could not forward access-log event; will retry")
                        break
                    cursor["offset"] = next_offset
                    save_cursor(cursor["inode"], cursor["offset"])

            time.sleep(0.5)
        except (OSError, KeyError, TypeError):
            logger.exception("Access-log read failed")
            time.sleep(1)


if __name__ == "__main__":
    run()
