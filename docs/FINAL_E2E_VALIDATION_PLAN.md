# Final End-to-End Validation Plan

This document outlines the rigorous final validation steps executed against the frozen TrustChain-AI repository to verify its operation as a complete, integrated system.

## 1. Environment & Installation Checks
- Confirm Python virtual environment.
- Confirm `pip install -e .` executes without error.
- Verify `a2a-sdk == 0.2.5` dependency constraint.
- Note any OS-level missing dependencies (e.g., `jq` on Windows).

## 2. Server Startup Checks
- Execute `python -m uvicorn akta.server:app --port 8050`.
- Verify no application crashes upon startup.
- Perform `GET /api/v1/.well-known/agent.json` and validate JSON output.

## 3. Cryptographic Identity & VC Checks
- Generate `did:key` pairs.
- Issue capability VC using Ed25519 signatures.
- Validate cryptographic signatures independently.
- Publish and retrieve from VDR.

## 4. Delegation Checks
- Execute valid multi-hop delegation (`canDelegate=true`).
- Ensure target API mathematically verifies the cryptographic token.
- Attempt invalid delegation (`canDelegate=false`) and verify rejection.

## 5. Trust Execution Pipeline Checks
- Emit telemetry to `POST /trust/telemetry`.
- Verify $S(t)$, $C(t)$, $L(t)$ raw inputs.
- Verify $P(t)$ composite score.
- Verify $T(t)$ exponential temporal decay calculation.

## 6. Dynamic Trust-State Checks
- **TRUSTED**: Confirm successful authorizations with HTTP 200.
- **SUSPICIOUS**: Confirm threshold boundary transitions.
- **QUARANTINED**: Confirm adaptive authorization intercepts valid credentials with HTTP 403.
- **RECOVERY**: Confirm sustained valid telemetry restores access.
- **REVOCATION**: Confirm administrative override forces terminal block.

## 7. Persistence & Audit Checks
- Generate trust transitions and stop the server.
- Restart the server and verify state retention.
- Verify chronological audit history via `GET /trust/audit/{did}`.

## 8. Dashboard & CLI Checks
- Verify `GET /api/v1/trust/dashboard` renders HTML with real DB data.
- Verify `akta trust` CLI commands execute accurately.

## 9. Automated Regression Checks
- Execute all Python logic and edge-case unit tests.
- Execute integration workflow tests.
- Execute original Akta baseline shell scripts.

## 10. Security Checks
- Ensure 401 (Authentication) and 403 (Authorization) are distinct.
- Identify spoofing or replay limitations in telemetry ingestion.
