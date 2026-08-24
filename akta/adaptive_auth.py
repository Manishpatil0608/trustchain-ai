from typing import Optional
from sqlalchemy.orm import Session

from akta.credentials import VerifiableCredential
from akta.did import resolve_verification_key
from akta.vdr import trust_crud
from akta.trust_engine import TrustState
from akta.exceptions import AktaError

class AuthorizationError(Exception):
    pass

class AdaptivePolicyEnforcer:
    @staticmethod
    def verify_request(
        token_vc_json: str,
        db: Session,
        expected_issuer_did: Optional[str] = None,
        expected_subject_did: Optional[str] = None,
    ) -> bool:
        """
        Executes the full TrustChain-AI adaptive authorization workflow:
        1. Parse VC
        2. Resolve public key
        3. Cryptographic signature check
        4. Temporal Trust State check
        5. Access Decision
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
        # This checks standard Akta boundaries (expiry, signature integrity, DIDs)
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
            
        if vc.is_expired():
            raise AuthorizationError("Credential has expired.")

        # Step 4: Trust State Query (TrustChain-AI Extension)
        subject_did = vc.subject_did
        if not subject_did:
            raise AuthorizationError("Credential Subject DID missing.")
            
        trust_state = trust_crud.get_trust_state(db, subject_did)

        # Step 5: Adaptive Policy Decision
        state_enum = TrustState(trust_state.trust_state)
        
        if state_enum == TrustState.QUARANTINED:
            # Important Research Distinction:
            # Identity is valid, signature is valid, but behavioral trust is severely degraded.
            raise AuthorizationError(
                f"Trust Policy Violation: Agent {subject_did} is currently QUARANTINED due to poor behavioral history."
            )
            
        elif state_enum == TrustState.REVOKED:
            raise AuthorizationError(
                f"Trust Policy Violation: Agent {subject_did} has been administratively REVOKED."
            )
            
        elif state_enum == TrustState.SUSPICIOUS:
            # Policy could enforce step-up or restricted scopes here.
            # For the baseline, we permit access but the state is known.
            pass
            
        return True
