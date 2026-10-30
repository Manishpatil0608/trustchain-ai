# TrustChain-AI: Installation & Setup Guide

**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**

Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
Academic Session: 2026–2027  
Repository: `https://github.com/Manishpatil0608/trustchain-ai`

---

## 1. System Requirements

| Component | Minimum Specification | Recommended Specification |
|---|---|---|
| **Operating System** | Windows 10/11, Ubuntu 22.04 LTS, macOS 13+ | Windows 11 / Ubuntu 24.04 LTS |
| **Python** | Python 3.11.x | Python 3.12.x (Tested on 3.12.3) |
| **Node.js** | Node.js 18.x | Node.js 20.x+ |
| **Package Managers**| `pip` >= 23.0, `npm` >= 9.0 | Latest `pip` and `npm` |
| **Memory (RAM)** | 4 GB | 8 GB+ |
| **Disk Storage** | 2 GB free space | 5 GB free space |
| **Network** | Offline-capable for execution; Internet required for initial dependency downloads | Broadband connection |

---

## 2. Quickstart via Automated Script (Windows)

If you are on Windows, the entire platform can be launched in two automated terminal windows using the included launcher:

```cmd
:: Run launcher from project root
START_TRUSTCHAIN.bat
```
This batch script will:
1. Verify the Python virtual environment and frontend directory.
2. Check if ports 8050 and 5173 are listening.
3. Launch the FastAPI backend on port 8050 in a dedicated green terminal.
4. Launch the React/Vite frontend on port 5173 in a dedicated cyan terminal.
5. Launch your default browser to `http://localhost:5173`.

To stop the running application:
```cmd
STOP_TRUSTCHAIN.bat
```

---

## 3. Manual Step-by-Step Installation (Windows PowerShell)

### Step 1: Clone Repository
```powershell
git clone https://github.com/Manishpatil0608/trustchain-ai.git
cd trustchain-ai
```

### Step 2: Configure Environment Variables
```powershell
Copy-Item .env.example .env
```

### Step 3: Set Up Python Backend
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install backend dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Initialize Database & Seed Demonstration Data
```powershell
# Initialize SQLite VDR schema (13 tables)
python scripts/database/init_db.py

# Seed demo agents, credentials, and baseline telemetry
python scripts/database/seed_demo_data.py
```

### Step 5: Set Up React Frontend
Open a second PowerShell window:
```powershell
cd trustchain-ai\frontend

# Install dependencies using clean install
npm ci

# Optional: verify linting
npm run lint
```

### Step 6: Start Application Services
**Terminal 1 (Backend):**
```powershell
cd trustchain-ai
.\.venv\Scripts\Activate.ps1
python -m uvicorn akta.server:app --host 127.0.0.1 --port 8050 --reload
```

**Terminal 2 (Frontend):**
```powershell
cd trustchain-ai\frontend
npm run dev
```

### Step 7: Open in Browser
Open [http://localhost:5173](http://localhost:5173).  
Log in with default development credentials:
- **Username:** `admin`
- **Password:** `Admin@TrustChain2026!`

---

## 4. Manual Step-by-Step Installation (Linux / macOS)

### Step 1: Clone Repository
```bash
git clone https://github.com/Manishpatil0608/trustchain-ai.git
cd trustchain-ai
```

### Step 2: Configure Environment Variables
```bash
cp .env.example .env
```

### Step 3: Set Up Python Backend
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Initialize Database & Seed Demonstration Data
```bash
python scripts/database/init_db.py
python scripts/database/seed_demo_data.py
```

### Step 5: Set Up React Frontend
In a new terminal:
```bash
cd frontend
npm ci
```

### Step 6: Start Application Services
**Terminal 1 (Backend):**
```bash
source .venv/bin/activate
python -m uvicorn akta.server:app --host 127.0.0.1 --port 8050 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

---

## 5. Containerized Deployment (Docker Compose)

If Docker Desktop is installed, you can build and run both services in an isolated multi-container network with persistent storage:

```bash
# Build and start all containers
docker-compose up --build -d

# Check running container status
docker-compose ps

# View real-time logs
docker-compose logs -f

# Verify backend health probe
curl http://localhost:8050/health

# Stop and remove containers
docker-compose down
```

The frontend will be accessible at `http://localhost:5173` and the backend API at `http://localhost:8050`.

---

## 6. Verification Checklist

1. **Backend Health Check:** Visit [http://127.0.0.1:8050/health](http://127.0.0.1:8050/health). Status must report `"status": "ok"`.
2. **Interactive API Docs:** Visit [http://127.0.0.1:8050/docs](http://127.0.0.1:8050/docs). Swagger UI should render 39 endpoints.
3. **Frontend SOC Dashboard:** Visit [http://localhost:5173](http://localhost:5173). Dashboard renders agent cards, charts, and metrics.
4. **Pytest Verification:** Run `pytest tests/ -v`. All 80 test cases must report `PASSED`.
