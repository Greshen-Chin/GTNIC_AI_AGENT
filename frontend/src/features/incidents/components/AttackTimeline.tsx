"use client";

import React from "react";
import { GitCommit, Clock, AlertTriangle } from "lucide-react";
import { AttackStoryStep } from "../types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { formatDateTime } from "@/lib/utils";

interface AttackTimelineProps {
  steps: AttackStoryStep[];
}

export const AttackTimeline: React.FC<AttackTimelineProps> = ({ steps }) => {
  const phaseColors: Record<string, string> = {
    Reconnaissance: "bg-cyan-950/70 text-cyan-300 border-cyan-700/50",
    "Initial Access": "bg-amber-950/70 text-amber-300 border-amber-600/50",
    Execution: "bg-rose-950/70 text-rose-300 border-rose-600/50",
    Persistence: "bg-purple-950/70 text-purple-300 border-purple-600/50",
    "Privilege Escalation": "bg-red-950/70 text-red-300 border-red-600/50",
    "Defense Evasion": "bg-indigo-950/70 text-indigo-300 border-indigo-600/50",
    "Credential Access": "bg-orange-950/70 text-orange-300 border-orange-600/50",
    Discovery: "bg-blue-950/70 text-blue-300 border-blue-600/50",
    "Lateral Movement": "bg-violet-950/70 text-violet-300 border-violet-600/50",
    Collection: "bg-yellow-950/70 text-yellow-300 border-yellow-600/50",
    "Command and Control": "bg-pink-950/70 text-pink-300 border-pink-600/50",
    Exfiltration: "bg-pink-950/70 text-pink-300 border-pink-600/50",
    Impact: "bg-rose-900 text-rose-100 border-rose-500",
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>
          <GitCommit className="w-3.5 h-3.5 text-emerald-400" />
          Attack Sequence Timeline
        </CardTitle>
        <span className="text-[10px] font-mono text-slate-400">
          Chronological
        </span>
      </CardHeader>

      <CardContent className="flex-1 p-4 overflow-y-auto max-h-[660px]">
        {steps.length === 0 ? (
          <div className="text-center py-10 text-xs font-mono text-slate-500">
            No chronological sequence steps recorded.
          </div>
        ) : (
          <div className="relative pl-5 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-px before:bg-slate-800">
            {steps.map((step, idx) => (
              <div key={idx} className="relative group">
                {/* Node indicator */}
                <div
                  className={`absolute -left-[24px] top-1.5 w-4 h-4 rounded-full flex items-center justify-center border transition-all ${
                    step.highlight
                      ? "bg-rose-950 border-rose-500 shadow-[0_0_8px_#f43f5e]"
                      : "bg-[#070b12] border-slate-700"
                  }`}
                >
                  <div
                    className={`w-1.5 h-1.5 rounded-full ${
                      step.highlight ? "bg-rose-400 animate-ping" : "bg-emerald-400"
                    }`}
                  />
                </div>

                {/* Step Content Box */}
                <div
                  className={`rounded border p-3 transition-colors duration-150 ${
                    step.highlight
                      ? "bg-rose-950/20 border-rose-600/40"
                      : "bg-[#070b12]/80 border-slate-800/90 hover:border-slate-700"
                  }`}
                >
                  {/* Step Header */}
                  <div className="flex flex-wrap items-center justify-between gap-1.5 mb-1.5">
                    <div className="flex items-center gap-1.5">
                      <span className="font-mono text-[9px] font-bold px-1.5 py-0.2 rounded bg-slate-900 border border-slate-800 text-slate-300">
                        PHASE {step.stepNumber.toString().padStart(2, "0")}
                      </span>
                      <span
                        className={`text-[9px] font-mono uppercase px-1.5 py-0.2 rounded border ${
                          phaseColors[step.phase] || "bg-slate-900 text-slate-300 border-slate-800"
                        }`}
                      >
                        {step.phase}
                      </span>
                    </div>

                    {step.timestamp && (
                      <div className="flex items-center gap-1 text-[10px] font-mono text-slate-400 tabular-nums">
                        <Clock className="w-2.5 h-2.5" />
                        <span>{formatDateTime(step.timestamp)}</span>
                      </div>
                    )}
                  </div>

                  {/* Title */}
                  <h4 className="text-xs font-semibold text-white mb-1 flex items-center gap-1.5 font-mono">
                    {step.title}
                    {step.highlight && (
                      <span className="inline-flex items-center gap-0.5 text-[9px] font-mono font-medium text-rose-300 bg-rose-950/90 px-1.5 py-0.2 rounded border border-rose-700/60">
                        <AlertTriangle className="w-2.5 h-2.5 text-rose-400" />
                        TRIGGER
                      </span>
                    )}
                  </h4>

                  {/* Description */}
                  <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
