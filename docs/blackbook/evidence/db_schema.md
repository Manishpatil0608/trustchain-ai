# TrustChain-AI — Database Schema (14 Tables)

Source: `akta/vdr/models.py` (194 lines), `akta/auth/` models
Database: SQLite, file `vdr.db`, WAL mode

---

## 1. `stored_vcs` — Verifiable Credentials Store

| Column | Type | Notes |
|--------|------|-------|
| vc_id | VARCHAR (PK) | Unique credential identifier |
| issuer_did | VARCHAR | Issuer DID:key |
| subject_did | VARCHAR | Credential subject DID |
| credential_type | VARCHAR | e.g. `AgentIdentityCredential` |
| credential_data | TEXT | Full JSON-LD credential document |
| issued_at | DATETIME | Issuance timestamp |
| expires_at | DATETIME | Expiry (nullable) |

---

## 2. `agent_trust_states` — Per-Agent Trust State

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER (PK) | Auto-increment |
| agent_did | VARCHAR | Agent DID (unique) |
| temporal_trust_score | FLOAT | T_i(t) ∈ [0.0, 1.0] |
| trust_state | VARCHAR | TRUSTED / SUSPICIOUS / QUARANTINED / REVOKED |
| last_updated | DATETIME | Timestamp of last recalculation |

---

## 3. `telemetry_logs` — Behavioural Telemetry Events

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER (PK) | Auto-increment |
| agent_did | VARCHAR | Agent DID |
| success | BOOLEAN | Task outcome |
| compliance_event | BOOLEAN | Policy compliance flag |
| latency_ms | FLOAT | Response latency in ms |
| timestamp | DATETIME | Event timestamp |
| task_type | VARCHAR | Task category (nullable) |
| metadata | TEXT | JSON extra data (nullable) |

---

## 4. `trust_audit_trails` — Trust State Change Audit

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER (PK) | Auto-increment |
| agent_did | VARCHAR | Agent DID |
| previous_state | VARCHAR | Prior trust state |
| new_state | VARCHAR | Updated trust state |
| previous_score | FLOAT | Prior score |
| new_score | FLOAT | Updated score |
| reason | TEXT | Reason for transition |
| timestamp | DATETIME | Transition timestamp |
| triggered_by | VARCHAR | `telemetry` or `admin_revocation` |

---

## 5. `agents` — Agent Registry

| Column | Type | Notes |
|--------|------|-------|
| agent_id | VARCHAR (PK) | Unique agent identifier (UUID) |
| did | VARCHAR | DID:key (unique) |
| name | VARCHAR | Human-readable name |
| description | TEXT | Agent description |
| capabilities | TEXT | JSON list of capability strings |
| status | VARCHAR | `active` / `inactive` |
| health_status | VARCHAR | `healthy` / `degraded` / `offline` |
| reputation_score | FLOAT | 1.0–5.0, from ratings |
| endpoint | VARCHAR | HTTP endpoint (nullable, for real HTTP agents) |
| successful_tasks | INTEGER | Total successful task count |
| total_tasks | INTEGER | Total tasks attempted |
| last_response_time_ms | FLOAT | Most recent response latency |
| registered_at | DATETIME | Registration timestamp |
| updated_at | DATETIME | Last update timestamp |

---

## 6. `collaboration_sessions` — Agent Collaboration

| Column | Type | Notes |
|--------|------|-------|
| session_id | VARCHAR (PK) | UUID |
| requester_did | VARCHAR | DID of initiating agent |
| target_did | VARCHAR | DID of collaborating agent |
| task_description | TEXT | Task goal |
| status | VARCHAR | `active` / `completed` / `failed` |
| started_at | DATETIME | Session start |
| completed_at | DATETIME | Session end (nullable) |
| task_result | TEXT | Final result (nullable) |
| productivity_score | FLOAT | Session productivity score (nullable) |

---

## 7. `collaboration_events` — Collaboration Message Log

| Column | Type | Notes |
|--------|------|-------|
| event_id | VARCHAR (PK) | UUID |
| session_id | VARCHAR | FK → collaboration_sessions |
| sender_did | VARCHAR | Message sender DID |
| receiver_did | VARCHAR | Message receiver DID |
| message_type | VARCHAR | `task_request` / `response` / `update` |
| content | TEXT | Message payload |
| timestamp | DATETIME | Event timestamp |

---

## 8. `agent_ratings` — Peer Ratings

| Column | Type | Notes |
|--------|------|-------|
| rating_id | VARCHAR (PK) | UUID |
| agent_id | VARCHAR | FK → agents |
| rater_did | VARCHAR | Rating agent DID |
| rating | FLOAT | 1.0–5.0 |
| feedback | TEXT | Optional text feedback |
| created_at | DATETIME | Rating timestamp |

---

## 9. `workflows` — Workflow Definitions

| Column | Type | Notes |
|--------|------|-------|
| workflow_id | VARCHAR (PK) | UUID |
| name | VARCHAR | Workflow name |
| description | TEXT | Workflow goal |
| pattern | VARCHAR | `SEQUENTIAL` / `PARALLEL` |
| status | VARCHAR | `pending` / `running` / `completed` / `failed` |
| created_at | DATETIME | Creation timestamp |
| started_at | DATETIME | Execution start (nullable) |
| completed_at | DATETIME | Execution end (nullable) |
| result | TEXT | Final aggregated result (nullable) |

---

## 10. `workflow_nodes` — Workflow Steps

| Column | Type | Notes |
|--------|------|-------|
| node_id | VARCHAR (PK) | UUID |
| workflow_id | VARCHAR | FK → workflows |
| agent_did | VARCHAR | Assigned agent DID |
| required_capability | VARCHAR | Capability required for this step |
| step_order | INTEGER | Execution order (0-based) |
| status | VARCHAR | `pending` / `running` / `completed` / `failed` |
| input_data | TEXT | Input to this node |
| output_data | TEXT | Output from this node (nullable) |
| started_at | DATETIME | Step start (nullable) |
| completed_at | DATETIME | Step end (nullable) |

---

## 11. `users` — Human Operator Accounts

| Column | Type | Notes |
|--------|------|-------|
| user_id | INTEGER (PK) | Auto-increment |
| username | VARCHAR | Unique username |
| email | VARCHAR | User email |
| password_hash | VARCHAR | Argon2id hash |
| role | VARCHAR | `ADMIN` / `OPERATOR` / `VIEWER` |
| is_active | BOOLEAN | Account status |
| failed_login_attempts | INTEGER | Lockout counter |
| locked_until | DATETIME | Lockout expiry (nullable) |
| created_at | DATETIME | Account creation |
| last_login | DATETIME | Last login (nullable) |

---

## 12. `refresh_tokens` — JWT Refresh Token Store

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER (PK) | Auto-increment |
| jti | VARCHAR | JWT token ID (unique) |
| token_hash | VARCHAR | SHA-256 hash of refresh token |
| user_id | INTEGER | FK → users |
| issued_at | DATETIME | Token issuance |
| expires_at | DATETIME | Token expiry |
| revoked_at | DATETIME | Revocation timestamp (nullable) |

---

## 13. `security_audit_events` — Security Event Log

| Column | Type | Notes |
|--------|------|-------|
| event_id | INTEGER (PK) | Auto-increment |
| event_type | VARCHAR | `LOGIN_SUCCESS` / `LOGIN_FAILURE` / `TOKEN_REVOKED` / `ACCOUNT_LOCKED` etc. |
| user_id | INTEGER | FK → users (nullable) |
| username | VARCHAR | Username at time of event |
| ip_address | VARCHAR | Client IP (nullable) |
| details | TEXT | JSON extra info |
| timestamp | DATETIME | Event timestamp |

---

## Summary Statistics

- **14 tables** total
- **Core trust tables:** agent_trust_states, telemetry_logs, trust_audit_trails
- **Identity tables:** stored_vcs (credentials)
- **Registry tables:** agents, agent_ratings
- **Collaboration tables:** collaboration_sessions, collaboration_events
- **Workflow tables:** workflows, workflow_nodes
- **Auth/Security tables:** users, refresh_tokens, security_audit_events
