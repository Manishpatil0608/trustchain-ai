# TrustChain-AI — Complete API Endpoint Inventory

Generated from source inspection of:
- `akta/vdr/registry_router.py` (363 lines)
- `akta/vdr/router.py` (293 lines)
- `akta/auth/router.py`
- `akta/server.py`

---

## Authentication Module (`/auth`)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register a new user (admin only, first user auto-admin) |
| POST | `/auth/login` | Authenticate user, returns access + refresh JWT pair |
| POST | `/auth/refresh` | Rotate refresh token, issue new access token |
| POST | `/auth/logout` | Revoke refresh token (blacklist via DB) |
| GET  | `/auth/me` | Return current authenticated user profile |
| GET  | `/auth/users` | List all users (admin only) |
| POST | `/auth/users` | Create user (admin only) |
| PUT  | `/auth/users/{user_id}` | Update user status/role (admin only) |
| GET  | `/auth/audit-events` | List security audit events (admin/operator) |

---

## Agent Registry Module (`/registry`)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/registry/agents` | Register new agent with DID, capabilities, endpoint |
| GET  | `/registry/agents` | List all agents with optional status filter |
| GET  | `/registry/agents/{agent_id}` | Get single agent details |
| PUT  | `/registry/agents/{agent_id}` | Update agent metadata |
| DELETE | `/registry/agents/{agent_id}` | Remove agent from registry |
| POST | `/registry/agents/{agent_id}/telemetry` | Submit telemetry event → triggers trust recalculation |
| GET  | `/registry/agents/{agent_id}/trust` | Get current trust score + state for agent |
| GET  | `/registry/agents/{agent_id}/trust-audit` | Get trust state transition audit trail |
| POST | `/registry/agents/{agent_id}/revoke` | Administrative trust revocation (REVOKED state) |
| POST | `/registry/discover` | Discover matching agents for a task (capability + trust filtering) |
| POST | `/registry/authorize` | Check adaptive authorization for operation |
| POST | `/registry/collaborate` | Initiate collaboration session between two agents |
| GET  | `/registry/collaborations/{session_id}` | Get collaboration session details |
| POST | `/registry/collaborations/{session_id}/message` | Send message within collaboration session |
| POST | `/registry/collaborations/{session_id}/complete` | Mark collaboration as complete |
| POST | `/registry/workflows` | Create workflow with sequential node steps |
| GET  | `/registry/workflows/{workflow_id}` | Get workflow status and node results |
| POST | `/registry/workflows/{workflow_id}/execute` | Execute workflow (orchestrate nodes via LocalAgentConnector) |
| GET  | `/registry/agents/{agent_id}/ratings` | Get ratings for an agent |
| POST | `/registry/agents/{agent_id}/rate` | Submit a rating (1.0–5.0) for an agent |

---

## VDR / Credential Module (`/vdr`)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/vdr/credentials` | Issue and store a Verifiable Credential (Ed25519Signature2020) |
| GET  | `/vdr/credentials` | List stored VCs with optional issuer/subject filter |
| GET  | `/vdr/credentials/{vc_id}` | Retrieve single VC by ID |
| DELETE | `/vdr/credentials/{vc_id}` | Revoke/delete a VC |
| POST | `/vdr/did/generate` | Generate a new DID:key with Ed25519 keypair |
| POST | `/vdr/did/resolve` | Resolve a DID:key to its DID Document |
| POST | `/vdr/did/verify` | Verify an Ed25519 signature against a DID:key |

---

## Core / Health Module

| Method | Path | Description |
|--------|------|-------------|
| GET  | `/health` | System health check (FastAPI + SQLite VDR + Trust Math Core) |
| GET  | `/` | Root redirect / welcome |

---

## Notes

- All `/registry` and `/vdr` endpoints require Bearer JWT authentication (except health)
- Role-based access: ADMIN can access all; OPERATOR can access most; VIEWER read-only
- `/registry/agents/{id}/revoke` requires ADMIN role
- Telemetry submission returns updated trust score and new trust state
