"use client";

import React from "react";
import { ShieldCheck, ExternalLink, Bookmark, Layers } from "lucide-react";
import { MitreContext, OwaspContext } from "../types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";

interface MitreOwaspPanelProps {
  mitreContext: MitreContext[];
  owaspContext?: OwaspContext[];
}

export const MitreOwaspPanel: React.FC<MitreOwaspPanelProps> = ({
  mitreContext,
  owaspContext = [],
}) => {
  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>
          <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
          MITRE ATT&CK & OWASP Matrix
        </CardTitle>
        <span className="text-[10px] font-mono text-slate-400">
          Tactical Mapping
        </span>
      </CardHeader>

      <CardContent className="flex-1 p-4 overflow-y-auto max-h-[660px] space-y-4">
        {/* MITRE Techniques Section */}
        <div className="space-y-2.5">
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 uppercase tracking-wider pb-1 border-b border-slate-800">
            <span className="flex items-center gap-1.5">
              <Layers className="w-3 h-3 text-indigo-400" />
              <span>ATT&CK Techniques</span>
            </span>
            <span className="text-indigo-400 font-semibold tabular-nums">{mitreContext.length} Mapped</span>
          </div>

          {mitreContext.length === 0 ? (
            <p className="text-xs font-mono text-slate-500 py-2">No MITRE tactics matched.</p>
          ) : (
            mitreContext.map((item) => (
              <div
                key={item.id}
                className="rounded bg-[#070b12] border border-indigo-900/30 hover:border-indigo-600/50 transition-colors duration-150 p-3 space-y-2 group"
              >
                <div className="flex items-start justify-between gap-1.5">
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="font-mono text-[10px] font-bold px-1.5 py-0.2 rounded bg-indigo-950 text-indigo-300 border border-indigo-700/60">
                        {item.id}
                      </span>
                      <span className="text-[9px] font-mono uppercase text-slate-400">
                        {item.tactic}
                      </span>
                    </div>
                    <h5 className="text-xs font-semibold text-slate-100 mt-1 font-mono group-hover:text-indigo-300 transition-colors">
                      {item.name}
                    </h5>
                  </div>

                  {item.url && (
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-500 hover:text-indigo-400 transition-colors p-1"
                      title="Open MITRE Framework Page"
                    >
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>

                <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                  {item.description}
                </p>

                {/* Mitigation Advice */}
                {item.mitigationAdvice && (
                  <div className="p-2 rounded bg-slate-900/90 border border-slate-800 text-[10px] space-y-0.5">
                    <div className="flex items-center gap-1 text-emerald-400 font-mono font-semibold uppercase">
                      <Bookmark className="w-2.5 h-2.5" />
                      Remediation Guideline
                    </div>
                    <p className="text-slate-300 leading-relaxed">{item.mitigationAdvice}</p>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* OWASP Context Section */}
        {owaspContext.length > 0 && (
          <div className="space-y-2.5 pt-2">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 uppercase tracking-wider pb-1 border-b border-slate-800">
              <span>OWASP Top 10</span>
              <span className="text-amber-400 font-semibold tabular-nums">{owaspContext.length} Matched</span>
            </div>

            {owaspContext.map((owasp) => (
              <div
                key={owasp.id}
                className="rounded bg-[#070b12] border border-amber-900/30 hover:border-amber-600/50 transition-colors duration-150 p-3 space-y-1.5 group"
              >
                <div className="flex items-start justify-between gap-1.5">
                  <div className="flex items-center gap-1.5">
                    <span className="font-mono text-[10px] font-bold px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 border border-amber-700/60">
                      {owasp.id}
                    </span>
                    <h5 className="text-xs font-semibold text-slate-100 font-mono group-hover:text-amber-300 transition-colors">
                      {owasp.name}
                    </h5>
                  </div>
                </div>
                <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                  {owasp.description}
                </p>
                {owasp.remediation && (
                  <div className="p-2 rounded bg-slate-900/90 border border-slate-800 text-[10px] space-y-0.5">
                    <div className="flex items-center gap-1 text-amber-400 font-mono font-semibold uppercase">
                      <Bookmark className="w-2.5 h-2.5" />
                      Remediation
                    </div>
                    <p className="text-slate-300 leading-relaxed">{owasp.remediation}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
