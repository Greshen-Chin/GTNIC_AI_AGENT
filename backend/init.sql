-- Database initialization script for Mini-SOAR GTNIC AI AGENT
-- Automatically executed when Postgres container starts

SELECT 'CREATE DATABASE soar_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'soar_db')\gexec
SELECT 'CREATE DATABASE n8n_db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'n8n_db')\gexec

\connect soar_db;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Incidents table (stores enriched incident reports with verified evidence & tool traces)
CREATE TABLE IF NOT EXISTS incidents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT now(),
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
    decided_at TIMESTAMPTZ
);

-- Atomic deduplication table (60 seconds window per srcip + rule_id)
CREATE TABLE IF NOT EXISTS alert_dedup (
    key TEXT PRIMARY KEY,
    window_start TIMESTAMPTZ NOT NULL,
    hits INT NOT NULL DEFAULT 1
);

-- RAG Knowledge Base table for MITRE ATT&CK & OWASP Top 10
CREATE TABLE IF NOT EXISTS security_knowledge (
    id BIGSERIAL PRIMARY KEY,
    source TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(768)
);

CREATE INDEX IF NOT EXISTS security_knowledge_embedding_hnsw_idx 
ON security_knowledge USING hnsw (embedding vector_cosine_ops);

-- Benchmark evaluations table (Agent vs Baseline)
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
    created_at TIMESTAMPTZ DEFAULT now()
);
