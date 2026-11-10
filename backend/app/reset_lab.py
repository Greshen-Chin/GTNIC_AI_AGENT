"""Explicit operator-only lab reset. Run with API and log forwarder stopped."""
import argparse
from datetime import datetime, timezone

import psycopg
from psycopg import sql

from app.database import get_connection_string
from app.services.juice_log_forwarder import LOG_PATH, save_cursor


def reset_lab(confirm):
    if confirm != "RESET_LAB":
        raise ValueError("Explicit --confirm RESET_LAB is required")
    if not LOG_PATH.exists():
        raise RuntimeError("Juice Shop log/state volumes must be mounted before reset")
    archive = "incidents_archive_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    # No fallback: do not acknowledge a reset if the persistent DB is unavailable.
    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE TABLE {} AS TABLE incidents").format(sql.Identifier(archive)))
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(archive)))
            archived = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM incidents")
            if cur.fetchone()[0] != archived:
                raise RuntimeError("Archive verification failed")
            cur.execute("TRUNCATE TABLE incidents")
            stat = LOG_PATH.stat()
            save_cursor(stat.st_ino, stat.st_size)
        # The archive and clear commit together. Logs themselves are retained.
    print(f"Archived {archived} incidents to {archive}; lab queue cleared; cursor advanced to current log end.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", required=True)
    reset_lab(parser.parse_args().confirm)
