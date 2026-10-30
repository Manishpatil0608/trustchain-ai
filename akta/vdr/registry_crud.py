import uuid
import asyncio
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from fastapi import HTTPException

from akta.vdr import models, schemas, trust_crud
from akta.did import DIDKey
from akta.trust_engine import TrustState
from akta.connectors import connector_factory
from akta.adaptive_auth import AdaptivePolicyEnforcer, AuthorizationError
from akta.logging import get_logger

logger = get_logger(__name__)


def register_agent(db: Session, request: schemas.AgentRegisterRequest) -> Dict[str, Any]:
    # 1. Resolve or Generate DID
    if request.did:
        agent_did = request.did
    else:
        agent_did = DIDKey().did

    # 2. Ensure AgentTrustStateModel exists
    trust_state_db = trust_crud.get_trust_state(db, agent_did)

    # 3. Create or Update AgentRegistryModel
    existing_agent = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.did == agent_did).first()
    if existing_agent:
        existing_agent.agent_name = request.agent_name
        existing_agent.agent_type = request.agent_type
        existing_agent.model_name = request.model_name
        existing_agent.model_provider = request.model_provider
        existing_agent.endpoint = request.endpoint
        existing_agent.description = request.description
        existing_agent.capabilities = request.capabilities
        db.commit()
        db.refresh(existing_agent)
        agent_db = existing_agent
    else:
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        agent_db = models.AgentRegistryModel(
            agent_id=agent_id,
            agent_name=request.agent_name,
            did=agent_did,
            description=request.description or f"{request.agent_name} ({request.agent_type})",
            agent_type=request.agent_type,
            model_name=request.model_name,
            model_provider=request.model_provider,
            endpoint=request.endpoint,
            capabilities=request.capabilities,
            status="AVAILABLE",
            health_status="HEALTHY",
            reputation_score=5.0,
            total_tasks=0,
            successful_tasks=0,
            failed_tasks=0
        )
        db.add(agent_db)
        db.commit()
        db.refresh(agent_db)

    return {
        "status": "success",
        "agent_id": agent_db.agent_id,
        "agent_name": agent_db.agent_name,
        "did": agent_db.did,
        "capabilities": agent_db.capabilities,
        "operational_status": agent_db.status,
        "health_status": agent_db.health_status,
        "trust_score": trust_state_db.temporal_trust_score,
        "trust_state": trust_state_db.trust_state,
        "reputation_score": agent_db.reputation_score
    }


def get_registered_agents(db: Session, capability: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    query = db.query(models.AgentRegistryModel)
    if capability:
        query = query.filter(models.AgentRegistryModel.capabilities.like(f"%{capability}%"))
    if status:
        query = query.filter(models.AgentRegistryModel.status == status)

    agents = query.all()
    results = []
    for a in agents:
        t_state = trust_crud.get_trust_state(db, a.did)
        results.append({
            "agent_id": a.agent_id,
            "agent_name": a.agent_name,
            "did": a.did,
            "agent_did": a.did,
            "description": a.description,
            "agent_type": a.agent_type,
            "model_name": a.model_name,
            "model_provider": a.model_provider,
            "endpoint": a.endpoint,
            "capabilities": a.capabilities,
            "operational_status": a.status,
            "health_status": a.health_status,
            "last_health_check": a.last_health_check,
            "last_response_time_ms": a.last_response_time_ms,
            "last_error": a.last_error,
            "trust_score": t_state.temporal_trust_score,
            "trust_state": t_state.trust_state,
            "reputation_score": a.reputation_score,
            "total_tasks": a.total_tasks,
            "successful_tasks": a.successful_tasks,
            "failed_tasks": a.failed_tasks,
            "created_at": a.created_at,
            "last_active_at": a.last_active_at
        })
    return results


def get_agent_profile(db: Session, did_or_id: str) -> Dict[str, Any]:
    agent = db.query(models.AgentRegistryModel).filter(
        or_(models.AgentRegistryModel.did == did_or_id, models.AgentRegistryModel.agent_id == did_or_id)
    ).first()

    if not agent:
        t_state = trust_crud.get_trust_state(db, did_or_id)
        return {
            "agent_id": f"unregistered_{did_or_id[:8]}",
            "agent_name": f"Agent {did_or_id[:16]}...",
            "did": did_or_id,
            "agent_did": did_or_id,
            "description": "Auto-discovered DID context",
            "agent_type": "general",
            "model_name": "unknown",
            "model_provider": "unknown",
            "endpoint": None,
            "capabilities": "general",
            "operational_status": "AVAILABLE" if t_state.trust_state != TrustState.REVOKED.value else "OFFLINE",
            "health_status": "HEALTHY" if t_state.trust_state != TrustState.REVOKED.value else "OFFLINE",
            "last_health_check": datetime.now(timezone.utc),
            "last_response_time_ms": 0,
            "last_error": None,
            "trust_score": t_state.temporal_trust_score,
            "trust_state": t_state.trust_state,
            "reputation_score": 5.0,
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "created_at": datetime.now(timezone.utc),
            "last_active_at": datetime.now(timezone.utc)
        }

    t_state = trust_crud.get_trust_state(db, agent.did)
    return {
        "agent_id": agent.agent_id,
        "agent_name": agent.agent_name,
        "did": agent.did,
        "agent_did": agent.did,
        "description": agent.description,
        "agent_type": agent.agent_type,
        "model_name": agent.model_name,
        "model_provider": agent.model_provider,
        "endpoint": agent.endpoint,
        "capabilities": agent.capabilities,
        "operational_status": agent.status,
        "health_status": agent.health_status,
        "last_health_check": agent.last_health_check,
        "last_response_time_ms": agent.last_response_time_ms,
        "last_error": agent.last_error,
        "trust_score": t_state.temporal_trust_score,
        "trust_state": t_state.trust_state,
        "reputation_score": agent.reputation_score,
        "total_tasks": agent.total_tasks,
        "successful_tasks": agent.successful_tasks,
        "failed_tasks": agent.failed_tasks,
        "created_at": agent.created_at,
        "last_active_at": agent.last_active_at
    }


async def check_agent_health(db: Session, did_or_id: str) -> Dict[str, Any]:
    agent = db.query(models.AgentRegistryModel).filter(
        or_(models.AgentRegistryModel.did == did_or_id, models.AgentRegistryModel.agent_id == did_or_id)
    ).first()

    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{did_or_id}' not found in registry.")

    # Execute health check via Connector
    res = await connector_factory.health_check(endpoint=agent.endpoint, provider=agent.model_provider)

    agent.health_status = res["status"]
    agent.last_response_time_ms = res["response_time_ms"]
    agent.last_error = res["error"]
    agent.last_health_check = datetime.now(timezone.utc)

    if res["status"] in ["OFFLINE", "UNHEALTHY"]:
        agent.status = "OFFLINE"

    db.commit()
    db.refresh(agent)

    return {
        "agent_id": agent.agent_id,
        "did": agent.did,
        "agent_name": agent.agent_name,
        "health_status": agent.health_status,
        "response_time_ms": agent.last_response_time_ms,
        "last_health_check": agent.last_health_check,
        "last_error": agent.last_error
    }


def discover_free_agents(
    db: Session, 
    capability: Optional[str] = None,
    min_trust: Optional[float] = None
) -> List[Dict[str, Any]]:
    agents = get_registered_agents(db, capability=capability, status="AVAILABLE")
    # Filter out QUARANTINED, REVOKED trust states & UNHEALTHY/OFFLINE endpoints for discovery
    free_candidates = [
        a for a in agents 
        if a["trust_state"] not in [TrustState.QUARANTINED.value, TrustState.REVOKED.value]
        and a["health_status"] == "HEALTHY"
        and (min_trust is None or a["trust_score"] >= min_trust)
    ]
    return free_candidates


def find_best_agent_match(db: Session, req: schemas.AgentMatchingRequest) -> List[Dict[str, Any]]:
    all_agents = get_registered_agents(db)
    candidates = []

    for a in all_agents:
        req_cap = req.required_capability.lower()
        has_cap = req_cap in a["capabilities"].lower()

        is_quarantined = a["trust_state"] == TrustState.QUARANTINED.value
        is_revoked = a["trust_state"] == TrustState.REVOKED.value
        is_suspicious = a["trust_state"] == TrustState.SUSPICIOUS.value
        is_busy = a["operational_status"] == "BUSY"
        is_unhealthy = a["health_status"] in ["UNHEALTHY", "OFFLINE"]

        is_priv_cap = (
            req.required_capability in AdaptivePolicyEnforcer.PRIVILEGED_OPERATIONS or
            req_cap in [p.lower() for p in AdaptivePolicyEnforcer.PRIVILEGED_OPERATIONS]
        )

        succ_rate = (a["successful_tasks"] / a["total_tasks"]) if a["total_tasks"] > 0 else 1.0
        norm_lat = min(a["last_response_time_ms"] / 2000.0, 1.0)

        # Determine Hard Boundary Decision
        if is_quarantined:
            decision = "REJECTED BY POLICY"
            reason = "Security Policy Violation: Agent is QUARANTINED due to behavioral degradation."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        elif is_revoked:
            decision = "REJECTED BY POLICY"
            reason = "Security Policy Violation: Agent has been administratively REVOKED."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        elif is_suspicious and is_priv_cap:
            decision = "REJECTED BY POLICY"
            reason = f"Security Policy Violation: Agent is SUSPICIOUS. Privileged capability '{req.required_capability}' restricted."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        elif req.min_trust_score is not None and a["trust_score"] < req.min_trust_score:
            decision = "REJECTED BY POLICY"
            reason = f"Trust score ({a['trust_score']:.2f}) does not meet requested minimum threshold ({req.min_trust_score:.2f})."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        elif not has_cap:
            decision = "REJECTED"
            reason = f"Missing required capability '{req.required_capability}'."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        elif is_unhealthy:
            decision = "REJECTED"
            reason = f"Endpoint health is {a['health_status']}."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        elif is_busy:
            decision = "REJECTED"
            reason = "Agent is currently BUSY on another collaboration session."
            match_score = 0.0
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": 0.0,
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": 0.0,
                "success_rate": round(succ_rate, 4),
                "success_contribution": 0.0,
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": 0.0,
                "composite_score": 0.0
            }
        else:
            decision = "ELIGIBLE"
            reason = "Passed all security policy, availability & endpoint health checks."

            # Calculate Transparent Match Score
            match_score = round(
                (0.4 * a["trust_score"]) + 
                (0.3 * (a["reputation_score"] / 5.0)) + 
                (0.2 * succ_rate) + 
                (0.1 * (1.0 - norm_lat)),
                3
            )
            score_breakdown = {
                "trust_score": round(a["trust_score"], 4),
                "trust_contribution": round(0.4 * a["trust_score"], 4),
                "reputation_score": round(a["reputation_score"], 2),
                "reputation_contribution": round(0.3 * (a["reputation_score"] / 5.0), 4),
                "success_rate": round(succ_rate, 4),
                "success_contribution": round(0.2 * succ_rate, 4),
                "latency_ms": a["last_response_time_ms"],
                "normalized_latency": round(norm_lat, 4),
                "latency_contribution": round(0.1 * (1.0 - norm_lat), 4),
                "composite_score": match_score
            }

        candidates.append({
            "agent_id": a["agent_id"],
            "agent_name": a["agent_name"],
            "did": a["did"],
            "description": a.get("description"),
            "agent_type": a.get("agent_type"),
            "model_name": a.get("model_name"),
            "model_provider": a.get("model_provider"),
            "endpoint": a.get("endpoint"),
            "capabilities": a["capabilities"],
            "trust_score": a["trust_score"],
            "trust_state": a["trust_state"],
            "reputation_score": a["reputation_score"],
            "operational_status": a["operational_status"],
            "health_status": a["health_status"],
            "total_tasks": a.get("total_tasks", 0),
            "successful_tasks": a.get("successful_tasks", 0),
            "failed_tasks": a.get("failed_tasks", 0),
            "last_response_time_ms": a.get("last_response_time_ms", 0),
            "match_score": match_score,
            "score_breakdown": score_breakdown,
            "decision": decision,
            "reason": reason
        })

    # Sort by match_score descending, and set top eligible as SELECTED
    eligible = [c for c in candidates if c["decision"] == "ELIGIBLE"]
    eligible.sort(key=lambda x: x["match_score"], reverse=True)

    if eligible:
        eligible[0]["decision"] = "SELECTED"
        eligible[0]["reason"] = "TOP MATCH: Selected based on highest combined trust, reputation & health score."

    candidates.sort(key=lambda x: (x["decision"] in ["SELECTED", "ELIGIBLE"], x["match_score"]), reverse=True)
    return candidates


def update_agent_status(db: Session, did: str, status: str) -> Dict[str, Any]:
    agent = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.did == did).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with DID '{did}' not found in registry.")
    agent.status = status
    agent.last_active_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(agent)
    return get_agent_profile(db, did)


def create_collaboration_request(db: Session, req: schemas.CollaborationRequestCreate) -> models.CollaborationSessionModel:
    requester = get_agent_profile(db, req.requester_did)
    
    # 1. Resolve Target Agent
    if req.target_did:
        target = get_agent_profile(db, req.target_did)
    else:
        candidates = discover_free_agents(db, capability=req.required_capability)
        candidates = [c for c in candidates if c["did"] != req.requester_did]
        if not candidates:
            raise HTTPException(
                status_code=404, 
                detail=f"No free, trusted & healthy agents available matching capability '{req.required_capability}'."
            )
        target = candidates[0]

    # 2. SECURITY ENFORCEMENT: Adaptive Trust Policy Check on Requester & Target Agent
    try:
        AdaptivePolicyEnforcer.check_agent_authorization(
            subject_did=req.requester_did,
            db=db,
            operation="collaboration:participate"
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=403,
            detail=f"Requester Trust Policy Violation: {str(e)}"
        )

    target_op = req.required_capability if req.required_capability in AdaptivePolicyEnforcer.PRIVILEGED_OPERATIONS else "collaboration:participate"
    try:
        AdaptivePolicyEnforcer.check_agent_authorization(
            subject_did=target["did"],
            db=db,
            operation=target_op
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=403,
            detail=f"Target Trust Policy Violation: {str(e)}"
        )

    # 3. Check Availability & Health
    if target["operational_status"] == "BUSY":
        raise HTTPException(
            status_code=400,
            detail=f"Agent '{target['agent_name']}' is currently BUSY on another collaboration session."
        )
    if target["health_status"] in ["OFFLINE", "UNHEALTHY"]:
        raise HTTPException(
            status_code=400,
            detail=f"Agent '{target['agent_name']}' endpoint is currently {target['health_status']}."
        )

    # 4. Create Session
    session_id = f"session_{uuid.uuid4().hex[:12]}"
    session = models.CollaborationSessionModel(
        session_id=session_id,
        requester_did=req.requester_did,
        target_did=target["did"],
        task_description=req.task_description,
        required_capability=req.required_capability,
        status="ACCEPTED"
    )
    db.add(session)

    # 5. Mark operational status as BUSY
    update_agent_status(db, req.requester_did, "BUSY")
    update_agent_status(db, target["did"], "BUSY")

    # 6. Record Initial Event
    event = models.CollaborationEventModel(
        id=str(uuid.uuid4()),
        session_id=session_id,
        sender_did=req.requester_did,
        receiver_did=target["did"],
        message_type="REQUEST",
        content=f"Collaboration Request: '{req.task_description}' [Capability: {req.required_capability}]"
    )
    db.add(event)

    db.commit()
    db.refresh(session)
    return session


async def execute_session_step(db: Session, session_id: str, sender_did: str, task_input: Optional[str] = None) -> Dict[str, Any]:
    session = db.query(models.CollaborationSessionModel).filter(models.CollaborationSessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    if session.status in ["COMPLETED", "TERMINATED"]:
        raise HTTPException(status_code=400, detail=f"Session '{session_id}' is already {session.status}.")

    receiver_did = session.target_did if sender_did == session.requester_did else session.requester_did
    target_profile = get_agent_profile(db, receiver_did)

    # Security re-check before execution
    step_op = session.required_capability if session.required_capability in AdaptivePolicyEnforcer.PRIVILEGED_OPERATIONS else "collaboration:step"
    try:
        AdaptivePolicyEnforcer.check_agent_authorization(
            subject_did=receiver_did,
            db=db,
            operation=step_op
        )
    except AuthorizationError as e:
        session.status = "TERMINATED"
        update_agent_status(db, session.requester_did, "AVAILABLE")
        update_agent_status(db, session.target_did, "AVAILABLE")
        db.commit()
        raise HTTPException(
            status_code=403,
            detail=f"Adaptive Policy Block: {str(e)}. Collaboration session terminated."
        )

    # Execute step via Connector Abstraction
    input_text = task_input or session.task_description
    exec_result = await connector_factory.send_task(
        task_description=input_text,
        capability=session.required_capability,
        endpoint=target_profile.get("endpoint")
    )

    # Ingest Telemetry & Update Trust
    from akta.telemetry import TelemetryEvent
    telemetry_event = TelemetryEvent(
        agent_did=receiver_did,
        task_id=f"collab_{session_id[:8]}_{uuid.uuid4().hex[:4]}",
        success=exec_result["success"],
        compliance_event=exec_result["compliance_event"],
        latency_ms=exec_result["latency_ms"],
        timestamp=datetime.now(timezone.utc)
    )
    new_trust_state = trust_crud.record_telemetry_and_update_trust(db, telemetry_event)

    target_reg = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.did == receiver_did).first()
    if target_reg:
        target_reg.total_tasks += 1
        if exec_result["success"]:
            target_reg.successful_tasks += 1
        else:
            target_reg.failed_tasks += 1
        db.commit()

    req_event = models.CollaborationEventModel(
        id=str(uuid.uuid4()),
        session_id=session_id,
        sender_did=sender_did,
        receiver_did=receiver_did,
        message_type="MESSAGE",
        content=input_text
    )
    db.add(req_event)

    resp_event = models.CollaborationEventModel(
        id=str(uuid.uuid4()),
        session_id=session_id,
        sender_did=receiver_did,
        receiver_did=sender_did,
        message_type="RESPONSE",
        content=exec_result["result"]
    )
    db.add(resp_event)

    session.status = "ACTIVE"
    session.task_result = exec_result["result"]
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.session_id,
        "status": session.status,
        "sender_did": sender_did,
        "receiver_did": receiver_did,
        "result": exec_result["result"],
        "telemetry": {
            "success": exec_result["success"],
            "latency_ms": exec_result["latency_ms"],
            "trust_score": new_trust_state.temporal_trust_score,
            "trust_state": new_trust_state.trust_state
        }
    }


def terminate_collaboration_session(db: Session, session_id: str) -> models.CollaborationSessionModel:
    session = db.query(models.CollaborationSessionModel).filter(models.CollaborationSessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    if session.status not in ["COMPLETED", "TERMINATED"]:
        session.status = "COMPLETED"
        session.completed_at = datetime.now(timezone.utc)
        events_count = db.query(models.CollaborationEventModel).filter(models.CollaborationEventModel.session_id == session_id).count()
        session.productivity_score = min(100.0, float(events_count * 25.0))

        update_agent_status(db, session.requester_did, "AVAILABLE")
        update_agent_status(db, session.target_did, "AVAILABLE")

        sys_event = models.CollaborationEventModel(
            id=str(uuid.uuid4()),
            session_id=session_id,
            sender_did="SYSTEM",
            receiver_did="ALL",
            message_type="SYSTEM",
            content=f"Session {session_id} completed and terminated. Operational status reset to AVAILABLE."
        )
        db.add(sys_event)
        db.commit()
        db.refresh(session)

    return session


def rate_agent(db: Session, req: schemas.SessionRatingRequest) -> Dict[str, Any]:
    if req.rating < 1.0 or req.rating > 5.0:
        raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 5.0")

    rating_entry = models.AgentRatingModel(
        id=str(uuid.uuid4()),
        session_id=getattr(req, "session_id", f"manual_{uuid.uuid4().hex[:6]}"),
        rater_did=req.rater_did,
        target_did=req.target_did,
        rating=req.rating,
        feedback=req.feedback or ""
    )
    db.add(rating_entry)
    db.commit()

    all_ratings = db.query(models.AgentRatingModel).filter(models.AgentRatingModel.target_did == req.target_did).all()
    avg_rating = sum(r.rating for r in all_ratings) / len(all_ratings) if all_ratings else 5.0

    target_agent = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.did == req.target_did).first()
    if target_agent:
        target_agent.reputation_score = round(avg_rating, 2)
        db.commit()

    return {
        "status": "success",
        "target_did": req.target_did,
        "rating_given": req.rating,
        "new_reputation_score": round(avg_rating, 2),
        "total_ratings": len(all_ratings)
    }


# ==========================================
# Feature 2: Workflow Orchestration Engine
# ==========================================

def create_workflow(db: Session, req: schemas.WorkflowCreateRequest) -> Dict[str, Any]:
    # Check orchestrator authorization
    try:
        AdaptivePolicyEnforcer.check_agent_authorization(
            subject_did=req.orchestrator_did,
            db=db,
            operation="workflow:orchestrate"
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=403,
            detail=f"Workflow Orchestration Policy Violation: {str(e)}"
        )

    workflow_id = f"wf_{uuid.uuid4().hex[:10]}"
    wf = models.WorkflowModel(
        workflow_id=workflow_id,
        workflow_name=req.workflow_name,
        task_description=req.task_description,
        orchestrator_did=req.orchestrator_did,
        pattern=req.pattern,
        status="PENDING"
    )
    db.add(wf)

    nodes_db = []
    for node_req in req.nodes:
        node_id = f"node_{uuid.uuid4().hex[:8]}"
        n = models.WorkflowNodeModel(
            node_id=node_id,
            workflow_id=workflow_id,
            agent_did=node_req.agent_did,
            required_capability=node_req.required_capability,
            step_order=node_req.step_order,
            status="PENDING"
        )
        db.add(n)
        nodes_db.append(n)

    db.commit()
    db.refresh(wf)
    return {
        "workflow_id": wf.workflow_id,
        "workflow_name": wf.workflow_name,
        "task_description": wf.task_description,
        "orchestrator_did": wf.orchestrator_did,
        "pattern": wf.pattern,
        "status": wf.status,
        "nodes": [
            {
                "node_id": n.node_id,
                "agent_did": n.agent_did,
                "required_capability": n.required_capability,
                "step_order": n.step_order,
                "status": n.status
            }
            for n in nodes_db
        ]
    }


async def execute_workflow(db: Session, workflow_id: str) -> Dict[str, Any]:
    wf = db.query(models.WorkflowModel).filter(models.WorkflowModel.workflow_id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found.")

    nodes = db.query(models.WorkflowNodeModel).filter(
        models.WorkflowNodeModel.workflow_id == workflow_id
    ).order_by(models.WorkflowNodeModel.step_order.asc()).all()

    wf.status = "RUNNING"
    db.commit()

    accumulated_output = wf.task_description
    executed_results = []

    for node in nodes:
        node.status = "RUNNING"
        node.input_data = accumulated_output
        db.commit()

        # 1. SECURITY & POLICY CHECK: Verify Node Agent Trust State via AdaptivePolicyEnforcer
        try:
            AdaptivePolicyEnforcer.check_agent_authorization(
                subject_did=node.agent_did,
                db=db,
                operation="workflow:execute"
            )
        except AuthorizationError as e:
            node.status = "BLOCKED"
            node.output_data = f"SECURITY POLICY BLOCK: {str(e)}"
            wf.status = "TERMINATED"
            wf.final_result = f"Workflow terminated due to security policy block on step {node.step_order} (Agent {node.agent_did}): {str(e)}"
            db.commit()
            raise HTTPException(
                status_code=403,
                detail=f"Workflow Policy Interception: {str(e)} Execution terminated."
            )

        # 2. HEALTH & OPERATIONAL CHECK
        agent_prof = get_agent_profile(db, node.agent_did)
        if agent_prof["health_status"] in ["OFFLINE", "UNHEALTHY"]:
            node.status = "FAILED"
            node.output_data = f"ENDPOINT ERROR: Agent {node.agent_did} health is {agent_prof['health_status']}."
            wf.status = "FAILED"
            wf.final_result = f"Workflow failed due to unreachable endpoint on step {node.step_order}."
            db.commit()
            raise HTTPException(
                status_code=503,
                detail=f"Workflow Execution Error: Node Agent {node.agent_did} endpoint is {agent_prof['health_status']}."
            )

        # 3. EXECUTE STEP
        step_task = f"Step {node.step_order} [{node.required_capability}]: {accumulated_output}"
        exec_res = await connector_factory.send_task(
            task_description=step_task,
            capability=node.required_capability,
            endpoint=agent_prof.get("endpoint")
        )

        # 4. RECORD TELEMETRY & UPDATE TRUST
        from akta.telemetry import TelemetryEvent
        telemetry_event = TelemetryEvent(
            agent_did=node.agent_did,
            task_id=f"wf_{workflow_id[:6]}_step{node.step_order}",
            success=exec_res["success"],
            compliance_event=exec_res["compliance_event"],
            latency_ms=exec_res["latency_ms"],
            timestamp=datetime.now(timezone.utc)
        )
        trust_crud.record_telemetry_and_update_trust(db, telemetry_event)

        # 5. UPDATE NODE RESULT
        node.status = "COMPLETED"
        node.output_data = exec_res["result"]
        node.execution_time_ms = exec_res["latency_ms"]
        node.executed_at = datetime.now(timezone.utc)
        accumulated_output = exec_res["result"]

        executed_results.append({
            "step_order": node.step_order,
            "agent_did": node.agent_did,
            "agent_name": agent_prof["agent_name"],
            "capability": node.required_capability,
            "status": node.status,
            "output": exec_res["result"],
            "latency_ms": exec_res["latency_ms"]
        })
        db.commit()

    wf.status = "COMPLETED"
    wf.final_result = accumulated_output
    wf.completed_at = datetime.now(timezone.utc)
    db.commit()

    return {
        "workflow_id": wf.workflow_id,
        "workflow_name": wf.workflow_name,
        "status": wf.status,
        "final_result": wf.final_result,
        "steps_executed": len(executed_results),
        "execution_chain": executed_results
    }
