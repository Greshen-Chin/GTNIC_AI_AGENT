"""Forward Nginx JSON access logs to soar-api without mounting the Docker socket."""

import json
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
            if cursor["inode"] != inode:
                cursor = {"inode": inode, "offset": 0}

            with LOG_PATH.open("r", encoding="utf-8", errors="replace") as log_file:
                log_file.seek(cursor["offset"])
                while line := log_file.readline():
                    next_offset = log_file.tell()
                    try:
                        event = json.loads(line)
                        response = httpx.post(
                            f"{API_URL}/integrations/juice-shop/access-log",
                            json=event,
                            headers=headers,
                            timeout=5.0,
                        )
                        response.raise_for_status()
                    except (json.JSONDecodeError, httpx.HTTPError, ValueError):
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
