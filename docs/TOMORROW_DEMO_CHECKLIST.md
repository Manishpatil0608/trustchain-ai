# TrustChain-AI: Live Demonstration & Viva Checklist (2-Terminal Architecture)

## 1. Environment & 2-Terminal Setup
- [ ] **Terminal 1 (Backend FastAPI Server)**
  ```cmd
  cd /d "D:\capstone project\trustchain-ai\akta-base"
  .venv\Scripts\activate
  python -m uvicorn akta.server:app --host 0.0.0.0 --port 8050
  ```
  *Verify:* Open Browser at `http://127.0.0.1:8050/health` -> returns `{"status":"ok",...}`.

- [ ] **Terminal 2 (Frontend React Vite Dashboard)**
  ```cmd
  cd /d "D:\capstone project\trustchain-ai\akta-base\frontend"
  npm run dev
  ```
  *Verify:* Open Browser at `http://localhost:5173`.

---

## 2. Authentication & Governance Checks
- [ ] Open `http://localhost:5173` -> `LoginPage` is presented.
- [ ] Log in as Admin: `admin` / `Admin@TrustChain2026!`.
- [ ] Confirm Sidebar displays User Badge (`admin`), Role Badge (`ADMIN`), and Logout icon.
- [ ] Navigate to `/admin/users` (User Governance panel) -> Verify User Directory, Create User, and Audit Log tabs.

---

## 3. Dashboard Browser Walkthrough Sequence
- [ ] **01. Command Center (`/`)**: Overview metrics, active agent cards, system trust distribution.
- [ ] **02. Multi-Agent Ecosystem (`/agents`)**: Search DIDs, filter by capabilities (`research`, `analysis`, `verification`), view status badges (`AVAILABLE`, `BUSY`).
- [ ] **03. Agent Details (`/agents/{did}`)**: Inspect DID document (`did:key:...`), Verifiable Credentials, telemetry history logs, and instant trust metrics.
- [ ] **04. Collaboration Hub (`/collaboration`)**: Start session between Agent A & Agent B, exchange structured inter-agent messages, rate agent (1-5 stars).
- [ ] **05. Workflows (`/workflows`)**: View 3-step sequential pipeline (`Research` -> `Analysis` -> `Verification`), execute workflow live, observe step-by-step progress and output certificates.
- [ ] **06. Trust Analytics (`/analytics`)**: View real-time trust score timeline charts, state breakdown (`TRUSTED`, `SUSPICIOUS`, `QUARANTINED`, `REVOKED`), and dynamic parameters ($\lambda=0.7$).
- [ ] **07. Telemetry Center (`/telemetry`)**: Inspect raw execution logs ($S_i, C_i, L_i$), instantaneous score $P_i(t)$, and temporal trust $T_i(t)$.
- [ ] **08. Identity & Credentials (`/identity`)**: Inspect W3C DID key documents, Ed25519 public keys, and JSON-LD Verifiable Credentials.
- [ ] **09. Authorization Visualizer (`/authorization`)**: Live policy evaluation testbed showing HTTP 200 for `TRUSTED` agents and HTTP 403 for `QUARANTINED` / `REVOKED` agents.
- [ ] **10. Audit Trail (`/audit`)**: Immutable log of trust state transition events with timestamped reasons.
- [ ] **11. User Governance (`/admin/users`)**: Platform RBAC user registry, enable/disable account toggles, and security audit log.

---

## 4. Non-Regression Verification Commands
- [ ] Automated Test Suite: `pytest -q` -> All 63 unit and integration tests passing.
- [ ] Production Frontend Build: `npm run build` in `frontend/` -> 0 errors.
