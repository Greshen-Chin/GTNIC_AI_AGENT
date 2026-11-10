"use client";

import React from "react";
import { AlertTriangle, CheckCircle2, ShieldCheck, Activity } from "lucide-react";
import { IncidentSummaryStats } from "../types";

interface StatsBarProps {
  stats?: IncidentSummaryStats;
  isValidating?: boolean;
}

export const StatsBar: React.FC<StatsBarProps> = ({ stats, isValidating }) => {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-5">
      {/* Active Threats In Queue */}
      <div className="rounded-lg bg-[#0c121e]/90 border border-slate-800/80 p-3.5 relative overflow-hidden backdrop-blur-md">
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1.5">
          <span className="tracking-wider uppercase">Active Threat Queue</span>
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
        </div>
        <div className="flex items-baseline justify-between">
          <span className="text-2xl sm:text-3xl font-bold font-mono text-white tabular-nums">
            {stats?.activeCount ?? "--"}
          </span>
          <span className="text-[10px] text-emerald-400 font-mono px-1.5 py-0.5 rounded bg-emerald-950/60 border border-emerald-800/40">
            Real-time Feed
          </span>
        </div>
        <p className="text-[10px] text-slate-400 font-mono mt-1">
          Alerts awaiting analyst decision
        </p>
      </div>

      {/* Critical Severity Alerts */}
      <div className="rounded-lg bg-[#0c121e]/90 border border-slate-800/80 p-3.5 relative overflow-hidden backdrop-blur-md">
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1.5">
          <span className="tracking-wider uppercase text-rose-300">Critical Priority</span>
          <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
        </div>
        <div className="flex items-baseline justify-between">
          <span className="text-2xl sm:text-3xl font-bold font-mono text-rose-400 tabular-nums">
            {stats?.criticalCount ?? "--"}
          </span>
          <span className="text-[10px] text-rose-400 font-mono px-1.5 py-0.5 rounded bg-rose-950/60 border border-rose-800/40">
            Immediate Action
          </span>
        </div>
        <p className="text-[10px] text-slate-400 font-mono mt-1">
          Urgent containment needed
        </p>
      </div>

      {/* Mitigated / Resolved */}
      <div className="rounded-lg bg-[#0c121e]/90 border border-slate-800/80 p-3.5 relative overflow-hidden backdrop-blur-md">
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1.5">
          <span className="tracking-wider uppercase text-cyan-300">Approved Mitigations</span>
          <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
        </div>
        <div className="flex items-baseline justify-between">
          <span className="text-2xl sm:text-3xl font-bold font-mono text-cyan-300 tabular-nums">
            {stats?.mitigatedCount ?? "--"}
          </span>
          <span className="text-[10px] text-cyan-400 font-mono px-1.5 py-0.5 rounded bg-cyan-950/60 border border-cyan-800/40">
            Analyst Approved
          </span>
        </div>
        <p className="text-[10px] text-slate-400 font-mono mt-1">
          Approval recorded; execution not verified
        </p>
      </div>

      {/* AI Correlation Confidence */}
      <div className="rounded-lg bg-[#0c121e]/90 border border-slate-800/80 p-3.5 relative overflow-hidden backdrop-blur-md">
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 mb-1.5">
          <span className="tracking-wider uppercase text-indigo-300">Avg Evidence Score</span>
          <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
        </div>
        <div className="flex items-baseline justify-between">
          <span className="text-2xl sm:text-3xl font-bold font-mono text-indigo-300 tabular-nums">
            {stats?.aiAverageConfidence != null ? `${Math.round(stats.aiAverageConfidence * 100)}%` : "--"}
          </span>
          <span className="text-[10px] text-slate-400 font-mono px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800">
            {isValidating ? "Syncing..." : "Assessed only"}
          </span>
        </div>
        <p className="text-[10px] text-slate-400 font-mono mt-1">
          Evidence support score, not accuracy
        </p>
      </div>
      <div className="rounded-lg bg-[#0c121e]/90 border border-slate-800/80 p-3.5 font-mono">
        <p className="text-[11px] uppercase text-emerald-300">Lab Detection Accuracy</p>
        <p className="text-2xl sm:text-3xl font-bold text-emerald-400 mt-1">
          {stats?.detectionAccuracy != null ? `${(stats.detectionAccuracy * 100).toFixed(1)}%` : "--"}
        </p>
        <p className="text-[10px] text-slate-400 mt-1">
          {stats?.evaluationCorrect ?? "--"}/{stats?.evaluationCases ?? "--"} labelled lab cases
        </p>
        <p className="text-[10px] text-slate-500 mt-1">Detector test set; excludes AI narrative</p>
      </div>
    </div>
  );
};
