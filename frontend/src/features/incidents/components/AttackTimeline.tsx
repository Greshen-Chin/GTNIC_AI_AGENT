"use client";

import React from "react";
import { GitCommit, Clock } from "lucide-react";
import { AttackStoryStep } from "../types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { formatDateTime } from "@/lib/utils";

interface AttackTimelineProps {
  steps: AttackStoryStep[];
}

export const AttackTimeline: React.FC<AttackTimelineProps> = ({ steps }) => {
  const phaseColors: Record<string, string> = {
    Reconnaissance: "bg-cyan-950 text-cyan-300 border-cyan-700/60",
    "Initial Access": "bg-amber-950 text-amber-300 border-amber-600/60",
    Execution: "bg-rose-950 text-rose-300 border-rose-600/70",
    Persistence: "bg-purple-950 text-purple-300 border-purple-600/60",
    "Privilege Escalation": "bg-red-950 text-red-300 border-red-600/60",
    "Defense Evasion": "bg-indigo-950 text-indigo-300 border-indigo-600/60",
    "Credential Access": "bg-orange-950 text-orange-300 border-orange-600/60",
    Discovery: "bg-blue-950 text-blue-300 border-blue-600/60",
    "Lateral Movement": "bg-violet-950 text-violet-300 border-violet-600/60",
    Collection: "bg-yellow-950 text-yellow-300 border-yellow-600/60",
    "Command and Control": "bg-pink-950 text-pink-300 border-pink-600/60",
    Exfiltration: "bg-pink-950 text-pink-300 border-pink-600/60",
    Impact: "bg-red-900 text-red-100 border-red-500",
  };

  return (
    <Card className="h-full border-slate-800 bg-slate-900/60 flex flex-col">
      <CardHeader className="bg-slate-950/40">
        <CardTitle>
          <GitCommit className="w-4 h-4 text-emerald-400" />
          AI Attack Story Timeline
        </CardTitle>
        <span className="text-[11px] font-mono text-slate-400">
          Chronological Reconstruction
        </span>
      </CardHeader>

      <CardContent className="flex-1 p-5 overflow-y-auto max-h-[680px]">
        {steps.length === 0 ? (
          <div className="text-center py-8 text-xs font-mono text-slate-500">
            No attack sequence steps identified by AI correlation engine.
          </div>
        ) : (
          <div className="relative pl-6 space-y-8 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-gradient-to-b before:from-emerald-500 before:via-cyan-500 before:to-rose-500">
            {steps.map((step, idx) => (
              <div key={idx} className="relative group">
                {/* Node icon / indicator */}
                <div
                  className={`absolute -left-[30px] top-1.5 w-5 h-5 rounded-full flex items-center justify-center border transition-all ${
                    step.highlight
                      ? "bg-rose-950 border-rose-500 shadow-[0_0_12px_#f43f5e]"
                      : "bg-slate-950 border-emerald-500/80 shadow-[0_0_8px_rgba(16,185,129,0.3)]"
                  }`}
                >
                  <div
                    className={`w-2 h-2 rounded-full ${
                      step.highlight ? "bg-rose-400 animate-ping" : "bg-emerald-400"
                    }`}
                  />
                </div>

                {/* Step Content Card */}
                <div
                  className={`rounded-lg border p-4 transition-all duration-200 ${
                    step.highlight
                      ? "bg-rose-950/20 border-rose-500/50 shadow-[0_0_15px_rgba(244,63,94,0.1)]"
                      : "bg-slate-950/60 border-slate-800/90 hover:border-slate-700"
                  }`}
                >
                  {/* Step Header */}
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-slate-300">
                        PHASE {step.stepNumber.toString().padStart(2, "0")}
                      </span>
                      <span
                        className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${
                          phaseColors[step.phase] || "bg-slate-800 text-slate-300 border-slate-700"
                        }`}
                      >
                        {step.phase}
                      </span>
                    </div>

                    <div className="flex items-center gap-1 text-[11px] font-mono text-slate-500">
                      <Clock className="w-3 h-3" />
                      <span>{formatDateTime(step.timestamp)}</span>
                    </div>
                  </div>

                  {/* Step Title & Details */}
                  <h4 className="text-sm font-semibold text-white mb-1.5 flex items-center gap-1.5">
                    {step.title}
                    {step.highlight && (
                      <span className="inline-flex items-center text-[10px] font-mono font-medium text-rose-400 bg-rose-950/80 px-1.5 py-0.2 rounded border border-rose-700/60">
                        CRITICAL TRIGGER
                      </span>
                    )}
                  </h4>
                  <p className="text-xs text-slate-300 leading-relaxed font-sans">
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
