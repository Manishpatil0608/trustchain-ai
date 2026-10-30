"""
scripts/database/seed_demo_data.py
Populates the TrustChain-AI database with safe demonstration agents,
credentials, telemetry observations, and collaborative workflows.
"""

import sys
import os
import uuid
from datetime import datetime, timezone

# Add project root to Python search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from akta.vdr.database import SessionLocal, create_tables
from akta.vdr import models, trust_crud, schemas, registry_crud
from akta.auth.crud import seed_default_admin
from akta.did import DIDKey
from akta.credentials import VerifiableCredential
from akta.trust_engine import TrustState, TrustEngine, TrustConfig
from akta.telemetry import TelemetryEvent

def seed():
    print("[*] Initializing database tables...")
    create_tables()
    db = SessionLocal()

    try:
        # 1. Seed Default Admin User
        print("[*] Verifying Administrator account...")
        admin = seed_default_admin(db)
        print(f"    [+] Admin confirmed: {admin.username} ({admin.role})")

        # 2. Seed Demonstration Agents
        print("[*] Seeding Demonstration Autonomous Agents...")
        demo_agents = [
            {
                "name": "Agent Alpha (Primary Coordinator)",
                "capabilities": "orchestration,analysis,general,map:generate",
                "agent_type": "orchestrator",
                "model_name": "gemini-1.5-pro",
                "model_provider": "Google DeepMind",
                "target_trust": 0.963,
                "target_state": TrustState.TRUSTED,
                "reputation": 4.9,
                "status": "AVAILABLE",
                "health": "HEALTHY",
                "latency_ms": 145,
                "total_tasks": 28,
                "successful_tasks": 27,
                "failed_tasks": 1
            },
            {
                "name": "Agent Beta (Data Pipeline Worker)",
                "capabilities": "processing,computation,data,task:execute",
                "agent_type": "worker",
                "model_name": "claude-3-5-sonnet",
                "model_provider": "Anthropic",
                "target_trust": 0.885,
                "target_state": TrustState.TRUSTED,
                "reputation": 4.6,
                "status": "AVAILABLE",
                "health": "HEALTHY",
                "latency_ms": 230,
                "total_tasks": 35,
                "successful_tasks": 33,
                "failed_tasks": 2
            },
            {
                "name": "Agent Gamma (Under Investigation)",
                "capabilities": "audit,verification,query",
                "agent_type": "auditor",
                "model_name": "gpt-4o-mini",
                "model_provider": "OpenAI",
                "target_trust": 0.655,
                "target_state": TrustState.SUSPICIOUS,
                "reputation": 3.8,
                "status": "AVAILABLE",
                "health": "HEALTHY",
                "latency_ms": 780,
                "total_tasks": 20,
                "successful_tasks": 14,
                "failed_tasks": 6
            },
            {
                "name": "Agent Delta (Quarantined Adversary)",
                "capabilities": "scraping,computation",
                "agent_type": "crawler",
                "model_name": "mistral-7b-instruct",
                "model_provider": "Mistral AI",
                "target_trust": 0.320,
                "target_state": TrustState.QUARANTINED,
                "reputation": 2.1,
                "status": "OFFLINE",
                "health": "UNHEALTHY",
                "latency_ms": 1950,
                "total_tasks": 15,
                "successful_tasks": 5,
                "failed_tasks": 10
            }
        ]

        seeded_dids = {}

        for spec in demo_agents:
            # Check if agent already exists
            existing = db.query(models.AgentRegistryModel).filter(models.AgentRegistryModel.agent_name == spec["name"]).first()
            if existing:
                print(f"    [-] Agent '{spec['name']}' already exists ({existing.did}). Updating state...")
                agent_did = existing.did
                agent_db = existing
            else:
                did_obj = DIDKey()
                agent_did = did_obj.did
                agent_id = f"agent_{uuid.uuid4().hex[:8]}"

                agent_db = models.AgentRegistryModel(
                    agent_id=agent_id,
                    agent_name=spec["name"],
                    did=agent_did,
                    description=f"{spec['name']} - Demonstrator for {spec['target_state'].value} baseline",
                    agent_type=spec["agent_type"],
                    model_name=spec["model_name"],
                    model_provider=spec["model_provider"],
                    endpoint=f"http://127.0.0.1:8050/api/v1/agents/{agent_id}",
                    capabilities=spec["capabilities"],
                    status=spec["status"],
                    health_status=spec["health"],
                    last_response_time_ms=spec["latency_ms"],
                    last_health_check=datetime.now(timezone.utc),
                    reputation_score=spec["reputation"],
                    total_tasks=spec["total_tasks"],
                    successful_tasks=spec["successful_tasks"],
                    failed_tasks=spec["failed_tasks"]
                )
                db.add(agent_db)
                db.commit()
                db.refresh(agent_db)
                print(f"    [+] Created agent '{spec['name']}': {agent_did}")

            seeded_dids[spec["agent_type"]] = agent_did

            # Update Trust State
            t_state = trust_crud.get_trust_state(db, agent_did)
            t_state.temporal_trust_score = spec["target_trust"]
            t_state.trust_state = spec["target_state"].value
            db.commit()

            # Record initial audit entry
            audit_entry = models.TrustAuditTrailModel(
                id=str(uuid.uuid4()),
                agent_did=agent_did,
                previous_state="INITIALIZING",
                new_state=spec["target_state"].value,
                reason=f"Baseline initialization with target score {spec['target_trust']:.3f}",
                timestamp=datetime.now(timezone.utc)
            )
            db.add(audit_entry)
            db.commit()

        # 3. Seed Issued Verifiable Credentials
        print("[*] Generating and storing W3C Verifiable Credentials...")
        issuer_key = DIDKey()
        subject_did = seeded_dids["orchestrator"]

        import json
        import base58

        vc_payload = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "id": f"urn:uuid:{uuid.uuid4()}",
            "type": ["VerifiableCredential", "AutonomousAgentAccessCard"],
            "issuer": issuer_key.did,
            "issuanceDate": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "credentialSubject": {
                "id": subject_did,
                "role": "Lead Orchestrator",
                "securityClearance": "LEVEL_3_PRIVILEGED",
                "issuedTo": "Agent Alpha",
                "organization": "TrustChain Network"
            }
        }
        # Cryptographic Ed25519 digital signature
        doc_bytes = json.dumps(vc_payload, sort_keys=True).encode("utf-8")
        sig_bytes = issuer_key.signing_key.sign(doc_bytes).signature
        vc_payload["proof"] = {
            "type": "Ed25519Signature2020",
            "created": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "verificationMethod": f"{issuer_key.did}#{issuer_key.did.split(':')[-1]}",
            "proofPurpose": "assertionMethod",
            "proofValue": "z" + base58.b58encode(sig_bytes).decode("utf-8")
        }
        vc_json = json.dumps(vc_payload)

        existing_vc = db.query(models.StoredVCModel).filter(models.StoredVCModel.subject_did == subject_did).first()
        if not existing_vc:
            vc_record = models.StoredVCModel(
                vc_id=f"vc_{uuid.uuid4().hex[:12]}",
                ldp_vc_json=vc_json,
                issuer_did=issuer_key.did,
                subject_did=subject_did,
                issuance_date=datetime.now(timezone.utc)
            )
            db.add(vc_record)
            db.commit()
            print(f"    [+] Stored VC for Agent Alpha ({vc_record.vc_id})")

        # 4. Seed Workflow Demonstration
        print("[*] Seeding Demonstration Sequential Workflow...")
        existing_wf = db.query(models.WorkflowModel).filter(models.WorkflowModel.workflow_name == "Cross-Agent Analytics Pipeline").first()
        if not existing_wf:
            wf_id = f"wf_{uuid.uuid4().hex[:8]}"
            wf = models.WorkflowModel(
                workflow_id=wf_id,
                workflow_name="Cross-Agent Analytics Pipeline",
                task_description="Execute distributed data ingestion, statistical analysis, and report generation",
                orchestrator_did=seeded_dids["orchestrator"],
                pattern="SEQUENTIAL",
                status="COMPLETED",
                final_result="Pipeline executed successfully with all intermediate nodes meeting SLA criteria."
            )
            db.add(wf)

            node1 = models.WorkflowNodeModel(
                node_id=f"node_{uuid.uuid4().hex[:8]}",
                workflow_id=wf_id,
                agent_did=seeded_dids["worker"],
                required_capability="processing",
                step_order=1,
                status="COMPLETED",
                input_data="Raw telemetry dataset [28 items]",
                output_data="Normalized metrics array",
                execution_time_ms=210,
                executed_at=datetime.now(timezone.utc)
            )
            node2 = models.WorkflowNodeModel(
                node_id=f"node_{uuid.uuid4().hex[:8]}",
                workflow_id=wf_id,
                agent_did=seeded_dids["orchestrator"],
                required_capability="analysis",
                step_order=2,
                status="COMPLETED",
                input_data="Normalized metrics array",
                output_data="Verified trust compliance report",
                execution_time_ms=180,
                executed_at=datetime.now(timezone.utc)
            )
            db.add(node1)
            db.add(node2)
            db.commit()
            print(f"    [+] Workflow created: {wf_id} (2 nodes)")

        print("\n[+] Demonstration data seeding completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
