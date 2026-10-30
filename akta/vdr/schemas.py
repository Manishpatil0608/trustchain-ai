from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class VCPublishRequest(BaseModel):
    verifiable_credential: dict

class VCPublishResponse(BaseModel):
    status: str
    vc_id: str
    message: Optional[str] = None

class StoredVCBase(BaseModel):
    vc_id: str = Field(primary_key=True, index=True)
    ldp_vc_json: str
    issuer_did: Optional[str] = Field(default=None, index=True)
    subject_did: Optional[str] = Field(default=None, index=True)
    issuance_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class StoredVCCreate(StoredVCBase):
    pass

class StoredVC(StoredVCBase):
    created_at: datetime
    updated_at: datetime


class TelemetryPublishRequest(BaseModel):
    agent_did: str
    task_id: Optional[str] = None
    success: bool
    compliance_event: bool = False
    latency_ms: int = 0
    
class TrustStateResponse(BaseModel):
    agent_did: str
    temporal_trust_score: float
    trust_state: str
    
class RevocationRequest(BaseModel):
    reason: str


class AgentRegisterRequest(BaseModel):
    agent_name: str
    agent_type: str = "general"
    model_name: str = "gpt-4o"
    model_provider: str = "OpenAI"
    endpoint: Optional[str] = None
    description: Optional[str] = None
    capabilities: str = "general"
    did: Optional[str] = None


class AgentRegisterResponse(BaseModel):
    status: str
    agent_id: str
    agent_name: str
    did: str
    capabilities: str
    operational_status: str
    health_status: str
    trust_score: float
    trust_state: str
    reputation_score: float


class AgentProfileResponse(BaseModel):
    agent_id: str
    agent_name: str
    did: str
    description: Optional[str] = None
    agent_type: str
    model_name: str
    model_provider: str
    endpoint: Optional[str] = None
    capabilities: str
    operational_status: str
    health_status: str
    last_health_check: Optional[datetime] = None
    last_response_time_ms: int
    last_error: Optional[str] = None
    trust_score: float
    trust_state: str
    reputation_score: float
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    created_at: datetime
    last_active_at: datetime


class AgentHealthCheckResponse(BaseModel):
    agent_id: str
    did: str
    agent_name: str
    health_status: str
    response_time_ms: int
    last_health_check: datetime
    last_error: Optional[str] = None


class CollaborationRequestCreate(BaseModel):
    requester_did: str
    target_did: Optional[str] = None
    task_description: str
    required_capability: str


class CollaborationSessionResponse(BaseModel):
    session_id: str
    requester_did: str
    target_did: str
    task_description: str
    required_capability: str
    status: str
    task_result: Optional[str] = None
    productivity_score: float
    created_at: datetime
    completed_at: Optional[datetime] = None


class SessionMessageRequest(BaseModel):
    sender_did: str
    content: str
    message_type: str = "MESSAGE"


class SessionRatingRequest(BaseModel):
    rater_did: str
    target_did: str
    rating: float
    feedback: Optional[str] = None


class AgentStatusUpdateRequest(BaseModel):
    status: str


class WorkflowNodeCreate(BaseModel):
    agent_did: str
    required_capability: str
    step_order: int = 1


class WorkflowCreateRequest(BaseModel):
    workflow_name: str
    task_description: str
    orchestrator_did: str
    pattern: str = "SEQUENTIAL"  # SEQUENTIAL, PARALLEL
    nodes: List[WorkflowNodeCreate]


class AgentMatchingRequest(BaseModel):
    required_capability: str
    requester_did: Optional[str] = None
    task_description: Optional[str] = None
    min_trust_score: Optional[float] = 0.5


class CandidateMatchResult(BaseModel):
    agent_id: str
    agent_name: str
    did: str
    capabilities: str
    trust_score: float
    trust_state: str
    reputation_score: float
    operational_status: str
    health_status: str
    match_score: float
    decision: str  # SELECTED, REJECTED
    reason: str
