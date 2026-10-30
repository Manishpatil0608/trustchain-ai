import uuid
from typing import Optional, Set
from sqlalchemy.orm import Session

from akta.credentials import VerifiableCredential
from akta.did import resolve_verification_key
from akta.vdr import trust_crud, models
from akta.trust_engine import TrustState
from akta.exceptions import AktaError
from akta.logging import get_logger

logger = get_logger(__name__)


class AuthorizationError(Exception):
    pass


class AdaptivePolicyEnforcer:
    """
    Centralized Adaptive Authorization Policy Enforcer for TrustChain-AI.
    
    Enforces dynamic access control based on cryptographic verification
    and continuous temporal behavioral trust states:
    
    1. TRUSTED (T >= 0.80):
       - Full access granted for standard and privileged operations.
       
    2. SUSPICIOUS (0.50 <= T < 0.80):
       - Explicit restricted authorization.
       - Privileged/sensitive operations (workflow orchestration, automated pipeline execution,
         credential delegation, administrative actions) are DENIED.
       - Legitimate lower-risk/standard operations (queries, standard tasks, supervised collaboration steps)
         are PERMITTED with heightened monitoring.
       - Policy decision and reason are recorded in the audit trail.
       
    3. QUARANTINED (T < 0.50):
       - Denies all protected operations (HTTP 403 Forbidden).
       
    4. REVOKED (Terminal State):
       - Permanently denies all operations regardless of recovery telemetry.
    """

    PRIVILEGED_OPERATIONS: Set[str] = {
        "workflow:execute",
        "workflow:orchestrate",
        "agent:delegate",
        "credential:issue",
        "admin:revoke",
        "admin:manage",
        "sensitive:execute",
    }

    STANDARD_OPERATIONS: Set[str] = {
        "read",
        "query",
        "map:generate",
        "task:execute",
        "collaboration:step",
        "collaboration:participate",
    }

    @classmethod
    def check_agent_authorization(
        cls,
        subject_did: str,
        db: Session,
        operation: str = "task:execute",
    ) -> bool:
        """
        Evaluates the agent's behavioral trust state and enforces granular policy decisions.
        """
        trust_state = trust_crud.get_trust_state(db, subject_did)
        state_enum = TrustState(trust_state.trust_state)

        # 1. QUARANTINED Check
        if state_enum == TrustState.QUARANTINED:
            cls._record_policy_audit(
                db=db,
                agent_did=subject_did,
                state="QUARANTINED",
                reason=f"Access Denied: Agent is QUARANTINED (T={trust_state.temporal_trust_score:.4f}). Operation '{operation}' blocked."
            )
            raise AuthorizationError(
                f"Trust Policy Violation: Agent {subject_did} is currently QUARANTINED due to poor behavioral history."
            )

        # 2. REVOKED Check (Administrative Terminal State)
        elif state_enum == TrustState.REVOKED:
            cls._record_policy_audit(
                db=db,
                agent_did=subject_did,
                state="REVOKED",
                reason=f"Access Denied: Agent is administratively REVOKED. Operation '{operation}' permanently blocked."
            )
            raise AuthorizationError(
                f"Trust Policy Violation: Agent {subject_did} has been administratively REVOKED."
            )

        # 3. SUSPICIOUS Check (Explicit Restricted Authorization)
        elif state_enum == TrustState.SUSPICIOUS:
            if operation in cls.PRIVILEGED_OPERATIONS:
                reason = (
                    f"Access Denied under Restricted Policy: Agent is SUSPICIOUS (T={trust_state.temporal_trust_score:.4f}). "
                    f"Privileged operation '{operation}' is prohibited."
                )
                cls._record_policy_audit(
                    db=db,
                    agent_did=subject_did,
                    state="SUSPICIOUS",
                    reason=reason
                )
                raise AuthorizationError(
                    f"Trust Policy Violation: Agent {subject_did} is SUSPICIOUS. Privileged operation '{operation}' denied."
                )
            else:
                reason = (
                    f"Access Granted under Restricted Policy: Agent is SUSPICIOUS (T={trust_state.temporal_trust_score:.4f}). "
                    f"Permitted lower-risk operation '{operation}' with heightened monitoring."
                )
                cls._record_policy_audit(
                    db=db,
                    agent_did=subject_did,
                    state="SUSPICIOUS",
                    reason=reason
                )
                logger.info(f"Restricted access permitted for SUSPICIOUS agent {subject_did} for operation '{operation}'")
                return True

        # 4. TRUSTED State
        elif state_enum == TrustState.TRUSTED:
            return True

        return True

    @classmethod
    def verify_request(
        cls,
        token_vc_json: str,
        db: Session,
        expected_issuer_did: Optional[str] = None,
        expected_subject_did: Optional[str] = None,
        operation: str = "task:execute",
    ) -> bool:
        """
        Executes the full TrustChain-AI adaptive authorization workflow:
        1. Parse VC
        2. Resolve public key
        3. Cryptographic signature check
        4. Expiration check
        5. Temporal Trust State & Adaptive Policy Decision
        """
        # Step 1: Parse VC
        try:
            vc = VerifiableCredential.from_json(token_vc_json)
        except Exception as e:
            raise AuthorizationError(f"Invalid Token format: {e}")

        # Step 2: Resolve public key from proof verificationMethod
        if not vc.proof or not vc.proof.verificationMethod:
            raise AuthorizationError("Token missing verificationMethod in proof.")

        try:
            issuer_public_key = resolve_verification_key(
                verification_method_url=vc.proof.verificationMethod,
                issuer_did_hint=vc.issuer_did
            )
        except Exception as e:
            raise AuthorizationError(f"Could not resolve issuer key: {e}")

        if not issuer_public_key:
            raise AuthorizationError("Issuer public key resolution failed.")

        # Step 3: Cryptographic signature verification
        try:
            is_valid = vc.verify_signature(
                issuer_public_key=issuer_public_key,
                expected_issuer_did=expected_issuer_did,
                expected_subject_did=expected_subject_did
            )
            if not is_valid:
                raise AuthorizationError("Cryptographic signature validation returned false.")
        except Exception as e:
            raise AuthorizationError(f"Cryptographic failure: {e}")

        # Step 4: Expiry check
        if vc.is_expired():
            raise AuthorizationError("Credential has expired.")

        # Step 5: Trust State Query & Policy Enforcement
        subject_did = vc.subject_did
        if not subject_did:
            raise AuthorizationError("Credential Subject DID missing.")

        return cls.check_agent_authorization(subject_did=subject_did, db=db, operation=operation)

    @staticmethod
    def _record_policy_audit(db: Session, agent_did: str, state: str, reason: str) -> None:
        """Persists access control decision events in the trust audit trail."""
        try:
            audit = models.TrustAuditTrailModel(
                id=str(uuid.uuid4()),
                agent_did=agent_did,
                previous_state=state,
                new_state=state,
                reason=reason
            )
            db.add(audit)
            db.commit()
        except Exception as e:
            logger.warning(f"Could not record policy audit event: {e}")
