"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Shield, Radio, Clock, ShieldAlert } from "lucide-react";

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
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/80 bg-[#070b12]/95 backdrop-blur-md">
      <div className="max-w-[1800px] mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        {/* Brand / SOC Triage Logo */}
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="flex items-center justify-center w-8 h-8 rounded bg-emerald-950/40 border border-emerald-500/40 text-emerald-400 group-hover:border-emerald-400 transition-colors">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs sm:text-sm font-bold tracking-tight text-white font-mono flex items-center gap-1.5">
                  GTNIC <span className="text-emerald-400">SOAR</span>
                </span>
                <span className="hidden sm:inline-flex text-[9px] uppercase font-mono px-1.5 py-0.2 rounded bg-slate-900 text-slate-400 border border-slate-800">
                  MONITOR
                </span>
              </div>
              <p className="text-[10px] text-slate-400 font-mono hidden md:block">
                Security Operations Center & Automated Threat Queue
              </p>
            </div>
          </Link>
        </div>

        {/* Operational Telemetry (Clean, no dummy LLM Core elements) */}
        <div className="flex items-center gap-2.5 sm:gap-4">
          {/* Stream / Correlation Status */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#0c121e] border border-slate-800 text-[11px] font-mono text-slate-300">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
            </span>
            <span className="text-slate-400 hidden sm:inline">Engine:</span>
            <span className="text-emerald-400 font-medium">Live Feed</span>
          </div>

          {/* Sync Polling Indicator */}
          <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#0c121e] border border-slate-800 text-[11px] font-mono text-slate-400">
            <Radio className="w-3 h-3 text-cyan-400" />
            <span>Telemetry: 3s Poll</span>
          </div>

          {/* UTC Clock with Tabular Numbers */}
          <div className="flex items-center gap-1.5 text-[11px] font-mono text-slate-400 px-2.5 py-1 rounded bg-black/50 border border-slate-800/80 tabular-nums">
            <Clock className="w-3 h-3 text-slate-500 hidden sm:inline" />
            <span>{currentTime || "2026-10-22 23:05:00 UTC"}</span>
          </div>

          {/* Navigation Link */}
          <Link
            href="/"
            className="text-[11px] font-mono px-3 py-1 rounded border border-slate-700/80 bg-slate-900/80 hover:bg-slate-800 text-slate-200 transition-colors flex items-center gap-1.5 active:scale-[0.97]"
          >
            <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
            <span>Queue</span>
          </Link>
        </div>
      </div>
    </header>
  );
};
