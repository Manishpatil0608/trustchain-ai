# TrustChain-AI: System Architecture

**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**

Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
Academic Session: 2026–2027  
Repository: `https://github.com/Manishpatil0608/trustchain-ai`

---

## 1. High-Level Architectural Blueprint

TrustChain-AI decouples identity verification from runtime authorization by introducing a continuous behavioral feedback loop between agent execution, telemetry ingestion, mathematical trust evaluation, and zero-trust policy gating.

```mermaid
flowchart TD
    subgraph UI["Presentation Layer (React 19 SOC Operations Center)"]
        Dashboard["SOC Dashboard Home"]
        Explorer["Agent Explorer & Drawer"]
        MatchingUI["Discovery & Matching Center"]
        CollabUI["Collaboration & Workflows"]
        AnalyticsUI["Trust Analytics & Charts"]
        AuthUI["RBAC & Security Audit"]
    end

    subgraph Gateway["FastAPI REST & Policy Gateway (:8050)"]
        RouterAuth["Auth & Security Router (/auth)"]
        RouterRegistry["Registry & Matching Router (/registry)"]
        RouterTrust["Trust & Telemetry Router (/trust)"]
        RouterVDR["Verifiable Credential Router (/vdr)"]
        RouterCollab["Collaboration & Workflow Router (/collaboration)"]
        
        PDP["AdaptivePolicyEnforcer (Policy Decision Point)"]
    end

    subgraph Core["Trust Intelligence & Identity Core"]
        DIDResolver["W3C did:key Resolver (Ed25519)"]
        VCEngine["W3C Linked Data Proof VC Builder"]
        TrustMath["Temporal EMA Trust Engine"]
        StateEngine["Four-State Machine (TRUSTED / SUSPICIOUS / QUARANTINED / REVOKED)"]
    end

    subgraph Persistence["Authoritative Persistence Layer (SQLite VDR - WAL Mode)"]
        DB_Agents[("agents")]
        DB_Trust[("agent_trust_states")]
        DB_Telemetry[("telemetry_logs")]
        DB_Audit[("trust_audit_trails")]
        DB_VCs[("stored_vcs")]
        DB_Sessions[("collaboration_sessions")]
        DB_Workflows[("workflows & nodes")]
        DB_Users[("users & refresh_tokens")]
    end

    UI -->|"HTTP/JSON & JWT"| Gateway
    Gateway --> PDP
    PDP --> StateEngine
    Gateway --> Core
    Core --> Persistence
    StateEngine --> DB_Trust
    StateEngine --> DB_Audit
    TrustMath --> DB_Telemetry
```

---

## 2. Core Architectural Subsystems

### A. Presentation Layer (React 19 SPA)
- Built with React 19, Vite 8, and TailwindCSS 4.
- Communicates with FastAPI via Axios with automatic Bearer token injection and HTTP-only cookie refresh rotation.
- Visualizes real-time temporal decay timelines, matching score breakdowns, radar capability maps, and state machine transitions.

### B. REST API & Policy Gateway (FastAPI)
- Exposes 39 authoritative REST endpoints across 7 functional routers.
- Enforces request-level security headers: `X-Request-ID`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`.
- Configured with CORS middleware allowing authorized origins (`http://localhost:5173`, `http://localhost:8050`).

### C. Zero-Trust Policy Decision Point (`AdaptivePolicyEnforcer`)
Located in `akta/adaptive_auth.py`, the `AdaptivePolicyEnforcer` evaluates the agent's current trust state before permitting any protected operation:

```text
Operation Request -> AdaptivePolicyEnforcer
                         │
        ┌────────────────┼────────────────┬────────────────┐
        ▼                ▼                ▼                ▼
     TRUSTED        SUSPICIOUS       QUARANTINED        REVOKED
   (T >= 0.80)   (0.50 <= T < 0.80)   (T < 0.50)   (Terminal State)
        │                │                │                │
     PERMIT        Privileged?          DENY             DENY
    (Full Access)  ├── Yes -> DENY (403) (HTTP 403)     (Permanent)
                   └── No  -> PERMIT (Monitored)
```

- **Privileged Operations:** `workflow:execute`, `workflow:orchestrate`, `agent:delegate`, `credential:issue`, `admin:revoke`, `admin:manage`, `sensitive:execute`.
- **Standard Operations:** `read`, `query`, `map:generate`, `task:execute`, `collaboration:step`, `collaboration:participate`.

### D. Decentralized Identity & Credential Core
- **`akta/did.py`:** Algorithmic public-key derivation using the W3C `did:key` method. Generates 32-byte Ed25519 signing seeds, derives public verification keys, prepends multicodec prefix `0xED01`, and encodes as base58btc with prefix `z`.
- **`akta/credentials.py`:** Implements W3C Verifiable Credentials with Linked Data Proofs (LDP). Normalizes RDF datasets via the URDNA2015 canonicalization algorithm, computes SHA-256 digests, and generates cryptographic signatures using `Ed25519Signature2020`.

### E. Temporal Behavioral Trust Engine
- **`akta/trust_engine.py`:** Evaluates sliding-window runtime observations into normalized metrics:
  - Task Success Rate $S_i(t) \in [0, 1]$
  - Protocol Compliance $C_i(t) \in [0, 1]$
  - Normalized Latency Penalty $L_i(t) \in [0, 1]$
- Computes single-period behavioral score:
  $$P_i(t) = 0.6 S_i(t) + 0.3 C_i(t) + 0.1 (1 - L_i(t))$$
- Applies temporal Exponential Moving Average smoothing with decay parameter $\lambda = 0.7$:
  $$T_i(t) = 0.7 T_i(t-1) + 0.3 P_i(t)$$

### F. Verifiable Data Registry (Local SQLite VDR)
- Embedded SQLite 3 database operating in Write-Ahead Logging (`WAL`) mode.
- Guarantees ACID transactional semantics with zero network consensus overhead.
- Persists 13 tables covering credentials, agents, trust scores, telemetry, workflows, sessions, and security audits.

---

## 3. End-to-End Behavioral Life Cycle Sequence

The following sequence diagram illustrates the lifecycle from agent registration, credential issuance, telemetry degradation, quarantine gating, to trust recovery:

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Security Admin / SOC
    participant Reg as Agent Registry
    participant VDR as SQLite VDR
    participant Telemetry as Telemetry Pipeline
    participant Math as Trust Engine
    participant Gate as Policy Enforcer (PEP/PDP)
    actor Agent as Autonomous Agent

    Note over Agent,Reg: 1. Registration & Credential Issuance
    Agent->>Reg: POST /api/v1/registry/agents (Capabilities, Model)
    Reg->>Reg: Generate W3C did:key (Ed25519)
    Reg->>VDR: Store Agent & Initialize TrustState (T = 1.0, TRUSTED)
    Reg-->>Agent: Return Agent Profile & DID

    Note over Agent,Gate: 2. Normal Operation Under TRUSTED State
    Agent->>Gate: POST /api/v1/map/generate (Execute Tool)
    Gate->>VDR: Check Trust State (did) -> T = 1.0 (TRUSTED)
    Gate-->>Agent: Access Permitted (200 OK)

    Note over Agent,Math: 3. Behavioral Degradation & Telemetry
    Agent->>Telemetry: POST /api/v1/trust/telemetry (Task Failed, Latency 1800ms)
    Telemetry->>Math: Ingest Event (S=0, C=0, L=0.9)
    Math->>Math: Compute Pi(t) = 0.010, Ti(t) = 0.7(1.0) + 0.3(0.01) = 0.703
    Math->>VDR: Transition State -> SUSPICIOUS (T = 0.703)
    Math->>VDR: Write Immutable TrustAuditTrail entry

    Agent->>Telemetry: POST /api/v1/trust/telemetry (Policy Violation)
    Telemetry->>Math: Ingest Event (S=0, C=0, L=1.0)
    Math->>Math: Compute Pi(t) = 0.000, Ti(t) = 0.7(0.703) + 0.3(0.0) = 0.492
    Math->>VDR: Transition State -> QUARANTINED (T = 0.492 < 0.50)
    Math->>VDR: Write TrustAuditTrail: "Degraded below suspicious threshold"

    Note over Agent,Gate: 4. Zero-Trust Enforcement Gating
    Agent->>Gate: POST /api/v1/map/generate (Execute Tool)
    Gate->>VDR: Check Trust State (did) -> T = 0.492 (QUARANTINED)
    Gate->>VDR: Log Policy Violation Audit Event
    Gate-->>Agent: HTTP 403 Forbidden: Agent QUARANTINED

    Note over Agent,Math: 5. Trust Recovery via Compliant Behavior
    loop 5x Compliant Telemetry Events
        Agent->>Telemetry: POST /api/v1/trust/telemetry (Success=True, Compliant=True, Latency=120ms)
        Telemetry->>Math: Ingest Clean Event
        Math->>Math: Re-evaluate Ti(t) through EMA smoothing
    end
    Math->>VDR: Ti(t) rises to 0.825 -> Transition State to TRUSTED
    Math->>VDR: Write TrustAuditTrail: "Recovered to TRUSTED state"

    Agent->>Gate: POST /api/v1/map/generate (Execute Tool)
    Gate->>VDR: Check Trust State (did) -> T = 0.825 (TRUSTED)
    Gate-->>Agent: Access Permitted (200 OK)
```

---

## 4. Multi-Agent Discovery vs. Task-Aware Matching Architecture

TrustChain-AI maintains a strict architectural distinction between **Discovery** and **Matching**:

```mermaid
flowchart TD
    subgraph Discovery["Phase 1: Agent Discovery (Candidate Eligibility Filtering)"]
        Pool["Global Agent Registry (N Candidates)"] --> F1{"Operational Status == AVAILABLE?"}
        F1 -->|No| R1["Excluded (BUSY / OFFLINE)"]
        F1 -->|Yes| F2{"Endpoint Health == HEALTHY?"}
        F2 -->|No| R2["Excluded (UNHEALTHY)"]
        F2 -->|Yes| F3{"Trust State != QUARANTINED or REVOKED?"}
        F3 -->|No| R3["Excluded (Security Policy Violation)"]
        F3 -->|Yes| F4{"Capability Match == True?"}
        F4 -->|No| R4["Excluded (Missing Capability)"]
        F4 -->|Yes| Eligible["Eligible Candidate Pool (M Candidates, M <= N)"]
    end

    subgraph Matching["Phase 2: Task-Aware Matching (Multi-Factor Composite Ranking)"]
        Eligible --> C_Trust["Trust Contribution (Weight = 0.40): 0.40 * Ti"]
        Eligible --> C_Rep["Reputation Contribution (Weight = 0.30): 0.30 * (Ri / 5.0)"]
        Eligible --> C_Succ["Success Contribution (Weight = 0.20): 0.20 * (Succ / Total)"]
        Eligible --> C_Lat["Latency Contribution (Weight = 0.10): 0.10 * (1 - norm_lat)"]
        
        C_Trust & C_Rep & C_Succ & C_Lat --> Score["Composite Match Score (0.0 to 1.0)"]
        Score --> Ranking["Ranked Candidate List (Top-K Allocation)"]
    end
```

---

## 5. Security Architecture & Boundary Layers

1. **Perimeter Boundary:** Reverse proxy with CORS validation, HTTP security headers, and rate limiting.
2. **Identity Boundary:** Pure algorithmic W3C `did:key` resolution; verification keys cannot be forged because the DID string is the encoded public key itself.
3. **Session Boundary:** JWT access tokens (30m expiry) with Argon2-hashed passwords and rotating HTTP-only refresh tokens.
4. **Behavioral Policy Boundary:** The `AdaptivePolicyEnforcer` enforces continuous zero-trust gating at the point of tool or workflow execution.
5. **Storage Boundary:** Local SQLite database with WAL journaling, foreign keys, and cryptographic audit records.
