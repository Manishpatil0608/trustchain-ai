-- ==============================================================================
-- TrustChain-AI SQLite Database Schema Definition (DDL)
-- Database Engine: SQLite 3 (WAL Mode, Foreign Keys, Normal Synchronous)
-- Total Tables: 13
-- ==============================================================================

-- 1. Verifiable Credential Registry (W3C Linked Data Proofs)
CREATE TABLE IF NOT EXISTS stored_vcs (
    vc_id VARCHAR NOT NULL PRIMARY KEY,
    ldp_vc_json TEXT NOT NULL,
    issuer_did VARCHAR,
    subject_did VARCHAR,
    issuance_date DATETIME,
    expiration_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_stored_vcs_vc_id ON stored_vcs(vc_id);
CREATE INDEX IF NOT EXISTS ix_stored_vcs_issuer_did ON stored_vcs(issuer_did);
CREATE INDEX IF NOT EXISTS ix_stored_vcs_subject_did ON stored_vcs(subject_did);

-- 2. Dynamic Behavioral Trust State (Continuously Updated)
CREATE TABLE IF NOT EXISTS agent_trust_states (
    did VARCHAR NOT NULL PRIMARY KEY,
    temporal_trust_score FLOAT NOT NULL DEFAULT 1.0,
    trust_state VARCHAR NOT NULL DEFAULT 'TRUSTED', -- TRUSTED, SUSPICIOUS, QUARANTINED, REVOKED
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_agent_trust_states_did ON agent_trust_states(did);

-- 3. Telemetry Event Logs (Runtime Execution Observations)
CREATE TABLE IF NOT EXISTS telemetry_logs (
    id VARCHAR NOT NULL PRIMARY KEY,
    agent_did VARCHAR NOT NULL,
    task_id VARCHAR NOT NULL,
    success BOOLEAN NOT NULL,
    compliance_event VARCHAR,
    latency_ms INTEGER NOT NULL DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_telemetry_logs_agent_did ON telemetry_logs(agent_did);
CREATE INDEX IF NOT EXISTS ix_telemetry_logs_task_id ON telemetry_logs(task_id);

-- 4. Trust State Machine Audit Trail (Immutable State Transitions)
CREATE TABLE IF NOT EXISTS trust_audit_trails (
    id VARCHAR NOT NULL PRIMARY KEY,
    agent_did VARCHAR NOT NULL,
    previous_state VARCHAR NOT NULL,
    new_state VARCHAR NOT NULL,
    reason VARCHAR NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_trust_audit_trails_agent_did ON trust_audit_trails(agent_did);

-- 5. Autonomous Agent Registry (Capabilities, Metadata, Reputation)
CREATE TABLE IF NOT EXISTS agents (
    agent_id VARCHAR NOT NULL PRIMARY KEY,
    agent_name VARCHAR NOT NULL,
    did VARCHAR NOT NULL UNIQUE,
    description TEXT,
    agent_type VARCHAR NOT NULL DEFAULT 'general',
    model_name VARCHAR NOT NULL DEFAULT 'default-model',
    model_provider VARCHAR NOT NULL DEFAULT 'Local',
    endpoint VARCHAR,
    capabilities VARCHAR NOT NULL DEFAULT 'general',
    status VARCHAR NOT NULL DEFAULT 'AVAILABLE', -- AVAILABLE, BUSY, OFFLINE
    health_status VARCHAR NOT NULL DEFAULT 'HEALTHY', -- HEALTHY, UNHEALTHY, OFFLINE
    last_health_check DATETIME,
    last_response_time_ms INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    reputation_score FLOAT NOT NULL DEFAULT 5.0,
    total_tasks INTEGER NOT NULL DEFAULT 0,
    successful_tasks INTEGER NOT NULL DEFAULT 0,
    failed_tasks INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_active_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_agents_did ON agents(did);

-- 6. Multi-Agent Collaboration Sessions
CREATE TABLE IF NOT EXISTS collaboration_sessions (
    session_id VARCHAR NOT NULL PRIMARY KEY,
    requester_did VARCHAR NOT NULL,
    target_did VARCHAR NOT NULL,
    task_description TEXT NOT NULL,
    required_capability VARCHAR NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'PENDING', -- PENDING, ACCEPTED, REJECTED, ACTIVE, COMPLETED, TERMINATED
    task_result TEXT,
    productivity_score FLOAT NOT NULL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at DATETIME
);
CREATE INDEX IF NOT EXISTS ix_collab_sessions_requester ON collaboration_sessions(requester_did);
CREATE INDEX IF NOT EXISTS ix_collab_sessions_target ON collaboration_sessions(target_did);

-- 7. Inter-Agent Communication Events
CREATE TABLE IF NOT EXISTS collaboration_events (
    id VARCHAR NOT NULL PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    sender_did VARCHAR NOT NULL,
    receiver_did VARCHAR NOT NULL,
    message_type VARCHAR NOT NULL DEFAULT 'MESSAGE', -- REQUEST, RESPONSE, SYSTEM, TELEMETRY
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_collab_events_session_id ON collaboration_events(session_id);

-- 8. Post-Collaboration Peer Evaluation Ratings
CREATE TABLE IF NOT EXISTS agent_ratings (
    id VARCHAR NOT NULL PRIMARY KEY,
    session_id VARCHAR NOT NULL,
    rater_did VARCHAR NOT NULL,
    target_did VARCHAR NOT NULL,
    rating FLOAT NOT NULL, -- Scale 1.0 to 5.0
    feedback TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_agent_ratings_target ON agent_ratings(target_did);

-- 9. Multi-Agent Orchestrated Workflows (DAG / Sequences)
CREATE TABLE IF NOT EXISTS workflows (
    workflow_id VARCHAR NOT NULL PRIMARY KEY,
    workflow_name VARCHAR NOT NULL,
    task_description TEXT NOT NULL,
    orchestrator_did VARCHAR NOT NULL,
    pattern VARCHAR NOT NULL DEFAULT 'SEQUENTIAL', -- SEQUENTIAL, PARALLEL
    status VARCHAR NOT NULL DEFAULT 'PENDING', -- PENDING, RUNNING, COMPLETED, FAILED, TERMINATED
    final_result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at DATETIME
);
CREATE INDEX IF NOT EXISTS ix_workflows_orchestrator ON workflows(orchestrator_did);

-- 10. Individual Workflow Execution Nodes
CREATE TABLE IF NOT EXISTS workflow_nodes (
    node_id VARCHAR NOT NULL PRIMARY KEY,
    workflow_id VARCHAR NOT NULL,
    agent_did VARCHAR NOT NULL,
    required_capability VARCHAR NOT NULL,
    step_order INTEGER NOT NULL DEFAULT 1,
    status VARCHAR NOT NULL DEFAULT 'PENDING', -- PENDING, RUNNING, COMPLETED, FAILED, BLOCKED
    input_data TEXT,
    output_data TEXT,
    execution_time_ms INTEGER NOT NULL DEFAULT 0,
    executed_at DATETIME
);
CREATE INDEX IF NOT EXISTS ix_workflow_nodes_wf_id ON workflow_nodes(workflow_id);
CREATE INDEX IF NOT EXISTS ix_workflow_nodes_agent_did ON workflow_nodes(agent_did);

-- 11. Platform Users & RBAC
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR NOT NULL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR UNIQUE,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'VIEWER', -- ADMIN, OPERATOR, VIEWER
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_verified BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_login_at DATETIME,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until DATETIME
);
CREATE INDEX IF NOT EXISTS ix_users_username ON users(username);

-- 12. JWT Refresh Token Sessions
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id VARCHAR NOT NULL PRIMARY KEY,
    jti VARCHAR NOT NULL UNIQUE,
    user_id VARCHAR NOT NULL,
    token_hash VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expires_at DATETIME NOT NULL,
    revoked_at DATETIME,
    replaced_by VARCHAR,
    user_agent VARCHAR,
    client_ip VARCHAR
);
CREATE INDEX IF NOT EXISTS ix_refresh_tokens_jti ON refresh_tokens(jti);
CREATE INDEX IF NOT EXISTS ix_refresh_tokens_user_id ON refresh_tokens(user_id);

-- 13. Security Audit Trail (Authentication & Administrative Events)
CREATE TABLE IF NOT EXISTS security_audit_events (
    id VARCHAR NOT NULL PRIMARY KEY,
    user_id VARCHAR,
    username VARCHAR,
    event_type VARCHAR NOT NULL, -- LOGIN_SUCCESS, LOGIN_FAILED, LOCKOUT, REFRESH_SUCCESS, PASSWORD_CHANGE, etc.
    details TEXT,
    ip_address VARCHAR,
    user_agent VARCHAR,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_security_audit_events_user_id ON security_audit_events(user_id);
CREATE INDEX IF NOT EXISTS ix_security_audit_events_type ON security_audit_events(event_type);
