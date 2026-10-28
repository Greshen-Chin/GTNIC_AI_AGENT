# GTNIC Autonomous SOC AI Agent Dashboard

An enterprise-grade, high-density Cybersecurity Operations Center (SOC) AI Agent Dashboard frontend built with **Next.js 14+ (App Router)**, **TypeScript**, **Tailwind CSS**, and **SWR**.

## 🛡️ Architecture (Feature-Sliced Design)

The project adheres strictly to layered modular boundaries:

```
src/
├── app/                                 # Routing & Page Composition Layer Only
│   ├── layout.tsx                       # Root Layout & Dark Theme Provider
│   ├── page.tsx                         # Route: / (Incident Queue Dashboard)
│   ├── incidents/
│   │   └── [id]/
│   │       └── page.tsx                 # Route: /incidents/[id] (Investigation Workspace)
│   └── globals.css                      # Cyber-palette, glow utilities, monospace setup
├── features/
│   └── incidents/
│       ├── types/
│       │   └── index.ts                 # TypeScript Domain Models (Incident, Evidence, ToolTrace, etc.)
│       ├── services/
│       │   ├── mockData.ts              # Realistic SOC alerts (SQLi, Credential Stuffing, WMI Living-off-the-land)
│       │   └── incidentService.ts       # Data fetchers & mitigation state handlers
│       ├── hooks/
│       │   ├── useIncidents.ts          # SWR Hooks with 3s auto-polling & optimistic UI
│       │   └── index.ts
│       └── components/
│           ├── IncidentTable.tsx        # Real-time incident data table with filters & telemetry
│           ├── StatsBar.tsx             # Active threats & AI confidence metric cards
│           ├── IncidentHeader.tsx       # Title, Target IP, Severity & Approve/Reject actions
│           ├── AttackTimeline.tsx       # Left Col: AI Attack Story Chronological Timeline
│           ├── EvidencePanel.tsx        # Middle Col: Pro vs Contra Side-by-Side Evidence
│           ├── MitreOwaspPanel.tsx      # Right Col: MITRE ATT&CK & OWASP Matrix Cards
│           ├── ToolTraceTerminal.tsx    # Bottom/Full-Width: Collapsible Terminal Audit Log
│           └── index.ts
├── components/
│   └── ui/                              # Shared & Reusable Design System Components
│       ├── Badge.tsx                    # Severity, Verdict, and Status Badges
│       ├── Button.tsx                   # Cyberpunk / SOC High-Contrast Button Variants
│       ├── Card.tsx                     # Glow border & Glassmorphism Containers
│       ├── Navbar.tsx                   # Top SOC Bar with Active Pulse & UTC Clock
│       └── index.ts
└── lib/
    └── utils.ts                         # Class merging (clsx + tailwind-merge) & Date formatters
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to view the Incident Queue and click **Investigate** on any alert to access the Incident Investigation Workspace.

### 3. Production Build
```bash
npm run build
npm run start
```

## Live API and Vercel deployment

Set the Vercel project's **Root Directory** to `frontend`, use the Next.js
framework preset, and use Node.js 22.x. Install with `npm install` and build with
`npm run build`. This project uses Next.js 15 and React 19.

Copy `.env.example` to `.env.local` for local development. Set the server-only
`DASHBOARD_API_KEY` to the same value configured in the backend. Add that variable
to the appropriate Vercel Production/Preview environments as well. Never use a
`NEXT_PUBLIC_` variable for this key. Environment files remain ignored by Git.

Browser requests use these same-origin endpoints:

| Action | Method | Browser path | Backend path |
| --- | --- | --- | --- |
| Incident list | GET | `/api/incidents` | `/api/incidents` |
| Incident detail | GET | `/api/incidents/{id}` | `/api/incidents/{id}` |
| Analyst decision | POST | `/api/incidents/{id}/decision` | `/api/incidents/{id}/decision` |
| Dashboard statistics | GET | `/api/stats` | `/api/stats` |

`vercel.json` rewrites `/api/:path*` to
`https://api.flummox.cloud/api/:path*`, preserving the backend's `/api` prefix,
request method, body, and query string. `next.config.mjs` reads the same rules for
local development and `next start`. There are no competing Next.js API handlers.
The browser stays on the frontend's HTTPS origin while Vercel proxies requests
to the Cloudflare Tunnel hostname. Middleware adds the dashboard key to the
upstream request; the key is not included in browser JavaScript or response
headers. Missing server credentials produce HTTP 503; upstream errors remain
errors and do not trigger a fallback to demo incidents.

Data fetching runs through SWR in Client Components after hydration, so relative
URLs are not passed to Node.js server-side `fetch` during builds or rendering.
The service translates backend snake_case fields into the existing UI models.
Optional details absent from the backend are shown as unknown or left empty.
Approve/Reject records the analyst decision; it does not itself enforce firewall
rules. The existing mock fixtures remain available as reference data but are no
longer used by the live dashboard.

The backend must be reachable at `https://api.flummox.cloud` through the
Cloudflare Tunnel. Set the GCP tunnel origin to `http://localhost:8080`; Docker
publishes the API container's port 8000 on that loopback address. A successful
frontend build alone does not verify backend availability, Wazuh, Vertex AI, or
database connections. Configure the same `DASHBOARD_API_KEY` in the backend and
Vercel Production/Preview environments.

Run the frontend checks before pushing:

```bash
npm run lint
npm test
npm run build
```
