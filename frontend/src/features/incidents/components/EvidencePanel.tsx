"use client";

import React, { useState } from "react";
import {
  Scale,
  CheckCircle,
  XCircle,
  FileCode,
  ShieldAlert,
  ChevronDown,
  ChevronUp,
  Fingerprint,
} from "lucide-react";
import { Evidence } from "../types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

interface EvidencePanelProps {
  proEvidence: Evidence[];
  contraEvidence: Evidence[];
}

export const EvidencePanel: React.FC<EvidencePanelProps> = ({
  proEvidence,
  contraEvidence,
}) => {
  const [expandedArtifactId, setExpandedArtifactId] = useState<string | null>(null);

  const toggleArtifact = (id: string) => {
    setExpandedArtifactId((prev) => (prev === id ? null : id));
  };

  return (
    <Card className="h-full border-slate-800 bg-slate-900/60 flex flex-col">
      <CardHeader className="bg-slate-950/40">
        <CardTitle>
          <Scale className="w-4 h-4 text-cyan-400" />
          Pro vs. Contra Evidence Analysis
        </CardTitle>
        <div className="flex items-center gap-3 text-[11px] font-mono">
          <span className="text-rose-400 font-medium">
            Pro: {proEvidence.length}
          </span>
          <span className="text-slate-600">|</span>
          <span className="text-emerald-400 font-medium">
            Contra: {contraEvidence.length}
          </span>
        </div>
      </CardHeader>

      <CardContent className="flex-1 p-5 overflow-y-auto max-h-[680px]">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* PRO EVIDENCE COLUMN */}
          <div className="space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-rose-900/40">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_8px_#f43f5e]" />
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-rose-300">
                  Supporting Attack (Pro)
                </span>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950/60 text-rose-400 border border-rose-700/50">
                Inculpatory
              </span>
            </div>

            {proEvidence.length === 0 ? (
              <div className="text-xs font-mono text-slate-500 p-4 text-center rounded bg-slate-950/40 border border-slate-800/60">
                No incriminating evidence logged.
              </div>
            ) : (
              proEvidence.map((item) => (
                <div
                  key={item.id}
                  className="rounded-lg bg-slate-950/70 border border-rose-900/40 hover:border-rose-700/60 transition-all p-3.5 space-y-2 group"
                >
                  <div className="flex items-start justify-between gap-2">
                    <h5 className="text-xs font-bold text-slate-100 group-hover:text-rose-300 transition-colors">
                      {item.title}
                    </h5>
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.5 rounded uppercase border whitespace-nowrap ${
                        item.confidence === "High"
                          ? "bg-rose-950 text-rose-400 border-rose-700/60"
                          : "bg-slate-900 text-slate-400 border-slate-700"
                      }`}
                    >
                      {item.confidence} Conf.
                    </span>
                  </div>

                  <p className="text-[12px] text-slate-300 leading-relaxed font-sans">
                    {item.description}
                  </p>

                  <div className="flex items-center justify-between pt-1 text-[10px] font-mono text-slate-500">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Fingerprint className="w-3 h-3 text-rose-400" />
                      {item.source}
                    </span>
                    <span>{item.timestamp}</span>
                  </div>

                  {/* Optional Raw Artifact preview */}
                  {item.rawArtifact && (
                    <div className="pt-1">
                      <button
                        type="button"
                        onClick={() => toggleArtifact(item.id)}
                        className="flex items-center gap-1 text-[11px] font-mono text-cyan-400 hover:text-cyan-300 transition-colors"
                      >
                        <FileCode className="w-3 h-3" />
                        <span>{expandedArtifactId === item.id ? "Hide Payload Artifact" : "Inspect Raw Payload"}</span>
                        {expandedArtifactId === item.id ? (
                          <ChevronUp className="w-3 h-3" />
                        ) : (
                          <ChevronDown className="w-3 h-3" />
                        )}
                      </button>

                      {expandedArtifactId === item.id && (
                        <pre className="mt-2 p-2.5 rounded bg-black/90 border border-slate-800 text-[11px] font-mono text-emerald-400 overflow-x-auto whitespace-pre-wrap leading-tight">
                          {item.rawArtifact}
                        </pre>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {/* CONTRA EVIDENCE COLUMN */}
          <div className="space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-emerald-900/40">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#10b981]" />
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-emerald-300">
                  Against Attack (Contra)
                </span>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-700/50">
                Exculpatory
              </span>
            </div>

            {contraEvidence.length === 0 ? (
              <div className="text-xs font-mono text-slate-500 p-4 text-center rounded bg-slate-950/40 border border-slate-800/60">
                No mitigating contra-evidence found.
              </div>
            ) : (
              contraEvidence.map((item) => (
                <div
                  key={item.id}
                  className="rounded-lg bg-slate-950/70 border border-emerald-900/40 hover:border-emerald-700/60 transition-all p-3.5 space-y-2 group"
                >
                  <div className="flex items-start justify-between gap-2">
                    <h5 className="text-xs font-bold text-slate-100 group-hover:text-emerald-300 transition-colors">
                      {item.title}
                    </h5>
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.5 rounded uppercase border whitespace-nowrap ${
                        item.confidence === "High"
                          ? "bg-emerald-950 text-emerald-400 border-emerald-700/60"
                          : "bg-slate-900 text-slate-400 border-slate-700"
                      }`}
                    >
                      {item.confidence} Conf.
                    </span>
                  </div>

                  <p className="text-[12px] text-slate-300 leading-relaxed font-sans">
                    {item.description}
                  </p>

                  <div className="flex items-center justify-between pt-1 text-[10px] font-mono text-slate-500">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Fingerprint className="w-3 h-3 text-emerald-400" />
                      {item.source}
                    </span>
                    <span>{item.timestamp}</span>
                  </div>

                  {item.rawArtifact && (
                    <div className="pt-1">
                      <button
                        type="button"
                        onClick={() => toggleArtifact(item.id)}
                        className="flex items-center gap-1 text-[11px] font-mono text-cyan-400 hover:text-cyan-300 transition-colors"
                      >
                        <FileCode className="w-3 h-3" />
                        <span>{expandedArtifactId === item.id ? "Hide Artifact" : "Inspect Raw Evidence"}</span>
                        {expandedArtifactId === item.id ? (
                          <ChevronUp className="w-3 h-3" />
                        ) : (
                          <ChevronDown className="w-3 h-3" />
                        )}
                      </button>

                      {expandedArtifactId === item.id && (
                        <pre className="mt-2 p-2.5 rounded bg-black/90 border border-slate-800 text-[11px] font-mono text-cyan-400 overflow-x-auto whitespace-pre-wrap leading-tight">
                          {item.rawArtifact}
                        </pre>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
