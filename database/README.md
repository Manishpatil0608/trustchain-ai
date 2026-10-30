# TrustChain-AI Database Design & VDR Architecture

TrustChain-AI utilizes an embedded, ACID-compliant **SQLite 3** storage engine configured in Write-Ahead Logging (WAL) mode as its local **Verifiable Data Registry (VDR)** and application persistence layer.

---

## 1. Architectural Clarification: Local VDR vs. Distributed Blockchain

> [!IMPORTANT]
> In TrustChain-AI, the Verifiable Data Registry (VDR) is implemented as an authoritative, locally hosted, high-integrity SQLite database operating under strict cryptographic verification rules.
> 
> While W3C Decentralized Identifier (DID) specifications permit distributed ledgers (blockchains) as VDRs, TrustChain-AI intentionally employs an embedded SQLite VDR for high-throughput, low-latency telemetry updates (sub-millisecond persistence) without consensus latency or transaction gas fees.
> 
> Cryptographic integrity is guaranteed mathematically via **W3C `did:key` algorithmic public key resolution** (self-certifying Ed25519 public keys) and **W3C Linked Data Proof (LDP) digital signatures**, rather than distributed mining or external consensus.

---

## 2. SQLite Engine Configuration

The database engine is configured in `akta/vdr/database.py` with the following performance and concurrency pragmas:

```python
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")     # Enables non-blocking concurrent reads and single-writer writes
    cursor.execute("PRAGMA synchronous=NORMAL")   # Guarantees durability with minimal disk sync overhead
    cursor.close()
```

- **Journal Mode:** `WAL` (Write-Ahead Logging) allows concurrent read transactions while a write transaction is executing.
- **Connection Timeout:** `30.0` seconds to gracefully handle concurrent write bursts.
- **Thread Safety:** `connect_args={"check_same_thread": False}` to support FastAPI multi-threaded async request workers.

---

## 3. Entity-Relationship & Table Inventory

The schema consists of 13 interrelated tables organized into four functional domains:

### A. Decentralized Identity & Credential Store
1. **`stored_vcs`**: Stores issued W3C Verifiable Credentials with JSON-LD Linked Data Proofs, issuer DIDs, subject DIDs, and validity dates.

### B. Behavioral Telemetry & Trust Intelligence
2. **`agent_trust_states`**: Authoritative record of each agent's current temporal trust score ($T_i(t) \in [0.0, 1.0]$) and active state (`TRUSTED`, `SUSPICIOUS`, `QUARANTINED`, `REVOKED`).
3. **`telemetry_logs`**: Continuous stream of runtime execution telemetry observations (task identifier, success flag, compliance violation string, and execution latency in ms).
4. **`trust_audit_trails`**: Immutable historical audit log capturing every state transition, previous state, new state, trigger timestamp, and natural language decision reason.

### C. Agent Catalog, Discovery & Collaboration
5. **`agents`**: Registry catalog holding agent metadata, DIDs, model providers, endpoints, operational statuses (`AVAILABLE`, `BUSY`, `OFFLINE`), endpoint health, and historical reputation.
6. **`collaboration_sessions`**: Records multi-agent task delegations, requester/target relationships, status lifecycles, and productivity outcomes.
7. **`collaboration_events`**: Audit trail of inter-agent messages, requests, responses, and intermediate payloads exchanged during a session.
8. **`agent_ratings`**: Post-collaboration peer evaluation feedback submitted by interacting agents.
9. **`workflows`**: Multi-agent task graphs (sequential and parallel execution plans).
10. **`workflow_nodes`**: Individual steps within a workflow assigned to specific agent DIDs with prerequisites and execution outputs.

### D. Authentication, RBAC & Security Audit
11. **`users`**: Platform user accounts with Argon2-hashed passwords, role designations (`ADMIN`, `OPERATOR`, `VIEWER`), and brute-force lockout counters.
12. **`refresh_tokens`**: Rotating JWT refresh token sessions with unique `jti` tracking and cryptographic reuse detection.
13. **`security_audit_events`**: Comprehensive authentication audit log capturing logins, failed attempts, logouts, session revocations, and administrative role updates.

---

## 4. Database Operations & Procedures

### Automatic Schema Creation
When the backend starts via `create_app()` or CLI, `akta/vdr/database.py:create_tables()` automatically invokes SQLAlchemy's `Base.metadata.create_all(bind=engine)`. If `vdr.db` does not exist, it is initialized immediately with all 13 tables.

### Development Auto-Seeding
If `APP_DEV_AUTO_SEED_ADMIN=True` in `.env`, the startup hook automatically creates a development administrator account if no users exist:
- **Username:** `admin`
- **Default Password:** `Admin@TrustChain2026!`
- **Role:** `ADMIN`

### Seeding Demonstration Data
To populate the database with realistic sample agents, verifiable credentials, and telemetry:
```bash
python scripts/database/seed_demo_data.py
```

### Resetting the Database
To perform a complete clean reset of local state:
```bash
# 1. Stop all TrustChain services
# 2. Delete database and WAL files
rm vdr.db vdr.db-shm vdr.db-wal

# 3. Re-initialize
python scripts/database/init_db.py
python scripts/database/seed_demo_data.py
```

### Backup Procedure
Because WAL mode is active, execute a safe backup checkpoint before copying:
```python
import sqlite3
conn = sqlite3.connect("vdr.db")
conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
conn.close()
```
Then safely copy `vdr.db` to the backup destination.
