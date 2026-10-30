# Implementation Baseline Report

**Project Title:** TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration  
**Repository Path:** `D:\capstone project\trustchain-ai\akta-base`  
**Git Branch:** `feature/trustchain-ai`  
**Baseline Date:** September 28, 2026  

---

## 1. Environment & Architecture Overview

TrustChain-AI is structured as a decoupled, full-stack security architecture:

- **Backend Framework:** FastAPI (Python 3.12) running on `http://127.0.0.1:8050`
- **Frontend Framework:** React 19 (Vite 8 SPA) running on `http://localhost:5173`
- **Database Engine:** SQLite (`vdr.db`) via SQLAlchemy 2.0 ORM
- **Cryptographic Suite:** W3C `did:key` base58btc Multibase + W3C Linked Data Proofs (LDP VC with Ed25519 signatures via PyNaCl)
- **Trust Engine:** Exponentially Weighted Moving Average (EWMA) dynamic trust model with 4 discrete trust states (`TRUSTED`, `SUSPICIOUS`, `QUARANTINED`, `REVOKED`)

---

## 2. Source Code Inventory

### 2.1 Backend Modules (`akta/`)
- `akta/server.py`: Application factory, CORS middleware (`localhost:5173`), route mounting
- `akta/config.py`: Pydantic settings schema (`app_name`, `host`, `port`, `secret_key`, admin credentials)
- `akta/logging.py`: Structured JSON logger and request ID middleware
- `akta/did.py`: W3C `did:key` Ed25519 keypair generator, base58btc multibase encoding/decoding
- `akta/credentials.py`: W3C Verifiable Credential builder & PyNaCl Ed25519 Linked Data Proof signer
- `akta/trust_engine.py`: TrustConfig model, TrustEngine calculator ($P_i$, $T_i$), TrustState Enum
- `akta/telemetry.py`: TelemetryEvent dataclass and TestHarnessTelemetrySource ingestion
- `akta/adaptive_auth.py`: AdaptivePolicyEnforcer class enforcing trust state checks
- `akta/connectors.py`: Task Execution Connector for inter-agent work dispatch
- `akta/models.py`: Pydantic data schemas for DIDs, VCs, skills, and API requests
- `akta/test_agent/router.py`: Execution test harness (`POST /map/generate`) enforcing VC & trust policies

### 2.2 Auth Module (`akta/auth/`)
- `akta/auth/router.py`: Login, Refresh, Logout, User Management, Audit endpoints
- `akta/auth/crud.py`: User authentication, password hashing (Argon2), lockout logic, session creation
- `akta/auth/security.py`: Passlib password verification and JWT token creation/decoding
- `akta/auth/schemas.py`: Pydantic models for authentication requests and responses
- `akta/auth/dependencies.py`: FastAPI `get_current_user` and `require_role` dependencies

### 2.3 VDR & Registry Module (`akta/vdr/`)
- `akta/vdr/database.py`: SQLAlchemy engine, session maker (`SessionLocal`), base class (`Base`)
- `akta/vdr/models.py`: 13 database table models (`stored_vcs`, `agent_trust_states`, `telemetry_logs`, `trust_audit_trails`, `agents`, `collaboration_sessions`, `collaboration_events`, `agent_ratings`, `workflows`, `workflow_nodes`, `users`, `refresh_sessions`, `security_audit_events`)
- `akta/vdr/crud.py`: Verifiable Credential store CRUD operations
- `akta/vdr/trust_crud.py`: Trust calculation updates and state transition audit record creation
- `akta/vdr/registry_crud.py`: Agent registration, discovery, trust-aware matching, collaboration execution, and sequential workflows
- `akta/vdr/router.py`: VDR API endpoints (`/vdr`, `/trust/telemetry`, `/trust/state/{did}`, `/trust/revoke/{did}`)
- `akta/vdr/registry_router.py`: Agent registry, collaboration, and workflow API endpoints

### 2.4 Frontend Views (`frontend/src/`)
- `frontend/src/App.jsx`: SPA Router mapping all 14 visual dashboards
- `frontend/src/api.js`: Axios API client with automatic JWT token attachment and HTTP 401 refresh handling
- `frontend/src/context/AuthContext.jsx`: React context managing user authentication state
- `frontend/src/components/`:
  1. `DashboardHome.jsx`: Command Center overview & active security metrics
  2. `AgentExplorer.jsx`: Agent Directory & health status indicators
  3. `AgentDetails.jsx`: Individual Agent Deep-Dive, VC card, and trust score history
  4. `TrustAnalytics.jsx`: Global trust state distribution & decay visualization
  5. `TelemetryCenter.jsx`: Real-time telemetry log feed & ingest form
  6. `IdentityCredentials.jsx`: VC Issuance, verification, and JSON-LD viewer
  7. `AuthorizationVisualizer.jsx`: VC Bearer token policy enforcement simulator
  8. `AuditTrail.jsx`: Immutable trust state transition logs & human security audit trail
  9. `CollaborationCenter.jsx`: Inter-Agent collaboration requester & step runner
  10. `WorkflowCenter.jsx`: Sequential multi-agent pipeline builder & execution engine
  11. `StateTransitionMap.jsx`: Dynamic trust state machine flowchart & rule explanation
  12. `SystemHealth.jsx`: API Gateway & backend endpoint health status monitor
  13. `UserManagement.jsx`: Admin governance for human operators & RBAC roles
  14. `DemoVisualizer.jsx`: Live demonstration visualizer syncing agent trust states in real-time
  15. `LoginPage.jsx`: Human operator authentication portal
  16. `ui/States.jsx`: Reusable trust state badges and UI components

---

## 3. Baseline Verification Status

- **Backend Test Suite (`pytest -q`):** **63 PASSED, 0 FAILED** (Execution time: 9.08s)
- **Frontend Production Build (`npm run build`):** **SUCCESS** (Built 2473 modules in 15.08s)
- **Deployment Mode:** Strict Two-Terminal Architecture (Terminal 1: Uvicorn, Terminal 2: Vite)
