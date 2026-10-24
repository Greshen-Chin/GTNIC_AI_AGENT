"use client";

import React from "react";
import { ShieldCheck, ExternalLink, BookOpen, Bookmark } from "lucide-react";
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
    <Card className="h-full border-slate-800 bg-slate-900/60 flex flex-col">
      <CardHeader className="bg-slate-950/40">
        <CardTitle>
          <ShieldCheck className="w-4 h-4 text-indigo-400" />
          MITRE ATT&CK & OWASP Matrix
        </CardTitle>
        <span className="text-[11px] font-mono text-slate-400">
          Tactical Mapping
        </span>
      </CardHeader>

      <CardContent className="flex-1 p-5 overflow-y-auto max-h-[680px] space-y-4">
        {/* MITRE Techniques Section */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400 uppercase tracking-wider pb-1 border-b border-slate-800">
            <span>Identified ATT&CK Techniques</span>
            <span className="text-indigo-400 font-semibold">{mitreContext.length} Mapped</span>
          </div>

          {mitreContext.length === 0 ? (
            <p className="text-xs font-mono text-slate-500">No MITRE tactics matched.</p>
          ) : (
            mitreContext.map((item) => (
              <div
                key={item.id}
                className="rounded-lg bg-slate-950/80 border border-indigo-900/40 hover:border-indigo-600/60 transition-all p-3.5 space-y-2 group"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-700/60">
                        {item.id}
                      </span>
                      <span className="text-[10px] font-mono uppercase text-slate-400">
                        {item.tactic}
                      </span>
                    </div>
                    <h5 className="text-xs font-semibold text-slate-100 mt-1.5 group-hover:text-indigo-300 transition-colors">
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
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  )}
                </div>

                <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                  {item.description}
                </p>

                {/* Mitigation Advice */}
                <div className="p-2.5 rounded bg-slate-900/90 border border-slate-800 text-[11px] space-y-1">
                  <div className="flex items-center gap-1.5 text-emerald-400 font-mono text-[10px] font-semibold uppercase">
                    <Bookmark className="w-3 h-3" />
                    Mitigation Guideline
                  </div>
                  <p className="text-slate-300 leading-normal">{item.mitigationAdvice}</p>
                </div>
              </div>
            ))
          )}
        </div>

        {/* OWASP Context Section */}
        {owaspContext.length > 0 && (
          <div className="space-y-3 pt-2">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400 uppercase tracking-wider pb-1 border-b border-slate-800">
              <span>OWASP Top 10 Classification</span>
              <span className="text-amber-400 font-semibold">{owaspContext.length} Matched</span>
            </div>

            {owaspContext.map((owasp) => (
              <div
                key={owasp.id}
                className="rounded-lg bg-slate-950/80 border border-amber-900/40 hover:border-amber-600/60 transition-all p-3.5 space-y-2 group"
              >
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-700/60">
                    {owasp.id}
                  </span>
                  <span className="text-xs font-semibold text-slate-100 group-hover:text-amber-300 transition-colors">
                    {owasp.name}
                  </span>
                </div>

                <p className="text-[11px] text-slate-300 leading-relaxed font-sans">
                  {owasp.description}
                </p>

                <div className="p-2.5 rounded bg-slate-900/90 border border-slate-800 text-[11px] space-y-1">
                  <div className="flex items-center gap-1.5 text-cyan-400 font-mono text-[10px] font-semibold uppercase">
                    <BookOpen className="w-3 h-3" />
                    Remediation Standard
                  </div>
                  <p className="text-slate-300 leading-normal">{owasp.remediation}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
