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
    none: "border-slate-800/80 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.5)]",
    emerald: "border-emerald-500/40 shadow-[0_0_20px_rgba(16,185,129,0.1)]",
    rose: "border-rose-500/40 shadow-[0_0_20px_rgba(244,63,94,0.1)]",
    cyan: "border-cyan-500/40 shadow-[0_0_20px_rgba(6,182,212,0.1)]",
    orange: "border-orange-500/40 shadow-[0_0_20px_rgba(249,115,22,0.1)]",
  };

  return (
    <div
      className={cn(
        "rounded-lg bg-slate-900/60 backdrop-blur-md border text-slate-200 transition-colors duration-200",
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
        "px-5 py-3.5 border-b border-slate-800/80 flex items-center justify-between",
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
        "text-sm font-semibold tracking-wide text-slate-100 flex items-center gap-2",
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
    <div className={cn("p-5", className)} {...props}>
      {children}
    </div>
  );
};
