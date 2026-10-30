# TrustChain-AI Implemented Architecture

**Project:** TrustChain-AI  
**Document Purpose:** Academic Report & Thesis Technical Reference  

---

## 1. System Architecture Overview

TrustChain-AI decouples cryptographic identity from operational authorization. While traditional Zero-Trust systems verify static credentials (VCs) at request time, TrustChain-AI introduces continuous behavioral telemetry evaluation to dynamically alter authorization states.

```
+-----------------------------------------------------------------------+
|                           React 19 SPA Frontend                       |
|                   (Vite 8, Tailwind CSS, Recharts)                    |
+-----------------------------------------------------------------------+
                                   | (REST API Calls / JWT Bearer)
                                   v
+-----------------------------------------------------------------------+
|                         FastAPI API Gateway Layer                     |
|            (CORS, Request ID Middleware, Authentication / RBAC)       |
+-----------------------------------------------------------------------+
                                   |
       +---------------------------+---------------------------+
       |                           |                           |
       v                           v                           v
+------------------+     +-------------------+     +--------------------+
| Cryptographic    |     | Behavioral Trust  |     | Multi-Agent        |
| Identity Subsystem|     | Subsystem         |     | Collaboration Engine|
| - W3C did:key    |     | - Telemetry Ingest|     | - Agent Discovery  |
| - W3C LDP VC     |     | - EWMA Calculator |     | - Trust Matching   |
| - PyNaCl Ed25519 |     | - State Machine   |     | - Workflows (Seq)  |
+------------------+     +-------------------+     +--------------------+
       |                           |                           |
       +---------------------------+---------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    SQLite Database Layer (vdr.db)                      |
|       (Stored VCs, Trust States, Telemetry, Audits, Agents, Workflows) |
+-----------------------------------------------------------------------+
```

---

## 2. Core Subsystems

### 2.1 Cryptographic Identity Subsystem
- **DID Specification:** W3C `did:key` format using multibase base58btc Ed25519 public key fingerprints (`did:key:z6M...`).
- **Verifiable Credentials:** W3C Linked Data Proof (LDP) VC format with `@context` definitions for `Ed25519Signature2020`.
- **Signatures:** Cryptographically signed using 32-byte Ed25519 private key seeds via PyNaCl (`nacl.signing.SigningKey`).

### 2.2 Dynamic Behavioral Trust Engine
- **Telemetry Ingestion:** Receives $(S, C, L)$ metrics from execution contexts.
- **Instantaneous Performance ($P_i$):** $P_i(t) = 0.6 S_i(t) + 0.3 C_i(t) + 0.1 (1 - L_i(t))$.
- **Temporal Trust ($T_i$):** $T_i(t) = 0.7 P_i(t) + 0.3 T_i(t-1)$.
- **State Machine:**
  - `TRUSTED`: $T \ge 0.80$ (Full authorization)
  - `SUSPICIOUS`: $0.50 \le T < 0.80$ (Allowed, step-up monitoring)
  - `QUARANTINED`: $T < 0.50$ (Blocked automatically with HTTP 403)
  - `REVOKED`: Terminal administrative state (Blocked permanently)

### 2.3 Adaptive Policy Enforcement Layer
- **`AdaptivePolicyEnforcer` (`akta/adaptive_auth.py`):** Intercepts resource requests. Even if a presented Verifiable Credential has a valid signature and active expiration date, the enforcer queries the database for the subject agent's current $T_i(t)$ state. If `QUARANTINED` or `REVOKED`, access is denied before resource execution.

### 2.4 Multi-Agent Collaboration & Workflow Engine
- **Agent Registry:** Manages active DIDs, capability lists, health checks, and reputation scores.
- **Trust-Aware Matching:** Discovers available agents filtered by capability and restricted to `TRUSTED` or `SUSPICIOUS` trust states.
- **Sequential Workflows:** Orchestrates step-by-step pipeline execution where Node $N_i$ output feeds into Node $N_{i+1}$ input, updating telemetry post-execution.
