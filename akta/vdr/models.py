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