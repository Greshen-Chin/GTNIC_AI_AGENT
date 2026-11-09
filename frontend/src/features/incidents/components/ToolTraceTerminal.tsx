"use client";

import React, { useState } from "react";
import {
  Terminal as TerminalIcon,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  CheckCircle2,
  XCircle,
  Clock,
  Layers,
} from "lucide-react";
import { ToolTrace } from "../types";

interface ToolTraceTerminalProps {
  toolTraces: ToolTrace[];
}

export const ToolTraceTerminal: React.FC<ToolTraceTerminalProps> = ({
  toolTraces,
}) => {
  const [isOpen, setIsOpen] = useState(true);
  const [activeTraceId, setActiveTraceId] = useState<string>(
    toolTraces[0]?.id || ""
  );
  const [copied, setCopied] = useState(false);

  const selectedTrace =
    toolTraces.find((t) => t.id === activeTraceId) || toolTraces[0];

  const handleCopyJson = () => {
    if (!selectedTrace) return;
    navigator.clipboard.writeText(JSON.stringify(selectedTrace, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-lg border border-slate-800/80 bg-[#070b12] shadow-xl overflow-hidden font-mono mt-5">
      {/* Tactical Title Bar */}
      <div className="bg-[#0c121e] border-b border-slate-800/80 px-4 py-2.5 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <TerminalIcon className="w-4 h-4 text-emerald-400" />
          <div className="flex items-center gap-2 text-xs">
            <span className="text-white font-semibold">SOAR Execution Trace & Tool Audit Log</span>
            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-900 text-slate-400 border border-slate-800 tabular-nums">
              {toolTraces.length} Calls Recorded
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isOpen && selectedTrace && (
            <button
              onClick={handleCopyJson}
              className="flex items-center gap-1 text-[10px] px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition-colors active:scale-[0.97]"
            >
              {copied ? (
                <>
                  <Check className="w-3 h-3 text-emerald-400" />
                  <span className="text-emerald-400">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" />
                  <span>Copy JSON</span>
                </>
              )}
            </button>
          )}

          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-white px-2 py-1 rounded hover:bg-slate-900 transition-colors active:scale-[0.97]"
          >
            {isOpen ? (
              <>
                <span>Collapse</span>
                <ChevronUp className="w-3.5 h-3.5" />
              </>
            ) : (
              <>
                <span>Expand Trace Log</span>
                <ChevronDown className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Terminal Body */}
      {isOpen && (
        <div className="grid grid-cols-1 lg:grid-cols-12 min-h-[300px] max-h-[440px] divide-y lg:divide-y-0 lg:divide-x divide-slate-800/80 bg-[#070b12]">
          {/* Tool List Sidebar */}
          <div className="lg:col-span-4 p-2.5 overflow-y-auto space-y-1 bg-[#090e18]/80">
            <div className="flex items-center gap-1.5 text-[10px] text-slate-400 uppercase px-2 py-1 tracking-wider">
              <Layers className="w-3 h-3 text-slate-400" />
              <span>Tool Call Sequence</span>
            </div>
            {toolTraces.length === 0 ? (
              <div className="text-[11px] text-slate-500 p-3 text-center">
                No tool traces logged.
              </div>
            ) : (
              toolTraces.map((trace) => {
                const isSelected = trace.id === (selectedTrace?.id || "");
                return (
                  <button
                    key={trace.id}
                    onClick={() => setActiveTraceId(trace.id)}
                    className={`w-full text-left p-2 rounded text-xs transition-colors flex items-center justify-between border active:scale-[0.98] ${
                      isSelected
                        ? "bg-[#0c121e] border-emerald-500/50 text-emerald-300"
                        : "bg-transparent border-transparent hover:bg-slate-900/60 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      {trace.status === "success" ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                      ) : (
                        <XCircle className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                      )}
                      <span className="truncate font-semibold font-mono text-[11px]">{trace.toolName}</span>
                    </div>
                    <span className="text-[10px] text-slate-400 flex-shrink-0 ml-2 font-mono tabular-nums">
                      {trace.durationMs}ms
                    </span>
                  </button>
                );
              })
            )}
          </div>

          {/* Trace Execution Raw Code Viewer */}
          <div className="lg:col-span-8 p-3.5 overflow-y-auto bg-[#070b12] text-xs">
            {selectedTrace ? (
              <div className="space-y-3">
                {/* Header metrics */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-slate-800 text-[11px] text-slate-400">
                  <div className="flex items-center gap-2">
                    <span className="text-emerald-400 font-bold">tool:</span>
                    <span className="text-white font-semibold font-mono">
                      {selectedTrace.toolName}()
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-slate-400 text-[10px] font-mono">
                    {selectedTrace.executedAt && (
                      <span className="flex items-center gap-1 tabular-nums">
                        <Clock className="w-2.5 h-2.5" />
                        {selectedTrace.executedAt}
                      </span>
                    )}
                    <span className="text-emerald-400 font-semibold tabular-nums">
                      Duration: {selectedTrace.durationMs}ms
                    </span>
                  </div>
                </div>

                {/* Parameters & Response */}
                <div className="space-y-2.5">
                  <div>
                    <span className="text-slate-400 text-[10px] block mb-1 uppercase tracking-wider">
                      Invocation Arguments:
                    </span>
                    <pre className="p-2.5 rounded bg-[#090e18] border border-slate-800 text-emerald-400/90 text-[11px] overflow-x-auto whitespace-pre-wrap leading-relaxed font-mono">
                      {JSON.stringify(selectedTrace.input, null, 2)}
                    </pre>
                  </div>

                  <div>
                    <span className="text-slate-400 text-[10px] block mb-1 uppercase tracking-wider">
                      Result Payload:
                    </span>
                    <pre className="p-2.5 rounded bg-[#090e18] border border-slate-800 text-cyan-300 text-[11px] overflow-x-auto whitespace-pre-wrap leading-relaxed font-mono">
                      {JSON.stringify(selectedTrace.output, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-center py-10 font-mono text-xs">
                Select a tool execution from the list to inspect arguments and response payload.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
