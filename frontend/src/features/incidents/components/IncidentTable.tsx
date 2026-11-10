"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Search,
  Clock,
  Globe,
  Radio,
  ArrowRight,
  Shield,
  X,
  Server,
} from "lucide-react";
import { Incident } from "../types";
import { SeverityBadge, VerdictBadge, StatusBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDateTime } from "@/lib/utils";

interface IncidentTableProps {
  incidents: Incident[];
  isLoading: boolean;
  isValidating: boolean;
}

export const IncidentTable: React.FC<IncidentTableProps> = ({
  incidents,
  isLoading,
  isValidating,
}) => {
  const router = useRouter();
  const searchInputRef = React.useRef<HTMLInputElement>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [severityFilter, setSeverityFilter] = useState<string>("ALL");
  const [verdictFilter, setVerdictFilter] = useState<string>("ALL");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (
        e.key === "/" &&
        document.activeElement?.tagName !== "INPUT" &&
        document.activeElement?.tagName !== "TEXTAREA"
      ) {
        e.preventDefault();
        searchInputRef.current?.focus();
      } else if (e.key === "Escape" && document.activeElement === searchInputRef.current) {
        searchInputRef.current?.blur();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const filteredIncidents = incidents.filter((incident) => {
    const matchesSearch =
      incident.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      incident.sourceIp.includes(searchQuery) ||
      incident.targetIp.includes(searchQuery) ||
      incident.targetAsset.toLowerCase().includes(searchQuery.toLowerCase()) ||
      incident.id.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesSeverity =
      severityFilter === "ALL" || incident.severity === severityFilter;

    const matchesVerdict =
      verdictFilter === "ALL" || incident.aiVerdict === verdictFilter;

    const matchesStatus =
      statusFilter === "ALL" || incident.status === statusFilter;

    return matchesSearch && matchesSeverity && matchesVerdict && matchesStatus;
  });

  return (
    <div className="rounded-lg border border-slate-800/80 bg-[#0c121e]/90 backdrop-blur-md overflow-hidden shadow-xl">
      {/* Table Control Bar */}
      <div className="p-3 sm:p-4 border-b border-slate-800/80 flex flex-col md:flex-row gap-3 justify-between items-stretch md:items-center bg-[#090e18]/80">
        <div className="flex flex-wrap items-center gap-2.5 flex-1">
          {/* Search Box */}
          <div className="relative flex-1 min-w-[220px] max-w-md">
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              ref={searchInputRef}
              type="text"
              placeholder="Search IP, asset, title, or ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[#070b12] border border-slate-800 rounded pl-10 pr-9 py-2 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
            />
            {searchQuery ? (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 p-0.5"
                aria-label="Clear search"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            ) : (
              <kbd className="hidden sm:inline-block absolute right-2.5 top-1/2 -translate-y-1/2 text-[9px] font-mono px-1 py-0.2 rounded bg-slate-900 border border-slate-800 text-slate-500 pointer-events-none">
                /
              </kbd>
            )}
          </div>

          {/* Quick Filters */}
          <div className="flex items-center gap-2">
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              aria-label="Filter by Severity"
              className="bg-[#070b12] border border-slate-800 rounded px-2.5 py-1.5 text-[11px] font-mono text-slate-300 focus:outline-none focus:border-emerald-500/60"
            >
              <option value="ALL">Severity: All</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>

            <select
              value={verdictFilter}
              onChange={(e) => setVerdictFilter(e.target.value)}
              aria-label="Filter by AI Verdict"
              className="bg-[#070b12] border border-slate-800 rounded px-2.5 py-1.5 text-[11px] font-mono text-slate-300 focus:outline-none focus:border-emerald-500/60"
            >
              <option value="ALL">Verdict: All</option>
              <option value="Malicious">Malicious</option>
              <option value="Suspicious">Suspicious</option>
              <option value="Benign">Benign</option>
              <option value="Under Review">Under Review</option>
            </select>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              aria-label="Filter by Status"
              className="bg-[#070b12] border border-slate-800 rounded px-2.5 py-1.5 text-[11px] font-mono text-slate-300 focus:outline-none focus:border-emerald-500/60"
            >
              <option value="ALL">Status: All</option>
              <option value="Active">Active Threat</option>
              <option value="Mitigated">Approved</option>
              <option value="False Positive">False Positive</option>
            </select>
          </div>
        </div>

        {/* Live Auto-Polling Status Badge */}
        <div className="flex items-center justify-between md:justify-end gap-3 text-[11px] font-mono">
          <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-[#070b12] border border-slate-800 text-slate-400">
            <Radio
              className={`w-3 h-3 ${
                isValidating ? "text-emerald-400 animate-pulse" : "text-slate-500"
              }`}
            />
            <span>
              {isValidating ? "Syncing..." : "Feed Synced"}
            </span>
          </div>
          <span className="text-slate-400 tabular-nums">
            {filteredIncidents.length} of {incidents.length} alerts
          </span>
        </div>
      </div>

      {/* Main Incident Data Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800/90 bg-[#070b12]/90 text-[10px] font-mono uppercase tracking-wider text-slate-400">
              <th className="py-2.5 px-4 font-medium">Timestamp (UTC)</th>
              <th className="py-2.5 px-4 font-medium">Incident & Target Asset</th>
              <th className="py-2.5 px-4 font-medium">Source / Origin</th>
              <th className="py-2.5 px-4 font-medium">AI Verdict</th>
              <th className="py-2.5 px-4 font-medium">Severity</th>
              <th className="py-2.5 px-4 font-medium">Status</th>
              <th className="py-2.5 px-4 font-medium text-right">Triage</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs text-slate-300">
            {isLoading && incidents.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-14 text-center text-slate-500 font-mono">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <div className="w-5 h-5 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                    <span className="text-xs">Loading real-time SOC incident queue...</span>
                  </div>
                </td>
              </tr>
            ) : filteredIncidents.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-14 text-center text-slate-500 font-mono">
                  <div className="flex flex-col items-center justify-center gap-1">
                    <Shield className="w-6 h-6 text-slate-600 mb-1" />
                    <span className="text-xs">No incidents match current filter criteria.</span>
                    <button
                      onClick={() => {
                        setSearchQuery("");
                        setSeverityFilter("ALL");
                        setVerdictFilter("ALL");
                        setStatusFilter("ALL");
                      }}
                      className="text-[11px] text-emerald-400 hover:underline mt-1"
                    >
                      Reset filters
                    </button>
                  </div>
                </td>
              </tr>
            ) : (
              filteredIncidents.map((incident) => (
                <tr
                  key={incident.id}
                  onClick={() => router.push(`/incidents/${incident.id}`)}
                  className="hover:bg-slate-800/35 transition-colors duration-150 group cursor-pointer"
                >
                  {/* Timestamp */}
                  <td className="py-3 px-4 font-mono text-[11px] text-slate-400 whitespace-nowrap tabular-nums">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3 h-3 text-slate-500" />
                      <span>{formatDateTime(incident.timestamp)}</span>
                    </div>
                  </td>

                  {/* Title & Target Asset */}
                  <td className="py-3 px-4 max-w-sm">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-mono text-[11px] text-emerald-400 font-semibold group-hover:underline">
                        {incident.id}
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono flex items-center gap-1">
                        <Server className="w-2.5 h-2.5 text-slate-400" />
                        {incident.targetAsset}
                      </span>
                      {incident.llmModel && incident.llmModel.toLowerCase().includes("gemini") ? (
                        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-mono bg-purple-950/60 border border-purple-500/30 text-purple-300">
                          Gemini
                        </span>
                      ) : incident.llmModel === "local-triage" ? (
                        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[9px] font-mono bg-amber-950/60 border border-amber-500/30 text-amber-300">
                          Local
                        </span>
                      ) : null}
                    </div>
                    <div className="font-medium text-slate-100 group-hover:text-emerald-300 transition-colors line-clamp-1 text-xs">
                      {incident.title}
                    </div>
                  </td>

                  {/* Source IP */}
                  <td className="py-3 px-4 font-mono text-xs whitespace-nowrap">
                    <div className="flex items-center gap-1.5 text-slate-200">
                      <Globe className="w-3 h-3 text-slate-500" />
                      <span className="bg-[#070b12] px-1.5 py-0.5 rounded border border-slate-800 text-cyan-300 text-[11px]">
                        {incident.sourceIp}
                      </span>
                    </div>
                    {incident.sourceCountry && (
                      <div className="text-[10px] text-slate-400 mt-0.5 pl-4.5 truncate max-w-[160px]">
                        {incident.sourceCountry}
                      </div>
                    )}
                  </td>

                  {/* AI Verdict */}
                  <td className="py-3 px-4 whitespace-nowrap">
                    <VerdictBadge
                      verdict={incident.aiVerdict}
                      confidence={incident.llmModel === "investigation-pending" ? undefined : incident.aiConfidence}
                    />
                  </td>

                  {/* Severity */}
                  <td className="py-3 px-4 whitespace-nowrap">
                    <SeverityBadge severity={incident.severity} />
                  </td>

                  {/* Status */}
                  <td className="py-3 px-4 whitespace-nowrap">
                    <StatusBadge status={incident.status} />
                  </td>

                  {/* Investigate Action */}
                  <td className="py-3 px-4 text-right whitespace-nowrap">
                    <Link
                      href={`/incidents/${incident.id}`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      <Button
                        size="sm"
                        variant="secondary"
                        rightIcon={
                          <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform duration-150" />
                        }
                        className="group-hover:border-emerald-500/50 group-hover:text-emerald-300"
                      >
                        Triage
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
