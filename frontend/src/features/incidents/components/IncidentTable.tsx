"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Search,
  Clock,
  Globe,
  Radio,
  ArrowRight,
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
  const [searchQuery, setSearchQuery] = useState("");
  const [severityFilter, setSeverityFilter] = useState<string>("ALL");
  const [verdictFilter, setVerdictFilter] = useState<string>("ALL");

  const filteredIncidents = incidents.filter((incident) => {
    const matchesSearch =
      incident.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      incident.sourceIp.includes(searchQuery) ||
      incident.targetIp.includes(searchQuery) ||
      incident.id.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesSeverity =
      severityFilter === "ALL" || incident.severity === severityFilter;

    const matchesVerdict =
      verdictFilter === "ALL" || incident.aiVerdict === verdictFilter;

    return matchesSearch && matchesSeverity && matchesVerdict;
  });

  return (
    <div className="rounded-xl border border-slate-800/90 bg-slate-900/60 backdrop-blur-md overflow-hidden shadow-2xl">
      {/* Table Control Bar */}
      <div className="p-4 border-b border-slate-800/80 flex flex-col md:flex-row gap-4 justify-between items-center bg-slate-950/40">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by IP, ID, or Alert Title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-md pl-9 pr-4 py-1.5 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              aria-label="Filter by Severity"
              className="bg-slate-900 border border-slate-700/80 rounded-md px-2.5 py-1.5 text-xs font-mono text-slate-300 focus:outline-none focus:border-emerald-500"
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
              className="bg-slate-900 border border-slate-700/80 rounded-md px-2.5 py-1.5 text-xs font-mono text-slate-300 focus:outline-none focus:border-emerald-500"
            >
              <option value="ALL">AI Verdict: All</option>
              <option value="Malicious">Malicious</option>
              <option value="Suspicious">Suspicious</option>
              <option value="Benign">Benign</option>
              <option value="Under Review">Under Review</option>
            </select>
          </div>
        </div>

        {/* Live Auto-Polling Status Badge */}
        <div className="flex items-center gap-3 text-xs font-mono">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400">
            <Radio
              className={`w-3.5 h-3.5 ${
                isValidating ? "text-emerald-400 animate-pulse" : "text-slate-500"
              }`}
            />
            <span>
              {isValidating ? "Polled New Telemetry" : "Queue Synced (3s)"}
            </span>
          </div>
          <span className="text-slate-500">
            Showing {filteredIncidents.length} of {incidents.length} alerts
          </span>
        </div>
      </div>

      {/* Main Incident Data Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/70 text-[11px] font-mono uppercase tracking-wider text-slate-400">
              <th className="py-3 px-4">Timestamp</th>
              <th className="py-3 px-4">Incident ID & Title</th>
              <th className="py-3 px-4">Source IP</th>
              <th className="py-3 px-4">AI Verdict</th>
              <th className="py-3 px-4">Severity</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-sans text-xs text-slate-300">
            {isLoading && incidents.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-500 font-mono">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                    <span>Loading real-time SOC incident queue...</span>
                  </div>
                </td>
              </tr>
            ) : filteredIncidents.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-500 font-mono">
                  No incidents match your filter criteria.
                </td>
              </tr>
            ) : (
              filteredIncidents.map((incident) => (
                <tr
                  key={incident.id}
                  className="hover:bg-slate-800/40 transition-colors group cursor-pointer"
                >
                  {/* Timestamp */}
                  <td className="py-3.5 px-4 font-mono text-[11px] text-slate-400 whitespace-nowrap">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      <span>{formatDateTime(incident.timestamp)}</span>
                    </div>
                  </td>

                  {/* Title & ID */}
                  <td className="py-3.5 px-4 max-w-md">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-mono text-[11px] text-emerald-400 font-semibold">
                        {incident.id}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">
                        Target: {incident.targetAsset}
                      </span>
                    </div>
                    <Link
                      href={`/incidents/${incident.id}`}
                      className="font-medium text-slate-100 hover:text-emerald-300 transition-colors line-clamp-1 group-hover:underline"
                    >
                      {incident.title}
                    </Link>
                  </td>

                  {/* Source IP */}
                  <td className="py-3.5 px-4 font-mono text-xs whitespace-nowrap">
                    <div className="flex items-center gap-1.5 text-slate-200">
                      <Globe className="w-3.5 h-3.5 text-slate-500" />
                      <span className="bg-slate-950/80 px-2 py-0.5 rounded border border-slate-800 text-cyan-300">
                        {incident.sourceIp}
                      </span>
                    </div>
                    {incident.sourceCountry && (
                      <div className="text-[10px] text-slate-500 mt-0.5 pl-5">
                        {incident.sourceCountry}
                      </div>
                    )}
                  </td>

                  {/* AI Verdict */}
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <VerdictBadge
                      verdict={incident.aiVerdict}
                      confidence={incident.aiConfidence}
                    />
                  </td>

                  {/* Severity */}
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <SeverityBadge severity={incident.severity} />
                  </td>

                  {/* Status */}
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    <StatusBadge status={incident.status} />
                  </td>

                  {/* Investigate Action */}
                  <td className="py-3.5 px-4 text-right whitespace-nowrap">
                    <Link href={`/incidents/${incident.id}`}>
                      <Button
                        size="sm"
                        variant="secondary"
                        rightIcon={
                          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                        }
                        className="group-hover:border-emerald-500/60 group-hover:text-emerald-300"
                      >
                        Investigate
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
