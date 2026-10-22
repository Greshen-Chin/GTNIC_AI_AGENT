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
