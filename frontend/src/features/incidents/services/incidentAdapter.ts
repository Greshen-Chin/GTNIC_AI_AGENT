import type {
  AIVerdict, AttackStoryStep, Evidence, Incident, MitreContext,
  OwaspContext, SeverityLevel, ToolTrace,
} from "../types";

interface ApiEvidence {
  claim: string;
  tool: string;
  evidence_ref: string;
  source?: string | null;
  confidence?: Evidence["confidence"] | null;
}

export interface ApiIncident {
  id: string;
  title: string;
  created_at?: string | null;
  source_ip?: string | null;
  raw_alert?: {
    data?: Record<string, unknown>;
    agent?: { name?: string };
    timestamp?: string;
    rule?: { description?: string };
  } | null;
  status: "confirmed" | "likely" | "uncertain" | "false_positive";
  severity_label: "critical" | "high" | "medium" | "low";
  confidence_score: number;
  human_decision: "pending" | "approved" | "rejected";
  attack_story?: Array<{
    step?: number;
    stepNumber?: number;
    event?: string;
    description?: string;
    title?: string | null;
    timestamp?: string | null;
    phase?: AttackStoryStep["phase"] | null;
  }>;
  pro_evidence?: ApiEvidence[];
  contra_evidence?: ApiEvidence[];
  tool_trace?: Array<{
    id?: string;
    tool?: string;
    toolName?: string;
    executed_at?: string;
    executedAt?: string;
    duration_ms?: number;
    durationMs?: number;
    status?: ToolTrace["status"];
    input?: Record<string, unknown>;
    output?: Record<string, unknown>;
  }>;
  mitre_context?: Array<Partial<MitreContext> & { id: string; name: string }>;
  owasp_context?: OwaspContext[];
  summary?: string;
  recommended_action?: string;
}

const verdicts: Record<ApiIncident["status"], AIVerdict> = {
  confirmed: "Malicious", likely: "Suspicious",
  uncertain: "Under Review", false_positive: "Benign",
};
const severities: Record<ApiIncident["severity_label"], SeverityLevel> = {
  critical: "Critical", high: "High", medium: "Medium", low: "Low",
};

export function toIncident(data: ApiIncident): Incident {
  const timestamp = data.created_at || data.raw_alert?.timestamp || "";
  const rawData = data.raw_alert?.data;
  const mapEvidence = (items: ApiEvidence[], type: Evidence["type"]): Evidence[] =>
    items.map((item, index) => ({
      id: `${data.id}-${type}-${index}`, type,
      title: item.claim, description: item.evidence_ref,
      source: item.source || item.tool,
      confidence: item.confidence || "Low", timestamp,
      rawArtifact: JSON.stringify(item, null, 2),
    }));

  return {
    id: data.id, title: data.title,
    description: data.summary || data.raw_alert?.rule?.description || data.title,
    timestamp, sourceIp: data.source_ip || "Unknown",
    targetIp: typeof rawData?.dstip === "string" ? rawData.dstip : "Unknown",
    targetAsset: data.raw_alert?.agent?.name || "Unknown",
    severity: severities[data.severity_label], aiVerdict: verdicts[data.status],
    aiConfidence: data.confidence_score / 100,
    status: data.human_decision === "approved" ? "Mitigated"
      : data.human_decision === "rejected" || data.status === "false_positive"
        ? "False Positive" : "Active",
    mitigationActionTaken: data.human_decision === "approved" ? "Approved"
      : data.human_decision === "rejected" ? "Rejected" : null,
    suggestedMitigation: data.recommended_action || "No recommendation provided.",
    attackStory: (data.attack_story || []).map((step, index) => ({
      stepNumber: step.stepNumber ?? step.step ?? index + 1,
      title: step.title || `Investigation step ${index + 1}`,
      description: step.description || step.event || "",
      timestamp: step.timestamp || "", phase: step.phase || "Unknown",
    })),
    evidence: {
      pro: mapEvidence(data.pro_evidence || [], "Pro"),
      contra: mapEvidence(data.contra_evidence || [], "Contra"),
    },
    toolTraces: (data.tool_trace || []).map((trace, index) => ({
      id: trace.id || `${data.id}-trace-${index}`,
      toolName: trace.toolName || trace.tool || "Unknown",
      executedAt: trace.executedAt || trace.executed_at || "",
      durationMs: trace.durationMs ?? trace.duration_ms ?? 0,
      status: trace.status || "failed", input: trace.input || {}, output: trace.output || {},
    })),
    mitreContext: (data.mitre_context || []).map((item) => ({
      ...item, tactic: item.tactic || "Unknown",
      description: item.description || "", mitigationAdvice: item.mitigationAdvice || "",
    })),
    owaspContext: data.owasp_context || [],
  };
}
