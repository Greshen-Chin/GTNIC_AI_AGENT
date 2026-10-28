Frontend changes verified on 25 October 2026 (Asia/Jakarta).

**Result: production build PASS (exit 0).** `npm install`, `npm run lint`
(exit 0), and `npm test` (8 passing tests) completed. All 45 local source imports
were checked for module resolution and filename casing. No build checks or lint
rules were disabled. The lint ignore file excludes generated artifacts only.

The existing `src/lib/utils.ts` was being excluded by the repository's Python
`lib/` ignore rule. The frontend now explicitly includes its source utility
directory. The existing `cn()` and `formatDateTime()` implementation is reused;
no duplicate utility module was created. `@/*` still resolves to `./src/*`.

Browser requests now use the centralized `/api` base path. The live service
maps backend incident fields into the existing UI, replacing its former mock
store. Analyst decisions are submitted as POST JSON and refresh the affected
SWR caches. Missing optional backend details remain empty or unknown. Existing
components, visual styles, and animations are retained; unused imports and JSX
label syntax were cleaned up to satisfy lint.

`vercel.json` maps `/api/:path*` to
`https://api.flummox.cloud/api/:path*`. The backend already uses `/api`, so this
preserves the prefix exactly once. Local Next.js uses the same rewrite rules.
There are no conflicting API route handlers. Middleware adds the server-only
`DASHBOARD_API_KEY` to upstream request headers and disables API response caching.

A production `next start` smoke test with an isolated upstream stub passed:
dashboard and incident pages return HTTP 200; GET query strings and headers are
preserved; POST methods, JSON bodies, Content-Type, and response status are
preserved; the dashboard key reaches the upstream but is absent from browser
response headers and bodies. This test verifies local Next.js proxy behavior,
not an actual Vercel deployment or the live GCP backend.

Next.js was upgraded from 14 to 15.5.28 with compatible React 19 and typings
because the installed 14.x dependency had critical audit findings. The PostCSS
dependency is overridden within its existing major version to a patched release.
`npm audit --omit=dev` reports **0 vulnerabilities**. The full audit still reports
3 moderate findings in development-only Tailwind CSS / selector-parser tooling;
a forced Tailwind major upgrade was not applied.

Required configuration remains: Vercel Root Directory `frontend`, Next.js preset,
Node.js 22.x, and a server-only `DASHBOARD_API_KEY` matching the backend. See
`.env.example` and `README.md`. The public backend's `/health`, `/api/incidents`,
and `/incidents` could not be reached from the verification environment
(`ConnectError`), so live connectivity, live redirects, and authenticated live
responses remain unverified. Backend availability must be restored/confirmed
before the deployed dashboard can load data. The backend and its deployment
configuration were not changed. Nothing was committed, pushed, or deployed.

Modified or newly included files, relative to `frontend/`:

```text
.env.example
.eslintignore
.eslintrc.json
.gitignore
BUILD_REPORT.md
README.md
next.config.mjs
package-lock.json
package.json
tsconfig.json
vercel.json
src/app/incidents/[id]/page.tsx
src/app/page.tsx
src/components/ui/Navbar.tsx
src/features/incidents/components/AttackTimeline.tsx
src/features/incidents/components/EvidencePanel.tsx
src/features/incidents/components/IncidentHeader.tsx
src/features/incidents/components/IncidentTable.tsx
src/features/incidents/components/MitreOwaspPanel.tsx
src/features/incidents/components/StatsBar.tsx
src/features/incidents/components/ToolTraceTerminal.tsx
src/features/incidents/hooks/useIncidents.ts
src/features/incidents/services/incidentAdapter.ts
src/features/incidents/services/incidentService.ts
src/features/incidents/types/index.ts
src/lib/api.ts
src/lib/utils.ts
src/middleware.ts
tests/api.test.ts
```

To commit and push these frontend changes from the repository root:

```powershell
git add -- frontend
git commit -m "Fix frontend production build and authenticated API proxy"
git push origin main
```
