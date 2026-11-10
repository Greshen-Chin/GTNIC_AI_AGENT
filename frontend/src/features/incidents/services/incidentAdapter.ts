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
  llm_model?: string;
}

const verdicts: Record<ApiIncident["status"], AIVerdict> = {
  confirmed: "Malicious", likely: "Suspicious",
  uncertain: "Under Review", false_positive: "Benign",
};
const severities: Record<ApiIncident["severity_label"], SeverityLevel> = {
  critical: "Critical", high: "High", medium: "Medium", low: "Low",
};

function getFallbackMitigation(data: ApiIncident): string {
  const title = (data.title || "").toLowerCase();
  const desc = (data.raw_alert?.rule?.description || "").toLowerCase();
  const rawData = (data.raw_alert?.data || {}) as Record<string, unknown>;
  const threatType = String(rawData.threat_type || "").toLowerCase();
  const srcIp = data.source_ip || "sumber";

  if (title.includes("sql") || desc.includes("sql") || threatType.includes("sql")) {
    return "Terapkan Prepared Statements (parameterized queries), blokir IP di edge gateway/firewall, dan batasi eksposur database backend.";
  }
  if (title.includes("xss") || desc.includes("xss") || threatType.includes("xss") || desc.includes("cross-site")) {
    return "Aktifkan Content Security Policy (CSP), terapkan Context-aware HTML entity encoding, dan pasang flag HttpOnly pada semua session cookie.";
  }
  if (title.includes("command") || desc.includes("command") || threatType.includes("command")) {
    return `Isolasi container/host terdampak, hentikan eksekusi command shell unauthorized, dan blokir IP ${srcIp} di firewall edge.`;
  }
  if (title.includes("traversal") || desc.includes("traversal") || threatType.includes("traversal") || desc.includes("passwd")) {
    return "Normalkan dan sanitasi input path request sebelum akses filesystem, tolak dot-dot-slash traversal, dan batasi direktori chroot.";
  }
  if (title.includes("login") || title.includes("brute") || desc.includes("login") || desc.includes("brute")) {
    return `Terapkan rate-limiting pada endpoint autentikasi, paksa tantangan MFA, dan tinjau potensi kompromi akun dari IP ${srcIp}.`;
  }
  if (title.includes("privilege") || title.includes("admin") || desc.includes("privilege") || desc.includes("sudo")) {
    return `Revokasi kredensial pengguna terkait, audit konfigurasi sudoers/PAM, dan blokir akses dari IP ${srcIp}.`;
  }
  if (data.severity_label === "critical" || data.severity_label === "high") {
    return `Blokir IP ${srcIp} pada edge firewall/WAF, batalkan sesi aktif, dan eskalasikan ke tim Incident Response.`;
  }
  return `Tinjau telemetri aktivitas dari ${srcIp}, batasi akses jaringan, dan pantau indikasi eskalasi anomali berulang.`;
}

export function toIncident(data: ApiIncident): Incident {
  const timestamp = data.raw_alert?.timestamp || data.created_at || "";
  const rawAlertObj = data.raw_alert as Record<string, unknown> | null | undefined;
  const rawData = (data.raw_alert?.data || {}) as Record<string, unknown>;
  const rawAction =
    data.recommended_action ||
    (rawAlertObj?.recommended_action as string | undefined) ||
    (rawData.recommended_action as string | undefined);
  const finalMitigation = (rawAction && rawAction.trim() !== "" && rawAction.toLowerCase() !== "no recommendation provided.")
    ? rawAction
    : getFallbackMitigation(data);

  const mapEvidence = (items: ApiEvidence[], type: Evidence["type"]): Evidence[] =>
    items.map((item, index) => ({
      id: `${data.id}-${type}-${index}`, type,
      title: item.claim, description: item.evidence_ref,
      source: item.source || item.tool,
      confidence: item.confidence || "Observed", timestamp,
      rawArtifact: JSON.stringify(item, null, 2),
    }));

  return {
    id: data.id, title: data.title,
    description: data.summary || (rawAlertObj?.summary as string | undefined) || data.raw_alert?.rule?.description || data.title,
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
    suggestedMitigation: finalMitigation,
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
    llmModel: data.llm_model || "autonomous-agent",
  };
}
