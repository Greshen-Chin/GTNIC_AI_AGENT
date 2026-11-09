"use client";

import React from "react";
import { useIncidents, useIncidentStats } from "@/features/incidents/hooks";
import { IncidentTable, StatsBar } from "@/features/incidents/components";
import { ShieldAlert, RefreshCw, AlertCircle } from "lucide-react";

export default function DashboardPage() {
  const { incidents, isLoading, isValidating, error } = useIncidents(3000);
  const { stats, error: statsError } = useIncidentStats(3000);

  const connectionState = error || statsError
    ? { label: "Backend Offline", className: "bg-rose-950/80 border-rose-600/60 text-rose-300" }
    : isLoading
      ? { label: "Connecting…", className: "bg-amber-950/80 border-amber-600/60 text-amber-300" }
      : { label: "Correlation Active", className: "bg-emerald-950/80 border-emerald-600/60 text-emerald-300" };

  return (
    <div className="space-y-5">
      {/* Page Header / Triage Operations Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-lg sm:text-xl font-bold tracking-tight text-white font-mono flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-emerald-400" />
              Incident Queue & Threat Triage
            </h1>
            <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono border ${connectionState.className}`}>
              <span className="h-1.5 w-1.5 rounded-full bg-current animate-pulse" />
              {connectionState.label}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time security alert correlation, autonomous reasoning, and operator approval console.
          </p>
        </div>

        {/* Polling / Heartbeat indicator */}
        <div className="flex items-center gap-2 self-start sm:self-auto font-mono text-[11px] text-slate-400 bg-[#0c121e] px-2.5 py-1.5 rounded border border-slate-800">
          <RefreshCw className={`w-3 h-3 text-emerald-400 ${isValidating ? "animate-spin" : ""}`} />
          <span className="text-slate-400">Stream:</span>
          <span className={`font-semibold tabular-nums ${error || statsError ? "text-rose-400" : "text-emerald-400"}`}>
            {error || statsError ? "Retrying" : "Live (3s sync)"}
          </span>
        </div>
      </div>

      {(error || statsError) && (
        <div role="alert" className="rounded-lg border border-rose-500/40 bg-rose-950/40 p-3.5 text-xs font-mono text-rose-300 flex items-center gap-2.5">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-400" />
          <span>Unable to reach SOAR backend telemetry API. Retrying connection automatically...</span>
        </div>
      )}

      {/* Top SOC Metrics */}
      <StatsBar stats={stats} isValidating={isValidating} />

      {/* Main Incident Queue Data Table */}
      <IncidentTable
        incidents={incidents}
        isLoading={isLoading}
        isValidating={isValidating}
      />
    </div>
  );
}
