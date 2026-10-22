import { Incident, IncidentSummaryStats } from "../types";
import { MOCK_INCIDENTS } from "./mockData";

// In-memory store for client-side state transitions within the session
let incidentsStore: Incident[] = [...MOCK_INCIDENTS];

export async function fetchIncidents(): Promise<Incident[]> {
  // Simulate network latency (150ms)
  await new Promise((resolve) => setTimeout(resolve, 150));
  return [...incidentsStore];
}

export async function fetchIncidentById(id: string): Promise<Incident | null> {
  await new Promise((resolve) => setTimeout(resolve, 120));
  const incident = incidentsStore.find((inc) => inc.id === id);
  return incident ? { ...incident } : null;
}

export async function updateMitigationAction(
  id: string,
  action: "Approved" | "Rejected"
): Promise<Incident> {
  await new Promise((resolve) => setTimeout(resolve, 200));
  const index = incidentsStore.findIndex((inc) => inc.id === id);
  if (index === -1) {
    throw new Error(`Incident with id ${id} not found.`);
  }

  const updatedIncident: Incident = {
    ...incidentsStore[index],
    mitigationActionTaken: action,
    status: action === "Approved" ? "Mitigated" : "False Positive",
  };

  incidentsStore[index] = updatedIncident;
  return updatedIncident;
}

export async function fetchIncidentStats(): Promise<IncidentSummaryStats> {
  await new Promise((resolve) => setTimeout(resolve, 100));
  const total = incidentsStore.length;
  const critical = incidentsStore.filter((i) => i.severity === "Critical").length;
  const high = incidentsStore.filter((i) => i.severity === "High").length;
  const active = incidentsStore.filter((i) => i.status === "Active").length;
  const mitigated = incidentsStore.filter((i) => i.status === "Mitigated").length;
  const totalConfidence = incidentsStore.reduce((acc, i) => acc + i.aiConfidence, 0);

  return {
    totalIncidents: total,
    criticalCount: critical,
    highCount: high,
    activeCount: active,
    mitigatedCount: mitigated,
    aiAverageConfidence: total > 0 ? totalConfidence / total : 0,
  };
}
