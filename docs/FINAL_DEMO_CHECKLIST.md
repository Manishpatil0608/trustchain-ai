# Final Demo Checklist

The TrustChain-AI system is **DEMO READY**.

A student or researcher can realistically demonstrate the entire project lifecycle by executing the following sequence from a clean environment.

## 1. Prerequisites
Ensure Python 3.10+ and the required packages are installed:
```bash
pip install -e .
```

## 2. Server Startup
Open a terminal and start the Uvicorn server:
```bash
python -m uvicorn akta.server:app --port 8050
```
Keep this terminal running in the background.

## 3. Automated End-to-End Demonstration
Open a separate terminal and run the demo script:
```bash
python scripts/demo_trustchain.py
```

### What to Expect During the Demo:
1. **Identity Layer:** The script will create an Issuer DID and an Agent Charlie DID.
2. **VC Generation:** The Issuer will sign and grant a verifiable credential (VC) to Charlie.
3. **Execution (TRUSTED):** Charlie will repeatedly invoke the protected `/map/generate` API and receive HTTP 200, generating successful telemetry.
4. **Behavioral Degradation (SUSPICIOUS $\rightarrow$ QUARANTINED):** The script simulates bad telemetry (e.g., failed tasks, policy violations). You will see the Trust Engine lower Charlie's score mathematically until it reaches the `QUARANTINED` threshold (<0.5).
5. **Adaptive Authorization Pivot:** The same agent, using the exact same unexpired cryptographic token, will suddenly be blocked with an HTTP 403 error.
6. **Recovery:** The script injects positive telemetry, raising the score back above 0.8, re-enabling access (HTTP 200).
7. **Terminal Override:** The system performs a manual administrative override (`REVOKED`), proving that revocation completely blocks access (HTTP 403) and supersedes numerical recovery.

## 4. UI Dashboard (Optional)
At any point during the demo, you can open a web browser to:
`http://localhost:8050/api/v1/trust/dashboard`
This displays the real-time trust state of all agents interacting with the system.

## 5. CLI Interactions (Optional)
You can manually inspect Charlie's state during the demo:
```bash
python -m akta.cli trust agents
python -m akta.cli trust score <Charlie's DID>
python -m akta.cli trust state <Charlie's DID>
```
