# System Limitations & Future Scope

**Project:** TrustChain-AI  
**Document Purpose:** Academic Claim Boundaries & Thesis Defense Reference  

---

## 1. Academic Claim Boundaries

To ensure strict academic rigor, the implementation features are classified into four explicit tiers:

```
+-----------------------------------------------------------------------+
|  1. IMPLEMENTED & VERIFIED IN CODE                                    |
|  - W3C did:key Ed25519 Cryptographic Identity                         |
|  - W3C LDP VC Issuance & Linked Data Proof Signature Checks           |
|  - Verifiable Data Registry (VDR) Persistence via SQLite              |
|  - Behavioral Telemetry Ingestion & Metric Normalization (S, C, L)    |
|  - EWMA Dynamic Trust Score Engine & 4-State Machine                  |
|  - Adaptive Authorization Policy Enforcement Layer                    |
|  - Trust-Aware Agent Discovery & Matching                             |
|  - Inter-Agent Collaboration & Sequential Workflow Pipelines          |
|  - State Transition Audit Trail & Human Authentication / RBAC         |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  2. SYSTEM LIMITATIONS (CURRENT RUNTIME BOUNDARIES)                    |
|  - Local SQLite Persistence (Not a distributed blockchain ledger)     |
|  - Single-Node API Gateway (Not a distributed service mesh)           |
|  - Simulated Telemetry Sources (Requires API Gateway signature wrap)  |
|  - Mock Task Work Output Generation (Local connector vs remote LLM)   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  3. FUTURE SCOPE (PROPOSED EXTENSIONS)                                |
|  - Blockchain VDR Anchoring (e.g. Ethereum / Hedera L2)               |
|  - API Gateway Sidecar Interceptor (Envoy / Kong post-execution telemetry)|
|  - Zero-Knowledge Proof (ZKP) VC Selective Disclosure                 |
|  - Distributed Byzantine Fault Tolerant (BFT) Consensus for Trust     |
+-----------------------------------------------------------------------+
```

---

## 2. Detailed Limitation Analysis

### 2.1 Storage Engine (VDR Persistence)
- **Current Realized State:** Local SQLite database (`vdr.db`) accessed via SQLAlchemy ORM.
- **Academic Boundary:** The system provides verifiable credential persistence locally. It does **NOT** currently execute smart contracts or write to an Ethereum / Hyperledger blockchain network. Blockchain integration is explicitly classified as **Future Scope**.

### 2.2 Telemetry Ingestion Boundary
- **Current Realized State:** Telemetry events are ingested via the `/api/v1/trust/telemetry` API endpoint.
- **Academic Boundary:** In the prototype execution, telemetry events are submitted by the test harness or client context. In production, telemetry generation must be enforced by an un-bypassable API Gateway proxy (such as Envoy or Kong) to sign latency and success metrics post-execution, preventing malicious agents from spoofing clean metrics.

### 2.3 Agent Model Execution
- **Current Realized State:** Local task connector (`akta/connectors.py`) processes task requests and simulates task latency/success outputs.
- **Academic Boundary:** Work outputs in collaboration steps and sequential workflows are structured task execution results, not live external LLM API (e.g. OpenAI / Anthropic) inference streams.

---

## 3. Future Scope Roadmap

1. **Distributed VDR Anchoring:** Replace/augment local SQLite storage with a decentralized ledger (e.g. Ceramic Network or L2 Ethereum) for tamper-evident DID document and credential revocation registration.
2. **Gateway-Enforced Telemetry Cryptography:** Implement an Envoy proxy sidecar that attaches cryptographic HMAC signatures to telemetry logs before dispatching to the Trust Engine.
3. **ZKP Credential Proofs:** Upgrade VC capabilities from full credential presentation to Zero-Knowledge Proof (ZKP) selective disclosure (e.g. proving skill authorization without exposing agent DID details).
