import uuid
from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from akta.server import app
from akta.vdr import models, trust_crud
from akta.vdr.database import get_db
from akta.trust_engine import TrustState
from akta.adaptive_auth import AdaptivePolicyEnforcer, AuthorizationError
from akta.telemetry import TelemetryEvent

client = TestClient(app)


def get_db_session():
    db_gen = get_db()
    db = next(db_gen)
    return db


def test_adaptive_policy_trusted_agent_allows_all():
    """
    Verify TRUSTED agents (T >= 0.80) have full authorization for both
    standard operations and privileged operations.
    """
    db = get_db_session()
    try:
        # Register a new agent (default T = 1.0, state = TRUSTED)
        reg_resp = client.post("/api/v1/registry/agents", json={
            "agent_name": "Trusted Policy Test Agent",
            "capabilities": "general,analysis"
        })
        assert reg_resp.status_code == 200
        agent_did = reg_resp.json()["did"]

        # Standard operations should succeed
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="map:generate") is True
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="collaboration:step") is True
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="task:execute") is True

        # Privileged operations should also succeed
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute") is True
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:orchestrate") is True
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="agent:delegate") is True
        assert AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="credential:issue") is True
    finally:
        db.close()


def test_adaptive_policy_suspicious_agent_restricted_authorization():
    """
    Verify SUSPICIOUS agents (0.50 <= T < 0.80):
    1. Standard operations are permitted under heightened monitoring and audited.
    2. Privileged operations are denied with AuthorizationError and audited.
    """
    db = get_db_session()
    try:
        reg_resp = client.post("/api/v1/registry/agents", json={
            "agent_name": "Suspicious Policy Test Agent",
            "capabilities": "general"
        })
        assert reg_resp.status_code == 200
        agent_did = reg_resp.json()["did"]

        # Set agent to SUSPICIOUS state (T = 0.65)
        t_state = trust_crud.get_trust_state(db, agent_did)
        t_state.temporal_trust_score = 0.65
        t_state.trust_state = TrustState.SUSPICIOUS.value
        db.commit()

        # 1. Standard operation: Should be PERMITTED under monitoring
        allowed = AdaptivePolicyEnforcer.check_agent_authorization(
            subject_did=agent_did,
            db=db,
            operation="map:generate"
        )
        assert allowed is True

        # Verify audit trail recorded for permitted restricted access
        audit_permit = db.query(models.TrustAuditTrailModel).filter(
            models.TrustAuditTrailModel.agent_did == agent_did,
            models.TrustAuditTrailModel.reason.like("%Permitted lower-risk operation%")
        ).first()
        assert audit_permit is not None
        assert audit_permit.new_state == "SUSPICIOUS"

        # 2. Privileged operations: Should be DENIED
        privileged_ops = ["workflow:execute", "workflow:orchestrate", "agent:delegate", "credential:issue", "admin:revoke"]
        for op in privileged_ops:
            with pytest.raises(AuthorizationError) as exc_info:
                AdaptivePolicyEnforcer.check_agent_authorization(
                    subject_did=agent_did,
                    db=db,
                    operation=op
                )
            assert "SUSPICIOUS" in str(exc_info.value)
            assert op in str(exc_info.value)

        # Verify audit trail recorded for denied privileged access
        audit_deny = db.query(models.TrustAuditTrailModel).filter(
            models.TrustAuditTrailModel.agent_did == agent_did,
            models.TrustAuditTrailModel.reason.like("%Access Denied under Restricted Policy%")
        ).first()
        assert audit_deny is not None
        assert audit_deny.new_state == "SUSPICIOUS"
    finally:
        db.close()


def test_suspicious_agent_workflow_execution_blocked():
    """
    Verify that an orchestrated workflow execution is intercepted and blocked (HTTP 403)
    if one of the execution nodes degrades to SUSPICIOUS state.
    """
    db = get_db_session()
    try:
        # Register 2 agents: an orchestrator and a worker
        orch = client.post("/api/v1/registry/agents", json={
            "agent_name": "Workflow Orch Agent",
            "capabilities": "orchestration"
        }).json()["did"]

        worker = client.post("/api/v1/registry/agents", json={
            "agent_name": "Workflow Worker Agent",
            "capabilities": "processing"
        }).json()["did"]

        # Create workflow
        wf_resp = client.post("/api/v1/workflows", json={
            "workflow_name": "Suspicious Interception Test",
            "task_description": "Execute critical business pipeline",
            "orchestrator_did": orch,
            "pattern": "SEQUENTIAL",
            "nodes": [
                {"agent_did": worker, "required_capability": "processing", "step_order": 1}
            ]
        })
        assert wf_resp.status_code == 200
        wf_id = wf_resp.json()["workflow_id"]

        # Degrade worker to SUSPICIOUS state (T = 0.60)
        worker_state = trust_crud.get_trust_state(db, worker)
        worker_state.temporal_trust_score = 0.60
        worker_state.trust_state = TrustState.SUSPICIOUS.value
        db.commit()

        # Execute workflow: Must fail with HTTP 403 because workflow:execute is privileged
        exec_resp = client.post(f"/api/v1/workflows/{wf_id}/execute")
        assert exec_resp.status_code == 403
        detail = exec_resp.json()["detail"]
        assert "SUSPICIOUS" in detail

        # Check workflow and node statuses in DB
        wf_db = db.query(models.WorkflowModel).filter(models.WorkflowModel.workflow_id == wf_id).first()
        assert wf_db.status == "TERMINATED"
        node_db = db.query(models.WorkflowNodeModel).filter(models.WorkflowNodeModel.workflow_id == wf_id).first()
        assert node_db.status == "BLOCKED"
    finally:
        db.close()


def test_quarantined_agent_all_operations_denied():
    """
    Verify QUARANTINED agents (T < 0.50):
    1. Both standard and privileged operations are blocked.
    2. Collaboration requests targeting or originating from quarantined agents return HTTP 403.
    3. Trust-aware matching rejects them as REJECTED BY POLICY.
    """
    db = get_db_session()
    try:
        reg_resp = client.post("/api/v1/registry/agents", json={
            "agent_name": "Quarantine Test Agent",
            "capabilities": "computation"
        })
        assert reg_resp.status_code == 200
        bad_did = reg_resp.json()["did"]

        # Set to QUARANTINED (T = 0.35)
        bad_state = trust_crud.get_trust_state(db, bad_did)
        bad_state.temporal_trust_score = 0.35
        bad_state.trust_state = TrustState.QUARANTINED.value
        db.commit()

        # Policy enforcer denies both standard and privileged
        with pytest.raises(AuthorizationError):
            AdaptivePolicyEnforcer.check_agent_authorization(bad_did, db, operation="map:generate")
        with pytest.raises(AuthorizationError):
            AdaptivePolicyEnforcer.check_agent_authorization(bad_did, db, operation="workflow:execute")

        # Collaboration request should return 403
        good_agent = client.post("/api/v1/registry/agents", json={
            "agent_name": "Good Agent",
            "capabilities": "coordination"
        }).json()["did"]

        collab_resp = client.post("/api/v1/collaboration/request", json={
            "requester_did": good_agent,
            "target_did": bad_did,
            "task_description": "Compute data",
            "required_capability": "computation"
        })
        assert collab_resp.status_code == 403
        assert "QUARANTINED" in collab_resp.json()["detail"]

        # Matching rejects quarantined agent
        match_resp = client.post("/api/v1/registry/matching", json={
            "required_capability": "computation"
        })
        assert match_resp.status_code == 200
        match_data = match_resp.json()
        target_candidate = next((c for c in match_data if c["did"] == bad_did), None)
        assert target_candidate is not None
        assert "REJECTED BY POLICY" in target_candidate["decision"]
    finally:
        db.close()


def test_revoked_agent_terminal_state_denial_and_no_recovery():
    """
    Verify REVOKED agents (Terminal State):
    1. Administratively revoked via API.
    2. Denied for all operations.
    3. Success telemetry events do NOT recover the agent back to TRUSTED.
    """
    db = get_db_session()
    try:
        reg_resp = client.post("/api/v1/registry/agents", json={
            "agent_name": "Revocation Test Agent",
            "capabilities": "security"
        })
        assert reg_resp.status_code == 200
        agent_did = reg_resp.json()["did"]

        # Administratively revoke
        revoke_resp = client.post(f"/api/v1/trust/revoke/{agent_did}", json={
            "reason": "Administrative security revocation"
        })
        assert revoke_resp.status_code == 200
        assert revoke_resp.json()["trust_state"] == "REVOKED"

        # Verify policy enforcer denies
        with pytest.raises(AuthorizationError) as exc_info:
            AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="task:execute")
        assert "REVOKED" in str(exc_info.value)

        # Attempt to inject positive telemetry (10 perfect events)
        for i in range(10):
            evt = TelemetryEvent(
                agent_did=agent_did,
                task_id=f"recovery_attempt_{uuid.uuid4().hex[:6]}",
                success=True,
                compliance_event=None,
                latency_ms=80,
                timestamp=datetime.now(timezone.utc)
            )
            state_after = trust_crud.record_telemetry_and_update_trust(db, evt)
            # Must remain REVOKED
            assert state_after.trust_state == "REVOKED"

        # Check DB state directly
        final_state = trust_crud.get_trust_state(db, agent_did)
        assert final_state.trust_state == "REVOKED"
    finally:
        db.close()


def test_suspicious_agent_recovery_to_trusted():
    """
    Verify recovery lifecycle:
    1. Agent starts in SUSPICIOUS state (T = 0.65). Privileged operations are denied.
    2. Agent executes compliant, successful tasks with low latency.
    3. T_i(t) mathematically increases past 0.80.
    4. State transitions back to TRUSTED, and privileged operations are now permitted.
    """
    db = get_db_session()
    try:
        reg_resp = client.post("/api/v1/registry/agents", json={
            "agent_name": "Recovery Test Agent",
            "capabilities": "processing"
        })
        assert reg_resp.status_code == 200
        agent_did = reg_resp.json()["did"]

        # Set to SUSPICIOUS (T = 0.65)
        t_state = trust_crud.get_trust_state(db, agent_did)
        t_state.temporal_trust_score = 0.65
        t_state.trust_state = TrustState.SUSPICIOUS.value
        db.commit()

        # Privileged operation initially fails
        with pytest.raises(AuthorizationError):
            AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute")

        # Inject consecutive successful, compliant, low latency events
        # P = 0.6*1.0 + 0.3*1.0 + 0.1*(1 - 50/2000) = 0.6 + 0.3 + 0.0975 = 0.9975
        # Each step: T = 0.7 * T_prev + 0.3 * 0.9975
        for i in range(8):
            evt = TelemetryEvent(
                agent_did=agent_did,
                task_id=f"recov_{uuid.uuid4().hex[:6]}",
                success=True,
                compliance_event=None,
                latency_ms=50,
                timestamp=datetime.now(timezone.utc)
            )
            state = trust_crud.record_telemetry_and_update_trust(db, evt)

        # Agent should have recovered to TRUSTED (T >= 0.80)
        assert state.temporal_trust_score >= 0.80
        assert state.trust_state == TrustState.TRUSTED.value

        # Privileged operation is now permitted
        allowed = AdaptivePolicyEnforcer.check_agent_authorization(agent_did, db, operation="workflow:execute")
        assert allowed is True
    finally:
        db.close()


def test_matching_suspicious_with_privileged_capability():
    """
    Verify that in trust-aware matching, an agent in SUSPICIOUS state:
    - Is ELIGIBLE for standard capabilities (e.g. 'translation')
    - Is REJECTED BY POLICY for privileged capabilities (e.g. 'workflow:execute')
    """
    db = get_db_session()
    try:
        reg_resp = client.post("/api/v1/registry/agents", json={
            "agent_name": "Capability Matching Agent",
            "capabilities": "translation,workflow:execute"
        })
        assert reg_resp.status_code == 200
        agent_did = reg_resp.json()["did"]

        # Set to SUSPICIOUS (T = 0.68)
        t_state = trust_crud.get_trust_state(db, agent_did)
        t_state.temporal_trust_score = 0.68
        t_state.trust_state = TrustState.SUSPICIOUS.value
        db.commit()

        # Match for standard capability: translation
        match_std = client.post("/api/v1/registry/matching", json={
            "required_capability": "translation",
            "min_trust_score": 0.50
        })
        assert match_std.status_code == 200
        std_candidate = next((c for c in match_std.json() if c["did"] == agent_did), None)
        assert std_candidate is not None
        assert std_candidate["decision"] in ["ELIGIBLE", "SELECTED"]

        # Match for privileged capability: workflow:execute
        match_priv = client.post("/api/v1/registry/matching", json={
            "required_capability": "workflow:execute",
            "min_trust_score": 0.50
        })
        assert match_priv.status_code == 200
        priv_candidate = next((c for c in match_priv.json() if c["did"] == agent_did), None)
        assert priv_candidate is not None
        assert "REJECTED BY POLICY" in priv_candidate["decision"]
    finally:
        db.close()
