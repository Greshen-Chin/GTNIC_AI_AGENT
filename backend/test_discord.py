"""
GTNIC SOAR - Discord Alert Integration Test (test_discord.py)
Validates Discord bot authentication, channel accessibility, and rich embed delivery.
"""

import sys
import os
import json
from pathlib import Path
import importlib.util

backend_dir = Path(__file__).resolve().parent

def load_env_vars():
    env_path = backend_dir / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

env = load_env_vars()
bot_token = env.get("DISCORD_BOT_TOKEN") or os.getenv("DISCORD_BOT_TOKEN", "")
channel_id = env.get("DISCORD_CHANNEL_ID") or os.getenv("DISCORD_CHANNEL_ID", "")
discord_enabled = (env.get("DISCORD_ENABLED", "true").lower() == "true")

class MockSettings:
    DISCORD_ENABLED = discord_enabled
    DISCORD_BOT_TOKEN = bot_token
    DISCORD_CHANNEL_ID = channel_id

# Load discord_service directly without triggering app.services.__init__
service_path = backend_dir / "app" / "services" / "discord_service.py"
spec = importlib.util.spec_from_file_location("discord_service_mod", str(service_path))
discord_service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_service)
discord_service.settings = MockSettings

send_discord_alert = discord_service.send_discord_alert

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    print(f"\n{BOLD}{CYAN}=== GTNIC SOAR: Discord Alert Bot Test ==={RESET}\n")
    masked_token = (MockSettings.DISCORD_BOT_TOKEN[:15] + "..." + MockSettings.DISCORD_BOT_TOKEN[-6:]) if MockSettings.DISCORD_BOT_TOKEN else "NONE"
    print(f"Configured Token: {masked_token}")
    print(f"Configured Channel ID: {MockSettings.DISCORD_CHANNEL_ID}")
    print(f"Discord Notifications Enabled: {MockSettings.DISCORD_ENABLED}\n")

    if not MockSettings.DISCORD_BOT_TOKEN or not MockSettings.DISCORD_CHANNEL_ID:
        print(f"{RED}[FAIL] Missing DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID in .env{RESET}")
        sys.exit(1)

    # Construct realistic test incident (Juice Shop SQLi simulation)
    test_incident = {
        "title": "Juice Shop SQL injection attempt (Request Body)",
        "source_ip": "104.28.192.42",
        "wazuh_rule_id": "juice-proxy-1001",
        "status": "likely",
        "severity_label": "high",
        "severity_score": 75,
        "confidence_score": 85,
        "flags": ["sql_injection", "juice-shop", "proxy-detected"],
        "llm_model": "GTNIC-Autonomous-Agent-v2",
        "attack_story": [
            {
                "step": 1,
                "title": "SQL Injection in Login Form",
                "event": "Reverse proxy recorded an authentication bypass attempt in the request body targeting /rest/user/login."
            }
        ],
        "raw_alert": {
            "agent": {"name": "juice-shop-proxy"},
            "data": {
                "srcip": "104.28.192.42",
                "threat_location": "Request Body",
                "threat_type": "sql_injection",
                "method": "POST",
                "url": "/rest/user/login",
                "payload": "{\"email\": \"' or 1=1--\", \"password\": \"test\"}",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        }
    }

    print("Dispatching simulated high-severity security alert to Discord...")
    success = send_discord_alert(test_incident, incident_id="inc-test-verified-001")

    if success:
        print(f"\n{GREEN}{BOLD}[PASS] Discord Alert successfully delivered to channel #{MockSettings.DISCORD_CHANNEL_ID}!{RESET}")
        print("Please check your Discord channel to view the formatted embed.\n")
    else:
        print(f"\n{RED}{BOLD}[FAIL] Could not deliver alert to Discord. Check logs above.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
