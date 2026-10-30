# TrustChain-AI: Comprehensive Troubleshooting Guide

**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**

Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
Academic Session: 2026–2027  
Repository: `https://github.com/Manishpatil0608/trustchain-ai`

---

## Quick Reference Index

1. [PowerShell Script Execution Policy Error](#1-powershell-script-execution-policy-error)
2. [Port 8050 Already In Use (Backend Conflict)](#2-port-8050-already-in-use-backend-conflict)
3. [Port 5173 Already In Use (Frontend Conflict)](#3-port-5173-already-in-use-frontend-conflict)
4. [SQLite Database Disk Lock or WAL Contention](#4-sqlite-database-disk-lock-or-wal-contention)
5. [PyLD Network Failure During Offline Normalization](#5-pyld-network-failure-during-offline-normalization)
6. [CORS Policy Blocking Frontend API Requests](#6-cors-policy-blocking-frontend-api-requests)
7. [Authentication Failures & Admin Login Rejection](#7-authentication-failures--admin-login-rejection)
8. [Node.js & npm Installation / Dependency Errors](#8-nodejs--npm-installation--dependency-errors)
9. [Starlette TestClient Socketpair Hang on Windows](#9-starlette-testclient-socketpair-hang-on-windows)
10. [Docker Compose Container Connectivity Issues](#10-docker-compose-container-connectivity-issues)

---

### 1. PowerShell Script Execution Policy Error

#### Symptoms
When running `.\.venv\Scripts\Activate.ps1`, PowerShell outputs:
```text
File ...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

#### Likely Cause
Windows PowerShell default execution policy is set to `Restricted`, which blocks third-party unsigned scripts.

#### Resolution
Change the execution policy for the current process:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```
Alternatively, bypass execution policy directly:
```powershell
powershell -ExecutionPolicy Bypass -File .\.venv\Scripts\Activate.ps1
```

---

### 2. Port 8050 Already In Use (Backend Conflict)

#### Symptoms
Starting Uvicorn fails with:
```text
[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8050): only one usage of each socket address is normally permitted
```

#### Likely Cause
A previous Uvicorn background process was not terminated cleanly and remains bound to port 8050.

#### Resolution
**On Windows:**
```powershell
# Find process listening on 8050
netstat -ano | findstr :8050

# Terminate process by PID (e.g., PID 1234)
taskkill /F /PID 1234
```
Or run the included batch script:
```cmd
STOP_TRUSTCHAIN.bat
```

**On Linux / macOS:**
```bash
lsof -ti:8050 | xargs kill -9
```

---

### 3. Port 5173 Already In Use (Frontend Conflict)

#### Symptoms
Vite starts on `http://localhost:5174` instead of `5173`, causing CORS or hardcoded redirect mismatches.

#### Likely Cause
Another instance of Vite or another development server is running on port 5173.

#### Resolution
**On Windows:**
```powershell
netstat -ano | findstr :5173
taskkill /F /PID <PID>
```
**On Linux / macOS:**
```bash
lsof -ti:5173 | xargs kill -9
```

---

### 4. SQLite Database Disk Lock or WAL Contention

#### Symptoms
FastAPI outputs:
```text
sqlite3.OperationalError: database is locked
```

#### Likely Cause
A long-running query or crashed process left an uncommitted transaction in `vdr.db-wal`.

#### Resolution
Execute an immediate WAL truncation checkpoint using Python:
```python
import sqlite3
conn = sqlite3.connect("vdr.db")
conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
conn.close()
```
If the lock persists, stop the server, delete runtime lock files, and restart:
```powershell
Remove-Item vdr.db-wal, vdr.db-shm -Force
```

---

### 5. PyLD Network Failure During Offline Normalization

#### Symptoms
When issuing or signing a Verifiable Credential in an air-gapped or network-isolated environment:
```text
urllib3.exceptions.NameResolutionError: Failed to resolve 'www.w3.org'
```

#### Likely Cause
By default, the `pyld` library attempts to dereference remote `@context` URLs (`https://www.w3.org/2018/credentials/v1`) over HTTPS.

#### Resolution
Use the offline-safe seeder provided in `scripts/database/seed_demo_data.py`, which formats and signs the W3C credential locally without remote network resolution.

---

### 6. CORS Policy Blocking Frontend API Requests

#### Symptoms
Browser developer console displays:
```text
Access to XMLHttpRequest at 'http://127.0.0.1:8050/api/v1/auth/login' from origin 'http://localhost:5173' has been blocked by CORS policy.
```

#### Likely Cause
Frontend origin is missing from `APP_CORS_ALLOWED_ORIGINS` in `.env`.

#### Resolution
Open `.env` in the project root and ensure your frontend origin is listed:
```ini
APP_CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:8050
```
Restart the FastAPI backend.

---

### 7. Authentication Failures & Admin Login Rejection

#### Symptoms
Logging into the frontend with `admin` / `Admin@TrustChain2026!` returns `401 Unauthorized` or `400 Bad Request`.

#### Likely Cause
Database was reset without auto-seeding enabled, or password hash was corrupted.

#### Resolution
Run the safe seeder script to recreate and verify the administrator account:
```powershell
python scripts/database/seed_demo_data.py
```
Verify the output confirms:
```text
[+] Admin confirmed: admin (ADMIN)
```

---

### 8. Node.js & npm Installation / Dependency Errors

#### Symptoms
`npm install` fails with `ERESOLVE unable to resolve dependency tree` or version warnings.

#### Likely Cause
Node.js version is below 18.x, or conflicting global npm packages exist.

#### Resolution
1. Verify Node version: `node --version` (Must be >= 18.0.0, Node 20 LTS recommended).
2. Use clean install:
```bash
cd frontend
npm ci
```

---

### 9. Starlette TestClient Socketpair Hang on Windows

#### Symptoms
When running `pytest` in sandboxed or loopback-restricted environments on Windows, tests hang indefinitely during `client = TestClient(app)`.

#### Likely Cause
Starlette's `TestClient` uses AnyIO's blocking portal which invokes `asyncio.ProactorEventLoop._make_self_pipe()`. On Windows, this creates a TCP loopback socket connection (`socket.socketpair()`). If loopback networking is blocked, `socketpair()` hangs waiting on `accept()`.

#### Resolution
Ensure loopback access (`127.0.0.1`) is permitted in the terminal execution environment. Run tests with:
```powershell
pytest tests/ -v
```

---

### 10. Docker Compose Container Connectivity Issues

#### Symptoms
Frontend container starts but shows "Backend unavailable" or "Failed to fetch".

#### Likely Cause
Container network hostname resolution mismatch. The frontend browser runs on the host machine and must connect to `http://localhost:8050` or through the Nginx reverse-proxy on port 5173.

#### Resolution
Verify both containers are healthy:
```bash
docker-compose ps
```
Both `trustchain-backend` and `trustchain-frontend` must show `Up (healthy)`. Inspect backend logs:
```bash
docker-compose logs -f backend
```
Test direct health check on host:
```bash
curl http://localhost:8050/health
```
