# TrustChain-AI: Developer & Contributor Guide

**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**

Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
Academic Session: 2026–2027  
Repository: `https://github.com/Manishpatil0608/trustchain-ai`

---

## 1. Development Principles

When contributing to TrustChain-AI, adhere to the following architectural tenets:
1. **Mathematical Grounding:** Every state transition and authorization decision must remain deterministically grounded in verifiable telemetry and cryptographic proofs.
2. **Defensive API Design:** All input payloads must be strictly validated using Pydantic models. Unhandled exceptions must never crash the ASGI worker.
3. **Audit Immutability:** Any security-critical or state-altering operation must produce an audit record in `trust_audit_trails` or `security_audit_events`.
4. **Offline Reproducibility:** Core identity and trust algorithms must be executable offline without mandatory reliance on cloud APIs.

---

## 2. Setting Up a Local Development Environment

```bash
# 1. Clone repository
git clone https://github.com/Manishpatil0608/trustchain-ai.git
cd trustchain-ai

# 2. Configure environment
cp .env.example .env

# 3. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1

# 4. Install backend dependencies in editable mode
pip install -r requirements.txt

# 5. Initialize database
python scripts/database/init_db.py
python scripts/database/seed_demo_data.py

# 6. Install frontend dependencies
cd frontend
npm ci
cd ..
```

---

## 3. Extending Platform Capabilities

### A. Adding a New Autonomous Agent Capability
1. Open `akta/vdr/registry_crud.py`.
2. Define the capability string in the registry validation schemas (`schemas.AgentRegisterRequest`).
3. If the capability is security-sensitive (e.g., executing code or administering resources), register it under `AdaptivePolicyEnforcer.PRIVILEGED_OPERATIONS` in `akta/adaptive_auth.py`:
   ```python
   PRIVILEGED_OPERATIONS: Set[str] = {
       "workflow:execute",
       "workflow:orchestrate",
       "agent:delegate",
       "credential:issue",
       "admin:revoke",
       "my_new_privileged_cap",  # Add here
   }
   ```
4. If it is standard, add it to `STANDARD_OPERATIONS`.

### B. Adjusting Trust Engine Mathematical Parameters
The mathematical weights and decay parameters are defined in `akta/trust_engine.py`:
```python
class TrustConfig(BaseModel):
    w1: float = 0.60  # Success Rate Weight
    w2: float = 0.30  # Compliance Rate Weight
    w3: float = 0.10  # Latency Penalty Weight
    lam: float = 0.70 # Temporal Memory Decay Factor
    
    trusted_threshold: float = 0.80
    suspicious_threshold: float = 0.50
    max_latency_ms: int = 2000
```
- Ensure $w_1 + w_2 + w_3 = 1.00$ and $0 \le \lambda \le 1$.
- Any modification must be verified by running `pytest tests/test_adaptive_policy.py`.

### C. Adding a New REST API Endpoint
1. Locate the appropriate router under `akta/` (e.g., `akta/vdr/registry_router.py` or `akta/auth/router.py`).
2. Define the Pydantic request and response schemas in `schemas.py`.
3. Add database queries in `crud.py` using SQLAlchemy session patterns:
   ```python
   @router.post("/registry/my-endpoint", response_model=schemas.MyResponse)
   async def my_endpoint(req: schemas.MyRequest, db: Session = Depends(get_db)):
       return my_crud.execute(db, req)
   ```
4. Update `tests/` with unit tests validating expected HTTP response codes (200, 400, 401, 403).

### D. Adding a New React Component
1. Place new JSX views in `frontend/src/components/`.
2. Register the route in `frontend/src/App.jsx`.
3. Add the navigation item in `frontend/src/components/TopBar.jsx` or sidebar menu.
4. Execute `npm run lint` and `npm run build` in `frontend/` to ensure zero compilation warnings or errors.

---

## 4. Git Conventions & PR Workflow

### Branch Naming
- Features: `feature/<feature-name>`
- Bugfixes: `fix/<issue-name>`
- Documentation: `docs/<doc-name>`

### Commit Message Format
TrustChain-AI adheres to [Conventional Commits](https://www.conventionalcommits.org/):
- `feat: implement dynamic radar visualization for agent matching`
- `fix: resolve SQLite busy timeout during telemetry bursts`
- `docs: update installation instructions for macOS ARM64`
- `test: add unit test for zero-trust workflow node interception`

### Pull Request Checklist
Before opening a PR to `main`:
1. `pytest tests/ -v` (80/80 passed).
2. `npm run lint` in `frontend/` (0 errors).
3. `npm run build` in `frontend/` (Clean build).
4. Verify no `.env`, `vdr.db`, or temporary log files are tracked in git.
