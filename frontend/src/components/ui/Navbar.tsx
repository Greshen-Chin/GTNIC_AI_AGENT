"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ShieldAlert, Activity, Cpu, Bell, Terminal, RefreshCw } from "lucide-react";
import { Badge } from "./Badge";

export const Navbar: React.FC = () => {
  const [currentTime, setCurrentTime] = useState<string>("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(
        now.toISOString().replace("T", " ").substring(0, 19) + " UTC"
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
      <div className="max-w-[1720px] mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand / Title */}
        <div className="flex items-center gap-4">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-lg bg-emerald-950/60 border border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.25)] group-hover:border-emerald-400 transition-all">
              <ShieldAlert className="w-5 h-5 text-emerald-400 group-hover:scale-105 transition-transform" />
              <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-sm sm:text-base font-bold tracking-tight text-white flex items-center gap-2">
                  GTNIC <span className="text-emerald-400 font-mono">SOC AGENT</span>
                </span>
                <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-600/40">
                  v2.4-AUTONOMOUS
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Autonomous Security Operations Center & Real-Time Incident Orchestration
              </p>
            </div>
          </Link>
        </div>

        {/* System Status Indicators */}
        <div className="flex items-center gap-4">
          {/* Agent Status Badge */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900 border border-slate-800">
            <span className="text-xs font-mono text-slate-400">Status:</span>
            <span className="inline-flex items-center gap-1.5 text-xs font-mono font-semibold text-emerald-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#10b981] animate-pulse" />
              Active
            </span>
          </div>

          {/* Engine Load Telemetry */}
          <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900/60 border border-slate-800 text-xs font-mono text-slate-400">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" />
            <span>LLM Core:</span>
            <span className="text-cyan-300 font-medium">GT-Reason-3.5</span>
          </div>

          {/* Polling / Heartbeat indicator */}
          <div className="hidden lg:flex items-center gap-2 text-xs font-mono text-slate-500">
            <RefreshCw className="w-3 h-3 text-emerald-500 animate-[spin_6s_linear_infinite]" />
            <span>Auto-Poll: 3s</span>
          </div>

          {/* UTC Clock */}
          <div className="hidden sm:block text-xs font-mono text-slate-400 px-3 py-1.5 rounded bg-black/40 border border-slate-800/80">
            {currentTime || "2026-10-22 23:05:00 UTC"}
          </div>

          {/* Navigation Links */}
          <Link
            href="/"
            className="text-xs font-mono px-3 py-1.5 rounded border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors"
          >
            Incident Queue
          </Link>
        </div>
      </div>
    </header>
  );
};
