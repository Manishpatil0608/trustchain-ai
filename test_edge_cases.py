from akta.telemetry import TelemetryEvent
from akta.trust_engine import TrustEngine, TrustConfig, TrustState
import datetime

engine = TrustEngine(TrustConfig())

def make_event(s, c, l):
    import uuid
    return TelemetryEvent(
        agent_did="did", task_id=str(uuid.uuid4()), success=s, compliance_event=c, latency_ms=l, timestamp=datetime.datetime.now(datetime.timezone.utc)
    )

print("Edge Cases Test")
# A. 100% success
events = [make_event(True, None, 100) for _ in range(10)]
print("A:", engine.calculate_S_i(events)) # 1.0

# B. 0% success
events = [make_event(False, None, 100) for _ in range(10)]
print("B:", engine.calculate_S_i(events)) # 0.0

# N. negative latency
events = [make_event(True, None, -50)]
print("N (neg latency penalty):", engine.calculate_L_i(events)) # 0.0

# O. extremely large latency
events = [make_event(True, None, 5000)]
print("O (large latency penalty):", engine.calculate_L_i(events)) # 1.0

# M. malformed telemetry (not possible if Pydantic validates)

print("Edge cases done.")
