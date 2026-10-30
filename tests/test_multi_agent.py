import pytest
from fastapi.testclient import TestClient
from akta.server import app
from akta.vdr import trust_crud
from akta.vdr.database import get_db

client = TestClient(app)

def test_multi_agent_registry_and_discovery():
    # 1. Register Agent A (Research Agent)
    resp1 = client.post("/api/v1/registry/agents", json={
        "agent_name": "Research Agent Alpha",
        "agent_type": "research",
        "model_name": "gpt-4o",
        "model_provider": "OpenAI",
        "capabilities": "research,planning"
    })
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["status"] == "success"
    assert "did:key:" in data1["did"]
    agent_a_did = data1["did"]

    # 2. Register Agent B (Analysis Agent)
    resp2 = client.post("/api/v1/registry/agents", json={
        "agent_name": "Analysis Agent Beta",
        "agent_type": "analysis",
        "model_name": "claude-3-5-sonnet",
        "model_provider": "Anthropic",
        "capabilities": "analysis,data_processing"
    })
    assert resp2.status_code == 200
    data2 = resp2.json()
    agent_b_did = data2["did"]

    # 3. Discover Free Agents
    disc_resp = client.get("/api/v1/registry/discover?capability=analysis")
    assert disc_resp.status_code == 200
    candidates = disc_resp.json()
    assert len(candidates) >= 1
    assert any(c["did"] == agent_b_did for c in candidates)

def test_collaboration_session_lifecycle_and_telemetry():
    # Register Requester and Target
    r_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": "Planner Agent",
        "agent_type": "planning",
        "capabilities": "planning"
    })
    requester_did = r_resp.json()["did"]

    t_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": "Coder Agent",
        "agent_type": "coding",
        "capabilities": "coding"
    })
    target_did = t_resp.json()["did"]

    # Initiate Collaboration Request
    req_resp = client.post("/api/v1/collaboration/request", json={
        "requester_did": requester_did,
        "target_did": target_did,
        "task_description": "Implement authentication middleware",
        "required_capability": "coding"
    })
    assert req_resp.status_code == 200
    sess_data = req_resp.json()
    session_id = sess_data["session_id"]
    assert sess_data["session_status"] == "ACCEPTED"

    # Verify agents are now BUSY
    prof_t = client.get(f"/api/v1/registry/agents/{target_did}").json()
    assert prof_t["operational_status"] == "BUSY"

    # Execute Session Step
    step_resp = client.post(f"/api/v1/collaboration/sessions/{session_id}/step", json={
        "sender_did": requester_did,
        "content": "Generate the python code"
    })
    assert step_resp.status_code == 200
    step_data = step_resp.json()
    assert "result" in step_data
    assert step_data["telemetry"]["success"] is True
    assert step_data["telemetry"]["trust_score"] >= 0.8

    # Terminate Session
    term_resp = client.post(f"/api/v1/collaboration/sessions/{session_id}/terminate")
    assert term_resp.status_code == 200
    term_data = term_resp.json()
    assert term_data["session_status"] == "COMPLETED"

    # Verify agents return to AVAILABLE status
    prof_t_after = client.get(f"/api/v1/registry/agents/{target_did}").json()
    assert prof_t_after["operational_status"] == "AVAILABLE"

    # Rate Agent
    rate_resp = client.post("/api/v1/collaboration/rate", json={
        "rater_did": requester_did,
        "target_did": target_did,
        "rating": 5.0,
        "feedback": "Outstanding performance and code quality"
    })
    assert rate_resp.status_code == 200
    assert rate_resp.json()["new_reputation_score"] == 5.0

def test_quarantined_agent_collaboration_rejection():
    # Register bad agent
    bad_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": "Rogue Agent",
        "capabilities": "execution"
    })
    bad_did = bad_resp.json()["did"]

    # Inject failure telemetry to force QUARANTINED state
    db_gen = get_db()
    db = next(db_gen)
    try:
        from akta.telemetry import TelemetryEvent
        from datetime import datetime, timezone
        import uuid

        for i in range(15):
            evt = TelemetryEvent(
                agent_did=bad_did,
                task_id=f"bad_task_{uuid.uuid4().hex[:8]}",
                success=False,
                compliance_event=False,
                latency_ms=3500,
                timestamp=datetime.now(timezone.utc)
            )
            trust_crud.record_telemetry_and_update_trust(db, evt)
    finally:
        db.close()

    # Check trust state is QUARANTINED
    state_resp = client.get(f"/api/v1/trust/state/{bad_did}").json()
    assert state_resp["trust_state"] == "QUARANTINED"

    # Try requesting collaboration with QUARANTINED agent -> Should return HTTP 403 Forbidden!
    r_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": "Supervisor Agent",
        "capabilities": "supervision"
    })
    supervisor_did = r_resp.json()["did"]

    collab_resp = client.post("/api/v1/collaboration/request", json={
        "requester_did": supervisor_did,
        "target_did": bad_did,
        "task_description": "Execute critical task",
        "required_capability": "execution"
    })
    assert collab_resp.status_code == 403
    assert "QUARANTINED" in collab_resp.json()["detail"]
