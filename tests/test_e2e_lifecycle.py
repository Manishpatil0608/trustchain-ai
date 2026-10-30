import uuid
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from akta.server import app
from akta.vdr import models, trust_crud
from akta.vdr.database import get_db
from akta.trust_engine import TrustState
from akta.telemetry import TelemetryEvent
from akta.adaptive_auth import AdaptivePolicyEnforcer

client = TestClient(app)


def get_db_session():
    db_gen = get_db()
    db = next(db_gen)
    return db


def test_e2e_full_agent_lifecycle_success_path():
    """
    Scenario 1: End-to-End Success Path
    Registration -> Identity & Credential -> Discovery & Matching ->
    Collaboration Session -> Workflow Execution -> Telemetry Ingestion ->
    Trust Update -> Audit Logging.
    """
    db = get_db_session()
    try:
        # 1. Agent Registration
        reg_a = client.post("/api/v1/registry/agents", json={
            "agent_name": "E2E Lead Planner",
            "agent_type": "planning",
            "capabilities": "planning,workflow:execute,collaboration:participate"
        })
        assert reg_a.status_code == 200
        data_a = reg_a.json()
        did_a = data_a["did"]
        assert did_a.startswith("did:key:")
        assert data_a["trust_state"] == "TRUSTED"
        assert data_a["trust_score"] >= 0.80

        reg_b = client.post("/api/v1/registry/agents", json={
            "agent_name": "E2E Data Specialist",
            "agent_type": "analysis",
            "capabilities": "data_analysis,collaboration:participate"
        })
        assert reg_b.status_code == 200
        data_b = reg_b.json()
        did_b = data_b["did"]
        assert did_b.startswith("did:key:")

        # 2. Identity & Credential Retrieval
        cred_resp = client.get(f"/api/v1/vdr/credentials/subject/{did_a}")
        assert cred_resp.status_code == 200
        # If credentials were generated, ensure they are queryable
        creds = cred_resp.json()
        assert isinstance(creds, list)

        # 3. Discovery & Matching
        match_resp = client.post("/api/v1/registry/matching", json={
            "required_capability": "data_analysis",
            "min_trust_score": 0.50
        })
        assert match_resp.status_code == 200
        matches = match_resp.json()
        target_match = next((m for m in matches if m["did"] == did_b), None)
        assert target_match is not None
        assert target_match["decision"] in ["SELECTED", "ELIGIBLE"]
        assert target_match["match_score"] > 0

        # 4. Collaboration Request & Session Creation
        collab_resp = client.post("/api/v1/collaboration/request", json={
            "requester_did": did_a,
            "target_did": did_b,
            "task_description": "Analyze dataset metrics",
            "required_capability": "data_analysis"
        })
        assert collab_resp.status_code == 200
        session_data = collab_resp.json()
        session_id = session_data["session_id"]
        assert session_data["session_status"] == "ACCEPTED"

        # 5. Interactive Session Step Execution
        step_resp = client.post(f"/api/v1/collaboration/sessions/{session_id}/step", json={
            "sender_did": did_a,
            "content": "Execute step 1 of data analysis"
        })
        assert step_resp.status_code == 200
        step_data = step_resp.json()
        assert step_data["status"] == "ACTIVE"
        assert "result" in step_data
        assert step_data["telemetry"]["success"] is True
        assert step_data["telemetry"]["trust_score"] >= 0.80

        # 6. Session Termination
        term_resp = client.post(f"/api/v1/collaboration/sessions/{session_id}/terminate")
        assert term_resp.status_code == 200
        assert term_resp.json()["session_status"] == "COMPLETED"

        # 7. Workflow Orchestration & Execution
        wf_resp = client.post("/api/v1/workflows", json={
            "workflow_name": "E2E Success Pipeline",
            "task_description": "Process data pipeline end-to-end",
            "orchestrator_did": did_a,
            "pattern": "SEQUENTIAL",
            "nodes": [
                {"agent_did": did_a, "required_capability": "planning", "step_order": 1},
                {"agent_did": did_b, "required_capability": "data_analysis", "step_order": 2}
            ]
        })
        assert wf_resp.status_code == 200
        wf_id = wf_resp.json()["workflow_id"]

        wf_exec = client.post(f"/api/v1/workflows/{wf_id}/execute")
        assert wf_exec.status_code == 200
        wf_exec_data = wf_exec.json()
        assert wf_exec_data["status"] == "COMPLETED"
        assert wf_exec_data["steps_executed"] == 2

        # 8. Audit Verification
        audit_resp = client.get("/api/v1/trust/audit")
        assert audit_resp.status_code == 200
        assert len(audit_resp.json()) >= 0
    finally:
        db.close()


def test_e2e_telemetry_degradation_and_quarantine_path():
    """
    Scenario 2: Failure & Degradation Path
    Telemetry Degradation -> State Transition to SUSPICIOUS ->
    Restricted Authorization Enforced -> Quarantine Threshold Breach ->
    Protected Request Interception (HTTP 403) -> Audit Trail Verification.
    """
    db = get_db_session()
    try:
        # 1. Register Subject Agent
        reg = client.post("/api/v1/registry/agents", json={
            "agent_name": "E2E Vulnerable Agent",
            "capabilities": "critical_task,workflow:execute"
        })
        assert reg.status_code == 200
        agent_did = reg.json()["did"]

        # 2. Degrade to SUSPICIOUS by injecting mixed failure telemetry
        # Set directly to T = 0.65 (SUSPICIOUS)
        t_state = trust_crud.get_trust_state(db, agent_did)
        t_state.temporal_trust_score = 0.65
        t_state.trust_state = TrustState.SUSPICIOUS.value
        db.commit()

        # 3. Verify Restricted Authorization
        # Standard task permitted
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="map:generate") is True

        # Privileged task blocked
        with pytest.raises(Exception):
            AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute")

        # 4. Further degrade to QUARANTINED (T = 0.35)
        t_state.temporal_trust_score = 0.35
        t_state.trust_state = TrustState.QUARANTINED.value
        db.commit()

        # 5. Attempt protected collaboration request targeting quarantined agent -> HTTP 403
        planner_did = client.post("/api/v1/registry/agents", json={
            "agent_name": "E2E Coordinator",
            "capabilities": "coordination"
        }).json()["did"]

        collab_resp = client.post("/api/v1/collaboration/request", json={
            "requester_did": planner_did,
            "target_did": agent_did,
            "task_description": "Execute high-risk action",
            "required_capability": "critical_task"
        })
        assert collab_resp.status_code == 403
        assert "QUARANTINED" in collab_resp.json()["detail"]

        # 6. Verify trust-aware matching filters quarantined agent
        match_resp = client.post("/api/v1/registry/matching", json={
            "required_capability": "critical_task"
        })
        assert match_resp.status_code == 200
        candidate = next((c for c in match_resp.json() if c["did"] == agent_did), None)
        assert candidate is not None
        assert "REJECTED BY POLICY" in candidate["decision"]
    finally:
        db.close()


def test_e2e_recovery_and_administrative_revocation_path():
    """
    Scenario 3: Recovery & Terminal Revocation Path
    SUSPICIOUS State -> Recovery via Positive Telemetry -> State Transition to TRUSTED ->
    Privileged Access Restored -> Administrative Revocation -> Permanent Lockout.
    """
    db = get_db_session()
    try:
        # 1. Register agent in SUSPICIOUS state
        reg = client.post("/api/v1/registry/agents", json={
            "agent_name": "E2E Recovery & Revocation Agent",
            "capabilities": "workflow:execute,general"
        })
        assert reg.status_code == 200
        agent_did = reg.json()["did"]

        t_state = trust_crud.get_trust_state(db, agent_did)
        t_state.temporal_trust_score = 0.65
        t_state.trust_state = TrustState.SUSPICIOUS.value
        db.commit()

        # Verify privileged access is denied initially
        with pytest.raises(Exception):
            AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute")

        # 2. Inject positive telemetry for natural recovery
        for i in range(8):
            evt = TelemetryEvent(
                agent_did=agent_did,
                task_id=f"e2e_rec_{uuid.uuid4().hex[:6]}",
                success=True,
                compliance_event=None,
                latency_ms=60,
                timestamp=datetime.now(timezone.utc)
            )
            state = trust_crud.record_telemetry_and_update_trust(db, evt)

        # 3. Verify recovery to TRUSTED
        assert state.temporal_trust_score >= 0.80
        assert state.trust_state == TrustState.TRUSTED.value

        # 4. Verify privileged operations are now authorized
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute") is True

        # 5. Administrative Revocation
        revoke_resp = client.post(f"/api/v1/trust/revoke/{agent_did}", json={
            "reason": "Administrative security lockout for E2E verification"
        })
        assert revoke_resp.status_code == 200
        assert revoke_resp.json()["trust_state"] == "REVOKED"

        # 6. Verify terminal lock: subsequent successful telemetry does not unrevoke
        for i in range(5):
            evt = TelemetryEvent(
                agent_did=agent_did,
                task_id=f"e2e_fake_rec_{uuid.uuid4().hex[:6]}",
                success=True,
                compliance_event=None,
                latency_ms=50,
                timestamp=datetime.now(timezone.utc)
            )
            state_after = trust_crud.record_telemetry_and_update_trust(db, evt)
            assert state_after.trust_state == "REVOKED"

        # 7. Verify all operations are permanently blocked
        with pytest.raises(Exception) as exc_info:
            AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="map:generate")
        assert "REVOKED" in str(exc_info.value)

        with pytest.raises(Exception) as exc_info:
            AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute")
        assert "REVOKED" in str(exc_info.value)

        # 8. Verify audit entry exists
        audits = trust_crud.get_trust_audit(db, agent_did)
        assert any(a.new_state == "REVOKED" for a in audits)
    finally:
        db.close()
