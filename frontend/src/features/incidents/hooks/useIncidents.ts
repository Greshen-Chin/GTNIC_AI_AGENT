"use client";

import useSWR, { useSWRConfig } from "swr";
import { fetchIncidents, fetchIncidentById, updateMitigationAction, fetchIncidentStats } from "../services/incidentService";

export function useIncidents(refreshInterval: number = 3000) {
  const { data, error, isLoading, isValidating, mutate } = useSWR(
    "/api/incidents",
    () => fetchIncidents(),
    {
      refreshInterval,
      revalidateOnFocus: true,
      dedupingInterval: 1000,
    }
  );

  return {
    incidents: data ?? [],
    isLoading,
    isValidating,
    error,
    mutate,
  };
}

export function useIncident(id: string | undefined | null) {
  const { mutate: mutateCache } = useSWRConfig();
  const { data, error, isLoading, isValidating, mutate } = useSWR(
    id ? `/api/incidents/${id}` : null,
    () => (id ? fetchIncidentById(id) : Promise.resolve(null)),
    {
      refreshInterval: 3000,
      revalidateOnFocus: true,
    }
  );

  const applyMitigation = async (action: "Approved" | "Rejected") => {
    if (!id) return;
    try {
      // Optimistic update
      mutate(
        (current) => {
          if (!current) return current;
          return {
            ...current,
            mitigationActionTaken: action,
            status: action === "Approved" ? "Mitigated" : "False Positive",
          };
        },
        false
      );

      const updated = await updateMitigationAction(id, action);
      await Promise.all([
        mutate(updated),
        mutateCache("/api/incidents"),
        mutateCache("/api/stats"),
      ]);
    } catch (err) {
      mutate();
      throw err;
    }
  };

  return {
    incident: data,
    isLoading,
    isValidating,
    error,
    mutate,
    applyMitigation,
  };
}

export function useIncidentStats(refreshInterval: number = 3000) {
  const { data, error, isLoading, mutate } = useSWR(
    "/api/stats",
    () => fetchIncidentStats(),
    {
      refreshInterval,
      dedupingInterval: 1000,
    }
  );

  return {
    stats: data,
    isLoading,
    error,
    mutate,
  };
}
