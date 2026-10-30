# TrustChain-AI — Comprehensive Viva Voce Preparation Guide (100 Questions & Answers)

**Project Title:** TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration  
**Repository:** `D:\capstone project\trustchain-ai\akta-base`  

---

## Group A: Project Fundamentals (Q1 – Q5)

### Q1: What is TrustChain-AI?
**Answer:** TrustChain-AI is a decentralized trust intelligence framework designed to secure multi-agent autonomous AI systems. It combines W3C `did:key` decentralized identities, W3C Verifiable Credentials (VCs), continuous behavioral telemetry monitoring, an Exponentially Weighted Moving Average (EWMA) trust engine, and dynamic adaptive authorization policy gateways.

### Q2: What core problem does TrustChain-AI solve?
**Answer:** Traditional security frameworks rely on static authentication (verifying credentials at login/request time). They fail to detect post-authentication compromise, behavioral degradation, or latency attacks. TrustChain-AI decouples identity verification from dynamic authorization by continuously scoring agent execution behavior.

### Q3: What are the main components of the TrustChain-AI architecture?
**Answer:** (1) React 19 SPA Frontend, (2) FastAPI Backend Gateway, (3) Argon2/JWT Human Auth Module, (4) W3C `did:key` & LDP VC Identity Engine, (5) EWMA Trust Engine, (6) Adaptive Policy Enforcer, (7) Multi-Agent Registry & Collaboration/Workflow Engine, and (8) SQLite Relational Storage (`vdr.db`).

### Q4: Is TrustChain-AI currently integrated with a live blockchain network?
**Answer:** No. TrustChain-AI currently uses a persistent local Verifiable Data Registry (VDR) backed by SQLite (`vdr.db`). Blockchain anchoring (e.g. Ethereum/Hedera L2) is explicitly classified as **Future Scope**.

### Q5: What is the primary novelty of this research project?
**Answer:** The primary novelty is the **dynamic revocation of authorization based on real-time behavioral trust decay** ($T_i < 0.50$), intercepting resource access even when an agent possesses a cryptographically valid, unexpired Verifiable Credential.

---

## Group B: Problem Statement & Motivation (Q6 – Q10)

### Q6: Why are static credentials insufficient for autonomous AI agents?
**Answer:** Autonomous AI agents make independent multi-step API calls over extended durations. If an agent is compromised, hijacked, or experiences software failure post-login, its static API key or credential remains valid, allowing malicious operations to continue undetected.

### Q7: What is a "confused deputy attack" in multi-agent systems?
**Answer:** A confused deputy attack occurs when a low-privilege or compromised agent trick a higher-privilege agent into executing unauthorized tasks on its behalf.

### Q8: How does TrustChain-AI mitigate the confused deputy problem?
**Answer:** By evaluating behavioral compliance ($C_i$) and enforcing trust checks on target agents during discovery and collaboration requests. Quarantined or suspicious agents are automatically filtered out during target matching.

### Q9: What metrics does TrustChain-AI use to measure agent behavior?
**Answer:** Three normalized metrics: Task Success Rate ($S_i \in [0,1]$), Protocol Compliance ($C_i \in [0,1]$), and Normalized Latency ($L_i \in [0,1]$).

### Q10: What is the relationship between security, compliance, and performance in the model?
**Answer:** Task success reflects functional correctness ($60\%$ weight), compliance reflects protocol integrity ($30\%$ weight), and latency reflects operational health ($10\%$ weight).

---

## Group C: Architecture & System Design (Q11 – Q15)

### Q11: Describe the end-to-end data flow when an agent requests a protected API resource.
**Answer:** (1) Agent presents VC in HTTP `Authorization: Bearer` header. (2) Gateway verifies VC signature with PyNaCl Ed25519 key. (3) `AdaptivePolicyEnforcer` queries `agent_trust_states` table for subject DID. (4) If state is `QUARANTINED` or `REVOKED`, request returns HTTP 403 Forbidden. (5) If `TRUSTED` or `SUSPICIOUS`, request executes. (6) Telemetry log is emitted and EWMA score is recalculated.

### Q12: How are backend services organized in FastAPI?
**Answer:** Mounted under `/api/v1` in `akta/server.py`: `auth_router` (`/auth`), `vdr_router` (`/vdr`, `/trust`), `registry_router` (`/registry`, `/collaboration`, `/workflows`), and `agent_router` (`/map/generate`).

### Q13: How does the frontend communicate with the backend?
**Answer:** Via Axios API client (`frontend/src/api.js`) directed to `http://localhost:8050/api/v1`, using request interceptors to automatically attach JWT bearer tokens.

### Q14: How is CORS handled?
**Answer:** FastAPI `CORSMiddleware` in `akta/server.py` explicitly allows origins `http://localhost:5173` and `http://127.0.0.1:5173` with `allow_credentials=True`.

### Q15: What is the execution model of the sequential workflow engine?
**Answer:** Sequential execution: Node 1 processes initial task description, records telemetry, and passes its output string as input to Node 2, continuing until all pipeline nodes complete or a node is blocked by policy.

---

## Group D: Decentralized Identity (DID) (Q16 – Q20)

### Q16: What DID method is implemented in TrustChain-AI?
**Answer:** W3C `did:key` method using base58btc multibase encoding of Ed25519 public keys.

### Q17: What is the format of a `did:key` string in the system?
**Answer:** Prefix `did:key:z6M...` where `z6M` is the multibase header for an Ed25519 public key fingerprint.

### Q18: How is a `did:key` generated in Python?
**Answer:** In `akta/did.py`: PyNaCl generates a 32-byte Ed25519 seed (`SigningKey.generate()`). The public key bytes are prefixed with multicodec header `0xed01` and encoded in base58btc with `z` prefix.

### Q19: Why use `did:key` instead of `did:ethr` or `did:web`?
**Answer:** `did:key` is self-certifying and completely offline — the DID string contains the public key itself, eliminating external blockchain or DNS network lookups during cryptographic verification.

### Q20: Can `did:web` be resolved by the system?
**Answer:** Yes, `akta/test_agent/router.py` includes helper functions `_resolve_did_web_verification_method` to resolve `did:web` JSON documents via HTTP/HTTPS.

---

## Group E: Verifiable Credentials (VCs) (Q21 – Q25)

### Q21: What VC specification does TrustChain-AI follow?
**Answer:** W3C Verifiable Credentials Data Model v1.1 using Linked Data Proofs (LDP).

### Q22: What is the proof suite used for VC signing?
**Answer:** `Ed25519Signature2020`.

### Q23: What information is contained in the `credentialSubject` block?
**Answer:** Subject agent DID (`id`) and a list of granted `skills` with `name`, `granted` boolean, and `scope` array (e.g. `["map:generate"]`).

### Q24: How is signature verification performed on a VC?
**Answer:** `VerifiableCredential.verify_signature` normalizes the JSON-LD document (RDF canonicalization via PyLD), reconstructs the signed payload bytes, and verifies the Ed25519 signature against the issuer's public key using PyNaCl (`VerifyKey.verify`).

### Q25: How are VCs transmitted in API calls?
**Answer:** Encoded as a Base64URL string of the JSON VC document and sent in the HTTP `Authorization: Bearer <token>` header.

---

## Group F: Verifiable Data Registry (VDR) (Q26 – Q30)

### Q26: What is the Verifiable Data Registry (VDR)?
**Answer:** The persistent storage repository that stores published VCs, mapping VC URN IDs to raw JSON-LD documents, issuer DIDs, and subject DIDs.

### Q27: What database table stores VCs?
**Answer:** `stored_vcs` table in `vdr.db`.

### Q28: How is a VC published to the VDR?
**Answer:** Via `POST /api/v1/vdr` passing the raw JSON-LD VC dictionary.

### Q29: How are VCs retrieved for a specific agent DID?
**Answer:** Via `GET /api/v1/vdr/credentials/subject/{did}` which queries `stored_vcs` filtered by `subject_did`.

### Q30: Is the VDR immutable?
**Answer:** In the current SQLite implementation, records are stored in relational tables. Immutable cryptographic verification is provided by verifying the Ed25519 signature inside the VC document itself.

---

## Group G: Cryptography & Security (Q31 – Q35)

### Q31: What key size is used for Ed25519 signing?
**Answer:** 256-bit (32-byte) private key seed and 256-bit (32-byte) public key.

### Q32: What password hashing algorithm is used for human operators?
**Answer:** Argon2id via `passlib.context.CryptContext`.

### Q33: How are JWT access tokens signed?
**Answer:** Using HMAC-SHA256 (`HS256`) with a 256-bit secret key configured in `akta/config.py`.

### Q34: How are refresh tokens protected against theft?
**Answer:** Refresh tokens are generated as high-entropy UUID hex strings, stored as SHA-256 hashes in the database (`refresh_sessions` table), and transmitted to the browser in HttpOnly, SameSite=Lax cookies.

### Q35: What happens if a refresh token is reused after rotation?
**Answer:** The `crud.rotate_refresh_token` logic detects reuse, revokes all active refresh sessions for that user ID, and logs a security audit event (`REFRESH_TOKEN_REUSE_DETECTED`).

---

## Group H: Trust Engine & Algorithm (Q36 – Q45)

### Q36: State the exact Instantaneous Performance Score equation.
**Answer:** $P_i(t) = 0.6 \cdot S_i(t) + 0.3 \cdot C_i(t) + 0.1 \cdot (1.0 - L_i(t))$.

### Q37: State the exact Temporal Trust Score update equation.
**Answer:** $T_i(t) = 0.7 \cdot P_i(t) + 0.3 \cdot T_i(t-1)$.

### Q38: Why is $\lambda = 0.7$ chosen for temporal decay?
**Answer:** $\lambda = 0.7$ gives $70\%$ weight to recent behavioral observations ($P_i$) and $30\%$ weight to historical trust ($T_{i-1}$), enabling rapid penalty detection while retaining historical context.

### Q39: How is Task Success Rate ($S_i$) calculated?
**Answer:** $S_i = \frac{\text{Successful Tasks}}{\text{Total Tasks in Window}}$. If window is empty, defaults to $1.0$.

### Q40: How is Protocol Compliance ($C_i$) calculated?
**Answer:** $C_i = \frac{\text{Compliant Tasks}}{\text{Total Tasks in Window}}$, where a task is compliant if `compliance_event` is null or false.

### Q41: How is Normalized Latency ($L_i$) calculated?
**Answer:** $L_i = \min\left(1.0, \max\left(0.0, \frac{\text{Average Latency (ms)}}{2000\text{ ms}}\right)\right)$.

### Q42: What are the exact state transition thresholds?
**Answer:** `TRUSTED` ($T \ge 0.80$), `SUSPICIOUS` ($0.50 \le T < 0.80$), `QUARANTINED` ($T < 0.50$).

### Q43: What is the `REVOKED` state?
**Answer:** An administrative terminal state manually set via `POST /api/v1/trust/revoke/{did}`. Unlike `QUARANTINED`, `REVOKED` agents cannot recover through clean telemetry.

### Q44: Can an agent recover from `QUARANTINED` to `TRUSTED`?
**Answer:** Yes. Submitting clean telemetry ($S=1, C=1, L=100\text{ms}$) dynamically increases $P_i(t)$, raising $T_i(t)$ back above $0.50$ (`SUSPICIOUS`) and $0.80$ (`TRUSTED`).

### Q45: Where is the trust engine implemented in code?
**Answer:** In `akta/trust_engine.py` (`TrustConfig` and `TrustEngine` classes) and `akta/vdr/trust_crud.py`.

---

## Group I: Behavioral Telemetry (Q46 – Q50)

### Q46: How is telemetry ingested by the system?
**Answer:** Via API request `POST /api/v1/trust/telemetry` containing `agent_did`, `task_id`, `success` (bool), `compliance_event` (bool), and `latency_ms` (int).

### Q47: What database table stores telemetry events?
**Answer:** `telemetry_logs` table in `vdr.db`.

### Q48: What is the current security limitation of telemetry ingestion?
**Answer:** The prototype `/trust/telemetry` endpoint accepts direct posts. In production, an API Gateway proxy must generate and sign telemetry post-execution to prevent agents from self-reporting fake success metrics.

### Q49: Does telemetry ingestion trigger immediate trust score updates?
**Answer:** Yes. `trust_crud.record_telemetry_and_update_trust` writes the log and immediately recalculates $P_i$ and $T_i$, updating `agent_trust_states` in a single transaction.

### Q50: How can telemetry be queried?
**Answer:** Via `GET /api/v1/trust/telemetry` (all logs) or `GET /api/v1/trust/telemetry/{did}` (agent-specific logs).

---

## Group J: Adaptive Authorization (Q51 – Q55)

### Q51: What class enforces adaptive authorization policies?
**Answer:** `AdaptivePolicyEnforcer` in `akta/adaptive_auth.py`.

### Q52: What is the difference between Authentication and Adaptive Authorization in TrustChain-AI?
**Answer:** Authentication verifies identity (is the VC signature valid?). Adaptive Authorization checks behavioral trust (is the subject DID's current score $T \ge 0.50$?).

### Q53: What HTTP status code is returned when authorization is denied due to trust decay?
**Answer:** `HTTP 403 Forbidden`.

### Q54: What exception detail message is returned for a Quarantined agent?
**Answer:** `"Trust Policy Violation: Agent {did} is currently QUARANTINED due to poor behavioral history."`

### Q55: What exception detail message is returned for a Revoked agent?
**Answer:** `"Trust Policy Violation: Agent {did} has been administratively REVOKED."`

---

## Group K: Agent Registry & Discovery (Q56 – Q60)

### Q56: What database table stores registered agents?
**Answer:** `agents` table in `vdr.db`.

### Q57: How are agents registered in the system?
**Answer:** Via `POST /api/v1/registry/agents` with `agent_name`, `agent_type`, and optional `did`. If DID is omitted, a fresh `did:key` is generated.

### Q58: How does agent discovery work?
**Answer:** `GET /api/v1/registry/discover?capability={cap}` queries `agents` matching capability string, filtering by active status (`AVAILABLE`).

### Q59: How does Trust-Aware Matching select candidate agents?
**Answer:** In `registry_crud.discover_free_agents`: Candidates are filtered to exclude `QUARANTINED` and `REVOKED` DIDs, then sorted by highest combined score: $\text{Match Score} = T_i + \text{Reputation} + \text{Health}$.

### Q60: What operational statuses can an agent have?
**Answer:** `AVAILABLE`, `BUSY`, or `OFFLINE`.

---

## Group L: Agent Health Monitoring (Q61 – Q65)

### Q61: What health statuses exist for registered agents?
**Answer:** `HEALTHY`, `UNHEALTHY`, or `OFFLINE`.

### Q62: How is agent health tracked?
**Answer:** The `agents` table stores `health_status`, `last_health_check`, `last_response_time_ms`, and `last_error`.

### Q63: What happens if a workflow node agent is `UNHEALTHY`?
**Answer:** `registry_crud.execute_workflow` halts execution for that node, marks node status `FAILED`, updates workflow status `FAILED`, and returns `HTTP 503 Service Unavailable`.

### Q64: How does reputation score relate to agent registry?
**Answer:** Agents maintain a `reputation_score` ($1.0$ to $5.0$, default $5.0$) updated via peer rating feedback (`POST /api/v1/collaboration/rate`).

### Q65: Where can platform registry stats be viewed?
**Answer:** Via `GET /api/v1/registry/stats` or on the **System Health** dashboard (`/health`).

---

## Group M: Agent-to-Agent Collaboration (Q66 – Q70)

### Q66: How is a collaboration session initiated?
**Answer:** Via `POST /api/v1/collaboration/request` passing `requester_did`, `target_did`, `task_description`, and `required_capability`.

### Q67: What security checks occur during collaboration session creation?
**Answer:** The target DID's trust state is checked. If target is `QUARANTINED` or `REVOKED`, request returns `HTTP 403 Forbidden`. If `BUSY` or `OFFLINE`, returns `HTTP 400 Bad Request`.

### Q68: What database tables store collaboration sessions and events?
**Answer:** `collaboration_sessions` and `collaboration_events`.

### Q69: How is a work step executed in a collaboration session?
**Answer:** Via `POST /api/v1/collaboration/sessions/{session_id}/step` with `sender_did` and `content`.

### Q70: Is telemetry recorded during collaboration steps?
**Answer:** Yes. `registry_crud.execute_session_step` dispatches work via `connector_factory`, emits telemetry, and updates trust scores.

---

## Group N: Sequential Multi-Agent Workflows (Q71 – Q75)

### Q71: How is a workflow created in TrustChain-AI?
**Answer:** Via `POST /api/v1/workflows` specifying `workflow_name`, `task_description`, `orchestrator_did`, `pattern` (`SEQUENTIAL`), and an array of `nodes`.

### Q72: What database tables store workflows?
**Answer:** `workflows` and `workflow_nodes`.

### Q73: How is a workflow executed?
**Answer:** Via `POST /api/v1/workflows/{workflow_id}/execute`.

### Q74: How does data flow between sequential workflow nodes?
**Answer:** Node 1 receives the workflow `task_description` as `input_data`. Its `output_data` string is passed as `input_data` to Node 2, forming a chained pipeline.

### Q75: What happens if Node 2 in a workflow belongs to a Quarantined agent?
**Answer:** Execution stops at Node 2. Node status becomes `BLOCKED`, workflow status becomes `TERMINATED`, and API returns `HTTP 403 Forbidden` with detail `"Workflow Policy Interception: Node Agent is in QUARANTINED state."`

---

## Group O: Audit Logging & Governance (Q76 – Q80)

### Q76: What database tables store audit logs?
**Answer:** `trust_audit_trails` (Agent trust state shifts) and `security_audit_events` (Human auth events).

### Q77: What fields are stored in `trust_audit_trails`?
**Answer:** `id`, `agent_did`, `previous_state`, `new_state`, `reason` (including numerical score delta), and `timestamp`.

### Q78: What fields are stored in `security_audit_events`?
**Answer:** `id`, `user_id`, `username`, `event_type` (e.g. `LOGIN_SUCCESS`, `LOGIN_FAILED`), `details`, `ip_address`, `user_agent`, and `timestamp`.

### Q79: How is the agent audit trail queried?
**Answer:** Via `GET /api/v1/trust/audit/{did}` or `GET /api/v1/trust/audit`.

### Q80: How is the human security audit log queried?
**Answer:** Via `GET /api/v1/auth/audit?limit=50` (requires Bearer JWT with `ADMIN` role).

---

## Group P: FastAPI Backend Architecture (Q81 – Q85)

### Q81: How is the FastAPI application created?
**Answer:** In `akta/server.py` via `create_app()` factory function which initializes database tables and registers API routers.

### Q82: What routers are mounted in the FastAPI app?
**Answer:** `auth_router`, `vdr_router`, `registry_router`, `agent_router`.

### Q83: What middleware is applied to FastAPI requests?
**Answer:** Security headers & request ID middleware (`add_security_headers_and_request_id`) and `CORSMiddleware`.

### Q84: How is database dependency injected in FastAPI endpoints?
**Answer:** Using `db: Session = Depends(get_db)` from `akta/vdr/database.py`.

### Q85: What command starts the backend server?
**Answer:** `python -m uvicorn akta.server:app --host 0.0.0.0 --port 8050`.

---

## Group Q: React 19 Frontend Architecture (Q86 – Q90)

### Q86: What framework powers the frontend SPA?
**Answer:** React 19, Vite 8, Tailwind CSS, Lucide React icons, and Recharts visualization library.

### Q87: How is client-side routing implemented?
**Answer:** Using `react-router-dom` v7 `BrowserRouter`, `Routes`, and `Route` in `frontend/src/App.jsx`.

### Q88: How is global auth state managed in React?
**Answer:** Via `AuthProvider` context in `frontend/src/context/AuthContext.jsx` storing token and user state.

### Q89: How does the frontend handle token expiration?
**Answer:** Axios response interceptor in `frontend/src/api.js` catches HTTP 401, calls `/auth/refresh` using HttpOnly cookie, updates token, and retries the failed request seamlessly.

### Q90: What command builds the frontend for production?
**Answer:** `npm run build` inside `frontend/` directory.

---

## Group R: Authentication & RBAC (Q91 – Q93)

### Q91: What user roles exist in TrustChain-AI?
**Answer:** `ADMIN`, `OPERATOR`, and `VIEWER`.

### Q92: Which endpoints require `ADMIN` role?
**Answer:** `/api/v1/auth/users` (User creation, status updates, session revocation) and `/api/v1/auth/audit`.

### Q93: How is account lockout enforced?
**Answer:** After 5 failed password attempts, `crud.authenticate_user` locks the account for 15 minutes (`settings.account_lockout_minutes`), returning HTTP 401 `"Account is locked"`.

---

## Group S: Testing & Validation (Q94 – Q96)

### Q94: How many unit/integration tests exist in the test suite?
**Answer:** 63 tests across 9 test files in `tests/`.

### Q95: What command runs the backend test suite?
**Answer:** `pytest -q`.

### Q96: What is the current test result?
**Answer:** **63 PASSED, 0 FAILED** (Pass rate: $100\%$).

---

## Group T: Limitations & Security Boundaries (Q97 – Q98)

### Q97: What is the primary architectural limitation of the prototype?
**Answer:** Storage is managed in local SQLite (`vdr.db`) rather than a distributed blockchain, and telemetry ingestion requires an API Gateway proxy in production to sign metrics.

### Q98: Can an agent manipulate its own trust score in the current prototype?
**Answer:** In the prototype without an API gateway proxy, any entity with network access to `/trust/telemetry` can post telemetry. This boundary is explicitly documented as a **Limitation / Future Scope**.

---

## Group U: Future Scope & Extensions (Q99 – Q100)

### Q99: What is the future scope for VDR storage?
**Answer:** Anchoring DID documents and VC revocation lists to a public or enterprise blockchain (e.g., Ethereum L2 or Hedera Hashgraph).

### Q100: What is the future scope for AI agent execution verification?
**Answer:** Integrating TEE (Trusted Execution Environments) or Zero-Knowledge Proofs (ZK-SNARKs) to cryptographically attest to model execution integrity alongside telemetry scoring.
