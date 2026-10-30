import pytest
from fastapi.testclient import TestClient
from akta.server import app
from akta.vdr import trust_crud
from akta.vdr.database import get_db

client = TestClient(app)

def test_feature1_agent_health_monitoring():
    # Register Agent
    reg_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": "Health Test Agent",
        "agent_type": "analysis",
        "capabilities": "analysis"
    })
    assert reg_resp.status_code == 200
    agent_did = reg_resp.json()["did"]

    # Trigger Health Check
    h_resp = client.post(f"/api/v1/registry/agents/{agent_did}/health")
    assert h_resp.status_code == 200
    data = h_resp.json()
    assert data["health_status"] == "HEALTHY"
    assert data["response_time_ms"] >= 0
    assert "last_health_check" in data

def test_feature2_multi_agent_workflow_orchestrator():
    # Register 3 Agents
    a1 = client.post("/api/v1/registry/agents", json={"agent_name": "Workflow Agent 1", "capabilities": "research"}).json()["did"]
    a2 = client.post("/api/v1/registry/agents", json={"agent_name": "Workflow Agent 2", "capabilities": "analysis"}).json()["did"]
    a3 = client.post("/api/v1/registry/agents", json={"agent_name": "Workflow Agent 3", "capabilities": "verification"}).json()["did"]

    # Create Workflow
    wf_resp = client.post("/api/v1/workflows", json={
        "workflow_name": "Test Sequential Pipeline",
        "task_description": "Verify workflow orchestration end-to-end",
        "orchestrator_did": a1,
        "pattern": "SEQUENTIAL",
        "nodes": [
            {"agent_did": a1, "required_capability": "research", "step_order": 1},
            {"agent_did": a2, "required_capability": "analysis", "step_order": 2},
            {"agent_did": a3, "required_capability": "verification", "step_order": 3}
        ]
    })
    assert wf_resp.status_code == 200
    wf_data = wf_resp.json()
    workflow_id = wf_data["workflow_id"]
    assert len(wf_data["nodes"]) == 3

    # Execute Workflow
    exec_resp = client.post(f"/api/v1/workflows/{workflow_id}/execute")
    assert exec_resp.status_code == 200
    exec_data = exec_resp.json()
    assert exec_data["status"] == "COMPLETED"
    assert exec_data["steps_executed"] == 3
    assert "final_result" in exec_data

def test_feature3_trust_aware_agent_matching():
    # Register Candidate Agents
    c1 = client.post("/api/v1/registry/agents", json={"agent_name": "Candidate Good", "capabilities": "coding"}).json()["did"]
    c2 = client.post("/api/v1/registry/agents", json={"agent_name": "Candidate Bad", "capabilities": "coding"}).json()["did"]

    # Degrade c2 to QUARANTINED
    db_gen = get_db()
    db = next(db_gen)
    try:
        from akta.telemetry import TelemetryEvent
        from datetime import datetime, timezone
        import uuid

        for i in range(15):
            evt = TelemetryEvent(
                agent_did=c2,
                task_id=f"match_fail_{uuid.uuid4().hex[:8]}",
                success=False,
                compliance_event=False,
                latency_ms=3500,
                timestamp=datetime.now(timezone.utc)
            )
            trust_crud.record_telemetry_and_update_trust(db, evt)
    finally:
        db.close()

    # Request Trust-Aware Matching for capability 'coding'
    match_resp = client.post("/api/v1/registry/matching", json={
        "required_capability": "coding"
    })
    assert match_resp.status_code == 200
    candidates = match_resp.json()
    assert len(candidates) >= 2

    c1_match = next(c for c in candidates if c["did"] == c1)
    c2_match = next(c for c in candidates if c["did"] == c2)

    assert c1_match["decision"] in ["SELECTED", "ELIGIBLE"]
    assert "REJECTED BY POLICY" in c2_match["decision"]
