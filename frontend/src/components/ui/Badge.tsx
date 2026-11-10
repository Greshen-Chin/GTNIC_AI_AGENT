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
    | "false_positive"
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
    sm: "text-[10px] px-1.5 py-0.5 font-mono",
    md: "text-[11px] px-2 py-0.5 font-mono",
    lg: "text-xs px-2.5 py-1 font-mono font-medium",
  };

  const variantClasses = {
    default: "bg-slate-900 text-slate-300 border-slate-700/60",
    critical: "bg-rose-950/70 text-rose-300 border-rose-600/40 font-semibold shadow-[0_0_8px_rgba(244,63,94,0.15)]",
    high: "bg-orange-950/70 text-orange-300 border-orange-600/40 font-semibold",
    medium: "bg-amber-950/60 text-amber-300 border-amber-600/40",
    low: "bg-sky-950/50 text-sky-300 border-sky-600/30",
    malicious: "bg-rose-950/80 text-rose-200 border-rose-600/50 font-semibold",
    suspicious: "bg-amber-950/70 text-amber-300 border-amber-500/50 font-semibold",
    benign: "bg-emerald-950/70 text-emerald-300 border-emerald-500/50",
    review: "bg-indigo-950/70 text-indigo-300 border-indigo-600/40",
    active: "bg-emerald-950/80 text-emerald-300 border-emerald-600/50",
    mitigated: "bg-slate-900 text-slate-400 border-slate-700/60",
    false_positive: "bg-slate-900 text-slate-400 border-slate-700/60 line-through decoration-slate-500",
    outline: "bg-transparent text-slate-300 border-slate-800",
  };

  const dotClasses = {
    critical: "bg-rose-500 shadow-[0_0_5px_#f43f5e]",
    high: "bg-orange-400 shadow-[0_0_5px_#fb923c]",
    medium: "bg-amber-400",
    low: "bg-sky-400",
    malicious: "bg-rose-500 shadow-[0_0_6px_#f43f5e]",
    suspicious: "bg-amber-400",
    benign: "bg-emerald-400",
    review: "bg-indigo-400",
    active: "bg-emerald-400 animate-pulse",
    mitigated: "bg-slate-400",
    false_positive: "bg-slate-500",
    default: "bg-slate-400",
    outline: "bg-slate-400",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded border tracking-wide uppercase select-none",
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {dot && <span className={cn("h-1.5 w-1.5 rounded-full inline-block flex-shrink-0", dotClasses[variant])} />}
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
    Malicious: { variant: "malicious", label: "Malicious" },
    Suspicious: { variant: "suspicious", label: "Suspicious" },
    Benign: { variant: "benign", label: "Benign" },
    "Under Review": { variant: "review", label: "Under Review" },
  };

  const item = map[verdict] || { variant: "default", label: verdict };

  return (
    <Badge variant={item.variant} dot>
      <span>{item.label}</span>
      {confidence !== undefined && (
        <span className="opacity-75 font-normal ml-0.5 tabular-nums">
          ({Math.round(confidence * 100)}%)
        </span>
      )}
    </Badge>
  );
}

export function StatusBadge({ status }: { status: IncidentStatus }) {
  const map: Record<IncidentStatus, { variant: "active" | "mitigated" | "false_positive" | "default"; label: string }> = {
    Active: { variant: "active", label: "Active Threat" },
    Investigating: { variant: "default", label: "Investigating" },
    Mitigated: { variant: "mitigated", label: "Approved" },
    "False Positive": { variant: "false_positive", label: "False Positive" },
  };

  const item = map[status] || { variant: "default", label: status };

  return (
    <Badge variant={item.variant} dot={status === "Active"}>
      {item.label}
    </Badge>
  );
}
