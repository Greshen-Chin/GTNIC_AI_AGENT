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
  Cpu,
  Info,
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

  const handleApprove = async () => {
    setIsApproving(true);
    setActionFeedback(null);
    try {
      await onMitigate("Approved");
      setActionFeedback("Mitigation approval recorded.");
    } catch {
      setActionFeedback("Failed to record mitigation approval.");
    } finally {
      setIsApproving(false);
    }
  };

  const handleReject = async () => {
    setIsRejecting(true);
    setActionFeedback(null);
    try {
      await onMitigate("Rejected");
      setActionFeedback("Incident marked as False Positive.");
    } catch {
      setActionFeedback("Failed to update status.");
    } finally {
      setIsRejecting(false);
    }
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/80 backdrop-blur-md p-6 mb-6 shadow-xl">
      {/* Top breadcrumb & metadata */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-emerald-400 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Back to Incident Queue
          </Link>
          <span className="text-slate-600">/</span>
          <span className="text-xs font-mono text-emerald-400 font-semibold">
            {incident.id}
          </span>
          <StatusBadge status={incident.status} />
        </div>

        <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
          <div className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-slate-500" />
            <span>Detected: {formatDateTime(incident.timestamp)}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-emerald-400" />
            <span>Agent Confidence: {(incident.aiConfidence * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* Main Title, Target IP, Severity and Action Buttons */}
      <div className="mt-4 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2.5">
            <SeverityBadge severity={incident.severity} />
            <VerdictBadge
              verdict={incident.aiVerdict}
              confidence={incident.aiConfidence}
            />
          </div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
            {incident.title}
          </h1>
          <p className="text-sm text-slate-400 max-w-4xl">{incident.description}</p>

          {/* Quick Target/Source Network Pill */}
          <div className="flex flex-wrap items-center gap-4 pt-1 text-xs font-mono">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-950 border border-slate-800">
              <Globe className="w-3.5 h-3.5 text-rose-400" />
              <span className="text-slate-400">Source:</span>
              <span className="text-slate-200 font-semibold">{incident.sourceIp}</span>
              {incident.sourceCountry && (
                <span className="text-slate-500 text-[11px]">({incident.sourceCountry})</span>
              )}
            </div>

            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-950 border border-slate-800">
              <Server className="w-3.5 h-3.5 text-cyan-400" />
              <span className="text-slate-400">Target IP:</span>
              <span className="text-slate-200 font-semibold">{incident.targetIp}</span>
              <span className="text-cyan-400 text-[11px]">({incident.targetAsset})</span>
            </div>
          </div>
        </div>

        {/* Big Action Buttons */}
        <div className="flex flex-col sm:flex-row lg:flex-col gap-3 min-w-[280px]">
          {incident.mitigationActionTaken ? (
            <div
              className={`p-4 rounded-lg border text-center ${
                incident.mitigationActionTaken === "Approved"
                  ? "bg-emerald-950/50 border-emerald-500/60 text-emerald-300"
                  : "bg-slate-900 border-slate-700 text-slate-300"
              }`}
            >
              <div className="flex items-center justify-center gap-2 font-mono text-sm font-bold">
                {incident.mitigationActionTaken === "Approved" ? (
                  <>
                    <CheckCircle className="w-4 h-4 text-emerald-400" />
                    MITIGATION ENFORCED
                  </>
                ) : (
                  <>
                    <XCircle className="w-4 h-4 text-slate-400" />
                    REJECTED (FALSE POSITIVE)
                  </>
                )}
              </div>
              <p className="text-xs font-mono text-slate-400 mt-1">
                Audit trail updated by operator
              </p>
            </div>
          ) : (
            <>
              <Button
                variant="emerald"
                size="lg"
                isLoading={isApproving}
                onClick={handleApprove}
                leftIcon={<CheckCircle className="w-4 h-4 text-emerald-950" />}
                className="w-full text-sm font-bold"
              >
                Approve Mitigation
              </Button>
              <Button
                variant="destructive"
                size="lg"
                isLoading={isRejecting}
                onClick={handleReject}
                leftIcon={<XCircle className="w-4 h-4 text-rose-300" />}
                className="w-full text-sm font-semibold"
              >
                Reject (False Positive)
              </Button>
            </>
          )}

          {actionFeedback && (
            <div className="p-2 rounded bg-slate-950 border border-slate-800 text-[11px] font-mono text-emerald-400 flex items-center gap-1.5 animate-fadeIn">
              <Info className="w-3.5 h-3.5 flex-shrink-0" />
              <span>{actionFeedback}</span>
            </div>
          )}
        </div>
      </div>

      {/* Suggested Mitigation Banner */}
      <div className="mt-5 p-3.5 rounded-lg bg-emerald-950/20 border border-emerald-500/30 flex items-start gap-3">
        <ShieldAlert className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
        <div className="text-xs">
          <span className="font-mono font-semibold text-emerald-300 mr-2 uppercase tracking-wide">
            AI Recommended Playbook:
          </span>
          <span className="text-slate-300">{incident.suggestedMitigation}</span>
        </div>
      </div>
    </div>
  );
};
