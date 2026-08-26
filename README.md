# TrustChain-AI

A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration.

TrustChain-AI extends standard Verifiable Credentials (VC) with continuous, behavioral trust metrics. Rather than relying solely on cryptographic identity (which proves *who* an agent is), TrustChain-AI evaluates *how* an agent behaves over time. 

If a cryptographically authenticated agent begins to act maliciously or erratically, TrustChain-AI's adaptive authorization middleware will gracefully quarantine the agent, protecting target APIs from compromised credentials.

## Architecture

1. **Cryptographic Identity Layer (Base)**: Agents authenticate using `did:key` and W3C Verifiable Credentials.
2. **Execution Context**: When an agent attempts an action (e.g. `POST /map/generate`), the request is validated.
3. **Telemetry Collection**: Actions generate telemetry (success/failure, compliance, latency) which is fed into the Trust Engine.
4. **Trust Engine**: Calculates real-time temporal trust scores based on Success Rate, Compliance Rate, and Latency, applying an exponential temporal decay ($\lambda$).
5. **Adaptive Authorization**: As scores decay below predefined thresholds (`SUSPICIOUS`, `QUARANTINED`), the agent's access is restricted at the API gateway layer regardless of their valid cryptographic token.

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/trustchain-ai.git
cd trustchain-ai/akta-base

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the End-to-End Demo

We provide a self-contained demonstration script that simulates the entire lifecycle of an AI agent collaborating in the TrustChain-AI ecosystem.

1. **Start the API Server**:
   ```bash
   python -m uvicorn akta.server:app --port 8050
   ```

2. **Run the Lifecycle Demo**:
   Open a new terminal and run:
   ```bash
   python scripts/demo_trustchain.py
   ```
   
   *This script will:*
   - Initialize cryptographic identities (DIDs).
   - Issue capability Verifiable Credentials.
   - Execute standard tasks, raising the agent's Trust Score to `TRUSTED`.
   - Simulate degraded agent behavior, dropping the agent to `QUARANTINED`.
   - Demonstrate the Adaptive Policy Enforcer actively blocking the agent (`HTTP 403 Forbidden`).
   - Allow the agent to recover behaviorally.
   - Conclude with an administrative revocation (`REVOKED`).

## CLI Commands

The `akta` CLI includes a powerful suite for both cryptographic and trust operations.

### Trust Management

```bash
# View the current trust score and state
akta trust score <did>
akta trust state <did>

# View the comprehensive audit trail of state transitions
akta trust audit <did>

# List all agents known to the system and their current state
akta trust agents

# Administratively revoke an agent permanently
akta trust revoke <did> --reason "Compromised key"
```

## Dashboard & APIs

**Web Dashboard**  
Navigate to `http://localhost:8050/api/v1/trust/dashboard` in your browser for a real-time HTML view of all active agents and their behavioral trust states.

**Key API Endpoints**
- `POST /api/v1/trust/telemetry` - Ingest an execution telemetry event.
- `GET /api/v1/trust/state/{did}` - Fetch real-time temporal trust state.
- `GET /api/v1/trust/audit/{did}` - Fetch immutable state transition history.
- `POST /api/v1/trust/revoke/{did}` - Terminate an agent.
- `POST /api/v1/map/generate` - The target API heavily protected by the Adaptive Policy Enforcer.