from datetime import datetime, timezone
import uuid
import sys

from akta.telemetry import TelemetryEvent
from akta.trust_engine import TrustEngine, TrustConfig, TrustState
from akta.vdr import trust_crud
from akta.vdr.database import Base, engine, SessionLocal, create_tables

# Initialize DB
create_tables()
db = SessionLocal()

AGENT_DID = f"did:key:zTrustChainTestAgent{uuid.uuid4().hex[:8]}"

print(f"===== TrustChain-AI Logic Tests =====")
print(f"Using Agent DID: {AGENT_DID}\n")

def send_telemetry(success: bool, compliance: bool, latency: float):
    import uuid
    dt = datetime.now(timezone.utc)
    event = TelemetryEvent(
        agent_did=AGENT_DID,
        task_id=str(uuid.uuid4()),
        success=success,
        compliance_event=compliance,
        latency_ms=latency,
        timestamp=dt
    )
    return trust_crud.record_telemetry_and_update_trust(db, event)

def test_1():
    print("TEST 1: Valid agent -> successful task -> TRUSTED")
    send_telemetry(True, None, 100)
    send_telemetry(True, None, 120)
    state = send_telemetry(True, None, 150)
    print(f"Score: {state.temporal_trust_score:.3f}, State: {state.trust_state}")
    assert state.trust_state == "TRUSTED"
    print("PASS: TEST 1\n")

def test_2():
    print("TEST 2 & 6: Repeated failed tasks -> SUSPICIOUS")
    for _ in range(5):
        send_telemetry(False, None, 150)
    state = send_telemetry(False, None, 150)
    print(f"Score: {state.temporal_trust_score:.3f}, State: {state.trust_state}")
    assert state.trust_state in ["SUSPICIOUS", "QUARANTINED"]
    print("PASS: TEST 2 & 6\n")

def test_3():
    print("TEST 3, 4, 7: Protocol violations + Latency -> QUARANTINED")
    for _ in range(10):
        send_telemetry(False, "invalid_scope", 2500)
    state = send_telemetry(False, "invalid_scope", 2500)
    print(f"Score: {state.temporal_trust_score:.3f}, State: {state.trust_state}")
    assert state.trust_state == "QUARANTINED"
    print("PASS: TEST 3, 4, 7\n")

def test_9():
    print("TEST 9: Agent behavior improves -> trust recovery")
    for _ in range(20):
        send_telemetry(True, None, 100)
    state = send_telemetry(True, None, 100)
    print(f"Score: {state.temporal_trust_score:.3f}, State: {state.trust_state}")
    assert state.trust_state != "QUARANTINED"
    print("PASS: TEST 9\n")

def test_10():
    print("TEST 10: Explicit revocation")
    state = trust_crud.revoke_agent(db, AGENT_DID, reason="Compromised key")
    print(f"Score: {state.temporal_trust_score:.3f}, State: {state.trust_state}")
    assert state.trust_state == "REVOKED"
    print("PASS: TEST 10\n")

if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_9()
    test_10()
    print("All TrustChain-AI internal workflow tests passed!")
