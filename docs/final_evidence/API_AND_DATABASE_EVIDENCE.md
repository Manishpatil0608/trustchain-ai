# API and Database Evidence Report

**Project:** TrustChain-AI  
**Database File:** `D:\capstone project\trustchain-ai\akta-base\vdr.db`  
**ORM Engine:** SQLAlchemy 2.0  

---

## 1. Implemented Database Schema Evidence

| Table Name | Entity Purpose | Primary Key | Key Columns | Indexes |
| :--- | :--- | :--- | :--- | :--- |
| `stored_vcs` | Verifiable Credential Store | `vc_id` | `ldp_vc_json`, `issuer_did`, `subject_did`, `issuance_date`, `expiration_date` | `issuer_did`, `subject_did` |
| `agent_trust_states` | Active Agent Trust State | `did` | `temporal_trust_score`, `trust_state`, `last_updated` | `did` |
| `telemetry_logs` | Raw Ingested Telemetry Logs | `id` | `agent_did`, `task_id`, `success`, `compliance_event`, `latency_ms`, `timestamp` | `agent_did`, `task_id` |
| `trust_audit_trails` | Audit Log for State Shifts | `id` | `agent_did`, `previous_state`, `new_state`, `reason`, `timestamp` | `agent_did` |
| `agents` | Agent Registry Directory | `agent_id` | `did`, `agent_name`, `agent_type`, `status`, `health_status`, `reputation_score` | `did`, `agent_id` |
| `collaboration_sessions` | Inter-Agent Sessions | `session_id` | `requester_did`, `target_did`, `task_description`, `status`, `productivity_score` | `requester_did`, `target_did` |
| `collaboration_events` | Collaboration Work Messages | `id` | `session_id`, `sender_did`, `receiver_did`, `message_type`, `content`, `timestamp` | `session_id`, `sender_did` |
| `agent_ratings` | Peer Reputation Feedback | `id` | `session_id`, `rater_did`, `target_did`, `rating`, `feedback`, `timestamp` | `session_id`, `target_did` |
| `workflows` | Multi-Agent Pipelines | `workflow_id` | `workflow_name`, `task_description`, `orchestrator_did`, `pattern`, `status` | `orchestrator_did` |
| `workflow_nodes` | Pipeline Execution Nodes | `node_id` | `workflow_id`, `agent_did`, `step_order`, `status`, `input_data`, `output_data` | `workflow_id`, `agent_did` |
| `users` | Human Operators | `id` | `username`, `email`, `password_hash`, `role`, `is_active` | `username`, `email` |
| `refresh_sessions` | Auth Refresh Token Sessions| `id` | `user_id`, `token_hash`, `user_agent`, `client_ip`, `expires_at`, `is_revoked` | `user_id` |
| `security_audit_events` | Human Security Log | `id` | `user_id`, `username`, `event_type`, `details`, `ip_address`, `timestamp` | `user_id`, `username` |

---

## 2. API Endpoint Evidence Table

| Endpoint | Method | Router Module | Purpose | Observed HTTP Status |
| :--- | :-: | :--- | :--- | :-: |
| `/health` | `GET` | `server.py` | Backend Server Health Check | **200 OK** |
| `/api/v1/auth/login` | `POST` | `auth/router.py` | Human User Authentication & JWT Issuance | **200 OK** |
| `/api/v1/auth/refresh` | `POST` | `auth/router.py` | JWT Access Token Refresh Rotation | **200 OK** |
| `/api/v1/auth/logout` | `POST` | `auth/router.py` | Session Revocation | **200 OK** |
| `/api/v1/auth/me` | `GET` | `auth/router.py` | Current Authenticated User Profile | **200 OK** |
| `/api/v1/auth/users` | `GET` | `auth/router.py` | User Governance List (Admin Role) | **200 OK** |
| `/api/v1/auth/audit` | `GET` | `auth/router.py` | Security Audit Event Feed | **200 OK** |
| `/api/v1/registry/agents` | `GET`/`POST`| `vdr/registry_router.py` | List Registered Agents / Register Agent | **200 OK** |
| `/api/v1/registry/discover` | `GET` | `vdr/registry_router.py` | Trust-Aware Agent Discovery | **200 OK** |
| `/api/v1/vdr` | `POST` | `vdr/router.py` | Publish W3C LDP VC to Registry | **200 OK** |
| `/api/v1/vdr/credentials/subject/{did}`| `GET` | `vdr/router.py` | Retrieve VCs for DID Subject | **200 OK** |
| `/api/v1/trust/state/{did}` | `GET` | `vdr/router.py` | Fetch Temporal Trust Score & State | **200 OK** |
| `/api/v1/trust/telemetry` | `POST` | `vdr/router.py` | Ingest Telemetry & Recalculate EWMA Trust | **200 OK** |
| `/api/v1/trust/revoke/{did}` | `POST` | `vdr/router.py` | Administrative Terminal Revocation | **200 OK** |
| `/api/v1/trust/audit/{did}` | `GET` | `vdr/router.py` | Fetch Agent State Transition Audit Log | **200 OK** |
| `/api/v1/collaboration/request` | `POST` | `vdr/registry_router.py` | Create Inter-Agent Collaboration Session | **200 OK** |
| `/api/v1/collaboration/sessions/{id}/step`| `POST` | `vdr/registry_router.py` | Execute Collaboration Work Step | **200 OK** |
| `/api/v1/workflows` | `GET`/`POST`| `vdr/registry_router.py` | List / Create Sequential Workflows | **200 OK** |
| `/api/v1/workflows/{id}/execute` | `POST` | `vdr/registry_router.py` | Execute Multi-Agent Workflow Pipeline | **200 OK** |
| `/api/v1/map/generate` | `POST` | `test_agent/router.py` | Target API Enforcing VC & Adaptive Trust Policy | **200 OK / 403 Forbidden** |
