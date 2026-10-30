from sqlalchemy import Column, String, Text, DateTime, func, Float, Boolean, Integer
from akta.vdr.database import Base

class StoredVCModel(Base):
    __tablename__ = "stored_vcs"

    vc_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    ldp_vc_json = Column(Text, nullable=False)

    issuer_did = Column(String, index=True, nullable=True)
    subject_did = Column(String, index=True, nullable=True)

    issuance_date = Column(DateTime(timezone=True), nullable=True)
    expiration_date = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<StoredVCModel(vc_id='{self.vc_id}', issuer_did='{self.issuer_did}')>"


class AgentTrustStateModel(Base):
    __tablename__ = "agent_trust_states"

    did = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    temporal_trust_score = Column(Float, nullable=False, default=1.0)
    trust_state = Column(String, nullable=False, default="TRUSTED")
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class TelemetryLogModel(Base):
    __tablename__ = "telemetry_logs"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    agent_did = Column(String, index=True, nullable=False)
    task_id = Column(String, index=True, nullable=False)
    success = Column(Boolean, nullable=False)
    compliance_event = Column(String, nullable=True)
    latency_ms = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TrustAuditTrailModel(Base):
    __tablename__ = "trust_audit_trails"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    agent_did = Column(String, index=True, nullable=False)
    previous_state = Column(String, nullable=False)
    new_state = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<TrustAuditTrailModel(agent_did='{self.agent_did}', new_state='{self.new_state}')>"


class AgentRegistryModel(Base):
    __tablename__ = "agents"

    agent_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    agent_name = Column(String, nullable=False)
    did = Column(String, index=True, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    agent_type = Column(String, nullable=False, default="general")
    model_name = Column(String, nullable=False, default="default-model")
    model_provider = Column(String, nullable=False, default="Local")
    endpoint = Column(String, nullable=True)
    capabilities = Column(String, nullable=False, default="general")  # Comma-separated list
    status = Column(String, nullable=False, default="AVAILABLE")  # AVAILABLE, BUSY, OFFLINE
    health_status = Column(String, nullable=False, default="HEALTHY")  # HEALTHY, UNHEALTHY, OFFLINE
    last_health_check = Column(DateTime(timezone=True), nullable=True)
    last_response_time_ms = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    reputation_score = Column(Float, nullable=False, default=5.0)
    total_tasks = Column(Integer, nullable=False, default=0)
    successful_tasks = Column(Integer, nullable=False, default=0)
    failed_tasks = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_active_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CollaborationSessionModel(Base):
    __tablename__ = "collaboration_sessions"

    session_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    requester_did = Column(String, index=True, nullable=False)
    target_did = Column(String, index=True, nullable=False)
    task_description = Column(Text, nullable=False)
    required_capability = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")  # PENDING, ACCEPTED, REJECTED, ACTIVE, COMPLETED, TERMINATED
    task_result = Column(Text, nullable=True)
    productivity_score = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class CollaborationEventModel(Base):
    __tablename__ = "collaboration_events"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    sender_did = Column(String, index=True, nullable=False)
    receiver_did = Column(String, index=True, nullable=False)
    message_type = Column(String, nullable=False, default="MESSAGE")  # REQUEST, RESPONSE, SYSTEM, TELEMETRY
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AgentRatingModel(Base):
    __tablename__ = "agent_ratings"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    rater_did = Column(String, index=True, nullable=False)
    target_did = Column(String, index=True, nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 - 5.0
    feedback = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class WorkflowModel(Base):
    __tablename__ = "workflows"

    workflow_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    workflow_name = Column(String, nullable=False)
    task_description = Column(Text, nullable=False)
    orchestrator_did = Column(String, index=True, nullable=False)
    pattern = Column(String, nullable=False, default="SEQUENTIAL")  # SEQUENTIAL, PARALLEL
    status = Column(String, nullable=False, default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED, TERMINATED
    final_result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class WorkflowNodeModel(Base):
    __tablename__ = "workflow_nodes"

    node_id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    workflow_id = Column(String, index=True, nullable=False)
    agent_did = Column(String, index=True, nullable=False)
    required_capability = Column(String, nullable=False)
    step_order = Column(Integer, nullable=False, default=1)
    status = Column(String, nullable=False, default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED, BLOCKED
    input_data = Column(Text, nullable=True)
    output_data = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=False, default=0)
    executed_at = Column(DateTime(timezone=True), nullable=True)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="VIEWER")  # ADMIN, OPERATOR, VIEWER
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, nullable=False, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    jti = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    token_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    replaced_by = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    client_ip = Column(String, nullable=True)


class SecurityAuditEventModel(Base):
    __tablename__ = "security_audit_events"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    user_id = Column(String, index=True, nullable=True)
    username = Column(String, index=True, nullable=True)
    event_type = Column(String, index=True, nullable=False)  # LOGIN_SUCCESS, LOGIN_FAILED, LOGOUT, REFRESH_SUCCESS, REFRESH_FAILED, LOCKOUT, REUSE_DETECTED, PASSWORD_CHANGE, ROLE_CHANGE, ADMIN_ACTION
    details = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)