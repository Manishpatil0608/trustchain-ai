# Reproducibility Guide

## Environment Specifications
- **Operating System**: Windows (Tested in PowerShell)
- **Python Version**: >= 3.12 (as tested)
- **Primary Dependencies**:
  - `a2a-sdk == 0.2.5` (Strict requirement for cryptographic baseline)
  - `fastapi`
  - `uvicorn`
  - `sqlalchemy`
  - `pydantic`
- **Environment Blocker**: Windows environment does not natively support `jq`. The baseline test `test_delegation_workflow.sh` relies on `jq` for parsing JSON. For true baseline regression testing on Windows, Git Bash with `jq` installed is required.

## Installation
```bash
# From the repository root
pip install -e .
```

## Server Startup
```bash
python -m uvicorn akta.server:app --port 8050
```

## Test Commands
```bash
# Internal logic verification (No server required)
python test_trustchain_logic.py
python test_edge_cases.py

# End-to-end integration tests (Server required)
python test_trustchain_workflow.py

# Full demonstration lifecycle
python scripts/demo_trustchain.py
```

## Experiments
```bash
python experiments/runners/run_experiments.py
```
