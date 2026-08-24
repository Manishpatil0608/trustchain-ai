from dataclasses import dataclass
from typing import Optional
from enum import Enum
import time

from datetime import datetime, timezone
@dataclass
class TelemetryEvent:
    agent_did: str
    task_id: str
    success: bool
    compliance_event: bool
    latency_ms: float
    timestamp: datetime

class TelemetrySource:
    """
    Abstract interface for secure telemetry ingestion.
    This separates the mathematical trust engine from the physical source of telemetry.
    """
    def ingest(self, raw_payload: dict) -> TelemetryEvent:
        raise NotImplementedError("Must implement ingest mechanism")


class TestHarnessTelemetrySource(TelemetrySource):
    """
    Current unauthenticated test harness source used for experimental evaluation.
    WARNING: Not for production use. Lacks cryptographic attestation.
    """
    def ingest(self, raw_payload: dict) -> TelemetryEvent:
        # allow parsing float timestamp or default to now
        ts = raw_payload.get("timestamp")
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        elif isinstance(ts, datetime):
            dt = ts
        else:
            dt = datetime.now(timezone.utc)
        
        return TelemetryEvent(
            agent_did=raw_payload.get("agent_did"),
            task_id=raw_payload.get("task_id", "unknown"),
            success=raw_payload.get("success", False),
            compliance_event=raw_payload.get("compliance_event", True),
            latency_ms=raw_payload.get("latency_ms", 0.0),
            timestamp=dt
        )

# FUTURE WORK:
# class SignedTelemetrySource(TelemetrySource):
#    def ingest(self, raw_payload: dict) -> TelemetryEvent:
#        # 1. Verify JWS/Ed25519 signature
#        # 2. Prevent replay attacks using nonces/timestamps
#        # 3. Return verified TelemetryEvent
#        pass
