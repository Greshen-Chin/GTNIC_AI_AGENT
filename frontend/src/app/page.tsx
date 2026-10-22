"use client";

import React from "react";
import { useIncidents, useIncidentStats } from "@/features/incidents/hooks";
import { IncidentTable, StatsBar } from "@/features/incidents/components";
import { ShieldCheck, Activity } from "lucide-react";

export default function DashboardPage() {
  // Use SWR hook with 3-second refresh interval as requested
  const { incidents, isLoading, isValidating } = useIncidents(3000);
  const { stats } = useIncidentStats(3000);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
              Incident Queue & Threat Triage
            </h1>
            <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-950/80 border border-emerald-500/50 text-emerald-400 text-xs font-mono">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
              Status: Active
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
          <span className="text-emerald-400 font-semibold">Online (3s polling)</span>
        </div>
      </div>

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
