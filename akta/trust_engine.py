from enum import Enum
from typing import List, Tuple
from pydantic import BaseModel
from datetime import datetime, timezone
from akta.telemetry import TelemetryEvent

class TrustState(str, Enum):
    TRUSTED = "TRUSTED"
    SUSPICIOUS = "SUSPICIOUS"
    QUARANTINED = "QUARANTINED"
    REVOKED = "REVOKED"


class TrustConfig(BaseModel):
    w1: float = 0.6  # Weight for Success
    w2: float = 0.3  # Weight for Compliance
    w3: float = 0.1  # Weight for Latency
    lam: float = 0.7  # Temporal decay factor (historical memory)
    
    trusted_threshold: float = 0.8
    suspicious_threshold: float = 0.5
    
    max_latency_ms: int = 2000 # Latency above this is fully penalized

    def __init__(self, **data):
        super().__init__(**data)
        if abs(self.w1 + self.w2 + self.w3 - 1.0) > 1e-6:
            raise ValueError("Weights w1, w2, w3 must sum to 1.0")


class TrustEngine:
    def __init__(self, config: TrustConfig = TrustConfig()):
        self.config = config

    def calculate_S_i(self, events: List[TelemetryEvent]) -> float:
        """Task Success Rate S_i(t)"""
        if not events:
            return 1.0  # Default if no observations
        success_count = sum(1 for e in events if e.success)
        return float(success_count) / len(events)

    def calculate_C_i(self, events: List[TelemetryEvent]) -> float:
        """Protocol Compliance C_i(t)"""
        if not events:
            return 1.0
        # Compliant if compliance_event is empty or None
        compliant_count = sum(1 for e in events if not e.compliance_event)
        return float(compliant_count) / len(events)

    def calculate_L_i(self, events: List[TelemetryEvent]) -> float:
        """Normalized Latency L_i(t) (0 = fast/good, 1 = slow/bad)"""
        if not events:
            return 0.0
        avg_latency = sum(e.latency_ms for e in events) / len(events)
        normalized = avg_latency / float(self.config.max_latency_ms)
        return min(1.0, max(0.0, normalized))

    def calculate_behavioral_score(self, S: float, C: float, L: float) -> float:
        """P_i(t)"""
        p = (self.config.w1 * S) + (self.config.w2 * C) + (self.config.w3 * (1.0 - L))
        return min(1.0, max(0.0, p))

    def calculate_temporal_trust(self, previous_trust: float, behavioral_score: float) -> float:
        """T_i(t)"""
        t = (self.config.lam * previous_trust) + ((1.0 - self.config.lam) * behavioral_score)
        return min(1.0, max(0.0, t))

    def determine_state(self, temporal_trust: float, current_state: TrustState) -> TrustState:
        """Maps Trust Score to Trust State. Does not recover REVOKED."""
        if current_state == TrustState.REVOKED:
            return TrustState.REVOKED

        if temporal_trust >= self.config.trusted_threshold:
            return TrustState.TRUSTED
        elif temporal_trust >= self.config.suspicious_threshold:
            return TrustState.SUSPICIOUS
        else:
            return TrustState.QUARANTINED
