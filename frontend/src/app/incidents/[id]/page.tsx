"use client";

import React from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useIncident } from "@/features/incidents/hooks";
import {
  IncidentHeader,
  AttackTimeline,
  EvidencePanel,
  MitreOwaspPanel,
  ToolTraceTerminal,
} from "@/features/incidents/components";
import { ShieldAlert, ArrowLeft } from "lucide-react";

export default function IncidentWorkspacePage() {
  const params = useParams();
  const id = typeof params?.id === "string" ? params.id : Array.isArray(params?.id) ? params.id[0] : "";

  const { incident, isLoading, error, applyMitigation } = useIncident(id);

  if (isLoading && !incident) {
    return (
      <div className="min-h-[50vh] flex flex-col items-center justify-center gap-2.5 font-mono text-slate-400">
        <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
        <span className="text-xs">Loading incident telemetry workspace for {id}...</span>
      </div>
    );
  }

  if (error || !incident) {
    return (
      <div className="min-h-[45vh] flex flex-col items-center justify-center gap-3 text-center">
        <div className="w-10 h-10 rounded-full bg-rose-950/60 border border-rose-500/40 flex items-center justify-center text-rose-400">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <h2 className="text-base font-bold text-white font-mono">Incident Not Found</h2>
        <p className="text-xs text-slate-400 max-w-sm">
          Unable to locate security incident <code className="text-rose-400 font-mono">{id}</code> in active queue.
        </p>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-900 border border-slate-700 text-xs font-mono text-slate-200 hover:text-emerald-400 transition-colors active:scale-[0.97]"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Return to Queue
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      {/* 1. Header: Incident Title, Target IP, Severity, and Mitigation Controls */}
      <IncidentHeader incident={incident} onMitigate={applyMitigation} />

      {/* 3-Column Core SOC Grid Layout:
          - Left Column (col-span-12 xl:col-span-4): Attack Sequence Timeline
          - Middle Column (col-span-12 xl:col-span-5): Pro vs. Contra Evidence Panel
          - Right Column (col-span-12 xl:col-span-3): MITRE ATT&CK & OWASP Context Matrix
      */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-5 items-stretch">
        {/* 2. Attack Story Timeline (Left Column) */}
        <div className="xl:col-span-4 flex flex-col">
          <AttackTimeline steps={incident.attackStory} />
        </div>

        {/* 3. Pro vs. Contra Evidence Panel (Middle Column) */}
        <div className="xl:col-span-5 flex flex-col">
          <EvidencePanel
            proEvidence={incident.evidence.pro}
            contraEvidence={incident.evidence.contra}
          />
        </div>

        {/* 4. MITRE ATT&CK & OWASP Context Panel (Right Column) */}
        <div className="xl:col-span-3 flex flex-col">
          <MitreOwaspPanel
            mitreContext={incident.mitreContext}
            owaspContext={incident.owaspContext}
          />
        </div>
      </div>

      {/* 5. Tool Trace / SOAR Execution Audit Log (Bottom/Full Width) */}
      <ToolTraceTerminal toolTraces={incident.toolTraces} />
    </div>
  );
}
