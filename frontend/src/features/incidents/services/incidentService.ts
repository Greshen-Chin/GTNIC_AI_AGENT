import { ApiError, apiRequest } from "@/lib/api";
import type { Incident, IncidentSummaryStats } from "../types";
import { toIncident, type ApiIncident } from "./incidentAdapter";

export async function fetchIncidents(): Promise<Incident[]> {
  return (await apiRequest<ApiIncident[]>("/incidents")).map(toIncident);
}

export async function fetchIncidentById(id: string): Promise<Incident | null> {
  try {
    return toIncident(await apiRequest<ApiIncident>(`/incidents/${encodeURIComponent(id)}`));
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) return null;
    throw error;
  }
}

export async function updateMitigationAction(
  id: string,
  action: "Approved" | "Rejected"
): Promise<Incident> {
  await apiRequest(`/incidents/${encodeURIComponent(id)}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision: action.toLowerCase(), decided_by: "soc-analyst" }),
  });
  const incident = await fetchIncidentById(id);
  if (!incident) throw new Error(`Incident with id ${id} not found.`);
  return incident;
}

export async function fetchIncidentStats(): Promise<IncidentSummaryStats> {
  return apiRequest<IncidentSummaryStats>("/stats");
}
