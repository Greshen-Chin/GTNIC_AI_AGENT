"use client";

import React from "react";
import { ShieldAlert, AlertTriangle, CheckCircle2, BrainCircuit, Activity } from "lucide-react";
import { IncidentSummaryStats } from "../types";

interface StatsBarProps {
  stats?: IncidentSummaryStats;
  isValidating?: boolean;
}

export const StatsBar: React.FC<StatsBarProps> = ({ stats, isValidating }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {/* Active Threats */}
      <div className="rounded-lg bg-slate-900/60 border border-slate-800/80 p-4 relative overflow-hidden backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
          <span>ACTIVE INCIDENTS</span>
          <Activity className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold font-mono text-white">
            {stats?.activeCount ?? "--"}
          </span>
          <span className="text-xs text-emerald-400 font-mono">Real-time Stream</span>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-emerald-500/50" />
      </div>

      {/* Critical Alerts */}
      <div className="rounded-lg bg-slate-900/60 border border-slate-800/80 p-4 relative overflow-hidden backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
          <span>CRITICAL SEVERITY</span>
          <AlertTriangle className="w-4 h-4 text-rose-500" />
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold font-mono text-rose-400">
            {stats?.criticalCount ?? "--"}
          </span>
          <span className="text-xs text-rose-400/80 font-mono">Immediate Action</span>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-rose-500/50" />
      </div>

      {/* Mitigated / Resolved */}
      <div className="rounded-lg bg-slate-900/60 border border-slate-800/80 p-4 relative overflow-hidden backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
          <span>AUTOMATED MITIGATIONS</span>
          <CheckCircle2 className="w-4 h-4 text-cyan-400" />
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold font-mono text-cyan-300">
            {stats?.mitigatedCount ?? "--"}
          </span>
          <span className="text-xs text-cyan-400/80 font-mono">SOAR Playbooks</span>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500/50" />
      </div>

      {/* AI Confidence Score */}
      <div className="rounded-lg bg-slate-900/60 border border-slate-800/80 p-4 relative overflow-hidden backdrop-blur-sm">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-2">
          <span>AI AGENT CONFIDENCE</span>
          <BrainCircuit className="w-4 h-4 text-indigo-400" />
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold font-mono text-indigo-300">
            {stats ? `${Math.round(stats.aiAverageConfidence * 100)}%` : "--"}
          </span>
          <span className="text-xs text-slate-400 font-mono">
            {isValidating ? "Syncing..." : "Calibrated"}
          </span>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-500/50" />
      </div>
    </div>
  );
};
