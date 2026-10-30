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

Set these variables in Vercel Project Settings → Environment Variables (and in
`frontend/.env.local` for local development):

```env
API_BASE=https://api.flummox.cloud
DASHBOARD_API_KEY=<same value as backend/.env>
```

`API_BASE` is server-side configuration. `NEXT_PUBLIC_API_URL` is accepted as a
compatibility fallback for existing Vercel projects, but `API_BASE` is preferred.
Never prefix `DASHBOARD_API_KEY` with `NEXT_PUBLIC_`: it must match the backend
key and is only attached by the server route handler. Redeploy Vercel after
changing environment variables.

Browser requests use these same-origin endpoints:

| Action | Method | Browser path | Backend path |
| --- | --- | --- | --- |
| Incident list | GET | `/api/incidents` | `/api/incidents` |
| Incident detail | GET | `/api/incidents/{id}` | `/api/incidents/{id}` |
| Analyst decision | POST | `/api/incidents/{id}/decision` | `/api/incidents/{id}/decision` |
| Dashboard statistics | GET | `/api/stats` | `/api/stats` |

The browser calls same-origin `/api/...` endpoints. A Next.js route handler
proxies them to `${API_BASE}/api/...`, preserving methods, request bodies, and
query strings while attaching `X-Dashboard-API-Key` on the server. The browser
never receives this key and no CORS setup is needed. Missing credentials return
HTTP 503; backend connectivity errors return HTTP 502.

Data fetching runs through SWR in Client Components after hydration, so relative
URLs are not passed to Node.js server-side `fetch` during builds or rendering.
The service translates backend snake_case fields into the existing UI models.
Optional details absent from the backend are shown as unknown or left empty.
Approve/Reject records the analyst decision; it does not itself enforce firewall
rules. The existing mock fixtures remain available as reference data but are no
longer used by the live dashboard.

The backend must be reachable at `https://api.flummox.cloud` through the
Cloudflare Tunnel. Set the GCP tunnel origin to `http://localhost:8080`; Docker
publishes the API container's port 8000 on that loopback address. Set the same
`DASHBOARD_API_KEY` in backend and Vercel Production/Preview. The dashboard polls
the backend every three seconds and now shows its connection state. Juice Shop
alerts appear after the backend's log forwarder stores them in the incidents
table; n8n notification delivery separately requires an active n8n webhook in
the backend's `WEBHOOK_URL` setting.

Run the frontend checks before pushing:

```bash
npm run lint
npm test
npm run build
```
