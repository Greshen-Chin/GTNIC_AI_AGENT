import { NextResponse, type NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const headers = new Headers(request.headers);
  const apiKey = process.env.DASHBOARD_API_KEY;

  if (apiKey) {
    // This request header is forwarded upstream, never returned to the browser.
    headers.set("X-Dashboard-API-Key", apiKey);
  } else if (
    !headers.has("X-Dashboard-API-Key") &&
    !headers.has("X-API-Key") &&
    !headers.has("Authorization")
  ) {
    return NextResponse.json(
      { detail: "Dashboard API credentials are not configured on the server." },
      { status: 503, headers: { "Cache-Control": "no-store" } }
    );
  }

  const response = NextResponse.next({ request: { headers } });
  response.headers.set("Cache-Control", "private, no-store");
  return response;
}

export const config = {
  matcher: "/api/:path*",
};
