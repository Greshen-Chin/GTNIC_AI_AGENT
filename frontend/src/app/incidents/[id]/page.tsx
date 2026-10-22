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
import { ShieldAlert, ArrowLeft, RefreshCw } from "lucide-react";

export default function IncidentWorkspacePage() {
  const params = useParams();
  const id = typeof params?.id === "string" ? params.id : Array.isArray(params?.id) ? params.id[0] : "";

  const { incident, isLoading, error, applyMitigation } = useIncident(id);

  if (isLoading && !incident) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3 font-mono text-slate-400">
        <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
        <span className="text-sm">Retrieving Autonomous Investigation Workspace for {id}...</span>
      </div>
    );
  }

  if (error || !incident) {
    return (
      <div className="min-h-[50vh] flex flex-col items-center justify-center gap-4 text-center">
        <div className="w-12 h-12 rounded-full bg-rose-950/60 border border-rose-500/50 flex items-center justify-center text-rose-400">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-white font-mono">Incident Not Found</h2>
        <p className="text-xs text-slate-400 max-w-md">
          Unable to locate security incident with identifier <code className="text-rose-400">{id}</code>.
        </p>
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-slate-900 border border-slate-700 text-xs font-mono text-slate-200 hover:text-emerald-400 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Return to Queue
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 1. Header: Incident Title, Target IP, Severity, and Approve/Reject buttons */}
      <IncidentHeader incident={incident} onMitigate={applyMitigation} />

      {/* 3-Column Core Grid Layout:
          - Left Column (col-span-12 xl:col-span-4): AI Attack Story Timeline
          - Middle Column (col-span-12 xl:col-span-5): Pro vs. Contra Evidence Panel
          - Right Column (col-span-12 xl:col-span-3): MITRE ATT&CK & OWASP Context Panel
      */}
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 items-stretch">
        {/* 2. AI Attack Story Timeline (Left Column) */}
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

        {/* 5. MITRE ATT&CK & OWASP Context Panel (Right Column) */}
        <div className="xl:col-span-3 flex flex-col">
          <MitreOwaspPanel
            mitreContext={incident.mitreContext}
            owaspContext={incident.owaspContext}
          />
        </div>
      </div>

      {/* 4. Tool Trace / Audit Log (Bottom/Full Width) */}
      <ToolTraceTerminal toolTraces={incident.toolTraces} />
    </div>
  );
}
