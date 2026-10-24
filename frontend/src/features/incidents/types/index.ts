export type SeverityLevel = "Critical" | "High" | "Medium" | "Low";

export type AIVerdict = "Malicious" | "Suspicious" | "Benign" | "Under Review";

export type IncidentStatus = "Active" | "Investigating" | "Mitigated" | "False Positive";

export interface Evidence {
  id: string;
  type: "Pro" | "Contra";
  title: string;
  description: string;
  source: string; // e.g. "Cloudflare WAF", "Suricata IDS", "Okta Logs", "CrowdStrike EDR"
  confidence: "High" | "Medium" | "Low";
  timestamp: string;
  rawArtifact?: string;
}

export interface ToolTrace {
  id: string;
  toolName: string;
  executedAt: string;
  durationMs: number;
  status: "success" | "failed" | "running";
  input: Record<string, unknown>;
  output: Record<string, unknown>;
}

export interface AttackStoryStep {
  stepNumber: number;
  timestamp: string;
  title: string;
  description: string;
  phase:
    | "Unknown"
    | "Reconnaissance"
    | "Initial Access"
    | "Execution"
    | "Persistence"
    | "Privilege Escalation"
    | "Defense Evasion"
    | "Credential Access"
    | "Discovery"
    | "Lateral Movement"
    | "Collection"
    | "Command and Control"
    | "Exfiltration"
    | "Impact";
  highlight?: boolean;
}

export interface MitreContext {
  id: string; // e.g., "T1190"
  name: string;
  tactic: string; // e.g., "Initial Access"
  description: string;
  mitigationAdvice: string;
  url?: string;
}

export interface OwaspContext {
  id: string; // e.g., "A03:2021"
  name: string;
  description: string;
  remediation: string;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  timestamp: string;
  sourceIp: string;
  sourceCountry?: string;
  targetIp: string;
  targetAsset: string;
  aiVerdict: AIVerdict;
  aiConfidence: number; // e.g., 0.94 for 94%
  severity: SeverityLevel;
  status: IncidentStatus;
  suggestedMitigation: string;
  mitigationActionTaken?: "Approved" | "Rejected" | null;
  attackStory: AttackStoryStep[];
  evidence: {
    pro: Evidence[];
    contra: Evidence[];
  };
  toolTraces: ToolTrace[];
  mitreContext: MitreContext[];
  owaspContext: OwaspContext[];
}

export interface IncidentSummaryStats {
  totalIncidents: number;
  criticalCount: number;
  highCount: number;
  activeCount: number;
  mitigatedCount: number;
  aiAverageConfidence: number;
}
