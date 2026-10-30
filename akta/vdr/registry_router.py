from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from akta.vdr import schemas, registry_crud, trust_crud, models
from akta.vdr.database import get_db
from akta.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    tags=["Agent Registry, Collaboration & Workflows"],
)


@router.post("/registry/agents", response_model=schemas.AgentRegisterResponse)
async def register_agent(
    req: schemas.AgentRegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        res = registry_crud.register_agent(db, req)
        return schemas.AgentRegisterResponse(**res)
    except Exception as e:
        logger.error(f"Error registering agent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/registry/agents")
async def list_agents(
    capability: Optional[str] = Query(None, description="Filter by capability"),
    status: Optional[str] = Query(None, description="Filter by operational status (AVAILABLE, BUSY, OFFLINE)"),
    db: Session = Depends(get_db)
):
    return registry_crud.get_registered_agents(db, capability=capability, status=status)


@router.get("/registry/agents/{did_or_id}")
async def get_agent_profile(
    did_or_id: str,
    db: Session = Depends(get_db)
):
    return registry_crud.get_agent_profile(db, did_or_id)


@router.post("/registry/agents/{did_or_id}/health", response_model=schemas.AgentHealthCheckResponse)
async def check_agent_health(
    did_or_id: str,
    db: Session = Depends(get_db)
):
    """
    Feature 1: Manually triggers endpoint/model availability health check for an agent.
    """
    res = await registry_crud.check_agent_health(db, did_or_id)
    return schemas.AgentHealthCheckResponse(**res)


@router.get("/registry/discover")
async def discover_agents(
    capability: Optional[str] = Query(None, description="Capability required for collaboration"),
    min_trust: Optional[float] = Query(None, description="Minimum trust score threshold"),
    db: Session = Depends(get_db)
):
    return registry_crud.discover_free_agents(db, capability=capability, min_trust=min_trust)


@router.post("/registry/matching")
async def match_best_agents(
    req: schemas.AgentMatchingRequest,
    db: Session = Depends(get_db)
):
    """
    Feature 3: Trust-Aware Agent Matching & Candidate Ranking.
    Applies Hard Security & Health Filters, then ranks eligible candidates transparently.
    """
    return registry_crud.find_best_agent_match(db, req)


@router.post("/registry/agents/{did}/status")
async def update_status(
    did: str,
    req: schemas.AgentStatusUpdateRequest,
    db: Session = Depends(get_db)
):
    if req.status not in ["AVAILABLE", "BUSY", "OFFLINE"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be AVAILABLE, BUSY, or OFFLINE.")
    return registry_crud.update_agent_status(db, did, req.status)


@router.post("/collaboration/request")
async def create_collaboration(
    req: schemas.CollaborationRequestCreate,
    db: Session = Depends(get_db)
):
    session = registry_crud.create_collaboration_request(db, req)
    return {
        "status": "success",
        "session_id": session.session_id,
        "requester_did": session.requester_did,
        "target_did": session.target_did,
        "task_description": session.task_description,
        "required_capability": session.required_capability,
        "session_status": session.status,
        "created_at": session.created_at
    }


@router.get("/collaboration/sessions")
async def list_collaboration_sessions(
    status: Optional[str] = Query(None, description="Filter by session status"),
    db: Session = Depends(get_db)
):
    query = db.query(models.CollaborationSessionModel)
    if status:
        query = query.filter(models.CollaborationSessionModel.status == status)
    sessions = query.order_by(models.CollaborationSessionModel.created_at.desc()).all()
    return [
        {
            "session_id": s.session_id,
            "requester_did": s.requester_did,
            "target_did": s.target_did,
            "task_description": s.task_description,
            "required_capability": s.required_capability,
            "status": s.status,
            "task_result": s.task_result,
            "productivity_score": s.productivity_score,
            "created_at": s.created_at,
            "completed_at": s.completed_at
        }
        for s in sessions
    ]


@router.get("/collaboration/sessions/{session_id}")
async def get_session_details(
    session_id: str,
    db: Session = Depends(get_db)
):
    session = db.query(models.CollaborationSessionModel).filter(models.CollaborationSessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    events = db.query(models.CollaborationEventModel).filter(
        models.CollaborationEventModel.session_id == session_id
    ).order_by(models.CollaborationEventModel.timestamp.asc()).all()

    ratings = db.query(models.AgentRatingModel).filter(
        models.AgentRatingModel.session_id == session_id
    ).all()

    return {
        "session": {
            "session_id": session.session_id,
            "requester_did": session.requester_did,
            "target_did": session.target_did,
            "task_description": session.task_description,
            "required_capability": session.required_capability,
            "status": session.status,
            "task_result": session.task_result,
            "productivity_score": session.productivity_score,
            "created_at": session.created_at,
            "completed_at": session.completed_at
        },
        "events": [
            {
                "id": e.id,
                "sender_did": e.sender_did,
                "receiver_did": e.receiver_did,
                "message_type": e.message_type,
                "content": e.content,
                "timestamp": e.timestamp
            }
            for e in events
        ],
        "ratings": [
            {
                "id": r.id,
                "rater_did": r.rater_did,
                "target_did": r.target_did,
                "rating": r.rating,
                "feedback": r.feedback,
                "timestamp": r.timestamp
            }
            for r in ratings
        ]
    }


@router.post("/collaboration/sessions/{session_id}/step")
async def execute_step(
    session_id: str,
    req: schemas.SessionMessageRequest,
    db: Session = Depends(get_db)
):
    return await registry_crud.execute_session_step(db, session_id, req.sender_did, req.content)


@router.post("/collaboration/sessions/{session_id}/terminate")
async def terminate_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    session = registry_crud.terminate_collaboration_session(db, session_id)
    return {
        "status": "success",
        "session_id": session.session_id,
        "session_status": session.status,
        "productivity_score": session.productivity_score,
        "completed_at": session.completed_at
    }


@router.post("/collaboration/rate")
async def rate_agent(
    req: schemas.SessionRatingRequest,
    db: Session = Depends(get_db)
):
    return registry_crud.rate_agent(db, req)


# ==========================================
# Feature 2: Multi-Agent Workflow Endpoints
# ==========================================

@router.post("/workflows")
async def create_workflow(
    req: schemas.WorkflowCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Creates a new Multi-Agent Workflow (Sequential or Parallel).
    """
    return registry_crud.create_workflow(db, req)


@router.get("/workflows")
async def list_workflows(
    db: Session = Depends(get_db)
):
    """
    Lists all Multi-Agent Workflows.
    """
    wfs = db.query(models.WorkflowModel).order_by(models.WorkflowModel.created_at.desc()).all()
    return [
        {
            "workflow_id": w.workflow_id,
            "workflow_name": w.workflow_name,
            "task_description": w.task_description,
            "orchestrator_did": w.orchestrator_did,
            "pattern": w.pattern,
            "status": w.status,
            "final_result": w.final_result,
            "created_at": w.created_at,
            "completed_at": w.completed_at
        }
        for w in wfs
    ]


@router.get("/workflows/{workflow_id}")
async def get_workflow_details(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves workflow status and execution step details.
    """
    wf = db.query(models.WorkflowModel).filter(models.WorkflowModel.workflow_id == workflow_id).first()
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found.")

    nodes = db.query(models.WorkflowNodeModel).filter(
        models.WorkflowNodeModel.workflow_id == workflow_id
    ).order_by(models.WorkflowNodeModel.step_order.asc()).all()

    return {
        "workflow": {
            "workflow_id": wf.workflow_id,
            "workflow_name": wf.workflow_name,
            "task_description": wf.task_description,
            "orchestrator_did": wf.orchestrator_did,
            "pattern": wf.pattern,
            "status": wf.status,
            "final_result": wf.final_result,
            "created_at": wf.created_at,
            "completed_at": wf.completed_at
        },
        "nodes": [
            {
                "node_id": n.node_id,
                "agent_did": n.agent_did,
                "required_capability": n.required_capability,
                "step_order": n.step_order,
                "status": n.status,
                "input_data": n.input_data,
                "output_data": n.output_data,
                "execution_time_ms": n.execution_time_ms,
                "executed_at": n.executed_at
            }
            for n in nodes
        ]
    }


@router.post("/workflows/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Executes the multi-agent workflow pipeline, attributing work per DID and ingesting telemetry.
    """
    return await registry_crud.execute_workflow(db, workflow_id)


@router.get("/registry/stats")
async def get_registry_stats(db: Session = Depends(get_db)):
    total_agents = db.query(models.AgentRegistryModel).count()
    available_agents = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.status == "AVAILABLE").count()
    busy_agents = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.status == "BUSY").count()
    offline_agents = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.status == "OFFLINE").count()

    healthy_count = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.health_status == "HEALTHY").count()
    unhealthy_count = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.health_status == "UNHEALTHY").count()

    trusted_count = db.query(models.AgentTrustStateModel).filter(models.AgentTrustStateModel.trust_state == "TRUSTED").count()
    suspicious_count = db.query(models.AgentTrustStateModel).filter(models.AgentTrustStateModel.trust_state == "SUSPICIOUS").count()
    quarantined_count = db.query(models.AgentTrustStateModel).filter(models.AgentTrustStateModel.trust_state == "QUARANTINED").count()
    revoked_count = db.query(models.AgentTrustStateModel).filter(models.AgentTrustStateModel.trust_state == "REVOKED").count()

    active_sessions = db.query(models.CollaborationSessionModel).filter(models.CollaborationSessionModel.status.in_(["PENDING", "ACCEPTED", "ACTIVE"])).count()
    completed_sessions = db.query(models.CollaborationSessionModel).filter(models.CollaborationSessionModel.status == "COMPLETED").count()

    active_workflows = db.query(models.WorkflowModel).filter(models.WorkflowModel.status.in_(["PENDING", "RUNNING"])).count()
    completed_workflows = db.query(models.WorkflowModel).filter(models.WorkflowModel.status == "COMPLETED").count()

    telemetry_count = db.query(models.TelemetryLogModel).count()

    return {
        "agents": {
            "total": total_agents,
            "available": available_agents,
            "busy": busy_agents,
            "offline": offline_agents,
            "healthy": healthy_count,
            "unhealthy": unhealthy_count
        },
        "trust_states": {
            "trusted": trusted_count,
            "suspicious": suspicious_count,
            "quarantined": quarantined_count,
            "revoked": revoked_count
        },
        "collaborations": {
            "active": active_sessions,
            "completed": completed_sessions
        },
        "workflows": {
            "active": active_workflows,
            "completed": completed_workflows
        },
        "total_telemetry_events": telemetry_count
    }
