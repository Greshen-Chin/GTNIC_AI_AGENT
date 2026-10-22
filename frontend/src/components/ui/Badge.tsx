import React from "react";
import { cn } from "@/lib/utils";
import { SeverityLevel, AIVerdict, IncidentStatus } from "@/features/incidents/types";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?:
    | "default"
    | "critical"
    | "high"
    | "medium"
    | "low"
    | "malicious"
    | "suspicious"
    | "benign"
    | "review"
    | "active"
    | "mitigated"
    | "outline";
  size?: "sm" | "md" | "lg";
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "default",
  size = "md",
  dot = false,
  className,
  ...props
}) => {
  const sizeClasses = {
    sm: "text-[11px] px-2 py-0.5 font-mono",
    md: "text-xs px-2.5 py-1 font-mono",
    lg: "text-sm px-3 py-1.5 font-mono font-medium",
  };

  const variantClasses = {
    default: "bg-slate-800 text-slate-300 border-slate-700/60",
    critical: "bg-red-950/70 text-red-400 border-red-700/60 shadow-[0_0_10px_rgba(239,68,68,0.2)]",
    high: "bg-orange-950/70 text-orange-400 border-orange-700/60 shadow-[0_0_10px_rgba(249,115,22,0.15)]",
    medium: "bg-amber-950/60 text-amber-300 border-amber-600/50",
    low: "bg-cyan-950/60 text-cyan-300 border-cyan-700/50",
    malicious: "bg-rose-950/80 text-rose-300 border-rose-600/70 font-semibold shadow-[0_0_12px_rgba(244,63,94,0.25)]",
    suspicious: "bg-amber-950/70 text-amber-300 border-amber-500/60 font-semibold",
    benign: "bg-emerald-950/70 text-emerald-300 border-emerald-500/60 shadow-[0_0_10px_rgba(16,185,129,0.2)]",
    review: "bg-indigo-950/70 text-indigo-300 border-indigo-600/50",
    active: "bg-emerald-950/80 text-emerald-400 border-emerald-600/60",
    mitigated: "bg-slate-800/80 text-slate-400 border-slate-700/60",
    outline: "bg-transparent text-slate-300 border-slate-700",
  };

  const dotClasses = {
    critical: "bg-red-500 shadow-[0_0_6px_#ef4444]",
    high: "bg-orange-500 shadow-[0_0_6px_#f97316]",
    medium: "bg-amber-400",
    low: "bg-cyan-400",
    malicious: "bg-rose-500 animate-pulse shadow-[0_0_6px_#f43f5e]",
    suspicious: "bg-amber-400 animate-pulse",
    benign: "bg-emerald-400 shadow-[0_0_6px_#10b981]",
    review: "bg-indigo-400",
    active: "bg-emerald-500 animate-pulse",
    mitigated: "bg-slate-500",
    default: "bg-slate-400",
    outline: "bg-slate-400",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded border tracking-wide uppercase transition-all duration-150 select-none",
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {dot && <span className={cn("h-1.5 w-1.5 rounded-full inline-block", dotClasses[variant])} />}
      {children}
    </span>
  );
};

export function SeverityBadge({ severity }: { severity: SeverityLevel }) {
  const map: Record<SeverityLevel, { variant: "critical" | "high" | "medium" | "low"; label: string }> = {
    Critical: { variant: "critical", label: "CRITICAL" },
    High: { variant: "high", label: "HIGH" },
    Medium: { variant: "medium", label: "MEDIUM" },
    Low: { variant: "low", label: "LOW" },
  };

  const item = map[severity] || { variant: "default", label: severity };

  return (
    <Badge variant={item.variant} dot>
      {item.label}
    </Badge>
  );
}

export function VerdictBadge({ verdict, confidence }: { verdict: AIVerdict; confidence?: number }) {
  const map: Record<AIVerdict, { variant: "malicious" | "suspicious" | "benign" | "review"; label: string }> = {
    Malicious: { variant: "malicious", label: "MALICIOUS" },
    Suspicious: { variant: "suspicious", label: "SUSPICIOUS" },
    Benign: { variant: "benign", label: "BENIGN" },
    "Under Review": { variant: "review", label: "UNDER REVIEW" },
  };

  const item = map[verdict] || { variant: "default", label: verdict };

  return (
    <Badge variant={item.variant} dot>
      <span>{item.label}</span>
      {confidence !== undefined && (
        <span className="opacity-80 font-normal ml-0.5">({Math.round(confidence * 100)}%)</span>
      )}
    </Badge>
  );
}

export function StatusBadge({ status }: { status: IncidentStatus }) {
  const map: Record<IncidentStatus, { variant: "active" | "mitigated" | "review" | "default"; label: string }> = {
    Active: { variant: "active", label: "ACTIVE" },
    Investigating: { variant: "review", label: "INVESTIGATING" },
    Mitigated: { variant: "mitigated", label: "MITIGATED" },
    "False Positive": { variant: "default", label: "FALSE POSITIVE" },
  };

  const item = map[status] || { variant: "default", label: status };

  return (
    <Badge variant={item.variant} size="sm" dot={status === "Active" || status === "Investigating"}>
      {item.label}
    </Badge>
  );
}
