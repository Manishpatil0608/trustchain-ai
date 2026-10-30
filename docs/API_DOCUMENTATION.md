# TrustChain-AI: REST API Documentation

**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**

Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
Academic Session: 2026–2027  
Repository: `https://github.com/Manishpatil0608/trustchain-ai`

---

## 1. Overview & Interactive Documentation

TrustChain-AI exposes **39 authoritative REST endpoints** structured under the `/api/v1` namespace, alongside system health probes and interactive OpenAPI specifications:

- **Interactive Swagger UI:** [http://127.0.0.1:8050/docs](http://127.0.0.1:8050/docs)
- **ReDoc Technical Specification:** [http://127.0.0.1:8050/redoc](http://127.0.0.1:8050/redoc)
- **OpenAPI JSON Schema:** [http://127.0.0.1:8050/openapi.json](http://127.0.0.1:8050/openapi.json)
- **Subsystem Health Probe:** [http://127.0.0.1:8050/health](http://127.0.0.1:8050/health)

---

## 2. Global Request & Response Specifications

### Standard Headers
All HTTP responses include security and traceability headers injected via middleware (`akta/server.py`):
- `X-Request-ID`: Unique UUID tracking each transaction through logs.
- `X-Content-Type-Options`: `nosniff`
- `X-Frame-Options`: `DENY`
- `Referrer-Policy`: `strict-origin-when-cross-origin`

### Authentication Header
Protected administrative and operator endpoints require a valid JWT Bearer token:
```http
Authorization: Bearer <access_token>
```

---

## 3. Comprehensive Endpoint Inventory

### A. Authentication & Access Control (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/v1/auth/login` | Authenticates username/password; returns JWT access token and sets HTTP-only refresh cookie. | None |
| `POST` | `/api/v1/auth/logout` | Revokes the current refresh token session and clears credentials. | None |
| `GET` | `/api/v1/auth/me` | Returns profile details and role of the currently authenticated user. | Bearer JWT |
| `POST` | `/api/v1/auth/refresh` | Rotates refresh token and issues a new access token (with reuse detection). | Cookie |
| `POST` | `/api/v1/auth/change-password` | Updates authenticated user password and revokes all active refresh sessions. | Bearer JWT |
| `GET` | `/api/v1/auth/users` | Lists registered user accounts with pagination. | `ADMIN`, `OPERATOR` |
| `POST` | `/api/v1/auth/users` | Creates a new user account with assigned role. | `ADMIN` |
| `PATCH` | `/api/v1/auth/users/{user_id}/status` | Updates user status (active/disabled) or changes RBAC role. | `ADMIN` |
| `POST` | `/api/v1/auth/users/{user_id}/revoke-sessions` | Administratively revokes all active refresh sessions for a user. | `ADMIN` |
| `GET` | `/api/v1/auth/audit` | Retrieves security audit events (logins, lockouts, role changes). | `ADMIN`, `OPERATOR` |

---

### B. Agent Registry & Catalog (`/api/v1/registry`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/v1/registry/agents` | Registers a new autonomous agent; generates or validates W3C `did:key`. | None / Optional |
| `GET` | `/api/v1/registry/agents` | Lists registered agents with capability and status query filters. | None |
| `GET` | `/api/v1/registry/agents/{did_or_id}` | Retrieves deep profile of a specific agent including DID and health metrics. | None |
| `POST` | `/api/v1/registry/agents/{did_or_id}/health` | Triggers a live responsiveness health check probe on an agent endpoint. | None |
| `POST` | `/api/v1/registry/agents/{did}/status` | Updates an agent's operational status (`AVAILABLE`, `BUSY`, `OFFLINE`). | None |
| `GET` | `/api/v1/registry/discover` | Discovers eligible candidate agents based on capabilities and min trust. | None |
| `POST` | `/api/v1/registry/matching` | Evaluates task requirements and ranks eligible candidates via composite scoring. | None |
| `GET` | `/api/v1/registry/stats` | Returns aggregate network statistics (total agents, active sessions, trust distribution). | None |

---

### C. Behavioral Telemetry & Trust Engine (`/api/v1/trust`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/v1/trust/telemetry` | Ingests a runtime telemetry observation (success, compliance, latency); recalculates trust. | None / Agent |
| `GET` | `/api/v1/trust/telemetry` | Returns the 100 most recent system-wide telemetry observations. | None |
| `GET` | `/api/v1/trust/telemetry/{did}` | Returns historical telemetry stream specifically for the target agent DID. | None |
| `GET` | `/api/v1/trust/state/{did}` | Computes and returns current temporal trust score ($T_i(t)$) and trust state. | None |
| `GET` | `/api/v1/trust/agents` | Lists all agents with their active trust scores and state machine classifications. | None |
| `GET` | `/api/v1/trust/audit` | Retrieves recent state machine transition audit records across all agents. | None |
| `GET` | `/api/v1/trust/audit/{did}` | Retrieves complete lifecycle transition history for a specific agent DID. | None |
| `POST` | `/api/v1/trust/revoke/{did}` | Administratively revokes/quarantines an agent; terminal transition. | `ADMIN` |
| `GET` | `/api/v1/trust/dashboard` | Returns built-in lightweight HTML status dashboard for quick diagnostics. | None |

---

### D. Verifiable Data Registry (VDR) & Decentralized Identity (`/api/v1/vdr`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/v1/vdr` | Stores an issued W3C Verifiable Credential in the local registry. | None |
| `GET` | `/api/v1/vdr/{vc_id_path}` | Retrieves a Verifiable Credential by its unique credential identifier. | None |
| `GET` | `/api/v1/vdr/credentials/subject/{did}` | Retrieves all active Verifiable Credentials issued to a specific subject DID. | None |

---

### E. Multi-Agent Collaboration Center (`/api/v1/collaboration`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/v1/collaboration/request` | Initiates a collaboration session between a requester DID and target DID. | None |
| `GET` | `/api/v1/collaboration/sessions` | Lists active and historical multi-agent collaboration sessions. | None |
| `GET` | `/api/v1/collaboration/sessions/{session_id}`| Returns session details, exchanged messages, status, and productivity score. | None |
| `POST` | `/api/v1/collaboration/sessions/{session_id}/step` | Executes an inter-agent collaborative task step / payload exchange. | None |
| `POST` | `/api/v1/collaboration/sessions/{session_id}/terminate`| Terminates an ongoing collaboration session early. | None |
| `POST` | `/api/v1/collaboration/rate` | Submits post-collaboration peer evaluation feedback and numerical rating (1-5). | None |

---

### F. Multi-Agent Workflows (`/api/v1/workflows`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `POST` | `/api/v1/workflows` | Registers a multi-agent sequential or parallel execution DAG. | None |
| `GET` | `/api/v1/workflows` | Lists all registered workflows and their operational statuses. | None |
| `GET` | `/api/v1/workflows/{workflow_id}` | Retrieves workflow execution graph, intermediate node statuses, and outputs. | None |
| `POST` | `/api/v1/workflows/{workflow_id}/execute` | Executes workflow steps sequentially; verifies trust-gating at each node. | None |

---

### G. System Health & Agent Discovery Specifications (`/health`, `/.well-known`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/health` | Authoritative subsystem health probe (FastAPI, SQLite VDR, Trust Math Core). | None |
| `GET` | `/api/v1/.well-known/agent.json` | Returns standard A2A Agent Card specification discovery document. | None |
| `POST` | `/api/v1/map/generate` | Demonstration tool execution endpoint; gated by Zero-Trust policy enforcer. | None |

---

## 4. Example API Invocations

### 1. Check Subsystem Health
```bash
curl -X GET http://127.0.0.1:8050/health
```
**Sample Response:**
```json
{
  "status": "ok",
  "app_name": "TrustChain-AI Platform",
  "timestamp": "2026-10-30T13:44:53.985Z",
  "version": "1.0.0",
  "components": {
    "fastapi": {
      "status": "ok",
      "port": 8050
    },
    "database": {
      "status": "ok",
      "engine": "sqlite",
      "mode": "WAL",
      "latency_ms": 0.42
    },
    "trust_engine": {
      "status": "ok",
      "mode": "in-process",
      "weights": {
        "w1_success": 0.6,
        "w2_compliance": 0.3,
        "w3_latency": 0.1,
        "decay_lambda": 0.7
      }
    }
  }
}
```

### 2. Ingest Telemetry Event
```bash
curl -X POST http://127.0.0.1:8050/api/v1/trust/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "agent_did": "did:key:z6MkhuSorXLwrvz78x6sJTBt7sFrezXuscKfbngGLfk3utFf",
    "task_id": "task_demo_01",
    "success": true,
    "compliance_event": null,
    "latency_ms": 145
  }'
```

### 3. Match Best Candidate Agents
```bash
curl -X POST http://127.0.0.1:8050/api/v1/registry/matching \
  -H "Content-Type: application/json" \
  -d '{
    "required_capability": "processing",
    "task_description": "Aggregate statistical metrics across edge sensor logs",
    "min_trust_score": 0.80
  }'
```
