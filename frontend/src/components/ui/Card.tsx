import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glow?: "emerald" | "rose" | "cyan" | "orange" | "none";
}

export const Card: React.FC<CardProps> = ({
  className,
  children,
  glow = "none",
  ...props
}) => {
  const glowClasses = {
    none: "border-slate-800/80 shadow-[0_2px_12px_rgba(0,0,0,0.4)]",
    emerald: "border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.08)]",
    rose: "border-rose-500/30 shadow-[0_0_15px_rgba(244,63,94,0.08)]",
    cyan: "border-cyan-500/30 shadow-[0_0_15px_rgba(6,182,212,0.08)]",
    orange: "border-orange-500/30 shadow-[0_0_15px_rgba(249,115,22,0.08)]",
  };

  return (
    <div
      className={cn(
        "rounded-lg bg-[#0c121e]/90 backdrop-blur-md border text-slate-200 transition-colors duration-150",
        glowClasses[glow],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div
      className={cn(
        "px-4 py-3 border-b border-slate-800/70 bg-[#090e18]/80 flex items-center justify-between",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({
  className,
  children,
  ...props
}) => {
  return (
    <h3
      className={cn(
        "text-xs font-semibold tracking-wider uppercase text-slate-200 flex items-center gap-2 font-mono",
        className
      )}
      {...props}
    >
      {children}
    </h3>
  );
};

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={cn("p-4 sm:p-5", className)} {...props}>
      {children}
    </div>
  );
};
