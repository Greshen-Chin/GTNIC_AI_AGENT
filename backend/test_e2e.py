"""
GTNIC SOAR-API End-to-End Automated Test Suite (test_e2e.py)
Validates all backend components:
  1. Health & Configuration Check
  2. Wazuh Tool 1: search_alerts_by_ip
  3. Wazuh Tool 2: get_login_history
  4. Wazuh Tool 4: inspect_web_attack (100% SQLi & XSS Deep Inspection)
  5. RAG Tool 3: mitre_owasp_rag (Vertex AI Embeddings + pgvector)
  6. Autonomous AI Agent Triage: SSH Brute Force
  7. Autonomous AI Agent Triage: SQL Injection (SQLi)
  8. Autonomous AI Agent Triage: Cross-Site Scripting (XSS)
  9. Dashboard Incidents List
  10. Incident Detail Retrieval
  11. Human-in-the-loop Decision (Approve Mitigation)
  12. SOC Dashboard Statistics
  13. Benchmark Comparison (Agent vs Baseline)

Usage:
  cd e:\\Projek\\GTNIC\\GTNIC_AI_AGENT\\backend
  python test_e2e.py
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Attempt to load .env variables
def load_env_file(env_path: Path) -> Dict[str, str]:
    env_vars = {}
    if not env_path.exists():
        return env_vars
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

env_path = backend_dir / ".env"
env_config = load_env_file(env_path)

INTERNAL_TOKEN = env_config.get("INTERNAL_TOKEN") or os.getenv("INTERNAL_TOKEN", "d51ebc9c939396154831ec6e856b6a03")
DASHBOARD_API_KEY = env_config.get("DASHBOARD_API_KEY") or os.getenv("DASHBOARD_API_KEY", "e8c491f27a6b40d39e8a15b2c7f4019a")
BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:8000")

# Import httpx (standard in backend requirements)
try:
    import httpx
except ImportError:
    print("[ERROR] httpx is not installed. Please run: pip install httpx")
    sys.exit(1)

# ANSI Colors for terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

class TestReport:
    def __init__(self):
        self.results = []
        self.start_time = time.time()

    def record(self, step_no: int, name: str, endpoint: str, passed: bool, duration_ms: int, note: str = ""):
        self.results.append({
            "step": step_no,
            "name": name,
            "endpoint": endpoint,
            "passed": passed,
            "duration_ms": duration_ms,
            "note": note
        })
        status_tag = f"{GREEN}[PASS]{RESET}" if passed else f"{RED}[FAIL]{RESET}"
        print(f" {status_tag} Step {step_no:02d}: {BOLD}{name:<38}{RESET} ({duration_ms:>4} ms) -> {note}")

    def summary(self):
        total_time = round(time.time() - self.start_time, 2)
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed

        print("\n" + "=" * 80)
        print(f"{BOLD}                  GTNIC SOAR-API E2E TEST SUMMARY{RESET}")
        print("=" * 80)
        print(f" Total Tests Run : {total}")
        print(f" Passed          : {GREEN}{passed}{RESET}")
        print(f" Failed          : {RED if failed else GREEN}{failed}{RESET}")
        print(f" Total Duration  : {total_time}s")
        print("-" * 80)
        print(f"{'#':<3} {'Test Name':<32} {'Endpoint':<26} {'Status':<8} {'Time'}")
        print("-" * 80)
        for r in self.results:
            st = f"{GREEN}PASS{RESET}" if r["passed"] else f"{RED}FAIL{RESET}"
            print(f"{r['step']:<3} {r['name']:<32} {r['endpoint']:<26} {st:<16} {r['duration_ms']}ms")
        print("=" * 80)

        if failed == 0:
            print(f"\n{GREEN}{BOLD}>>> ALL END-TO-END TESTS COMPLETED SUCCESSFULLY! <<<{RESET}\n")
        else:
            print(f"\n{RED}{BOLD}>>> SOME TESTS FAILED. Please review the logs above. <<<{RESET}\n")

        return failed == 0


def run_e2e_tests():
    report = TestReport()
    print("\n" + "=" * 80)
    print(f"{BOLD}   GTNIC CYBERSECURITY SOAR PLATFORM - END-TO-END AUTOMATED VERIFICATION{RESET}")
    print("=" * 80)
    print(f" Target Server : {CYAN}{BASE_URL}{RESET}")
    print(f" Loaded .env   : {Path(env_path).name} (Internal Token & Dashboard Key loaded)")
    print("=" * 80 + "\n")

    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # ---------------------------------------------------------
    # TEST 1: Health Check & Model Verification
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        res = client.get("/health")
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            data = res.json()
            model = data.get("model", "unknown")
            embed = data.get("embed_model", "unknown")
            report.record(1, "API Health & Model Check", "GET /health", True, dt, f"Model: {model}, Embed: {embed}")
        else:
            report.record(1, "API Health & Model Check", "GET /health", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(1, "API Health & Model Check", "GET /health", False, dt, f"Connection Failed: {e}")
        print(f"\n{RED}[FATAL] Could not connect to {BASE_URL}. Ensure uvicorn server is running!{RESET}\n")
        report.summary()
        return

    # Internal auth headers
    internal_headers = {
        "Authorization": f"Bearer {INTERNAL_TOKEN}",
        "Content-Type": "application/json"
    }

    # Dashboard auth headers
    dashboard_headers = {
        "X-API-Key": DASHBOARD_API_KEY,
        "Content-Type": "application/json"
    }

    # ---------------------------------------------------------
    # TEST 2: Tool 1 - Search Alerts by IP (Wazuh Indexer)
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        payload = {"srcip": "203.0.113.10", "time_window": "now-24h", "max_alerts": 5}
        res = client.post("/internal/tools/search_alerts_by_ip", headers=internal_headers, json=payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            data = res.json()
            facts = data.get("facts", [])
            hits = data.get("total_hits", 0)
            report.record(2, "Tool 1: Wazuh Alert Search", "POST /internal/tools/...", True, dt, f"Facts: {facts}, Total Hits: {hits}")
        else:
            report.record(2, "Tool 1: Wazuh Alert Search", "POST /internal/tools/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(2, "Tool 1: Wazuh Alert Search", "POST /internal/tools/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 3: Tool 2 - Get Login History (Wazuh Indexer)
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        payload = {"srcip": "203.0.113.20"}
        res = client.post("/internal/tools/get_login_history", headers=internal_headers, json=payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            data = res.json()
            facts = data.get("facts", [])
            failed = data.get("failed_count", 0)
            success = data.get("success_count", 0)
            report.record(3, "Tool 2: Wazuh Login History", "POST /internal/tools/...", True, dt, f"Failed: {failed}, Success: {success}, Facts: {facts}")
        else:
            report.record(3, "Tool 2: Wazuh Login History", "POST /internal/tools/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(3, "Tool 2: Wazuh Login History", "POST /internal/tools/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 4: Tool 4 - Inspect Web Attack (SQLi & XSS Inspection)
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        payload = {"srcip": "203.0.113.10", "attack_type": "all", "time_window": "now-24h"}
        res = client.post("/internal/tools/inspect_web_attack", headers=internal_headers, json=payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            data = res.json()
            facts = data.get("facts", [])
            sqli_ok = data.get("sqli", {}).get("detected", False)
            status_map = data.get("status_breakdown", {})
            report.record(4, "Tool 4: Inspect Web Attack", "POST /internal/tools/...", True, dt, f"SQLi Detected: {sqli_ok}, HTTP Statuses: {status_map}, Facts: {len(facts)}")
        else:
            report.record(4, "Tool 4: Inspect Web Attack", "POST /internal/tools/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(4, "Tool 4: Inspect Web Attack", "POST /internal/tools/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 5: Tool 3 - MITRE / OWASP RAG (Vertex AI + pgvector)
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        payload = {"query": "SQL Injection UNION SELECT and Cross-Site Scripting XSS", "top_k": 3}
        res = client.post("/internal/tools/mitre_owasp_rag", headers=internal_headers, json=payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            data = res.json()
            matches = data.get("matches", [])
            facts = data.get("facts", [])
            report.record(5, "Tool 3: MITRE/OWASP RAG", "POST /internal/tools/...", True, dt, f"Found {len(matches)} matches (Facts: {facts})")
        else:
            report.record(5, "Tool 3: MITRE/OWASP RAG", "POST /internal/tools/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(5, "Tool 3: MITRE/OWASP RAG", "POST /internal/tools/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 6: Autonomous AI Agent - SSH Brute Force Triage
    # ---------------------------------------------------------
    created_incident_id = None
    t0 = time.perf_counter()
    try:
        ssh_alert_payload = {
            "alert": {
                "id": "alert-e2e-ssh-001",
                "rule": {
                    "id": "100100",
                    "level": 10,
                    "description": "Multiple SSH failed login attempts detected"
                },
                "data": {
                    "srcip": "203.0.113.88",
                    "dstuser": "root"
                },
                "agent": {"id": "001", "name": "gtnic-bastion"},
                "timestamp": "2026-10-24T21:00:00Z"
            },
            "dedup_key": f"test_e2e_ssh_{int(time.time())}"
        }
        res = client.post("/internal/agent/investigate", headers=internal_headers, json=ssh_alert_payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code in (200, 201):
            data = res.json()
            created_incident_id = data.get("incident_id")
            verdict = data.get("status")
            sev = data.get("severity_score")
            conf = data.get("confidence_score")
            report.record(6, "AI Agent: SSH Brute Force", "POST /internal/agent/...", True, dt, f"Verdict: {verdict}, Sev: {sev}, Conf: {conf}%")
        else:
            report.record(6, "AI Agent: SSH Brute Force", "POST /internal/agent/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(6, "AI Agent: SSH Brute Force", "POST /internal/agent/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 7: Autonomous AI Agent - SQL Injection (SQLi) Triage
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        sqli_alert_payload = {
            "alert": {
                "id": "alert-e2e-sqli-002",
                "rule": {
                    "id": "100101",
                    "level": 9,
                    "description": "SQL Injection attempt detected in query parameters"
                },
                "data": {
                    "srcip": "203.0.113.10",
                    "url": "/api/v1/search?q=1%27+UNION+SELECT+1%2Cusername%2Cpassword+FROM+users--",
                    "status": "500"
                },
                "agent": {"id": "002", "name": "web-prod-api"},
                "timestamp": "2026-10-24T21:05:00Z"
            },
            "dedup_key": f"test_e2e_sqli_{int(time.time())}"
        }
        res = client.post("/internal/agent/investigate", headers=internal_headers, json=sqli_alert_payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code in (200, 201):
            data = res.json()
            verdict = data.get("status")
            sev = data.get("severity_score")
            conf = data.get("confidence_score")
            report.record(7, "AI Agent: SQL Injection", "POST /internal/agent/...", True, dt, f"Verdict: {verdict}, Sev: {sev}, Conf: {conf}%")
        else:
            report.record(7, "AI Agent: SQL Injection", "POST /internal/agent/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(7, "AI Agent: SQL Injection", "POST /internal/agent/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 8: Autonomous AI Agent - Cross-Site Scripting (XSS) Triage
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        xss_alert_payload = {
            "alert": {
                "id": "alert-e2e-xss-003",
                "rule": {
                    "id": "31105",
                    "level": 8,
                    "description": "XSS (Cross Site Scripting) attempt detected in URI"
                },
                "data": {
                    "srcip": "203.0.113.15",
                    "url": "/search?query=%3Cscript%3Edocument.location%3D%27http%3A%2F%2Fattacker.com%27%3C%2Fscript%3E",
                    "status": "200"
                },
                "agent": {"id": "002", "name": "web-prod-api"},
                "timestamp": "2026-10-24T21:10:00Z"
            },
            "dedup_key": f"test_e2e_xss_{int(time.time())}"
        }
        res = client.post("/internal/agent/investigate", headers=internal_headers, json=xss_alert_payload)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code in (200, 201):
            data = res.json()
            verdict = data.get("status")
            sev = data.get("severity_score")
            conf = data.get("confidence_score")
            report.record(8, "AI Agent: Cross-Site Scripting", "POST /internal/agent/...", True, dt, f"Verdict: {verdict}, Sev: {sev}, Conf: {conf}%")
        else:
            report.record(8, "AI Agent: Cross-Site Scripting", "POST /internal/agent/...", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(8, "AI Agent: Cross-Site Scripting", "POST /internal/agent/...", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 9: Dashboard Incidents List
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        res = client.get("/api/incidents", headers=dashboard_headers)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            incidents = res.json()
            if not created_incident_id and len(incidents) > 0:
                created_incident_id = incidents[0].get("id")
            report.record(9, "Dashboard Incident List", "GET /api/incidents", True, dt, f"Retrieved {len(incidents)} incidents from DB")
        else:
            report.record(9, "Dashboard Incident List", "GET /api/incidents", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(9, "Dashboard Incident List", "GET /api/incidents", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 10: Single Incident Detail
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    if created_incident_id:
        try:
            res = client.get(f"/api/incidents/{created_incident_id}", headers=dashboard_headers)
            dt = int((time.perf_counter() - t0) * 1000)
            if res.status_code == 200:
                inc = res.json()
                story_steps = len(inc.get("attack_story", []))
                tools_used = len(inc.get("tool_trace", []))
                report.record(10, "Incident Detail View", f"GET /api/incidents/{{id}}", True, dt, f"Title: {inc.get('title')[:30]}..., Story: {story_steps} steps, Traces: {tools_used}")
            else:
                report.record(10, "Incident Detail View", f"GET /api/incidents/{{id}}", False, dt, f"HTTP {res.status_code}: {res.text}")
        except Exception as e:
            dt = int((time.perf_counter() - t0) * 1000)
            report.record(10, "Incident Detail View", f"GET /api/incidents/{{id}}", False, dt, str(e))
    else:
        report.record(10, "Incident Detail View", "GET /api/incidents/{id}", False, 0, "Skipped (no incident ID available)")

    # ---------------------------------------------------------
    # TEST 11: Human-in-the-Loop Decision Recording
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    if created_incident_id:
        try:
            decision_payload = {
                "decision": "approved",
                "decided_by": "analyst-marcelinus"
            }
            res = client.post(f"/api/incidents/{created_incident_id}/decision", headers=dashboard_headers, json=decision_payload)
            dt = int((time.perf_counter() - t0) * 1000)
            if res.status_code == 200:
                data = res.json()
                report.record(11, "Human Decision Approval", f"POST /api/incidents/{{id}}/...", True, dt, f"Decision: {data.get('human_decision')}, By: {data.get('decided_by')}")
            else:
                report.record(11, "Human Decision Approval", f"POST /api/incidents/{{id}}/...", False, dt, f"HTTP {res.status_code}: {res.text}")
        except Exception as e:
            dt = int((time.perf_counter() - t0) * 1000)
            report.record(11, "Human Decision Approval", f"POST /api/incidents/{{id}}/...", False, dt, str(e))
    else:
        report.record(11, "Human Decision Approval", "POST /api/incidents/{id}/decision", False, 0, "Skipped (no incident ID available)")

    # ---------------------------------------------------------
    # TEST 12: SOC Dashboard Summary Stats
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        res = client.get("/api/stats", headers=dashboard_headers)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            stats = res.json()
            total_inc = stats.get("totalIncidents", 0)
            crit = stats.get("criticalCount", 0)
            avg_conf = stats.get("aiAverageConfidence", 0.0)
            report.record(12, "Dashboard Stats Metrics", "GET /api/stats", True, dt, f"Total: {total_inc}, Critical: {crit}, Avg Conf: {avg_conf}%")
        else:
            report.record(12, "Dashboard Stats Metrics", "GET /api/stats", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(12, "Dashboard Stats Metrics", "GET /api/stats", False, dt, str(e))

    # ---------------------------------------------------------
    # TEST 13: AI vs Baseline Benchmark Results
    # ---------------------------------------------------------
    t0 = time.perf_counter()
    try:
        res = client.get("/api/benchmark", headers=dashboard_headers)
        dt = int((time.perf_counter() - t0) * 1000)
        if res.status_code == 200:
            bm = res.json()
            agent_acc = bm.get("agent_accuracy", 0.0)
            base_acc = bm.get("baseline_accuracy", 0.0)
            val_ratio = bm.get("avg_evidence_validity", 0.0)
            report.record(13, "Benchmark Evaluation", "GET /api/benchmark", True, dt, f"Agent Acc: {agent_acc}%, Baseline: {base_acc}%, Validity: {val_ratio}")
        else:
            report.record(13, "Benchmark Evaluation", "GET /api/benchmark", False, dt, f"HTTP {res.status_code}: {res.text}")
    except Exception as e:
        dt = int((time.perf_counter() - t0) * 1000)
        report.record(13, "Benchmark Evaluation", "GET /api/benchmark", False, dt, str(e))

    # Print full summary report
    report.summary()


if __name__ == "__main__":
    run_e2e_tests()
