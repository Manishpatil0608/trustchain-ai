# TrustChain-AI Backend Service (`akta`)

The backend service for **TrustChain-AI** is a high-performance Python ASGI application built with FastAPI, SQLAlchemy, and PyNaCl. It exposes 39 authoritative REST endpoints providing decentralized agent identity, W3C Verifiable Credential registration, continuous behavioral telemetry ingestion, temporal trust scoring, adaptive zero-trust policy gating, task matching, and sequential workflow orchestration.

---

## Technical Stack & Architecture

- **Language:** Python >= 3.11, < 3.14 (Verified on Python 3.12.3)
- **Web Framework:** FastAPI (`fastapi` >= 0.115.0)
- **ASGI Server:** Uvicorn (`uvicorn` >= 0.34.0) with standard event loop
- **Persistence Layer:** SQLite 3 in WAL mode via SQLAlchemy 2.0 ORM
- **Identity & Keys:** W3C `did:key` (Ed25519 multicodec `0xED01`, multibase base58btc `z...`)
- **Verifiable Credentials:** W3C Linked Data Proofs with URDNA2015 canonicalization and `Ed25519Signature2020`
- **Security & RBAC:** JWT access tokens (HMAC-SHA256) with Argon2 password hashing and HTTP-only refresh rotation
- **Testing:** Pytest 9.1 with 80 comprehensive automated tests (100% pass rate)

---

## Directory Organization

```text
akta/
├── auth/                 # User authentication, JWT issuance, Argon2 hashing, RBAC, security audit
│   ├── crud.py           # User management, session tracking, security event logger
│   ├── dependencies.py   # FastAPI security dependencies (get_current_user, require_role)
│   ├── router.py         # Auth endpoints (/login, /refresh, /users, /audit)
│   ├── schemas.py        # Pydantic auth request/response schemas
│   └── security.py       # Password hashing, token generation, cryptographic validation
├── commands/             # CLI commands (claim, keys, registry, token, trust, vdr)
├── vdr/                  # Verifiable Data Registry & Database Models
│   ├── database.py       # SQLAlchemy engine, session maker, WAL pragma, table creation
│   ├── models.py         # Database schema (12 tables)
│   ├── registry_crud.py  # Agent registry, health check, discovery & matching algorithm
│   ├── registry_router.py# Agent registry & collaboration API routes
│   ├── router.py         # VDR, VC storage, telemetry & trust API routes
│   ├── schemas.py        # Pydantic models for VDR, agents, workflows, matching
│   └── trust_crud.py     # Database queries for telemetry, trust state, audits
├── adaptive_auth.py      # AdaptivePolicyEnforcer (Zero-trust policy decision point)
├── cli.py                # Command-line entry point
├── config.py             # Pydantic Settings configuration loader
├── connectors.py         # Connector factory for simulated and deterministic agent tools
├── credentials.py        # W3C Verifiable Credential builder, normalizer, and verifier
├── did.py                # W3C DID Core resolver, Ed25519 key generator, multibase parser
├── exceptions.py         # Domain-specific exception definitions
├── logging.py            # Structured JSON / Text logging with request ID tracking
├── server.py             # FastAPI application factory, middleware, CORS, health probe
├── telemetry.py          # Telemetry event schemas and synthetic observation harnesses
└── trust_engine.py       # Mathematical Trust Core (EMA decay, behavioral scoring)
```

---

## Quickstart & Execution

### 1. Create Virtual Environment
```bash
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database & Seed Safe Demo Data
```bash
python scripts/database/init_db.py
python scripts/database/seed_demo_data.py
```

### 4. Run Server
```bash
python -m uvicorn akta.server:app --host 127.0.0.1 --port 8050 --reload
```

### 5. Access Interactive API Documentation
- Swagger UI: [http://127.0.0.1:8050/docs](http://127.0.0.1:8050/docs)
- ReDoc: [http://127.0.0.1:8050/redoc](http://127.0.0.1:8050/redoc)
- Health Probe: [http://127.0.0.1:8050/health](http://127.0.0.1:8050/health)

### 6. Run Test Suite
```bash
pytest tests/ -v
```
