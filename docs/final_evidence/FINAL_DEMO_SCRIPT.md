# TrustChain-AI — Final Live Demonstration Script

**Project Title:** TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration  
**Demonstration Mode:** Strict Two-Terminal Architecture (No Terminal 3)  
**Target Duration:** 7 – 10 Minutes  

---

## 1. System Pre-Flight Checklist & Setup

### Terminal 1 — FastAPI Backend Server
```powershell
cd /d "D:\capstone project\trustchain-ai\akta-base"
.venv\Scripts\activate
python -m uvicorn akta.server:app --host 0.0.0.0 --port 8050
```
*Expected Output:* `INFO: Application startup complete. Uvicorn running on http://0.0.0.0:8050`

### Terminal 2 — React Vite Frontend SPA
```powershell
cd /d "D:\capstone project\trustchain-ai\akta-base\frontend"
npm run dev
```
*Expected Output:* `VITE v8.2.2 ready in 450 ms. Local: http://localhost:5173/`

### Browser Access:
- **URL:** `http://localhost:5173`
- **Default Operator Credentials:** `admin` / `Admin@TrustChain2026!`

---

## 2. Minute-by-Minute Live Walkthrough Script

### Minute 0:00 – 1:00 | Introduction & Human Authentication
- **Action:** Open `http://localhost:5173`. Show the **Human Operator Login Portal**.
- **Spoken Commentary:**
  > *"Good morning/afternoon respected evaluators. Welcome to the practical demonstration of TrustChain-AI. We begin at the Human Operator Login portal. TrustChain-AI enforces strict Role-Based Access Control (RBAC). Upon entering the administrator credentials (`admin` / `Admin@TrustChain2026!`), the FastAPI backend authenticates the user using Argon2 password hashing and issues a short-lived JWT access token along with an HTTPOnly refresh token cookie."*
- **Verification Point:** Click **Authenticate Platform Session**. App redirects to the **Command Center** (`/`). Show user badge `admin (ADMIN)`.

### Minute 1:00 – 2:30 | Agent Registry & W3C Cryptographic Identity
- **Action:** Navigate to **Multi-Agent Ecosystem → Agents** (`/agents`). Click **Register Agent**.
- **Form Input:** Name: `Research Agent 01`, Type: `research`. Click Submit.
- **Spoken Commentary:**
  > *"Next, we register a new autonomous AI agent. In TrustChain-AI, agent identity is strictly decentralized. Notice the generated Identifier: `did:key:z6M...`. The backend uses PyNaCl to generate a 32-byte Ed25519 keypair and formats the public key as a W3C multibase base58btc string. This cryptographic DID serves as the root of identity."*
- **Verification Point:** Show agent in Agent Directory with initial trust score `1.0000` (`TRUSTED`).

### Minute 2:30 – 4:00 | Verifiable Credentials & Scope Grants
- **Action:** Navigate to **Identity & Security → Identity** (`/identity`). Select `Research Agent 01`.
- **Spoken Commentary:**
  > *"Here we inspect the agent's Verifiable Credential. TrustChain-AI implements W3C Linked Data Proof (LDP) VCs. Under `credentialSubject`, we see granted capabilities such as `map:generate`. Crucially, the credential includes an `Ed25519Signature2020` proof block. While this credential proves identity and capability, traditional systems stop here. TrustChain-AI goes further by continuously evaluating behavioral trust."*
- **Verification Point:** Click **Inspect Raw JSON-LD**. Highlight the `proof` block and `verificationMethod`.

### Minute 4:00 – 5:30 | Behavioral Telemetry Ingestion & Trust Decay
- **Action:** Navigate to **Multi-Agent Ecosystem → Telemetry** (`/telemetry`). Select `Research Agent 01`.
- **Action Details:** Submit 6 consecutive failing telemetry logs:
  - Task Success: `False`
  - Compliance Event: `False`
  - Latency: `3500 ms`
- **Spoken Commentary:**
  > *"Now we simulate behavioral degradation. The telemetry engine ingests task success ($S$), compliance ($C$), and latency ($L$). Using our EWMA formula $P_i = 0.6S + 0.3C + 0.1(1-L)$ and $T_i = 0.7P_i + 0.3T_{i-1}$, notice how each failing event penalizes the temporal trust score. As the score drops below 0.5000, the state machine automatically transitions the agent into `QUARANTINED`."*
- **Verification Point:** Navigate to **Analytics** (`/analytics`) or **State Transitions** (`/transitions`). Show score drop to `0.3097` and red `QUARANTINED` status badge.

### Minute 5:30 – 7:00 | Adaptive Authorization Policy Refusal
- **Action:** Navigate to **Identity & Security → Authorization** (`/authorization`). Select `Research Agent 01`.
- **Action Details:** Present the valid VC token and click **Simulate Resource Request** (`POST /api/v1/map/generate`).
- **Spoken Commentary:**
  > *"This is the central thesis of TrustChain-AI. The agent possesses a valid, unexpired, cryptographically signed Verifiable Credential. However, when it requests access to the protected `/map/generate` endpoint, the `AdaptivePolicyEnforcer` intercepts the request, checks the agent's current temporal trust state, detects `QUARANTINED`, and blocks the request with an **HTTP 403 Forbidden** refusal."*
- **Verification Point:** Show the red alert box: `HTTP 403 Forbidden - Trust Policy Violation: Agent is currently QUARANTINED due to poor behavioral history.`

### Minute 7:00 – 8:30 | Trust Recovery & Execution Success
- **Action:** Return to `/telemetry`. Submit 50 clean telemetry events ($S=true, C=true, L=100\text{ms}$).
- **Action Details:** Return to `/authorization` and re-test `/map/generate`.
- **Spoken Commentary:**
  > *"Trust in TrustChain-AI is dynamic, not a permanent death sentence. By submitting a series of successful, compliant, low-latency execution events, the EWMA algorithm restores the trust score back above 0.5000 into the `SUSPICIOUS` state. Upon re-testing the resource request, the gateway now grants access with an **HTTP 200 OK** response."*
- **Verification Point:** Show green box: `HTTP 200 OK - Map generation successfully authorized and executed!`

### Minute 8:30 – 10:00 | Multi-Agent Collaboration, Workflows & Audit
- **Action:** Navigate to **Workflows** (`/workflows`). Click **Execute Sequential Pipeline**.
- **Action:** Navigate to **Audit Trail** (`/audit`).
- **Spoken Commentary:**
  > *"Finally, we view multi-agent orchestration and governance. Our sequential workflow engine executes multi-agent pipelines, passing task outputs from Node 1 to Node 2 while recording execution telemetry for each step. Under the Audit Trail view, every single state transition is recorded with timestamped score deltas and transition reasons, alongside the human security audit log."*
- **Verification Point:** Show completed workflow chain and immutable transition audit log. Conclude demonstration.
