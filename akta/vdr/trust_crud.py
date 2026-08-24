import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc

from akta.vdr import models
from akta.telemetry import TelemetryEvent
from akta.trust_engine import TrustEngine, TrustState, TrustConfig
from akta.logging import get_logger

logger = get_logger(__name__)
trust_engine = TrustEngine(TrustConfig())

def get_trust_state(db: Session, did: str) -> models.AgentTrustStateModel:
    state = db.query(models.AgentTrustStateModel).filter(models.AgentTrustStateModel.did == did).first()
    if not state:
        # Implicitly Trusted if unknown (until behavioral degradation)
        state = models.AgentTrustStateModel(
            did=did, 
            temporal_trust_score=1.0, 
            trust_state=TrustState.TRUSTED.value
        )
        db.add(state)
        db.commit()
        db.refresh(state)
    return state

def get_recent_telemetry(db: Session, did: str, limit: int = 10):
    return db.query(models.TelemetryLogModel).filter(
        models.TelemetryLogModel.agent_did == did
    ).order_by(desc(models.TelemetryLogModel.timestamp)).limit(limit).all()

def record_telemetry_and_update_trust(db: Session, event: TelemetryEvent) -> models.AgentTrustStateModel:
    # 1. Store the event
    db_event = models.TelemetryLogModel(
        id=event.task_id,
        agent_did=event.agent_did,
        task_id=event.task_id,
        success=event.success,
        compliance_event=event.compliance_event or "",
        latency_ms=event.latency_ms,
        timestamp=event.timestamp
    )
    db.add(db_event)
    
    # 2. Get current state
    current_state = get_trust_state(db, event.agent_did)
    if current_state.trust_state == TrustState.REVOKED.value:
        db.commit() # Just save event, state is locked
        return current_state
    
    # 3. Retrieve recent window for metrics calculation
    recent_db_logs = get_recent_telemetry(db, event.agent_did, limit=10)
    
    # Convert DB logs back to TelemetryEvents for engine
    events_list = [
        TelemetryEvent(
            agent_did=log.agent_did,
            task_id=log.task_id,
            success=log.success,
            compliance_event=log.compliance_event if log.compliance_event else None,
            latency_ms=log.latency_ms,
            timestamp=log.timestamp
        )
        for log in recent_db_logs
    ]
    # Ensure current event is included if not fetched (due to uncommitted state)
    if not any(e.task_id == event.task_id for e in events_list):
        events_list.insert(0, event)

    # 4. Calculate new metrics
    S_i = trust_engine.calculate_S_i(events_list)
    C_i = trust_engine.calculate_C_i(events_list)
    L_i = trust_engine.calculate_L_i(events_list)
    P_i = trust_engine.calculate_behavioral_score(S_i, C_i, L_i)
    
    previous_trust = current_state.temporal_trust_score
    T_i = trust_engine.calculate_temporal_trust(previous_trust, P_i)
    
    # 5. Determine State
    old_state_enum = TrustState(current_state.trust_state)
    new_state_enum = trust_engine.determine_state(T_i, old_state_enum)
    
    # 6. Update State
    current_state.temporal_trust_score = T_i
    current_state.trust_state = new_state_enum.value
    
    # 7. Record Audit Trail if state changed
    if old_state_enum != new_state_enum:
        audit = models.TrustAuditTrailModel(
            id=str(uuid.uuid4()),
            agent_did=event.agent_did,
            previous_state=old_state_enum.value,
            new_state=new_state_enum.value,
            reason=f"Score shifted from {previous_trust:.3f} to {T_i:.3f} (P_i: {P_i:.3f})"
        )
        db.add(audit)
        
        logger.info(
            "State Transition",
            extra={
                "agent_did": event.agent_did,
                "previous_trust": previous_trust,
                "behavioral_score": P_i,
                "new_trust": T_i,
                "previous_state": old_state_enum.value,
                "new_state": new_state_enum.value,
                "reason": audit.reason
            }
        )
    
    db.commit()
    db.refresh(current_state)
    return current_state

def revoke_agent(db: Session, did: str, reason: str = "Admin revocation") -> models.AgentTrustStateModel:
    state = get_trust_state(db, did)
    if state.trust_state != TrustState.REVOKED.value:
        old_state = state.trust_state
        state.trust_state = TrustState.REVOKED.value
        
        audit = models.TrustAuditTrailModel(
            id=str(uuid.uuid4()),
            agent_did=did,
            previous_state=old_state,
            new_state=TrustState.REVOKED.value,
            reason=reason
        )
        db.add(audit)
        db.commit()
        db.refresh(state)
    return state

def get_trust_audit(db: Session, did: str):
    return db.query(models.TrustAuditTrailModel).filter(
        models.TrustAuditTrailModel.agent_did == did
    ).order_by(desc(models.TrustAuditTrailModel.timestamp)).all()

