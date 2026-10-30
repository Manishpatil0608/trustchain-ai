# TrustChain-AI — Diagram to Implementation Mapping

This document provides a line-item trace linking every major node, edge, algorithm, and data model represented in the 25 Mermaid diagrams directly to the underlying Python backend, React frontend, SQLite schema, and test suite.

---

## 1. System-Wide Architectural Mapping

| Diagram Layer / Subsystem | Concrete Codebase Path | Classes / Functions / Endpoints | Database Model / Table |
|---|---|---|---|
| **Presentation Tier** | `frontend/src/` | `DashboardHome.jsx`, `AgentExplorer.jsx`, `AgentDetails.jsx`, `DiscoveryMatching.jsx`, `TrustAnalytics.jsx`, `TelemetryCenter.jsx`, `StateTransitionMap.jsx`, `AuthorizationVisualizer.jsx`, `CollaborationCenter.jsx`, `WorkflowCenter.jsx`, `IdentityCredentials.jsx`, `AuditTrail.jsx`, `SystemHealth.jsx`, `UserManagement.jsx` | N/A (Consumes JSON API via Axios `api.js`) |
| **API Gateway Tier** | `akta/server.py` | FastAPI app instance, CORS middleware, exception handlers, router mounts (`/auth`, `/registry`, `/vdr`, `/health`) | N/A |
| **User Authentication & RBAC** | `akta/auth/` | `authenticate_user()`, `create_access_token()`, `create_refresh_token()`, `rotate_refresh_token()`, `get_current_active_user()`, `require_admin()`, `require_operator()` | `UserModel` (`users`), `RefreshTokenModel` (`refresh_tokens`), `SecurityAuditEventModel` (`security_audit_events`) |
| **Cryptographic Identity** | `akta/did.py` | `DIDKey.generate()`, `DIDKey.resolve()`, `DIDKey.sign()`, `DIDKey.verify()`, PyNaCl Libsodium Ed25519 bindings | `AgentRegistryModel.did` (`agents`) |
| **Verifiable Credentials** | `akta/credentials.py`, `akta/vdr/router.py` | `create_verifiable_credential()`, `verify_credential()`, `canonicalize_ldp()` via PyLD URDNA2015 | `StoredVCModel` (`stored_vcs`) |
| **Trust Intelligence Core** | `akta/trust_engine.py` | `TrustEngine.compute_performance_score()`, `TrustEngine.compute_temporal_trust()`, `TrustEngine.classify_trust_state()`, `TrustConfig` | `AgentTrustStateModel` (`agent_trust_states`), `TrustAuditTrailModel` (`trust_audit_trails`) |
| **Telemetry Ingestion** | `akta/telemetry.py` | `record_telemetry()`, sliding window queries (last 10 records) | `TelemetryLogModel` (`telemetry_logs`) |
| **Adaptive Policy Enforcer** | `akta/adaptive_auth.py` | `AdaptivePolicyEnforcer.enforce_policy()`, `PRIVILEGED_OPERATIONS`, `STANDARD_OPERATIONS`, `AuthorizationError` | `AgentTrustStateModel` (`agent_trust_states`), `SecurityAuditEventModel` (`security_audit_events`) |
| **Discovery & Match Scoring** | `akta/vdr/registry_crud.py` | `discover_agents()`, `compute_match_score()` | `AgentRegistryModel` (`agents`), `AgentTrustStateModel` (`agent_trust_states`) |
| **Collaboration Engine** | `akta/vdr/registry_crud.py`, `akta/agent_connector.py` | `create_collaboration_session()`, `send_collaboration_message()`, `complete_collaboration_session()`, `LocalAgentConnector.execute_agent_task()` | `CollaborationSessionModel` (`collaboration_sessions`), `CollaborationEventModel` (`collaboration_events`) |
| **Sequential Workflows** | `akta/vdr/registry_crud.py` | `create_workflow()`, `execute_workflow()` | `WorkflowModel` (`workflows`), `WorkflowNodeModel` (`workflow_nodes`) |
| **System Health Probes** | `akta/server.py` | `/health` route inspecting FastAPI, SQLite WAL latency, and TrustEngine state | In-process probes |

---

## 2. Mathematical Model Implementation Verification

### A. Observation Normalization (Sliding Window: $n = 10$)
- **File:** `akta/trust_engine.py` (and `akta/telemetry.py`)
- **Formula:**
  - $S_i(t) = \frac{\text{success\_count}}{n}$
  - $C_i(t) = \frac{\text{compliance\_count}}{n}$
  - $L_i(t) = \min\left(\frac{\bar{\ell}_i}{2000}, 1.0\right)$
- **Code Trace:**
  ```python
  window = telemetry_records[:10]
  s_score = sum(1 for r in window if r.success) / len(window)
  c_score = sum(1 for r in window if r.compliance_event is None) / len(window)
  avg_latency = sum(r.latency_ms for r in window) / len(window)
  l_penalty = min(avg_latency / 2000.0, 1.0)
  ```

### B. Composite Performance Score $P_i(t)$
- **File:** `akta/trust_engine.py`
- **Formula:** $P_i(t) = 0.6 \cdot S_i(t) + 0.3 \cdot C_i(t) + 0.1 \cdot (1 - L_i(t))$
- **Weights:** $w_1 = 0.6$, $w_2 = 0.3$, $w_3 = 0.1$ (Sum = 1.0)

### C. Temporal Trust Score $T_i(t)$ (Exponential Moving Average)
- **File:** `akta/trust_engine.py`
- **Formula:** $T_i(t) = 0.7 \cdot P_i(t) + 0.3 \cdot T_i(t-1)$
- **Smoothing Parameter:** $\lambda = 0.7$
- **Initial Baseline:** $T_i(0) = 1.0$ (Benefit of the doubt on genesis registration)

### D. Multi-Factor Match Score
- **File:** `akta/vdr/registry_crud.py`
- **Formula:** $\text{match\_score}_i = 0.4 \cdot T_i + 0.3 \cdot \left(\frac{r_i}{5.0}\right) + 0.2 \cdot \sigma_i + 0.1 \cdot (1 - \lambda_i)$
- **Components:**
  - $T_i$: Temporal Trust Score ($0.0 - 1.0$)
  - $r_i$: Reputation Score ($1.0 - 5.0$ scale, normalized by $/ 5.0$)
  - $\sigma_i$: Historical Success Rate ($\frac{\text{successful\_tasks}}{\text{total\_tasks}}$)
  - $\lambda_i$: Normalized Latency ($\min(\frac{\text{last\_response\_time\_ms}}{2000}, 1.0)$)

---

## 3. Discrepancy & Reality Analysis (Grounded Truth)

| Subsystem | Theoretical / Paper Concept | Actual Implemented Reality | Handling in Diagrams |
|---|---|---|---|
| **Verifiable Data Registry (VDR)** | Often conceptualized as a distributed public or consortium blockchain (e.g. Hyperledger Indy, Ethereum). | Implemented as a local **SQLite database (`vdr.db`) in WAL mode** with 13 relational tables. | Accurately depicted as a local SQLite VDR; distributed blockchain marked as `PROPOSED / FUTURE SCOPE`. |
| **Agent Execution Engine** | Conceived as autonomous agents running live LLMs (OpenAI GPT-4, Claude, Gemini). | Implemented as **`LocalAgentConnector`**, providing deterministic structured capability simulations (research, analysis, coding, planning, verification) with an optional HTTP POST fallback. | Explicitly labeled as deterministic capability simulation in Diagrams 01, 14, 15, 18, 24. |
| **Workflow Execution Engine** | Schema accommodates both `SEQUENTIAL` and `PARALLEL` execution patterns. | Runtime orchestrator currently implements **`SEQUENTIAL` output-to-input chaining**. Parallel execution is defined in schema enum but not implemented as an async DAG. | Sequential execution shown in Diagrams 07, 15, 19; parallel execution explicitly labeled as `FUTURE SCOPE`. |
| **VC API Key Validation** | Production zero-trust access control for credential endpoints. | Currently commented out in development mode within `akta/vdr/router.py` to facilitate local development and automated testing. | Noted in index and sequence diagrams as local development configuration. |
| **Distributed Tracing** | OpenTelemetry SDK instrumentation. | OpenTelemetry packages are imported, but external collector export is not running in the local test environment. | Depicted as local FastAPI/in-process instrumentation only. |

---

## 4. Test Verification Trace

Every implemented behavior depicted in the sequence diagrams is verified by automated pytest test cases in `tests/`:

| Diagram | Key Behavioral Features Verified | Pytest Test Case |
|---|---|---|
| **09** (Identity Auth) | Argon2id verification, lockout after 5 attempts, token rotation, reuse detection. | `tests/test_authentication.py` |
| **10** (VC Lifecycle) | W3C credential creation, canonicalization, signature check, store & retrieve. | `tests/test_e2e_lifecycle.py` |
| **11** (Telemetry & Trust) | Sliding window computation, EMA update, state change detection. | `tests/test_e2e_lifecycle.py::test_e2e_telemetry_degradation_and_quarantine_path` |
| **12** (Adaptive Auth) | Gating privileged operations for SUSPICIOUS; blocking all for QUARANTINED and REVOKED. | `tests/test_adaptive_policy.py`, `tests/test_e2e_lifecycle.py` |
| **13** (Discovery Matching) | Capability filtering, exclusion of quarantined agents, match_score ranking. | `tests/test_platform_features.py::test_feature3_trust_aware_agent_matching` |
| **14** (Collaboration) | Session initiation, message logging, task execution, automatic telemetry emission. | `tests/test_multi_agent.py::test_collaboration_session_lifecycle_and_telemetry` |
| **15** (Workflows) | 3-node sequential execution, output-to-input data propagation, step status tracking. | `tests/test_platform_features.py::test_feature2_multi_agent_workflow_orchestrator` |
| **20** (State Machine) | Full degradation path (TRUSTED $\to$ SUSPICIOUS $\to$ QUARANTINED), recovery, administrative revocation. | `tests/test_e2e_lifecycle.py::test_e2e_recovery_and_administrative_revocation_path` |
