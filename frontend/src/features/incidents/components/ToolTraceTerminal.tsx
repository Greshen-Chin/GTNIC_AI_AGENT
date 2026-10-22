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
  Play,
  Clock,
  Code2,
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
    <div className="rounded-xl border border-slate-800 bg-black shadow-2xl overflow-hidden font-mono mt-6">
      {/* Terminal Title Bar */}
      <div className="bg-zinc-950 border-b border-zinc-800 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* OS Window Dots */}
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block" />
            <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block" />
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block" />
          </div>

          <div className="flex items-center gap-2 text-xs text-zinc-300 ml-2">
            <TerminalIcon className="w-4 h-4 text-emerald-400" />
            <span className="text-emerald-400 font-bold">soc-agent@kernel:</span>
            <span className="text-zinc-400">~/audit-traces/execution.log</span>
            <span className="text-[10px] px-1.5 py-0.2 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">
              {toolTraces.length} TOOLS EXECUTED
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isOpen && selectedTrace && (
            <button
              onClick={handleCopyJson}
              className="flex items-center gap-1 text-[11px] px-2.5 py-1 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 transition-colors"
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
            className="flex items-center gap-1 text-xs text-zinc-400 hover:text-white px-2 py-1 rounded hover:bg-zinc-800 transition-colors"
          >
            {isOpen ? (
              <>
                <span>Collapse</span>
                <ChevronUp className="w-4 h-4" />
              </>
            ) : (
              <>
                <span>Expand Terminal</span>
                <ChevronDown className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Terminal Body */}
      {isOpen && (
        <div className="grid grid-cols-1 lg:grid-cols-12 min-h-[320px] max-h-[460px] divide-y lg:divide-y-0 lg:divide-x divide-zinc-800 bg-black">
          {/* Tool List Sidebar */}
          <div className="lg:col-span-4 p-3 overflow-y-auto space-y-1.5 bg-zinc-950/50">
            <div className="text-[10px] text-zinc-500 uppercase px-2 py-1 tracking-wider">
              Autonomous Tool Sequence
            </div>
            {toolTraces.map((trace) => {
              const isSelected = trace.id === (selectedTrace?.id || "");
              return (
                <button
                  key={trace.id}
                  onClick={() => setActiveTraceId(trace.id)}
                  className={`w-full text-left p-2.5 rounded text-xs transition-all flex items-center justify-between border ${
                    isSelected
                      ? "bg-zinc-900 border-emerald-500/60 text-emerald-300 shadow-[0_0_10px_rgba(16,185,129,0.15)]"
                      : "bg-black/40 border-zinc-850 hover:bg-zinc-900/60 text-zinc-400 hover:text-zinc-200"
                  }`}
                >
                  <div className="flex items-center gap-2 truncate">
                    {trace.status === "success" ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                    ) : (
                      <XCircle className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                    )}
                    <span className="truncate font-semibold">{trace.toolName}</span>
                  </div>
                  <span className="text-[10px] text-zinc-500 flex-shrink-0 ml-2">
                    {trace.durationMs}ms
                  </span>
                </button>
              );
            })}
          </div>

          {/* Trace Execution Raw Code Viewer */}
          <div className="lg:col-span-8 p-4 overflow-y-auto bg-black text-xs">
            {selectedTrace ? (
              <div className="space-y-3">
                {/* Header metrics */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-zinc-800 text-[11px] text-zinc-400">
                  <div className="flex items-center gap-2">
                    <span className="text-emerald-400 font-bold">$ call</span>
                    <span className="text-white font-semibold">
                      {selectedTrace.toolName}()
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-zinc-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {selectedTrace.executedAt}
                    </span>
                    <span className="text-emerald-400 font-semibold">
                      Execution: {selectedTrace.durationMs}ms
                    </span>
                  </div>
                </div>

                {/* JSON Tree */}
                <div className="space-y-2">
                  <div>
                    <span className="text-zinc-500 text-[11px] block mb-1">
                      // Input Arguments:
                    </span>
                    <pre className="p-3 rounded bg-zinc-950 border border-zinc-800/80 text-emerald-400/90 text-[11px] overflow-x-auto whitespace-pre-wrap leading-relaxed">
                      {JSON.stringify(selectedTrace.input, null, 2)}
                    </pre>
                  </div>

                  <div>
                    <span className="text-zinc-500 text-[11px] block mb-1">
                      // Agent Response Output:
                    </span>
                    <pre className="p-3 rounded bg-zinc-950 border border-zinc-800/80 text-cyan-300 text-[11px] overflow-x-auto whitespace-pre-wrap leading-relaxed">
                      {JSON.stringify(selectedTrace.output, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-zinc-600 text-center py-12">
                Select a tool trace to view execution payload.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
