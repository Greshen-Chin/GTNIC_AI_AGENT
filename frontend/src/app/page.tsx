"use client";

import React from "react";
import { useIncidents, useIncidentStats } from "@/features/incidents/hooks";
import { IncidentTable, StatsBar } from "@/features/incidents/components";
import { Activity } from "lucide-react";

export default function DashboardPage() {
  // Use SWR hook with 3-second refresh interval as requested
  const { incidents, isLoading, isValidating, error } = useIncidents(3000);
  const { stats, error: statsError } = useIncidentStats(3000);
  const connectionState = error || statsError
    ? { label: "Backend unavailable", className: "bg-rose-950/80 border-rose-500/50 text-rose-400" }
    : isLoading
      ? { label: "Connecting…", className: "bg-amber-950/80 border-amber-500/50 text-amber-300" }
      : { label: "Backend connected", className: "bg-emerald-950/80 border-emerald-500/50 text-emerald-400" };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              Incident Queue & Threat Triage
            </h1>
            <span className={`flex items-center gap-1.5 px-2.5 py-0.5 rounded-full border text-xs font-mono ${connectionState.className}`}>
              <span className="h-1.5 w-1.5 rounded-full bg-current" />
              {connectionState.label}
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Real-time automated correlation feed driven by GTNIC Autonomous SOC Agent.
          </p>
        </div>

        {/* Status Chip */}
        <div className="flex items-center gap-2 self-start sm:self-auto font-mono text-xs text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span>Stream Engine: </span>
          <span className={`font-semibold ${error || statsError ? "text-rose-400" : "text-emerald-400"}`}>
            {error || statsError ? "Retrying" : "Polling every 3s"}
          </span>
        </div>
      </div>

      {(error || statsError) && (
        <div role="alert" className="rounded-lg border border-rose-500/50 bg-rose-950/30 p-4 text-sm text-rose-300">
          Unable to load live dashboard data. Retrying automatically.
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
