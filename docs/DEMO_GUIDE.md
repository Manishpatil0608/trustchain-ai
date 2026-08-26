# TrustChain-AI Project Demonstration Guide

This guide explains how a reviewer or researcher can independently run and evaluate the complete TrustChain-AI lifecycle.

## 1. Prerequisites
- Python 3.12+
- Operating System: Linux, macOS, or Windows (Note: The baseline Akta test `test_delegation_workflow.sh` requires `jq`, which is typically absent natively on Windows powershell. Use Git Bash if verifying the baseline on Windows).

## 2. Installation
Install the project dependencies in a clean virtual environment from the repository root:
```bash
pip install -e .
```

## 3. Start the TrustChain Server
The framework relies on a persistent FastAPI background service.
```bash
python -m uvicorn akta.server:app --port 8050
```

## 4. Run the Full Lifecycle Demo
This is the primary demonstration script. It autonomously initializes agents, delegates capabilities, executes valid requests, simulates a behavioral attack, observes quarantine denial, recovers the agent, and manually revokes it.
```bash
python scripts/demo_trustchain.py
```

## 5. Verify the Test Suite
The following commands execute the mathematical logic verification and API boundary assertions. (Ensure the server is running for workflow tests).
```bash
python test_trustchain_logic.py
python test_edge_cases.py
python test_trustchain_workflow.py
```

## 6. Verify Baseline Cryptography (Optional)
To prove the original cryptographic foundation (Akta) remains functionally intact:
```bash
bash test_delegation_workflow.sh
```

## 7. Run Research Experiments
Execute the simulated experiments to regenerate the mathematical boundary data supporting the H3 and H4 research claims.
```bash
python experiments/runners/run_experiments.py
```

## 8. Explore the Dashboard
Navigate to your browser while the server is active:
[http://127.0.0.1:8050/api/v1/trust/dashboard](http://127.0.0.1:8050/api/v1/trust/dashboard)
