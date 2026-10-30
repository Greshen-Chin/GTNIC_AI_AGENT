import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type RouteContext = { params: Promise<{ path: string[] }> };

async function proxyToBackend(request: NextRequest, context: RouteContext) {
  // API_BASE is server-only. NEXT_PUBLIC_API_URL remains a compatibility fallback
  // for the variable already configured in this Vercel project.
  const apiBase = process.env.API_BASE || process.env.NEXT_PUBLIC_API_URL;
  const dashboardKey = process.env.DASHBOARD_API_KEY;

  if (!apiBase || !dashboardKey) {
    return NextResponse.json(
      {
        detail: !apiBase
          ? "API_BASE is not configured on the frontend deployment."
          : "DASHBOARD_API_KEY is not configured on the frontend deployment.",
      },
      { status: 503, headers: { "Cache-Control": "no-store" } },
    );
  }

  let target: URL;
  try {
    const { path } = await context.params;
    const encodedPath = path.map((part) => encodeURIComponent(part)).join("/");
    target = new URL(`/api/${encodedPath}`, apiBase);
    target.search = new URL(request.url).search;
  } catch {
    return NextResponse.json(
      { detail: "API_BASE must be a valid backend origin, for example https://api.example.com." },
      { status: 503, headers: { "Cache-Control": "no-store" } },
    );
  }

  const headers = new Headers();
  const accept = request.headers.get("accept");
  const contentType = request.headers.get("content-type");
  const requestId = request.headers.get("x-request-id");
  if (accept) headers.set("accept", accept);
  if (contentType) headers.set("content-type", contentType);
  if (requestId) headers.set("x-request-id", requestId);
  headers.set("X-Dashboard-API-Key", dashboardKey);

  try {
    const method = request.method.toUpperCase();
    const response = await fetch(target, {
      method,
      headers,
      body: method === "GET" || method === "HEAD" ? undefined : await request.arrayBuffer(),
      cache: "no-store",
      redirect: "manual",
      signal: AbortSignal.timeout(15_000),
    });

    const responseHeaders = new Headers({ "Cache-Control": "private, no-store" });
    for (const name of ["content-type", "retry-after", "x-request-id"]) {
      const value = response.headers.get(name);
      if (value) responseHeaders.set(name, value);
    }

    return new Response(response.body, {
      status: response.status,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error("Dashboard backend request failed", error);
    return NextResponse.json(
      { detail: "Could not reach the SOAR backend. Check API_BASE and backend availability." },
      { status: 502, headers: { "Cache-Control": "no-store" } },
    );
  }
}

export const GET = proxyToBackend;
export const POST = proxyToBackend;
export const PUT = proxyToBackend;
export const PATCH = proxyToBackend;
export const DELETE = proxyToBackend;
