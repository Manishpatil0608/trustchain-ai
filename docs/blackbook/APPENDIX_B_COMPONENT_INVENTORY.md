# APPENDIX B: PROJECT COMPONENTS AND MODULE DESCRIPTION

This appendix provides an architectural inventory and module specification for the components comprising **TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**.

---

### B.1 — Frontend Component Architecture

The presentation layer is implemented as a modern React 19 Single Page Application (SPA) bundled via Vite 8. It features 17 view components providing real-time telemetry observation, dynamic policy visualization, interactive agent discovery, workflow creation, and cryptographic credential management. State management utilizes React hooks (`useState`, `useEffect`) and Context providers (`AuthContext`, `ThemeContext`), communicating with the backend over Axios with JWT Bearer injection.

---

### B.2 — Backend Subsystem Architecture

The application tier is powered by FastAPI 0.141 and Uvicorn 0.52. Request validation and serialization are handled via Pydantic v2 schemas. The API exposes 39 endpoints structured into four core modules: Authentication (`/auth`), Registry & Orchestration (`/registry`), Verifiable Data Registry (`/vdr`), and Health Probes (`/health`). Dependency injection enforces user session validation, lockout traps, and role-based access control.

---

### B.3 — Identity and Trust Intelligence Engines

- **DID Engine (`akta/did.py`):** Generates and verifies W3C `did:key` identifiers using PyNaCl Ed25519 bindings and multicodec formatting.
- **Verifiable Credential Engine (`akta/credentials.py`):** Assembles W3C VC v1.1 data models, executes URDNA2015 canonicalization via PyLD, and appends `Ed25519Signature2020` proofs.
- **Trust Scoring Engine (`akta/trust_engine.py`):** Calculates multi-factor performance scores ($P_i$) and updates temporal Exponential Moving Averages ($T_i$) across sliding observation windows ($n=10$).
- **Adaptive Policy Enforcer (`akta/adaptive_auth.py`):** Dynamically gates `PRIVILEGED` vs `STANDARD` operations according to live agent trust states.

---

### B.4 — Agent Registry, Collaboration, and Workflows

- **Agent Registry (`akta/vdr/registry_crud.py`):** Maintains operational status, capabilities, and health metrics for all participating agents.
- **Collaboration Manager:** Coordinates pairwise agent sessions, logs dialogue events, invokes `LocalAgentConnector` for structured simulation, and auto-submits telemetry.
- **Workflow Orchestrator:** Implements multi-step sequential execution pipelines, passing output data between dependent steps and enforcing pre-step trust checks.

---

### B.5 — Database and Persistence Layer

The Verifiable Data Registry is realized as a local relational SQLite database (`vdr.db`) operating in Write-Ahead Logging (`WAL`) mode. High-concurrency ACID transactions are managed via SQLAlchemy 2.0 ORM across 13 relational tables.

---

### B.6 — Authentication, RBAC, Governance, and Health

Human operator access is governed by Argon2id password hashing, short-lived JWT access tokens (30 min), and rotated refresh tokens (7 days) with replay-attack detection and 5-strike account lockouts. Comprehensive immutable logs are maintained across `security_audit_events` and `trust_audit_trails`. Subsystem health is actively monitored via `/health`.

---

### B.7 — Verified Technology Stack

| Layer | Technologies & Libraries | Verified Versions |
|---|---|---|
| **Presentation** | React, Vite, Recharts, Tailwind CSS, Lucide-React, Axios | React 19.2.8, Vite 8.2.2, Recharts 3.10.1, Tailwind 4.3.3 |
| **API & Core** | FastAPI, Uvicorn, Pydantic v2, Python | FastAPI 0.141.1, Uvicorn 0.52.4, Python 3.12.3 |
| **Security & Crypto** | PyNaCl, PyLD, PyJWT, passlib, argon2-cffi, base58 | PyNaCl 1.6.2, PyLD 3.2.0, PyJWT 2.14.0, Argon2 25.1.0 |
| **Persistence** | SQLite (WAL Mode), SQLAlchemy | SQLite 3, SQLAlchemy 2.0.52 |

---

### B.8 — Component Interaction Summary

When an operator initiates a task, the React frontend issues an authenticated Axios request carrying a JWT Bearer token to FastAPI. FastAPI verifies the user role (`ADMIN` or `OPERATOR`). The workflow engine resolves candidate agents via capability discovery and evaluates their real-time trust state using the `AdaptivePolicyEnforcer`. If trusted, the task is dispatched to the `LocalAgentConnector`. Upon completion, task metrics (success, compliance, latency) are ingested into `telemetry_logs`. The `TrustEngine` recomputes the sliding window performance score $P_i(t)$ and temporal EMA $T_i(t)$, updating `agent_trust_states` and logging state transitions in `trust_audit_trails`. Real-time metrics are streamed back to update the React dashboard.

---

## Required Inventory Tables

### Table B.1 — Frontend Component Inventory

| Component / Page | File Path | Responsibility | Related API / Service |
|---|---|---|---|
| `DashboardHome` | `frontend/src/components/DashboardHome.jsx` | KPI metric cards, trust trend charts, system overview | `/health`, `/registry/agents` |
| `AgentExplorer` | `frontend/src/components/AgentExplorer.jsx` | Agent registry roster, status toggles, trust badges | `/registry/agents` |
| `DiscoveryMatching` | `frontend/src/components/DiscoveryMatching.jsx` | Capability search, min-trust filtering, match ranking | `/registry/discover` |
| `TrustAnalytics` | `frontend/src/components/TrustAnalytics.jsx` | Temporal trust charts, factor breakdown, Recharts views | `/registry/agents/{id}/trust` |
| `TelemetryCenter` | `frontend/src/components/TelemetryCenter.jsx` | Telemetry injection UI and empirical observation logs | `/registry/agents/{id}/telemetry` |
| `CollaborationCenter`| `frontend/src/components/CollaborationCenter.jsx` | Session initiation, message exchanges, task tracking | `/registry/collaborate` |
| `WorkflowCenter` | `frontend/src/components/WorkflowCenter.jsx` | Sequential pipeline creation, step tracing, execution | `/registry/workflows` |
| `IdentityCredentials`| `frontend/src/components/IdentityCredentials.jsx`| DID:key genesis, VC issuance and proof verification | `/vdr/did`, `/vdr/credentials` |
| `AuditTrail` | `frontend/src/components/AuditTrail.jsx` | Security events and mathematical trust state trails | `/auth/audit-events` |
| `UserManagement` | `frontend/src/components/UserManagement.jsx` | RBAC admin, user creation, role assignment, lockout | `/auth/users` |

### Table B.2 — Backend Module Inventory

| Module / Router | File Path | Main Responsibility | Important Functions / Endpoints |
|---|---|---|---|
| `auth` | `akta/auth/router.py` | User authentication, token rotation, RBAC, lockout | `/auth/login`, `/auth/refresh`, `/auth/users` |
| `registry` | `akta/vdr/registry_router.py` | Agent lifecycle, telemetry, matching, workflows | `/registry/agents`, `/registry/telemetry`, `/registry/workflows` |
| `vdr` | `akta/vdr/router.py` | Cryptographic identity resolution, VC storage | `/vdr/did/generate`, `/vdr/credentials` |
| `trust_engine` | `akta/trust_engine.py` | Mathematical performance scoring and EMA updates | `calculate_behavioral_score()`, `calculate_temporal_trust()` |
| `adaptive_auth` | `akta/adaptive_auth.py` | Operation-level trust state gating and policy audits | `check_agent_authorization()`, `verify_request()` |
| `agent_connector` | `akta/agent_connector.py` | Deterministic local simulation & HTTP post fallback | `execute_agent_task()`, `send_task()` |
| `health` | `akta/server.py` | End-to-end multi-component probe and latency test | `/health` |

### Table B.3 — Database Component Inventory

| Table Name | Purpose | Primary Key | Important Relationships |
|---|---|---|---|
| `agents` | Registered agent profiles, capabilities, reputation | `agent_id` (PK, string) | 1:1 with `agent_trust_states`, 1:N with telemetry |
| `agent_trust_states` | Live temporal trust score ($T_i$) and state classification | `did` (PK, string) | Unique foreign key to `agents.did` |
| `telemetry_logs` | Empirical execution records ($S$, $C$, latency) | `id` (PK, string) | Foreign key to `agents.did` (indexed) |
| `trust_audit_trails` | Immutable history of trust score and state transitions | `id` (PK, string) | Foreign key to `agents.did` |
| `stored_vcs` | Persisted W3C JSON-LD Verifiable Credentials | `vc_id` (PK, string) | References `issuer_did` and `subject_did` |
| `collaboration_sessions` | Multi-agent collaborative session state and results | `session_id` (PK, string) | References `requester_did` and `target_did` |
| `collaboration_events` | Granular dialogue messages exchanged in sessions | `id` (PK, string) | Foreign key to `collaboration_sessions.session_id` |
| `workflows` | Chained multi-agent execution pipeline metadata | `workflow_id` (PK, string)| 1:N with `workflow_nodes` |
| `workflow_nodes` | Individual step definitions, assigned agent, and output | `node_id` (PK, string) | Foreign keys to `workflows` and `agents` |
| `users` | Human operator profiles, roles, and password hashes | `id` (PK, string) | 1:N with `refresh_tokens`, `security_audit_events` |
| `refresh_tokens` | Active JWT refresh tokens with rotation metadata | `id` (PK, string) | Foreign key to `users.id` |
| `security_audit_events`| Security and access-control event logging | `id` (PK, string) | Foreign key to `users.id` |
| `agent_ratings` | Peer feedback and reputation ratings (1.0 - 5.0) | `id` (PK, string) | Foreign key to `collaboration_sessions` |

### Table B.4 — Technology Stack

| Technology | Verified Version | Project Usage | Architectural Layer |
|---|---|---|---|
| Python | 3.12.3 | Core runtime environment | Backend / Systems |
| FastAPI | 0.141.1 | High-performance asynchronous REST API framework | API Gateway |
| Uvicorn | 0.52.4 | ASGI server hosting FastAPI applications | Server Hosting |
| SQLAlchemy | 2.0.52 | Relational database ORM and connection pooling | Persistence |
| SQLite (WAL) | 3.x (Built-in) | Embedded relational verifiable data registry | Persistence Store |
| PyNaCl | 1.6.2 | Libsodium bindings for Ed25519 signing and verification | Cryptography |
| PyLD | 3.2.0 | JSON-LD processing & URDNA2015 RDF normalization | Credential Integrity |
| PyJWT | 2.14.0 | JSON Web Token encoding, signing, and verification | Session Security |
| argon2-cffi | 25.1.0 | Memory-hard password hashing algorithm | Authentication |
| React | 19.2.8 | Declarative component UI framework | Presentation |
| Vite | 8.2.2 | Frontend build tooling and development server | Presentation Tooling |
| Recharts | 3.10.1 | Composable charting library for temporal trust visualizers | Data Visualization |
| Tailwind CSS | 4.3.3 | Utility-first CSS framework for modern responsive UI | Styling & Themes |

### Table B.5 — Security Component Inventory

| Component | Security Responsibility | Enforcement Location | Verification Evidence |
|---|---|---|---|
| `PasswordHasher` | Argon2id salted memory-hard password protection | `akta/auth/security.py` | `tests/test_authentication.py` |
| `JWTSessionGuard` | Short-lived access token gating and JTI rotation | `akta/auth/security.py` | `tests/test_authentication.py` |
| `AccountLockout` | 5-strike failed attempt lockout and cooldown trap | `akta/auth/crud.py` | `tests/test_authentication.py` |
| `RBACMiddleware` | Route-level role enforcement (`ADMIN`, `OPERATOR`, `VIEWER`) | `akta/auth/dependencies.py` | `tests/test_authentication.py` |
| `DIDKeyDeriver` | Cryptographic Ed25519 public key multi-codec genesis | `akta/did.py` | `tests/test_e2e_lifecycle.py` |
| `VCSignatureProof` | URDNA2015 JSON-LD hashing & `Ed25519Signature2020` | `akta/credentials.py` | `tests/test_e2e_lifecycle.py` |
| `AdaptivePolicyEnforcer`| Operation gating by trust state (`PRIVILEGED` vs `STANDARD`)| `akta/adaptive_auth.py` | `tests/test_adaptive_policy.py` |
| `BehavioralQuarantine`| Total exclusion of degraded agents ($T < 0.50$) | `akta/adaptive_auth.py` | `tests/test_e2e_lifecycle.py` |
| `AdminRevocation` | Terminal administrative revocation and lockout | `akta/vdr/registry_crud.py` | `tests/test_e2e_lifecycle.py` |
| `AuditLogger` | Tamper-evident logging of security and trust transitions | `akta/vdr/trust_crud.py` | `tests/test_adaptive_policy.py` |
