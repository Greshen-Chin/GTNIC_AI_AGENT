-- Enable vector extension for RAG embeddings
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Incidents Table (Core SOC Auditable Tickets)
CREATE TABLE IF NOT EXISTS incidents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    dedup_key TEXT,
    suppressed_count INT DEFAULT 0,
    wazuh_rule_id TEXT,
    title TEXT NOT NULL,
    source_ip TEXT,
    raw_alert JSONB,
    status TEXT CHECK (status IN ('confirmed', 'likely', 'uncertain', 'false_positive')),
    flags JSONB DEFAULT '[]'::jsonb,
    severity_score INT,
    severity_label TEXT CHECK (severity_label IN ('low', 'medium', 'high', 'critical')),
    confidence_score INT,
    attack_story JSONB,
    pro_evidence JSONB,
    contra_evidence JSONB,
    invalid_evidence JSONB,
    tool_trace JSONB,
    mitre_context JSONB,
    llm_model TEXT,
    prompt_version TEXT,
    tokens_in INT,
    tokens_out INT,
    latency_ms INT,
    human_decision TEXT DEFAULT 'pending' CHECK (human_decision IN ('pending', 'approved', 'rejected')),
    decided_by TEXT,
    decided_at TIMESTAMPTZ,
    summary TEXT,
    recommended_action TEXT
);

CREATE INDEX IF NOT EXISTS idx_incidents_created_at ON incidents (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_incidents_source_ip ON incidents (source_ip);
CREATE INDEX IF NOT EXISTS idx_incidents_dedup_key ON incidents (dedup_key);
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents (status);

-- 2. Alert Deduplication Table (Atomic 60-second window)
CREATE TABLE IF NOT EXISTS alert_dedup (
    key TEXT PRIMARY KEY,
    window_start TIMESTAMPTZ NOT NULL,
    hits INT NOT NULL DEFAULT 1
);

-- 3. Security Knowledge Base (MITRE ATT&CK + OWASP Top 10 with HNSW Index)
CREATE TABLE IF NOT EXISTS security_knowledge (
    id BIGSERIAL PRIMARY KEY,
    source TEXT,
    content TEXT,
    metadata JSONB,
    embedding vector(768)
);

CREATE INDEX IF NOT EXISTS idx_security_knowledge_hnsw 
ON security_knowledge USING hnsw (embedding vector_cosine_ops);

-- 4. Benchmark Runs Table (Evaluation against baseline)
CREATE TABLE IF NOT EXISTS benchmark_runs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    run_id TEXT,
    scenario_name TEXT,
    expected_verdict TEXT,
    detected BOOLEAN,
    agent_verdict TEXT,
    baseline_verdict TEXT,
    agent_time_ms INT,
    baseline_time_ms INT,
    agent_tokens INT,
    baseline_tokens INT,
    evidence_valid_ratio NUMERIC,
    evidence_completeness NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
