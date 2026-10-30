# TrustChain-AI Security Operations Center (Frontend)

The frontend for **TrustChain-AI** is a high-performance Security Operations Center (SOC) single-page application built with React 19, Vite 8, and TailwindCSS 4. It provides real-time visibility into multi-agent identities, verifiable credentials, live behavioral telemetry streams, dynamic trust decay, policy gating, agent discovery, task-aware matching, and sequential workflow execution.

---

## Key Highlights

- **Framework:** React 19 (`react` ^19.2.8, `react-dom` ^19.2.8)
- **Bundler & Dev Server:** Vite 8 (`vite` ^8.2.2) with Hot Module Replacement (HMR)
- **Styling:** TailwindCSS 4 (`tailwindcss` ^4.3.3) with PostCSS 8
- **Icons:** Lucide React (`lucide-react` ^1.38.0)
- **Data Visualizations:** Recharts (`recharts` ^3.10.1) for real-time temporal decay and radar charts
- **State & Routing:** React Router 7 (`react-router-dom` ^7.18.3) with Context-based authentication
- **HTTP Client:** Axios with JWT bearer interceptors and automated HTTP-only cookie refresh rotation

---

## Module & View Inventory

| View / Route | Component | Purpose |
|---|---|---|
| `/` | `DashboardHome.jsx` | High-level SOC telemetry overview, health status, and quick metrics |
| `/login` | `LoginPage.jsx` | Argon2-authenticated login with JWT session initialization |
| `/agents` | `AgentExplorer.jsx` | Interactive catalog of registered autonomous agents |
| `/agents/:did` | `AgentDetails.jsx` | Deep inspection drawer with DID key resolution, VC proofs, and stats |
| `/discovery` | `DiscoveryCenter.jsx` | Eligibility-based candidate agent discovery with capability filters |
| `/matching` | `MatchingCenter.jsx` | Multi-factor composite task matching and policy compliance scoring |
| `/collaboration`| `CollaborationCenter.jsx`| Session orchestrator for inter-agent messaging and task execution |
| `/workflows` | `WorkflowCenter.jsx` | Multi-node sequential workflow execution with trust-gate verification |
| `/analytics` | `TrustAnalytics.jsx` | Mathematical trust charts, EMA degradation timelines, and parameters |
| `/identity` | `IdentityCredentials.jsx`| W3C `did:key` resolver and Verifiable Credential inspector |
| `/telemetry` | `TelemetryCenter.jsx` | Live telemetry event ingestion tester (success, compliance, latency) |
| `/authorization`| `AuthorizationVisualizer.jsx`| Zero-trust policy enforcement simulator (403 Quarantine test) |
| `/transitions` | `StateTransitionMap.jsx`| Visual state machine map (TRUSTED -> SUSPICIOUS -> QUARANTINED -> REVOKED) |
| `/audit` | `AuditTrail.jsx` | Cryptographic and trust state transition security audit trail |
| `/users` | `UserManagement.jsx` | RBAC user administration, session revocation, and role assignment |
| `/health` | `SystemHealth.jsx` | Live probes for FastAPI server, SQLite VDR, and Trust Math Core |

---

## Development Setup

### 1. Prerequisites
- Node.js >= 18.0.0 (Node 20+ Recommended)
- npm >= 9.0.0

### 2. Installation
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies using lockfile
npm ci # or npm install
```

### 3. Environment Configuration
Create a `.env` file if connecting to an external backend:
```bash
cp .env.example .env
```
Default configuration connects to `http://localhost:8050/api/v1`.

### 4. Running Development Server
```bash
npm run dev
```
The Vite development server will start at `http://localhost:5173`.

### 5. Production Build
```bash
npm run build
```
Generates optimized, minified production assets in the `frontend/dist/` directory.

### 6. Linting
```bash
npm run lint
```
Executes Oxlint high-speed static analysis across all JSX and JS source files.
