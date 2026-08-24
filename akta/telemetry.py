import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class TelemetryEvent(BaseModel):
    agent_did: str = Field(..., description="DID of the agent that performed the action")
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the task execution")
    success: bool = Field(..., description="Whether the task was successful")
    compliance_event: Optional[str] = Field(None, description="Any protocol compliance issue detected (empty/None if compliant)")
    latency_ms: int = Field(default=0, description="Execution latency in milliseconds")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="When the event occurred")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")

class TelemetryCollector:
    """
    Abstract collector for telemetry events.
    In the prototype, this will likely push events directly to the database or trigger the TrustEngine.
    """
    def record_event(self, event: TelemetryEvent) -> None:
        raise NotImplementedError("Subclasses must implement record_event")
