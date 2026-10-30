import assert from "node:assert/strict";
import { afterEach, test } from "node:test";
import { NextRequest } from "next/server";
import { ApiError, apiRequest } from "../src/lib/api";
import { GET, POST } from "../src/app/api/[...path]/route";
import { toIncident, type ApiIncident } from "../src/features/incidents/services/incidentAdapter";
import {
  fetchIncidents, fetchIncidentById, fetchIncidentStats, updateMitigationAction,
} from "../src/features/incidents/services/incidentService";

const originalFetch = globalThis.fetch;
const originalKey = process.env.DASHBOARD_API_KEY;
const originalApiBase = process.env.API_BASE;
const originalPublicApiUrl = process.env.NEXT_PUBLIC_API_URL;
afterEach(() => {
  globalThis.fetch = originalFetch;
  if (originalKey === undefined) delete process.env.DASHBOARD_API_KEY;
  else process.env.DASHBOARD_API_KEY = originalKey;
  if (originalApiBase === undefined) delete process.env.API_BASE;
  else process.env.API_BASE = originalApiBase;
  if (originalPublicApiUrl === undefined) delete process.env.NEXT_PUBLIC_API_URL;
  else process.env.NEXT_PUBLIC_API_URL = originalPublicApiUrl;
});

const incident: ApiIncident = {
  id: "inc-1", title: "SQL injection attempt", status: "likely",
  severity_label: "high", confidence_score: 83, human_decision: "pending",
  source_ip: "192.0.2.1", created_at: "2026-10-25T00:00:00Z",
  attack_story: [{ step: 2, event: "Payload observed" }],
  pro_evidence: [{ claim: "SQL syntax", tool: "inspect_web_attack", evidence_ref: "sqli_detected=true" }],
  tool_trace: [{ tool: "inspect_web_attack", durationMs: 12, executedAt: "2026-10-25T00:00:00Z", status: "success" }],
};

test("maps the backend schema without inventing timestamps or target details", () => {
  const mapped = toIncident(incident);
  assert.equal(mapped.aiConfidence, 0.83);
  assert.equal(mapped.aiVerdict, "Suspicious");
  assert.equal(mapped.severity, "High");
  assert.equal(mapped.attackStory[0].stepNumber, 2);
  assert.equal(mapped.attackStory[0].description, "Payload observed");
  assert.equal(mapped.attackStory[0].timestamp, "");
  assert.equal(mapped.attackStory[0].phase, "Unknown");
  assert.equal(mapped.toolTraces[0].toolName, "inspect_web_attack");
  assert.equal(mapped.toolTraces[0].durationMs, 12);
  assert.equal(mapped.evidence.pro[0].description, "sqli_detected=true");
  assert.equal(mapped.targetIp, "Unknown");
  assert.equal(toIncident({ ...incident, human_decision: "approved" }).status, "Mitigated");
  assert.equal(toIncident({ ...incident, human_decision: "rejected" }).status, "False Positive");
});

test("list, detail, and statistics use the exact same-origin API paths", async () => {
  const urls: string[] = [];
  globalThis.fetch = async (url) => {
    urls.push(String(url));
    return Response.json(String(url) === "/api/incidents" ? [incident]
      : String(url) === "/api/stats" ? { totalIncidents: 1 } : incident);
  };
  assert.equal((await fetchIncidents()).length, 1);
  await fetchIncidentById("incident /?#");
  assert.equal((await fetchIncidentStats()).totalIncidents, 1);
  assert.deepEqual(urls, ["/api/incidents", "/api/incidents/incident%20%2F%3F%23", "/api/stats"]);
});

test("decision preserves POST JSON and refreshes the persisted incident", async () => {
  const requests: Array<{ url: string; init?: RequestInit }> = [];
  globalThis.fetch = async (url, init) => {
    requests.push({ url: String(url), init });
    return Response.json(init?.method === "POST" ? { human_decision: "approved" }
      : { ...incident, human_decision: "approved" });
  };
  assert.equal((await updateMitigationAction("inc-1", "Approved")).status, "Mitigated");
  assert.equal(requests[0].url, "/api/incidents/inc-1/decision");
  assert.equal(requests[0].init?.method, "POST");
  assert.deepEqual(JSON.parse(String(requests[0].init?.body)), { decision: "approved", decided_by: "soc-analyst" });
  assert.equal(requests[1].url, "/api/incidents/inc-1");
});

test("404 details return null while authentication failures remain errors", async () => {
  globalThis.fetch = async () => new Response(null, { status: 404 });
  assert.equal(await fetchIncidentById("missing"), null);
  globalThis.fetch = async () => new Response(null, { status: 401 });
  await assert.rejects(fetchIncidents(), (error) => error instanceof ApiError && error.status === 401);
});

test("API client preserves headers and query parameters without adding browser credentials", async () => {
  globalThis.fetch = async (url, init) => {
    assert.equal(url, "/api/incidents?status=likely");
    const headers = new Headers(init?.headers);
    assert.equal(headers.get("X-Request-ID"), "test-id");
    assert.equal(headers.get("X-Dashboard-API-Key"), null);
    assert.equal(init?.cache, "no-store");
    return Response.json([]);
  };
  await apiRequest("/incidents?status=likely", { headers: new Headers({ "X-Request-ID": "test-id" }) });
});

test("server proxy fetches from API_BASE and keeps the dashboard key out of the browser request", async () => {
  process.env.API_BASE = "https://api.example.test";
  process.env.DASHBOARD_API_KEY = "test-server-only-key";
  let upstreamUrl = "";
  let upstreamHeaders: Headers | undefined;
  globalThis.fetch = async (url, init) => {
    upstreamUrl = String(url);
    upstreamHeaders = new Headers(init?.headers);
    return Response.json([{ id: "inc-1" }]);
  };

  const response = await GET(
    new NextRequest("https://dashboard.example/api/incidents?status=likely"),
    { params: Promise.resolve({ path: ["incidents"] }) },
  );

  assert.equal(upstreamUrl, "https://api.example.test/api/incidents?status=likely");
  assert.equal(upstreamHeaders?.get("X-Dashboard-API-Key"), "test-server-only-key");
  assert.equal(response.headers.get("X-Dashboard-API-Key"), null);
  assert.equal(response.headers.get("Cache-Control"), "private, no-store");
  assert.deepEqual(await response.json(), [{ id: "inc-1" }]);
});

test("server proxy forwards POST JSON to the backend and supports the configured URL fallback", async () => {
  delete process.env.API_BASE;
  process.env.NEXT_PUBLIC_API_URL = "https://api.example.test";
  process.env.DASHBOARD_API_KEY = "test-server-only-key";
  let upstreamUrl = "";
  let upstreamBody = "";
  globalThis.fetch = async (url, init) => {
    upstreamUrl = String(url);
    upstreamBody = new TextDecoder().decode(init?.body as ArrayBuffer);
    return Response.json({ human_decision: "approved" });
  };

  const response = await POST(
    new NextRequest("https://dashboard.example/api/incidents/inc-1/decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision: "approved" }),
    }),
    { params: Promise.resolve({ path: ["incidents", "inc-1", "decision"] }) },
  );

  assert.equal(upstreamUrl, "https://api.example.test/api/incidents/inc-1/decision");
  assert.equal(upstreamBody, JSON.stringify({ decision: "approved" }));
  assert.deepEqual(await response.json(), { human_decision: "approved" });
});

test("server proxy returns setup errors when backend variables are missing", async () => {
  delete process.env.API_BASE;
  delete process.env.NEXT_PUBLIC_API_URL;
  delete process.env.DASHBOARD_API_KEY;
  const response = await GET(
    new NextRequest("https://dashboard.example/api/incidents"),
    { params: Promise.resolve({ path: ["incidents"] }) },
  );
  assert.equal(response.status, 503);
  assert.match((await response.json()).detail, /API_BASE/);
});
