export const API_BASE_PATH = "/api";

export class ApiError extends Error {
  constructor(public readonly status: number) {
    super(`Dashboard API request failed (HTTP ${status}).`);
    this.name = "ApiError";
  }
}

// SWR calls this in Client Components after hydration, not during server rendering.
export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (!headers.has("Accept")) headers.set("Accept", "application/json");
  const response = await fetch(`${API_BASE_PATH}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
  if (!response.ok) throw new ApiError(response.status);
  return response.json() as Promise<T>;
}
