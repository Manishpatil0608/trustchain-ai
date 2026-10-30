# APPENDIX A: IMPORTANT SOURCE CODE IMPLEMENTATION

This appendix provides verbatim source-code excerpts for the core technical algorithms, cryptographic workflows, and policy enforcement mechanisms in **TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**.

All excerpts are extracted directly from the operational repository at `D:\capstone project\trustchain-ai\akta-base`. Non-essential boilerplate or repetitive imports are omitted using `# ... omitted for brevity ...` to focus strictly on foundational logic.

---

### A.1 — Decentralized Identifier (DID:key) Genesis & Resolution

- **Source:** `akta/did.py`
- **Function/Class:** `_public_bytes_to_multibase_ed25519()`, `DIDKey.__init__()`
- **Purpose:** Derives self-certifying W3C `did:key` identifiers from raw 32-byte Ed25519 public keys using multicodec prefixing (`0xED, 0x01`) and Base58-btc multibase encoding (`z` prefix).
- **Source code:**

```python
import base58
from nacl.signing import SigningKey, VerifyKey
from akta.exceptions import AktaError

def _public_bytes_to_multibase_ed25519(key_bytes: bytes) -> str:
    # 2-byte multicodec prefix for Ed25519 public keys in W3C did:key context (0xed01)
    codec_prefix = bytes([0xED, 0x01])
    multicodec_pubkey = codec_prefix + key_bytes
    return "z" + base58.b58encode(multicodec_pubkey).decode("utf-8")

class DIDKey:
    """Represents a Decentralized Identifier using the W3C did:key method."""
    def __init__(self, private_key_multibase: str = None, did_string: str = None):
        if did_string:
            if not did_string.startswith("did:key:z"):
                raise AktaError("Invalid did:key format. Must start with 'did:key:z'.")
            self._public_key_multibase = did_string[len("did:key:"):]
            self._public_key_bytes = _multibase_ed25519_to_public_bytes(self._public_key_multibase)
            self._verify_key = VerifyKey(self._public_key_bytes)
            self._did = did_string
        elif private_key_multibase:
            seed_bytes = _multibase_to_private_seed(private_key_multibase)
            self._signing_key = SigningKey(seed_bytes)
            self._verify_key = self._signing_key.verify_key
            self._public_key_bytes = self._verify_key.encode()
            self._public_key_multibase = _public_bytes_to_multibase_ed25519(self._public_key_bytes)
            self._did = f"did:key:{self._public_key_multibase}"
        else:
            self._signing_key = SigningKey.generate()
            self._verify_key = self._signing_key.verify_key
            self._public_key_bytes = self._verify_key.encode()
            self._public_key_multibase = _public_bytes_to_multibase_ed25519(self._public_key_bytes)
            self._did = f"did:key:{self._public_key_multibase}"
```

- **Explanation:** The method provides zero-infrastructure decentralized identity. The public key is embedded directly into the identifier URI (`did:key:z...`), enabling offline cryptographic verification without external certificate authorities or network registries.

---

### A.2 — Verifiable Credential Canonicalization, Signing, and Verification

- **Source:** `akta/credentials.py`
- **Function/Class:** `VerifiableCredential.sign()`, `VerifiableCredential.verify_signature()`
- **Purpose:** Constructs W3C Verifiable Credentials, performs deterministic RDF dataset normalization via PyLD (`URDNA2015`), generates `Ed25519Signature2020` linked data proofs, and verifies proof integrity.
- **Source code:**

```python
import json
from datetime import datetime, UTC
from pyld import jsonld
from pyld.documentloader.requests import requests_document_loader
import base58
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

class VerifiableCredential:
    # ... omitted for brevity ...
    def sign(self, issuer_signing_key: SigningKey, verification_method_id: str) -> "VerifiableCredential":
        doc_to_canonicalize = json.loads(self.model.model_dump_json(by_alias=True, exclude_none=True))
        doc_to_canonicalize.pop("proof", None)
        proof_options = {
            "type": "Ed25519Signature2020",
            "created": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "verificationMethod": verification_method_id,
            "proofPurpose": "assertionMethod",
        }
        doc_to_canonicalize["proof"] = proof_options

        # Deterministic RDF dataset canonicalization (URDNA2015)
        normalized = jsonld.normalize(doc_to_canonicalize, options={
            "algorithm": "URDNA2015", "format": "application/n-quads",
            "documentLoader": requests_document_loader()
        })
        # Cryptographic signing using PyNaCl libsodium Ed25519
        sig_bytes = issuer_signing_key.sign(normalized.encode("utf-8")).signature
        proof_value = "z" + base58.b58encode(sig_bytes).decode("utf-8")
        self.model.proof = ProofModel(**{**proof_options, "proofValue": proof_value})
        return self

    def verify_signature(self, issuer_public_key: VerifyKey) -> bool:
        doc = json.loads(self.model.model_dump_json(by_alias=True, exclude_none=True))
        proof = doc.pop("proof", None)
        raw_sig = base58.b58decode(proof["proofValue"][1:] if proof["proofValue"].startswith("z") else proof["proofValue"])
        doc["proof"] = {k: v for k, v in proof.items() if k != "proofValue"}
        normalized = jsonld.normalize(doc, options={"algorithm": "URDNA2015", "format": "application/n-quads"})
        try:
            issuer_public_key.verify(normalized.encode("utf-8"), raw_sig)
            return True
        except BadSignatureError:
            return False
```

- **Explanation:** Ensures tamper-evidence for issued agent capabilities. The canonicalization step prevents serialization mismatches, guaranteeing that any post-issuance mutation invalidates the cryptographic proof.

---

### A.3 — Behavioral Telemetry Event Modeling and Ingestion

- **Source:** `akta/telemetry.py`
- **Function/Class:** `TelemetryEvent`, `TestHarnessTelemetrySource.ingest()`
- **Purpose:** Ingests runtime agent behavioral signals (task success, protocol compliance, response latency) into typed structures for sliding-window evaluation.
- **Source code:**

```python
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class TelemetryEvent:
    agent_did: str
    task_id: str
    success: bool
    compliance_event: bool
    latency_ms: float
    timestamp: datetime

class TestHarnessTelemetrySource:
    """Ingests behavioral observations from task harnesses and collaboration sessions."""
    def ingest(self, raw_payload: dict) -> TelemetryEvent:
        ts = raw_payload.get("timestamp")
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        elif isinstance(ts, datetime):
            dt = ts
        else:
            dt = datetime.now(timezone.utc)
        
        return TelemetryEvent(
            agent_did=raw_payload.get("agent_did"),
            task_id=raw_payload.get("task_id", "unknown"),
            success=bool(raw_payload.get("success", False)),
            compliance_event=bool(raw_payload.get("compliance_event", True)),
            latency_ms=float(raw_payload.get("latency_ms", 0.0)),
            timestamp=dt
        )
```

- **Explanation:** Telemetry events represent empirical behavioral observations. Each record captures task execution outcome ($S$), protocol compliance status ($C$), and execution latency ($L$).

---

### A.4 — Multi-Factor Performance Score and Temporal EMA Trust Calculation

- **Source:** `akta/trust_engine.py`
- **Function/Class:** `TrustConfig`, `TrustEngine.calculate_behavioral_score()`, `TrustEngine.calculate_temporal_trust()`
- **Purpose:** Computes the composite performance score $P_i(t)$ and updates the temporal Exponential Moving Average (EMA) trust score $T_i(t)$ across sliding windows.
- **Source code:**

```python
from pydantic import BaseModel
from typing import List
from akta.telemetry import TelemetryEvent

class TrustConfig(BaseModel):
    w1: float = 0.6  # Weight for task success
    w2: float = 0.3  # Weight for protocol compliance
    w3: float = 0.1  # Weight for latency penalty
    lam: float = 0.7 # Temporal decay smoothing factor
    trusted_threshold: float = 0.8
    suspicious_threshold: float = 0.5
    max_latency_ms: int = 2000

class TrustEngine:
    def __init__(self, config: TrustConfig = TrustConfig()):
        self.config = config

    def calculate_behavioral_score(self, S: float, C: float, L: float) -> float:
        """Computes composite performance score P_i(t) = w1*S + w2*C + w3*(1 - L)."""
        p = (self.config.w1 * S) + (self.config.w2 * C) + (self.config.w3 * (1.0 - L))
        return min(1.0, max(0.0, p))

    def calculate_temporal_trust(self, previous_trust: float, behavioral_score: float) -> float:
        """
        Updates temporal EMA trust score:
        Note: The implementation assigns lam=0.7 to historical memory and (1-lam)=0.3 to new observations
        in the engine method, while maintaining identical asymptotic convergence to threshold boundaries.
        """
        t = (self.config.lam * previous_trust) + ((1.0 - self.config.lam) * behavioral_score)
        return min(1.0, max(0.0, t))
```

- **Explanation:** Eliminates sudden volatility by smoothing behavioral scores against historical trust. $P_i(t)$ balances effectiveness ($S$), safety ($C$), and responsiveness ($L$). Agents enter the system with initial benefit-of-the-doubt trust ($T_0 = 1.0$).

---

### A.5 — Dynamic Adaptive Policy Enforcement and State Gating

- **Source:** `akta/adaptive_auth.py`
- **Function/Class:** `AdaptivePolicyEnforcer.check_agent_authorization()`
- **Purpose:** Gates access to `PRIVILEGED_OPERATIONS` versus `STANDARD_OPERATIONS` based on the agent's real-time behavioral trust state.
- **Source code:**

```python
from sqlalchemy.orm import Session
from akta.trust_engine import TrustState
from akta.vdr import trust_crud

class AuthorizationError(Exception): pass

class AdaptivePolicyEnforcer:
    PRIVILEGED_OPERATIONS = {
        "workflow:execute", "workflow:orchestrate", "agent:delegate",
        "credential:issue", "admin:revoke", "admin:manage", "sensitive:execute"
    }
    STANDARD_OPERATIONS = {
        "read", "query", "map:generate", "task:execute", "collaboration:step", "collaboration:participate"
    }

    @classmethod
    def check_agent_authorization(cls, subject_did: str, db: Session, operation: str = "task:execute") -> bool:
        trust_state = trust_crud.get_trust_state(db, subject_did)
        state_enum = TrustState(trust_state.trust_state)

        if state_enum == TrustState.REVOKED:
            cls._record_policy_audit(db, subject_did, "REVOKED", f"Terminal denial for '{operation}'.")
            raise AuthorizationError(f"Agent {subject_did} is administratively REVOKED.")

        if state_enum == TrustState.QUARANTINED:
            cls._record_policy_audit(db, subject_did, "QUARANTINED", f"Quarantine denial (T={trust_state.temporal_trust_score:.4f}).")
            raise AuthorizationError(f"Agent {subject_did} is QUARANTINED due to behavioral degradation.")

        if state_enum == TrustState.SUSPICIOUS:
            if operation in cls.PRIVILEGED_OPERATIONS:
                cls._record_policy_audit(db, subject_did, "SUSPICIOUS", f"Privileged op '{operation}' blocked.")
                raise AuthorizationError(f"SUSPICIOUS agent denied privileged operation '{operation}'.")
            cls._record_policy_audit(db, subject_did, "SUSPICIOUS", f"Standard op '{operation}' allowed under heightened audit.")
            return True

        return True # TRUSTED state: full authorization granted
```

- **Explanation:** Implements zero-trust runtime access control. Cryptographic credentials prove authority, but behavioral trust states dynamically throttle privileges if an agent begins failing tasks or violating policy.

---

### A.6 — Trust-Weighted Capability Discovery and Match Scoring

- **Source:** `akta/vdr/registry_crud.py`
- **Function/Class:** `find_best_agent_match()`
- **Purpose:** Discovers eligible candidate agents matching required capabilities and ranks them using a transparent multi-factor scoring formula.
- **Source code:**

```python
def find_best_agent_match(db: Session, req: schemas.AgentMatchingRequest) -> List[Dict[str, Any]]:
    all_agents = get_registered_agents(db)
    candidates = []

    for a in all_agents:
        req_cap = req.required_capability.lower()
        has_cap = req_cap in a["capabilities"].lower()
        is_quarantined = a["trust_state"] == TrustState.QUARANTINED.value
        is_revoked = a["trust_state"] == TrustState.REVOKED.value

        if is_quarantined or is_revoked or not has_cap:
            continue # Exclude untrusted or non-capable agents from ranking

        # Multi-factor score: 40% trust, 30% reputation, 20% success rate, 10% latency
        succ_rate = (a["successful_tasks"] / a["total_tasks"]) if a["total_tasks"] > 0 else 1.0
        norm_lat = min(a["last_response_time_ms"] / 2000.0, 1.0)
        
        match_score = round(
            (0.4 * a["trust_score"]) + 
            (0.3 * (a["reputation_score"] / 5.0)) + 
            (0.2 * succ_rate) + 
            (0.1 * (1.0 - norm_lat)), 
            3
        )
        candidates.append({**a, "match_score": match_score, "decision": "ELIGIBLE"})

    candidates.sort(key=lambda x: x["match_score"], reverse=True)
    if candidates:
        candidates[0]["decision"] = "SELECTED"
    return candidates
```

- **Explanation:** Guarantees that collaboration delegators select partners optimizing both competency (capability matching) and reliability (temporal trust + historical reputation).

---

### A.7 — Sequential Multi-Agent Workflow Orchestration Pipeline

- **Source:** `akta/vdr/registry_crud.py`
- **Function/Class:** `execute_workflow()`
- **Purpose:** Executes multi-step agent pipelines sequentially, enforcing trust verification before step execution, propagating outputs as subsequent inputs, and logging telemetry.
- **Source code:**

```python
async def execute_workflow(db: Session, workflow_id: str) -> Dict[str, Any]:
    wf = db.query(models.WorkflowModel).filter_by(workflow_id=workflow_id).first()
    nodes = db.query(models.WorkflowNodeModel).filter_by(workflow_id=workflow_id).order_by(models.WorkflowNodeModel.step_order.asc()).all()
    wf.status = "RUNNING"
    accumulated_output = wf.task_description

    for node in nodes:
        # Pre-execution security check via AdaptivePolicyEnforcer
        AdaptivePolicyEnforcer.check_agent_authorization(subject_did=node.agent_did, db=db, operation="workflow:execute")
        
        # Dispatch task to agent connector (passing accumulated previous step output)
        exec_res = await connector_factory.send_task(
            task_description=f"Step {node.step_order}: {accumulated_output}",
            capability=node.required_capability
        )
        
        # Record execution telemetry and trigger trust re-evaluation
        telemetry = TelemetryEvent(
            agent_did=node.agent_did, task_id=f"wf_{workflow_id[:6]}_{node.step_order}",
            success=exec_res["success"], compliance_event=exec_res["compliance_event"],
            latency_ms=exec_res["latency_ms"], timestamp=datetime.now(timezone.utc)
        )
        trust_crud.record_telemetry_and_update_trust(db, telemetry)

        node.status = "COMPLETED"
        node.output_data = exec_res["result"]
        accumulated_output = exec_res["result"] # Pipe forward
        db.commit()

    wf.status = "COMPLETED"
    wf.final_result = accumulated_output
    db.commit()
    return {"workflow_id": wf.workflow_id, "status": wf.status, "final_result": wf.final_result}
```

- **Explanation:** Implements trustworthy multi-agent pipelining. A rogue or degraded agent is intercepted prior to executing its assigned node, preventing corrupt state from propagating through the collaborative workflow.

---

### A.8 — Role-Based Access Control (RBAC) and JWT Authentication Gating

- **Source:** `akta/auth/dependencies.py`
- **Function/Class:** `require_role()`, `get_current_user()`
- **Purpose:** Enforces server-side authentication and RBAC boundaries (`ADMIN`, `OPERATOR`, `VIEWER`) across REST endpoints.
- **Source code:**

```python
from fastapi import Depends, HTTPException, status
from akta.auth import security, crud
from akta.vdr.models import UserModel

def require_role(allowed_roles: List[str]):
    """Creates a FastAPI dependency enforcing server-side Role-Based Access Control."""
    def role_checker(current_user: UserModel = Depends(get_current_user)) -> UserModel:
        if current_user.role.upper() not in [r.upper() for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Insufficient privileges. Required role: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker
```

- **Explanation:** Separates human user administration from machine agent trust states. Only administrators can perform terminal revocations and user roster modifications, while operators initiate workflows and viewers inspect metrics.
