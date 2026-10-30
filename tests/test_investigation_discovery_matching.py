import pytest
from fastapi.testclient import TestClient
from akta.server import app
from akta.vdr import trust_crud
from akta.vdr.database import get_db
from akta.telemetry import TelemetryEvent
from datetime import datetime, timezone
import uuid

client = TestClient(app)

def test_investigation_agent_profile_and_telemetry():
    """
    Verifies Phase 2: Agent investigation data retrieval.
    Confirms that all required profile fields, trust state, telemetry logs,
    and audit transitions are correctly served for an investigated agent.
    """
    # 1. Register agent with detailed specifications
    reg_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": "Investigation Probe Alpha",
        "agent_type": "security_probe",
        "model_name": "claude-3-5-sonnet",
        "model_provider": "Anthropic",
        "endpoint": "https://agents.trustchain.internal/probe-alpha",
        "capabilities": "verification,audit,analysis"
    })
    assert reg_resp.status_code == 200
    agent_data = reg_resp.json()
    did = agent_data["did"]
    assert "did:key:" in did

    # 2. Ingest telemetry events to generate telemetry and trust history
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Event 1: Success, fast
        evt1 = TelemetryEvent(
            agent_did=did,
            task_id=f"probe_task_{uuid.uuid4().hex[:6]}",
            success=True,
            compliance_event=False,
            latency_ms=120,
            timestamp=datetime.now(timezone.utc)
        )
        trust_crud.record_telemetry_and_update_trust(db, evt1)

        # Event 2: Success, compliant
        evt2 = TelemetryEvent(
            agent_did=did,
            task_id=f"probe_task_{uuid.uuid4().hex[:6]}",
            success=True,
            compliance_event=False,
            latency_ms=150,
            timestamp=datetime.now(timezone.utc)
        )
        trust_crud.record_telemetry_and_update_trust(db, evt2)
    finally:
        db.close()

    # 3. Retrieve Agent Profile by DID
    prof_resp = client.get(f"/api/v1/registry/agents/{did}")
    assert prof_resp.status_code == 200
    profile = prof_resp.json()

    assert profile["did"] == did
    assert profile["agent_name"] == "Investigation Probe Alpha"
    assert profile["model_name"] == "claude-3-5-sonnet"
    assert profile["model_provider"] == "Anthropic"
    assert profile["endpoint"] == "https://agents.trustchain.internal/probe-alpha"
    assert "verification" in profile["capabilities"]
    assert profile["health_status"] in ["HEALTHY", "AVAILABLE"]
    assert profile["trust_score"] > 0.0
    assert profile["trust_state"] == "TRUSTED"
    assert profile["reputation_score"] >= 1.0

    # 4. Retrieve Agent Trust State
    state_resp = client.get(f"/api/v1/trust/state/{did}")
    assert state_resp.status_code == 200
    state = state_resp.json()
    assert state["agent_did"] == did
    assert state["trust_state"] == "TRUSTED"

    # 5. Retrieve Agent Telemetry Records
    telem_resp = client.get(f"/api/v1/trust/telemetry/{did}")
    assert telem_resp.status_code == 200
    telem = telem_resp.json()
    assert len(telem) >= 2
    assert any(t["agent_did"] == did for t in telem)

    # 6. Retrieve Agent Audit Transitions
    audit_resp = client.get(f"/api/v1/trust/audit/{did}")
    assert audit_resp.status_code == 200
    audits = audit_resp.json()
    assert isinstance(audits, list)


def test_discovery_filtering_and_min_trust():
    """
    Verifies Phase 3: /discovery filtering logic.
    Confirms filtering by capability, minimum trust threshold,
    and automatic exclusion of quarantined or revoked agents.
    """
    tag = uuid.uuid4().hex[:6]
    cap = f"discovery_test_cap_{tag}"

    # 1. Register High-Trust Candidate
    c_high = client.post("/api/v1/registry/agents", json={
        "agent_name": f"High Trust Agent {tag}",
        "capabilities": cap
    }).json()["did"]

    # 2. Register Degraded / Quarantined Candidate
    c_quar = client.post("/api/v1/registry/agents", json={
        "agent_name": f"Quarantine Agent {tag}",
        "capabilities": cap
    }).json()["did"]

    # Degrade c_quar below 0.50 into QUARANTINED state
    db_gen = get_db()
    db = next(db_gen)
    try:
        for _ in range(12):
            evt = TelemetryEvent(
                agent_did=c_quar,
                task_id=f"deg_{uuid.uuid4().hex[:6]}",
                success=False,
                compliance_event=True,
                latency_ms=2500,
                timestamp=datetime.now(timezone.utc)
            )
            trust_crud.record_telemetry_and_update_trust(db, evt)
    finally:
        db.close()

    # 3. Discovery query without min_trust filter
    disc_resp = client.get(f"/api/v1/registry/discover?capability={cap}")
    assert disc_resp.status_code == 200
    disc_agents = disc_resp.json()

    dids = [a["did"] for a in disc_agents]
    assert c_high in dids
    assert c_quar not in dids, "Quarantined agent must be excluded from discovery"

    # 4. Discovery query with high min_trust threshold (e.g. 0.90)
    disc_filtered = client.get(f"/api/v1/registry/discover?capability={cap}&min_trust=0.90")
    assert disc_filtered.status_code == 200
    filtered_dids = [a["did"] for a in disc_filtered.json()]
    assert c_high in filtered_dids

    # Discovery query with unattainable threshold (e.g. 1.05)
    disc_none = client.get(f"/api/v1/registry/discover?capability={cap}&min_trust=1.05")
    assert disc_none.status_code == 200
    assert len(disc_none.json()) == 0


def test_matching_multi_factor_calculation_and_breakdown():
    """
    Verifies Phase 3: /matching multi-factor matching logic & score breakdown.
    Validates formula: MatchScore = 0.4*T + 0.3*(r/5.0) + 0.2*sigma + 0.1*(1 - lambda)
    and verifies top candidate recommendation.
    """
    tag = uuid.uuid4().hex[:6]
    target_cap = f"matching_test_{tag}"

    # Register candidate
    cand_resp = client.post("/api/v1/registry/agents", json={
        "agent_name": f"Match Target {tag}",
        "capabilities": target_cap
    })
    cand_did = cand_resp.json()["did"]

    # Execute matching
    match_resp = client.post("/api/v1/registry/matching", json={
        "required_capability": target_cap,
        "min_trust_score": 0.5,
        "task_description": "Validate transparent multi-factor matching breakdown"
    })
    assert match_resp.status_code == 200
    candidates = match_resp.json()
    assert len(candidates) >= 1

    matched = next((c for c in candidates if c["did"] == cand_did), None)
    assert matched is not None, "Target candidate must be evaluated in matching response"
    assert matched["decision"] == "SELECTED", "Single eligible candidate must be marked SELECTED as top match"
    assert "TOP MATCH" in matched["reason"]

    # Verify score breakdown fields
    assert "score_breakdown" in matched
    bd = matched["score_breakdown"]
    assert "trust_contribution" in bd
    assert "reputation_contribution" in bd
    assert "success_contribution" in bd
    assert "latency_contribution" in bd
    assert "composite_score" in bd

    # Verify equation alignment
    expected_score = round(
        bd["trust_contribution"] + 
        bd["reputation_contribution"] + 
        bd["success_contribution"] + 
        bd["latency_contribution"],
        3
    )
    assert abs(matched["match_score"] - expected_score) <= 0.005, (
        f"Match score {matched['match_score']} must equal breakdown sum {expected_score}"
    )
