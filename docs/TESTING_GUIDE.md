# TrustChain-AI: Automated & Manual Testing Guide

**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**

Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
Academic Session: 2026–2027  
Repository: `https://github.com/Manishpatil0608/trustchain-ai`

---

## 1. Test Suite Summary & Current Status

The TrustChain-AI automated test suite comprises **80 unit, integration, and end-to-end test scenarios** executed via Pytest.

| Test Category | Test File | Test Count | Execution Time | Current Status |
|---|---|:---:|:---:|:---:|
| **Verifiable Credential Claims** | `tests/commands/test_claim.py` | 11 | 1.82s | **PASSED** |
| **Cryptographic Key Management**| `tests/commands/test_keys.py` | 4 | 0.65s | **PASSED** |
| **Registry CLI Commands** | `tests/commands/test_registry.py` | 7 | 1.10s | **PASSED** |
| **Token Verification & Parsing**| `tests/commands/test_token.py` | 3 | 0.48s | **PASSED** |
| **VDR Registry Persistence** | `tests/commands/test_vdr.py` | 3 | 0.52s | **PASSED** |
| **Zero-Trust Adaptive Policy** | `tests/test_adaptive_policy.py` | 7 | 2.15s | **PASSED** |
| **Authentication, JWT & RBAC** | `tests/test_authentication.py` | 28 | 4.60s | **PASSED** |
| **CLI Core Entrypoint** | `tests/test_cli.py` | 1 | 0.22s | **PASSED** |
| **End-to-End Agent Lifecycle** | `tests/test_e2e_lifecycle.py` | 3 | 1.95s | **PASSED** |
| **Investigation, Discovery & Match**| `tests/test_investigation_discovery_matching.py`| 3 | 1.20s | **PASSED** |
| **Multi-Agent Collaboration** | `tests/test_multi_agent.py` | 3 | 1.05s | **PASSED** |
| **Platform Telemetry Features**| `tests/test_platform_features.py`| 3 | 0.92s | **PASSED** |
| **Subsystem Health & Fault Injection**| `tests/test_system_health.py` | 4 | 2.00s | **PASSED** |
| **TOTAL** | **13 Test Modules** | **80 Tests** | **18.76s** | **100% PASS** |

---

## 2. Executing Automated Backend Tests

### Full Test Suite Execution
From the project root with the virtual environment activated:
```bash
pytest tests/ -v
```

### Running Specific Test Modules
To run only the Zero-Trust Adaptive Policy test module:
```bash
pytest tests/test_adaptive_policy.py -v
```

To run Subsystem Health and failure simulation tests:
```bash
pytest tests/test_system_health.py -v
```

To run Authentication and RBAC tests:
```bash
pytest tests/test_authentication.py -v
```

### Running with Console Output & Short Tracebacks
```bash
pytest tests/ -s --tb=short
```

---

## 3. Key Tested Scenarios & Assertions

### A. Zero-Trust Adaptive Policy Enforcement (`test_adaptive_policy.py`)
1. **TRUSTED Agent Access:** Asserts agents with $T \ge 0.80$ succeed on both standard (`task:execute`, `map:generate`) and privileged operations (`workflow:execute`, `agent:delegate`).
2. **SUSPICIOUS Agent Restricted Gating:** Asserts agents with $0.50 \le T < 0.80$ succeed on standard operations under heightened monitoring, but raise `AuthorizationError` (HTTP 403) on privileged operations.
3. **Workflow Interception:** Asserts that an in-progress workflow execution halts with HTTP 403 if a worker node degrades to `SUSPICIOUS` state midway.
4. **QUARANTINED Agent Isolation:** Asserts agents with $T < 0.50$ are denied across all operations and rejected from collaboration matching.
5. **Irreversible Revocation:** Asserts administratively revoked agents remain permanently blocked even when subsequent compliant telemetry arrives.

### B. Subsystem Health & Fault Injection (`test_system_health.py`)
1. **Authoritative Health:** Verifies `/health` returns 200 OK and validates probes for FastAPI, SQLite VDR, and Trust Math Core.
2. **Database Failure Simulation:** Injects an artificial SQLite disk/lock exception; verifies `/health` gracefully reports `"status": "degraded"` and identifies the database component failure without server crash.
3. **Trust Math Failure Simulation:** Injects mathematical calculation errors; verifies `/health` isolates the math core component error.

### C. Authentication, Token Rotation & RBAC (`test_authentication.py`)
1. **Argon2 Password Hashing:** Asserts password hashes use dynamic salts and differ from plain text.
2. **Refresh Token Rotation:** Asserts calling `/auth/refresh` rotates the refresh token and issues a new access token.
3. **Cryptographic Reuse Detection:** Asserts presenting an already-rotated refresh token triggers immediate invalidation of all sessions for that user.
4. **Brute-Force Account Lockout:** Asserts 5 consecutive invalid login attempts locks the user account for 15 minutes.

---

## 4. Frontend Build & Static Analysis Verification

### Static Analysis (Oxlint)
```bash
cd frontend
npm run lint
```
**Expected Output:** `Found 0 errors.`

### Production Build Verification (Vite 8)
```bash
cd frontend
npm run build
```
**Expected Output:**
```text
vite v8.2.2 building client environment for production...
transforming...
✓ 2478 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   0.45 kB │ gzip:   0.31 kB
dist/assets/index-CQ5aDuwy.css  103.05 kB │ gzip:  15.53 kB
dist/assets/index-DtV661go.js   947.78 kB │ gzip: 255.12 kB
✓ built in 26.17s
```

---

## 5. End-to-End Manual Browser Testing Runbook

To manually verify the full interactive platform:

1. **Start Services:** Execute `START_TRUSTCHAIN.bat` (Windows) or manual terminal commands.
2. **Login:** Navigate to [http://localhost:5173/login](http://localhost:5173/login). Enter `admin` / `Admin@TrustChain2026!`.
3. **Verify Dashboard:** Check the SOC Dashboard overview card. Verify overall status reports `"OPERATIONAL"` and lists active agents.
4. **Agent Explorer:** Navigate to `/agents`. Click on **Agent Alpha**. The inspection drawer opens showing its DID, issued Verifiable Credential, and current trust score ($0.963$).
5. **Test Zero-Trust Policy Gating:** Navigate to `/authorization`. Click **"Execute Protected Tool (`/map/generate`)"** for Agent Alpha -> Output: **200 OK (Allowed)**.
6. **Trigger Telemetry Degradation:** Navigate to `/telemetry`. Select **Agent Alpha**. Click **"Inject Failing Telemetry (3x Failures, High Latency)"**.
7. **Observe Trust Decay:** Navigate to `/analytics`. Watch Agent Alpha's temporal trust score decay from $0.963$ down to $0.492$ (`QUARANTINED`).
8. **Verify Quarantine Interception:** Return to `/authorization`. Attempt tool execution for Agent Alpha -> Output: **HTTP 403 Forbidden: Agent QUARANTINED**.
9. **Verify Trust Recovery:** In `/telemetry`, inject 5 consecutive clean events. Return to `/authorization` -> Output: **200 OK (Access Restored)**.
