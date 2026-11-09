"use client";

import React, { useState } from "react";
import {
  Scale,
  FileCode,
  ChevronDown,
  ChevronUp,
  Fingerprint,
  Copy,
  Check,
} from "lucide-react";
import { Evidence } from "../types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";

interface EvidencePanelProps {
  proEvidence: Evidence[];
  contraEvidence: Evidence[];
}

export const EvidencePanel: React.FC<EvidencePanelProps> = ({
  proEvidence,
  contraEvidence,
}) => {
  const [expandedArtifactId, setExpandedArtifactId] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const toggleArtifact = (id: string) => {
    setExpandedArtifactId((prev) => (prev === id ? null : id));
  };

  const copyArtifact = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>
          <Scale className="w-3.5 h-3.5 text-cyan-400" />
          Pro vs Contra Evidence Analysis
        </CardTitle>
        <div className="flex items-center gap-2 text-[10px] font-mono">
          <span className="text-rose-400 font-semibold tabular-nums">
            Inculpatory: {proEvidence.length}
          </span>
          <span className="text-slate-600">/</span>
          <span className="text-emerald-400 font-semibold tabular-nums">
            Exculpatory: {contraEvidence.length}
          </span>
        </div>
      </CardHeader>

      <CardContent className="flex-1 p-4 overflow-y-auto max-h-[660px]">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {/* PRO EVIDENCE COLUMN */}
          <div className="space-y-2.5">
            <div className="flex items-center justify-between pb-1.5 border-b border-rose-900/40">
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-rose-500 shadow-[0_0_6px_#f43f5e]" />
                <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-rose-300">
                  Supporting Attack (Pro)
                </span>
              </div>
              <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-rose-950/60 text-rose-400 border border-rose-800/40">
                Inculpatory
              </span>
            </div>

            {proEvidence.length === 0 ? (
              <div className="text-[11px] font-mono text-slate-500 p-3 text-center rounded bg-[#070b12] border border-slate-800">
                No incriminating evidence logged.
              </div>
            ) : (
              proEvidence.map((item) => (
                <div
                  key={item.id}
                  className="rounded bg-[#070b12] border border-rose-900/30 hover:border-rose-700/50 transition-colors duration-150 p-3 space-y-2"
                >
                  <div className="flex items-start justify-between gap-1.5">
                    <h5 className="text-xs font-semibold text-slate-100 font-mono">
                      {item.title}
                    </h5>
                    <span
                      className={`text-[9px] font-mono px-1.5 py-0.2 rounded uppercase border whitespace-nowrap ${
                        item.confidence === "High"
                          ? "bg-rose-950 text-rose-300 border-rose-700/60 font-semibold"
                          : "bg-slate-900 text-slate-400 border-slate-700"
                      }`}
                    >
                      {item.confidence} Conf.
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                    {item.description}
                  </p>

                  <div className="flex items-center justify-between pt-1 text-[10px] font-mono text-slate-400">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Fingerprint className="w-3 h-3 text-rose-400" />
                      {item.source}
                    </span>
                    {item.timestamp && <span className="tabular-nums">{item.timestamp}</span>}
                  </div>

                  {item.rawArtifact && (
                    <div className="pt-1.5 border-t border-slate-800/80">
                      <button
                        onClick={() => toggleArtifact(item.id)}
                        className="flex items-center justify-between w-full text-[10px] font-mono text-slate-400 hover:text-rose-300 transition-colors"
                      >
                        <span className="flex items-center gap-1">
                          <FileCode className="w-3 h-3" />
                          <span>Raw Payload Artifact</span>
                        </span>
                        {expandedArtifactId === item.id ? (
                          <ChevronUp className="w-3 h-3" />
                        ) : (
                          <ChevronDown className="w-3 h-3" />
                        )}
                      </button>

                      {expandedArtifactId === item.id && (
                        <div className="mt-2 relative">
                          <pre className="p-2.5 rounded bg-black border border-slate-800 text-[10px] font-mono text-emerald-400 overflow-x-auto whitespace-pre-wrap max-h-36">
                            {item.rawArtifact}
                          </pre>
                          <button
                            onClick={() => copyArtifact(item.id, item.rawArtifact!)}
                            className="absolute top-1.5 right-1.5 p-1 rounded bg-slate-900 border border-slate-700 text-slate-400 hover:text-white transition-colors"
                            title="Copy payload"
                          >
                            {copiedId === item.id ? (
                              <Check className="w-3 h-3 text-emerald-400" />
                            ) : (
                              <Copy className="w-3 h-3" />
                            )}
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {/* CONTRA EVIDENCE COLUMN */}
          <div className="space-y-2.5">
            <div className="flex items-center justify-between pb-1.5 border-b border-emerald-900/40">
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_6px_#10b981]" />
                <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-emerald-300">
                  Defending Legitimacy (Contra)
                </span>
              </div>
              <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/40">
                Exculpatory
              </span>
            </div>

            {contraEvidence.length === 0 ? (
              <div className="text-[11px] font-mono text-slate-500 p-3 text-center rounded bg-[#070b12] border border-slate-800">
                No exculpatory evidence found.
              </div>
            ) : (
              contraEvidence.map((item) => (
                <div
                  key={item.id}
                  className="rounded bg-[#070b12] border border-emerald-900/30 hover:border-emerald-700/50 transition-colors duration-150 p-3 space-y-2"
                >
                  <div className="flex items-start justify-between gap-1.5">
                    <h5 className="text-xs font-semibold text-slate-100 font-mono">
                      {item.title}
                    </h5>
                    <span
                      className={`text-[9px] font-mono px-1.5 py-0.2 rounded uppercase border whitespace-nowrap ${
                        item.confidence === "High"
                          ? "bg-emerald-950 text-emerald-300 border-emerald-700/60 font-semibold"
                          : "bg-slate-900 text-slate-400 border-slate-700"
                      }`}
                    >
                      {item.confidence} Conf.
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                    {item.description}
                  </p>

                  <div className="flex items-center justify-between pt-1 text-[10px] font-mono text-slate-400">
                    <span className="flex items-center gap-1 text-slate-400">
                      <Fingerprint className="w-3 h-3 text-emerald-400" />
                      {item.source}
                    </span>
                    {item.timestamp && <span className="tabular-nums">{item.timestamp}</span>}
                  </div>

                  {item.rawArtifact && (
                    <div className="pt-1.5 border-t border-slate-800/80">
                      <button
                        onClick={() => toggleArtifact(item.id)}
                        className="flex items-center justify-between w-full text-[10px] font-mono text-slate-400 hover:text-emerald-300 transition-colors"
                      >
                        <span className="flex items-center gap-1">
                          <FileCode className="w-3 h-3" />
                          <span>Raw Telemetry Artifact</span>
                        </span>
                        {expandedArtifactId === item.id ? (
                          <ChevronUp className="w-3 h-3" />
                        ) : (
                          <ChevronDown className="w-3 h-3" />
                        )}
                      </button>

                      {expandedArtifactId === item.id && (
                        <div className="mt-2 relative">
                          <pre className="p-2.5 rounded bg-black border border-slate-800 text-[10px] font-mono text-cyan-300 overflow-x-auto whitespace-pre-wrap max-h-36">
                            {item.rawArtifact}
                          </pre>
                          <button
                            onClick={() => copyArtifact(item.id, item.rawArtifact!)}
                            className="absolute top-1.5 right-1.5 p-1 rounded bg-slate-900 border border-slate-700 text-slate-400 hover:text-white transition-colors"
                            title="Copy payload"
                          >
                            {copiedId === item.id ? (
                              <Check className="w-3 h-3 text-emerald-400" />
                            ) : (
                              <Copy className="w-3 h-3" />
                            )}
                          </button>
                        </div>
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
