import requests
import time
import uuid

BASE_URL = "http://127.0.0.1:8050/api/v1/trust"
AGENT_DID = f"did:key:zTrustChainTestAgent{int(time.time())}"

print(f"===== TrustChain-AI Integration Tests =====")
print(f"Using Agent DID: {AGENT_DID}\n")

def send_telemetry(success, compliance_event, latency_ms):
    payload = {
        "agent_did": AGENT_DID,
        "task_id": str(uuid.uuid4()),
        "success": success,
        "compliance_event": compliance_event if compliance_event is not None else False,
        "latency_ms": latency_ms
    }
    requests.post(f"{BASE_URL}/telemetry", json=payload)

def get_state():
    r = requests.get(f"{BASE_URL}/state/{AGENT_DID}")
    if r.status_code == 200:
        return r.json()
    return None

def test_1():
    print("TEST 1: Valid agent -> successful task -> TRUSTED")
    send_telemetry(True, None, 100)
    send_telemetry(True, None, 120)
    send_telemetry(True, None, 150)
    state = get_state()
    print(f"Score: {state['temporal_trust_score']}, State: {state['trust_state']}")
    assert state['trust_state'] == "TRUSTED"
    print("PASS: TEST 1\n")

def test_2():
    print("TEST 2 & 6: Repeated failed tasks -> SUSPICIOUS")
    for _ in range(5):
        send_telemetry(False, None, 150)
    state = get_state()
    print(f"Score: {state['temporal_trust_score']}, State: {state['trust_state']}")
    assert state['trust_state'] in ["SUSPICIOUS", "QUARANTINED"]
    print("PASS: TEST 2 & 6\n")

def test_3():
    print("TEST 3, 4, 7: Protocol violations + Latency -> QUARANTINED")
    for _ in range(10):
        send_telemetry(False, True, 2500)
    state = get_state()
    print(f"Score: {state['temporal_trust_score']}, State: {state['trust_state']}")
    assert state['trust_state'] == "QUARANTINED"
    print("PASS: TEST 3, 4, 7\n")

def test_9():
    print("TEST 9: Agent behavior improves -> trust recovery")
    for _ in range(20):
        send_telemetry(True, None, 100)
    state = get_state()
    print(f"Score: {state['temporal_trust_score']}, State: {state['trust_state']}")
    assert state['trust_state'] != "QUARANTINED"
    print("PASS: TEST 9\n")

def test_10():
    print("TEST 10: Explicit revocation")
    requests.post(f"{BASE_URL}/revoke/{AGENT_DID}", json={"reason": "Compromised key"})
    state = get_state()
    print(f"Score: {state['temporal_trust_score']}, State: {state['trust_state']}")
    assert state['trust_state'] == "REVOKED"
    print("PASS: TEST 10\n")

if __name__ == "__main__":
    try:
        # Check initial state to ensure server is running
        get_state()
    except requests.exceptions.ConnectionError:
        print("ERROR: FastAPI server is not running on http://localhost:8050")
        exit(1)
        
    test_1()
    test_2()
    test_3()
    test_9()
    test_10()
    print("All TrustChain-AI workflow tests passed!")
