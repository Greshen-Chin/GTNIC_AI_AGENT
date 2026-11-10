"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  ShieldAlert,
  Server,
  Globe,
  Clock,
  ShieldCheck,
  Info,
  Check,
  Copy,
  Sparkles,
  Cpu,
} from "lucide-react";
import { Incident } from "../types";
import { SeverityBadge, VerdictBadge, StatusBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDateTime } from "@/lib/utils";

interface IncidentHeaderProps {
  incident: Incident;
  onMitigate: (action: "Approved" | "Rejected") => Promise<void>;
}

export const IncidentHeader: React.FC<IncidentHeaderProps> = ({
  incident,
  onMitigate,
}) => {
  const [isApproving, setIsApproving] = useState(false);
  const [isRejecting, setIsRejecting] = useState(false);
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState(false);

  const handleCopyId = () => {
    navigator.clipboard.writeText(incident.id);
    setCopiedId(true);
    setTimeout(() => setCopiedId(false), 2000);
  };

  const handleApprove = async () => {
    setIsApproving(true);
    setActionFeedback(null);
    try {
      await onMitigate("Approved");
      setActionFeedback("Mitigation approval recorded. Execution has not been verified.");
    } catch {
      setActionFeedback("Failed to record mitigation decision.");
    } finally {
      setIsApproving(false);
    }
  };

  const handleReject = async () => {
    setIsRejecting(true);
    setActionFeedback(null);
    try {
      await onMitigate("Rejected");
      setActionFeedback("Incident marked as False Positive. Alarm closed.");
    } catch {
      setActionFeedback("Failed to update incident status.");
    } finally {
      setIsRejecting(false);
    }
  };

  return (
    <div className="rounded-lg border border-slate-800/80 bg-[#0c121e]/90 backdrop-blur-md p-4 sm:p-5 mb-5 shadow-xl font-mono">
      {/* Top breadcrumb & operational metadata */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3.5 border-b border-slate-800/70">
        <div className="flex items-center gap-2 text-xs">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-slate-400 hover:text-emerald-400 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Triage Queue</span>
          </Link>
          <span className="text-slate-600">/</span>
          <button
            onClick={handleCopyId}
            title="Click to copy incident ID"
            className="inline-flex items-center gap-1 text-emerald-400 hover:text-emerald-300 font-semibold transition-colors"
          >
            <span>{incident.id}</span>
            {copiedId ? (
              <Check className="w-3 h-3 text-emerald-400" />
            ) : (
              <Copy className="w-3 h-3 opacity-60 hover:opacity-100" />
            )}
          </button>
          <StatusBadge status={incident.status} />
        </div>

        <div className="flex items-center gap-3 text-[11px] text-slate-400">
          <div className="flex items-center gap-1.5">
            <Clock className="w-3 h-3 text-slate-500" />
            <span>Detected:</span>
            <span className="text-slate-300 tabular-nums">{formatDateTime(incident.timestamp)}</span>
          </div>
          <div className="hidden sm:flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span>Confidence:</span>
            <span className="text-indigo-300 font-semibold tabular-nums">
              {Math.round(incident.aiConfidence * 100)}%
            </span>
          </div>
        </div>
      </div>

      {/* Main Title, Target IP, Severity, and Action Controls */}
      <div className="mt-3.5 flex flex-col lg:flex-row lg:items-start justify-between gap-5">
        <div className="space-y-2.5 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <SeverityBadge severity={incident.severity} />
            <VerdictBadge
              verdict={incident.aiVerdict}
              confidence={incident.llmModel === "investigation-pending" ? undefined : incident.aiConfidence}
            />
            {incident.llmModel && (
              incident.llmModel.toLowerCase().includes("gemini") ? (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[11px] font-mono font-medium bg-purple-950/60 border border-purple-500/40 text-purple-300">
                  <Sparkles className="w-3 h-3 text-purple-400" />
                  <span>Agent: {incident.llmModel}</span>
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded text-[11px] font-mono font-medium bg-amber-950/60 border border-amber-500/40 text-amber-300">
                  <Cpu className="w-3 h-3 text-amber-400" />
                  <span>Engine: {incident.llmModel}</span>
                </span>
              )
            )}
          </div>
          <h1 className="text-lg sm:text-xl font-bold tracking-tight text-white font-sans">
            {incident.title}
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed font-sans">
            {incident.description}
          </p>

          {/* Adversary & Asset Target Telemetry */}
          <div className="flex flex-wrap items-center gap-2.5 pt-1 text-xs">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#070b12] border border-slate-800">
              <Globe className="w-3.5 h-3.5 text-rose-400" />
              <span className="text-slate-400">Adversary IP:</span>
              <span className="text-slate-200 font-semibold">{incident.sourceIp}</span>
              {incident.sourceCountry && (
                <span className="text-slate-400 text-[11px]">({incident.sourceCountry})</span>
              )}
            </div>

            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#070b12] border border-slate-800">
              <Server className="w-3.5 h-3.5 text-cyan-400" />
              <span className="text-slate-400">Target Asset:</span>
              <span className="text-slate-200 font-semibold">{incident.targetAsset}</span>
              <span className="text-cyan-400 text-[11px]">[{incident.targetIp}]</span>
            </div>
          </div>
        </div>

        {/* Triage Decision Control Panel */}
        <div className="flex flex-col gap-2.5 min-w-[300px] sm:min-w-[340px] self-stretch lg:self-start">
          {incident.mitigationActionTaken ? (
            <div
              className={`p-4 rounded-lg border text-center ${
                incident.mitigationActionTaken === "Approved"
                  ? "bg-emerald-950/40 border-emerald-500/50 text-emerald-300"
                  : "bg-slate-900/80 border-slate-700/80 text-slate-300"
              }`}
            >
              <div className="flex items-center justify-center gap-2 text-sm font-bold uppercase tracking-wide">
                {incident.mitigationActionTaken === "Approved" ? (
                  <>
                    <CheckCircle className="w-5 h-5 text-emerald-400" />
                    MITIGATION APPROVED
                  </>
                ) : (
                  <>
                    <XCircle className="w-5 h-5 text-slate-400" />
                    FALSE POSITIVE MARKED
                  </>
                )}
              </div>
              <p className="text-xs text-slate-400 mt-1.5 font-mono">
                Triage decision locked in SOAR audit trail
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-2.5">
              <Button
                variant="primary"
                size="xl"
                isLoading={isApproving}
                onClick={handleApprove}
                leftIcon={<CheckCircle className="w-5 h-5 text-slate-950" />}
                className="w-full text-sm font-extrabold uppercase tracking-wide shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_25px_rgba(16,185,129,0.45)]"
              >
                Approve Mitigation
              </Button>
              <Button
                variant="destructive"
                size="lg"
                isLoading={isRejecting}
                onClick={handleReject}
                leftIcon={<XCircle className="w-4.5 h-4.5 text-rose-300" />}
                className="w-full text-xs sm:text-sm font-bold tracking-wide"
              >
                Reject (False Positive)
              </Button>
            </div>
          )}

          {actionFeedback && (
            <div className="p-2 rounded bg-[#070b12] border border-slate-800 text-[11px] text-emerald-400 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 flex-shrink-0" />
              <span>{actionFeedback}</span>
            </div>
          )}
        </div>
      </div>

      {/* Suggested Mitigation Banner */}
      <div className="mt-4 p-3 rounded bg-emerald-950/20 border border-emerald-500/30 flex items-start gap-2.5">
        <ShieldAlert className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
        <div className="text-xs">
          <span className="font-semibold text-emerald-300 mr-2 uppercase tracking-wide">
            Suggested Mitigation:
          </span>
          <span className="text-slate-300 font-sans">{incident.suggestedMitigation}</span>
        </div>
      </div>
    </div>
  );
};
