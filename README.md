# GTNIC AI AGENT - Modular Monolith Repository

This repository is structured as a **Modular Monolith** containing isolated domains and services.

## 📂 Repository Structure

```
GTNIC_AI_AGENT/
├── frontend/                   # Cybersecurity SOC AI Agent Next.js Frontend
│   ├── src/
│   │   ├── app/                # App Router (pages: /, /incidents/[id])
│   │   ├── components/ui/      # Shared Design System
│   │   ├── features/incidents/ # Incidents domain (types, services, hooks, components)
│   │   └── lib/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── README.md
├── backend/                    # (Ready for your backend / agent orchestrator service)
└── README.md
```

## 🚀 Running the Frontend

Navigate to the `frontend` folder or use npm prefix:

```bash
cd frontend
npm run dev
```

Or from the root directory:
```bash
npm --prefix frontend run dev
```
