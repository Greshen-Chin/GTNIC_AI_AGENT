import logging
from typing import List, Dict, Any
from app.services.vertex_service import generate_embedding
from app.database import db_search_rag_knowledge

logger = logging.getLogger("soar-api.rag")

# Baseline knowledge fallback if security_knowledge table is not yet populated
BASE_KNOWLEDGE = [
    {
        "id": 1,
        "source": "MITRE ATT&CK",
        "content": "T1190 Exploit Public-Facing Application: Adversaries may attempt to exploit weaknesses in Internet-facing programs (e.g. SQL Injection, path traversal).",
        "metadata": {"external_id": "T1190", "name": "Exploit Public-Facing Application", "tactic": "Initial Access"}
    },
    {
        "id": 2,
        "source": "MITRE ATT&CK",
        "content": "T1110 Brute Force: Adversaries use repetitive attempts to guess user passwords or credentials.",
        "metadata": {"external_id": "T1110", "name": "Brute Force", "tactic": "Credential Access"}
    },
    {
        "id": 3,
        "source": "OWASP Top 10 2021",
        "content": "A03:2021-Injection: Applications are vulnerable to injection when user-supplied data is not validated before execution in SQL queries.",
        "metadata": {"category": "A03:2021", "name": "Injection", "owasp_id": "A03:2021"}
    },
    {
        "id": 4,
        "source": "OWASP Top 10 2021",
        "content": "A07:2021-Identification and Authentication Failures: Flaws in authentication mechanisms permitting credential stuffing or brute force.",
        "metadata": {"category": "A07:2021", "name": "Identification and Authentication Failures", "owasp_id": "A07:2021"}
    }
]


def search_mitre_owasp_rag(query: str, top_k: int = 4) -> Dict[str, Any]:
    """
    Tool: mitre_owasp_rag
    1. Embeds query using Vertex AI (text-embedding-004, 768 dims) configured via .env.
    2. Performs pgvector cosine similarity search against security_knowledge table in PostgreSQL.
    3. Produces deterministic facts directly from records: ['doc:<id>', 'mitre:<id>', 'owasp:<id>'].
    """
    query_vector = generate_embedding(query)
    matches = db_search_rag_knowledge(query_vector, top_k=top_k)

    if not matches:
        # Fallback to base knowledge if table is not yet ingested
        q_lower = query.lower()
        scored = []
        for item in BASE_KNOWLEDGE:
            score = 0.5
            content_lower = item["content"].lower()
            if any(k in q_lower for k in ["sql", "inject", "100101"]) and ("injection" in content_lower or "t1190" in content_lower):
                score += 0.4
            if any(k in q_lower for k in ["login", "brute", "password", "100100"]) and ("brute" in content_lower or "t1110" in content_lower):
                score += 0.4
            scored.append({**item, "similarity": score})
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        matches = scored[:top_k]

    facts: List[str] = []
    formatted_matches = []

    for m in matches:
        doc_id = m.get("id")
        meta = m.get("metadata", {}) or {}
        doc_ref = f"doc:{doc_id}"
        facts.append(doc_ref)

        mitre_id = meta.get("external_id") or meta.get("technique")
        if mitre_id:
            facts.append(f"mitre:{mitre_id}")

        owasp_id = meta.get("owasp_id") or meta.get("category")
        if owasp_id:
            facts.append(f"owasp:{owasp_id}")

        formatted_matches.append({
            "id": doc_id,
            "source": m.get("source", "Knowledge Base"),
            "content": m.get("content", ""),
            "metadata": meta,
            "similarity": float(m.get("similarity", 0.0)),
            "doc_ref": doc_ref,
            "mitre_id": mitre_id,
            "owasp_id": owasp_id
        })

    unique_facts = list(dict.fromkeys(facts))

    return {
        "query": query,
        "facts": unique_facts,
        "matches": formatted_matches
    }
