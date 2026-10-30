# Live Demonstration Runbook (Two-Terminal Architecture)

**Project:** TrustChain-AI  
**Target Environment:** Local Machine (Windows / PowerShell)  
**Strict Setup Constraint:** Exactly Two Runtime Terminals (No Terminal 3)  

---

## 1. Terminal Launch Procedures

### Terminal 1 — Backend FastAPI Server
```powershell
cd /d "D:\capstone project\trustchain-ai\akta-base"
.venv\Scripts\activate
python -m uvicorn akta.server:app --host 0.0.0.0 --port 8050
```
*Expected Output:* `INFO: Application startup complete. Uvicorn running on http://0.0.0.0:8050`

### Terminal 2 — Frontend Vite Application
```powershell
cd /d "D:\capstone project\trustchain-ai\akta-base\frontend"
npm run dev
```
*Expected Output:* `VITE v8.2.2 ready in 450 ms. Local: http://localhost:5173/`

### Browser Access:
Navigate to: `http://localhost:5173`

---

## 2. Step-by-Step Demonstration Sequence

### Step 1: Human Operator Login
1. Open `http://localhost:5173`.
2. Enter Credentials:
   - **Username:** `admin`
   - **Password:** `Admin@TrustChain2026!`
3. Click **Authenticate Platform Session**.
4. *Key Concept:* Demonstrates JWT access token generation, HTTPOnly cookie setup, and role-based access control (`ADMIN` role).

### Step 2: Agent Identity & W3C `did:key` Generation
1. Navigate to **Multi-Agent Ecosystem → Agents** (`/agents`).
2. Click **Register Agent**.
3. Fill details:
   - Name: `Research Agent 01`
   - Type: `research`
4. Submit form.
5. *Key Concept:* Demonstrates generation of base58btc multibase `did:key:z6M...` using PyNaCl Ed25519 keypairs.

### Step 3: Verifiable Credentials (W3C LDP VC)
1. Navigate to **Identity & Security → Identity** (`/identity`).
2. Select `Research Agent 01` from the dropdown.
3. Observe the rendered Verifiable Credential card.
4. Click **Inspect Raw JSON-LD**.
5. *Key Concept:* Demonstrates W3C Linked Data Proof VC schema with Ed25519 signature proof.

### Step 4: Telemetry Ingestion & Trust Decay
1. Navigate to **Multi-Agent Ecosystem → Telemetry** (`/telemetry`).
2. Select `Research Agent 01`.
3. Submit 6 failing telemetry events:
   - Success: `False`
   - Compliance: `False`
   - Latency: `3500 ms`
4. *Key Concept:* Demonstrates real-time EWMA calculation ($P_i$ and $T_i$) decaying the score from `1.0000` down below `0.5000`.

### Step 5: State Machine & Quarantine Enforcement
1. Navigate to **Identity & Security → Authorization** (`/authorization`).
2. Select `Research Agent 01` (State: `QUARANTINED`).
3. Click **Simulate Authorized Resource Request** (`/map/generate`).
4. *Key Concept:* Demonstrates Adaptive Authorization Policy refusal — **HTTP 403 Forbidden** with detail: *"Trust Policy Violation: Agent is currently QUARANTINED due to poor behavioral history."*

### Step 6: Trust Recovery
1. Return to `/telemetry`.
2. Submit 50 clean telemetry events ($S=true, C=true, L=100\text{ms}$).
3. Observe score rise above `0.5000` (State shifts from `QUARANTINED` to `SUSPICIOUS`).
4. Return to `/authorization` and re-test resource request.
5. *Key Concept:* Demonstrates dynamic recovery — request succeeds with **HTTP 200 OK**.

### Step 7: Multi-Agent Collaboration & Sequential Workflows
1. Navigate to **Multi-Agent Ecosystem → Collaboration Hub** (`/collaboration`).
2. Request collaboration between Agent 01 and Agent 02. Observe session creation and work step execution.
3. Navigate to **Workflows** (`/workflows`).
4. Execute the sequential multi-agent pipeline.
5. *Key Concept:* Demonstrates trust-aware agent discovery, matching, and chained workflow execution.

### Step 8: Audit Logging & Governance
1. Navigate to **Identity & Security → Audit** (`/audit`).
2. Inspect **Agent Trust State Transitions** (shows exact previous/new states, timestamps, and score shift reasons).
3. Inspect **Human Security Audit Trail** (shows login events, user IDs, and client IP addresses).
