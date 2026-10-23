#!/usr/bin/env python3
"""
Tahap 7 - Ingestion RAG (MITRE ATT&CK & OWASP Top 10)
Uses Google Cloud Vertex AI (text-embedding-004, 768 dimensions) to embed cybersecurity knowledge
into PostgreSQL pgvector table 'security_knowledge'.
"""

import sys
import os
import json
import logging
import httpx
import psycopg
from pgvector.psycopg import register_vector

# Ensure current dir is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.services.vertex_service import generate_embedding

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ingest-rag")

MITRE_CTI_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

OWASP_TOP_10 = [
    {
        "id": "A01:2021",
        "name": "Broken Access Control",
        "content": (
            "OWASP A01:2021 - Broken Access Control. "
            "Access control enforces policy such that users cannot act outside of their intended permissions. "
            "Failures typically lead to unauthorized information disclosure, modification, or destruction of data. "
            "Symptoms include path traversal (/ftp/../), bypassing access control checks by modifying URLs or internal state, "
            "elevation of privilege, and insecure direct object references (IDOR). "
            "Mitigation: Deny by default, enforce record-level ownership, disable web server directory listing."
        ),
        "metadata": {"category": "A01:2021", "name": "Broken Access Control", "owasp_id": "A01:2021"}
    },
    {
        "id": "A02:2021",
        "name": "Cryptographic Failures",
        "content": (
            "OWASP A02:2021 - Cryptographic Failures. "
            "Focuses on failures related to cryptography which often leads to sensitive data exposure or system compromise. "
            "Symptoms include transmitting sensitive data in cleartext (HTTP, FTP, Telnet), using old or weak cryptographic algorithms (MD5, SHA1, DES), "
            "or improper key management. "
            "Mitigation: Encrypt all data in transit with secure protocols like TLS 1.3, use strong adaptive hashing functions (bcrypt, Argon2) for passwords."
        ),
        "metadata": {"category": "A02:2021", "name": "Cryptographic Failures", "owasp_id": "A02:2021"}
    },
    {
        "id": "A03:2021",
        "name": "Injection",
        "content": (
            "OWASP A03:2021 - Injection (SQL Injection, Command Injection, Cross-Site Scripting). "
            "An application is vulnerable to injection when user-supplied data is not validated, filtered, or sanitized by the application before inclusion in commands or queries. "
            "Symptoms include UNION SELECT queries, ' OR 1=1-- statements, unexpected SQL syntax error messages, and arbitrary shell command execution. "
            "Mitigation: Use safe API parameterized queries (Prepared Statements), ORMs, and strict context-aware input validation."
        ),
        "metadata": {"category": "A03:2021", "name": "Injection", "owasp_id": "A03:2021"}
    },
    {
        "id": "A07:2021",
        "name": "Identification and Authentication Failures",
        "content": (
            "OWASP A07:2021 - Identification and Authentication Failures. "
            "Confirmation of the user's identity, authentication, and session management is critical to protect against authentication-related attacks. "
            "Symptoms include permitting brute force attacks without lockout, credential stuffing from automated tools, weak password recovery, and missing multi-factor authentication. "
            "Mitigation: Implement multi-factor authentication (MFA), rate limiting, and automated account lockout after repeated failures."
        ),
        "metadata": {"category": "A07:2021", "name": "Identification and Authentication Failures", "owasp_id": "A07:2021"}
    }
]


def fetch_curated_mitre_techniques():
    """
    Returns high-impact MITRE ATT&CK techniques relevant to web security and SOAR triage.
    """
    logger.info("Loading curated MITRE ATT&CK Enterprise techniques...")
    return [
        {
            "external_id": "T1190",
            "name": "Exploit Public-Facing Application",
            "tactic": "Initial Access",
            "content": (
                "MITRE ATT&CK T1190: Exploit Public-Facing Application. "
                "Adversaries may attempt to exploit weaknesses in Internet-facing programs, services, or servers. "
                "Common web application exploits include SQL injection (SQLi), remote code execution, and parameter tampering. "
                "Mitigation: Application firewalls (WAF), secure input sanitization, network segmentation, and regular patching."
            ),
            "metadata": {"external_id": "T1190", "name": "Exploit Public-Facing Application", "tactic": "Initial Access"}
        },
        {
            "external_id": "T1110",
            "name": "Brute Force",
            "tactic": "Credential Access",
            "content": (
                "MITRE ATT&CK T1110: Brute Force. "
                "Adversaries use repetitive attempts to guess user passwords, PINs, or credentials. "
                "Sub-techniques include Password Spraying (T1110.003), Credential Stuffing (T1110.004), and Dictionary Attacks. "
                "Symptoms: Sudden spikes in failed HTTP POST login requests followed by a successful login. "
                "Mitigation: Rate limiting, IP throttling, CAPTCHA, and account lockout."
            ),
            "metadata": {"external_id": "T1110", "name": "Brute Force", "tactic": "Credential Access"}
        },
        {
            "external_id": "T1059",
            "name": "Command and Scripting Interpreter",
            "tactic": "Execution",
            "content": (
                "MITRE ATT&CK T1059: Command and Scripting Interpreter. "
                "Adversaries may abuse interpreters like Bash, PowerShell, or Python to execute malicious code. "
                "Mitigation: Restrict script execution, enable detailed process execution logs."
            ),
            "metadata": {"external_id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution"}
        },
        {
            "external_id": "T1595",
            "name": "Active Scanning",
            "tactic": "Reconnaissance",
            "content": (
                "MITRE ATT&CK T1595: Active Scanning. "
                "Adversaries execute scans to gather information on targets (ports, vulnerabilities, services) using automated tools (e.g. Nikto, sqlmap, gobuster). "
                "Symptoms: Rapid burst of HTTP 404 responses and scanners' User-Agent headers. "
                "Mitigation: Block known vulnerability scanner signatures at WAF."
            ),
            "metadata": {"external_id": "T1595", "name": "Active Scanning", "tactic": "Reconnaissance"}
        }
    ]


def run_ingestion():
    logger.info("Connecting to PostgreSQL pgvector...")
    conn_str = (
        f"host={settings.POSTGRES_HOST} port={settings.POSTGRES_PORT} "
        f"dbname={settings.POSTGRES_DB} user={settings.POSTGRES_USER} "
        f"password={settings.POSTGRES_PASSWORD}"
    )

    try:
        with psycopg.connect(conn_str, autocommit=True) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                # Ensure table exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS security_knowledge (
                        id BIGSERIAL PRIMARY KEY,
                        source TEXT,
                        content TEXT,
                        metadata JSONB,
                        embedding VECTOR(768)
                    );
                    CREATE INDEX IF NOT EXISTS security_knowledge_embedding_hnsw_idx 
                    ON security_knowledge USING hnsw (embedding vector_cosine_ops);
                """)

                # Ingest OWASP
                logger.info("Embedding and inserting OWASP Top 10...")
                for item in OWASP_TOP_10:
                    vec = generate_embedding(item["content"])
                    cur.execute(
                        """
                        INSERT INTO security_knowledge (source, content, metadata, embedding)
                        VALUES (%s, %s, %s, %s);
                        """,
                        ("OWASP Top 10 2021", item["content"], json.dumps(item["metadata"]), vec)
                    )

                # Ingest MITRE
                mitre_items = fetch_curated_mitre_techniques()
                logger.info("Embedding and inserting MITRE ATT&CK techniques...")
                for item in mitre_items:
                    vec = generate_embedding(item["content"])
                    cur.execute(
                        """
                        INSERT INTO security_knowledge (source, content, metadata, embedding)
                        VALUES (%s, %s, %s, %s);
                        """,
                        ("MITRE ATT&CK Enterprise", item["content"], json.dumps(item["metadata"]), vec)
                    )

                # Quality check query (Step 4 of Tahap 7 in PDF)
                test_query = "sql injection login"
                logger.info(f"Running quality check query: '{test_query}'...")
                test_vec = generate_embedding(test_query)
                cur.execute(
                    """
                    SELECT id, source, metadata->>'name' as name, 
                           (1 - (embedding <=> %s::vector)) as similarity
                    FROM security_knowledge
                    ORDER BY embedding <=> %s::vector
                    LIMIT 4;
                    """,
                    (test_vec, test_vec)
                )
                results = cur.fetchall()
                logger.info("--- Quality Check Top 4 Results ---")
                for r in results:
                    logger.info(f"ID={r[0]} | Source={r[1]} | Name={r[2]} | Sim={r[3]:.4f}")

        logger.info("RAG Ingestion successfully completed!")
    except Exception as e:
        logger.error(f"Ingestion encountered error: {e}")


if __name__ == "__main__":
    run_ingestion()
