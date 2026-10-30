# TrustChain-AI — Master Diagram Index

This document provides a comprehensive index of all 25 Mermaid diagrams created for the B.Tech final-year capstone project:
**TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**.

All diagrams are grounded strictly in the actual codebase located at `D:\capstone project\trustchain-ai\akta-base`. Any conceptual or future architectural aspirations are explicitly annotated as `PROPOSED` or `FUTURE SCOPE`.

---

## Master Diagram Catalogue

| # | Title | Filename | Mermaid Type | Purpose | Primary Source Files | Status | Target Chapter |
|---|-------|----------|--------------|---------|----------------------|--------|----------------|
| **01** | System Architecture | `01_system_architecture.mmd` | `flowchart TB` | Comprehensive 5-layer system stack from React 19 UI to SQLite VDR. | `akta/server.py`, `akta/trust_engine.py`, `frontend/src/` | **Implemented** | Chapter 3 (3.2) |
| **02** | System Context | `02_system_context.mmd` | `flowchart TB` | System boundary depicting human actors (Admin/Operator/Viewer) vs autonomous agents. | `akta/auth/`, `akta/vdr/router.py` | **Implemented** | Chapter 1 (1.5) / Chapter 3 (3.2) |
| **03** | Data Flow Diagram — Level 0 | `03_dfd_level_0.mmd` | `flowchart LR` | Context-level DFD showing external entities, primary inputs, and generated artifacts. | `akta/server.py`, `akta/vdr/router.py` | **Implemented** | Chapter 3 (3.2) |
| **04** | Data Flow Diagram — Level 1 | `04_dfd_level_1.mmd` | `flowchart TB` | Subsystem decomposition into 9 functional processes and 9 SQLite datastores. | `akta/vdr/models.py`, `akta/vdr/registry_crud.py` | **Implemented** | Chapter 3 (3.2) |
| **05** | DFD Level 2 — Trust Evaluation Pipeline | `05_dfd_level_2_trust_evaluation.mmd` | `flowchart TB` | Granular data transformations from raw telemetry ingestion to temporal EMA state updates. | `akta/telemetry.py`, `akta/trust_engine.py` | **Implemented** | Chapter 3 (3.4) |
| **06** | Behavioral View Across Lifecycle | `06_behavioral_view.mmd` | `flowchart TD` | Longitudinal dynamics across registration, task execution, degradation, and recovery. | `akta/trust_engine.py`, `tests/test_e2e_lifecycle.py` | **Implemented** | Chapter 3 (3.4) |
| **07** | Use Case Diagram | `07_use_case_diagram.mmd` | `flowchart LR` | UML-style use cases mapped to human roles and autonomous agent actors. | `akta/auth/`, `akta/adaptive_auth.py` | **Implemented** | Chapter 3 (3.5) |
| **08** | Activity Diagram — Agent Request Lifecycle | `08_activity_diagram.mmd` | `flowchart TD` | Detailed control-flow with decision branching for authentication, trust gating, and telemetry. | `akta/adaptive_auth.py`, `akta/agent_connector.py` | **Implemented** | Chapter 3 (3.5) |
| **09** | Sequence — Identity & User Authentication | `09_sequence_identity_authentication.mmd` | `sequenceDiagram` | Argon2id login, 5-strike lockout, JWT refresh rotation, and DID signature validation. | `akta/auth/`, `akta/did.py` | **Implemented** | Chapter 3 (3.9) |
| **10** | Sequence — Verifiable Credential Lifecycle | `10_sequence_vc_lifecycle.mmd` | `sequenceDiagram` | W3C VC issuance, URDNA2015 canonicalization, Ed25519Signature2020 signing, and verification. | `akta/credentials.py`, `akta/vdr/router.py` | **Implemented** | Chapter 3 (3.3) |
| **11** | Sequence — Telemetry & Dynamic Trust Scoring | `11_sequence_telemetry_trust.mmd` | `sequenceDiagram` | Ingestion of telemetry, sliding window computation, EMA update, and audit trail generation. | `akta/telemetry.py`, `akta/trust_engine.py` | **Implemented** | Chapter 3 (3.4) |
| **12** | Sequence — Adaptive Authorization Enforcement | `12_sequence_adaptive_authorization.mmd` | `sequenceDiagram` | Operation-level gating (PRIVILEGED vs STANDARD) across TRUSTED, SUSPICIOUS, QUARANTINED, REVOKED. | `akta/adaptive_auth.py` | **Implemented** | Chapter 3 (3.5) |
| **13** | Sequence — Agent Discovery & Matching | `13_sequence_agent_discovery_matching.mmd` | `sequenceDiagram` | Multi-factor capability filtering and composite match scoring ranking. | `akta/vdr/registry_crud.py` | **Implemented** | Chapter 3 (3.6) |
| **14** | Sequence — Multi-Agent Collaboration Session | `14_sequence_collaboration_session.mmd` | `sequenceDiagram` | Mutual trust verification, interactive message exchange, task execution, and mutual telemetry. | `akta/vdr/registry_crud.py`, `akta/agent_connector.py` | **Implemented** | Chapter 3 (3.7) |
| **15** | Sequence — Sequential Workflow Orchestration | `15_sequence_sequential_workflow.mmd` | `sequenceDiagram` | Multi-step chained pipeline passing step outputs to subsequent node inputs. | `akta/vdr/registry_crud.py`, `akta/agent_connector.py` | **Implemented** | Chapter 3 (3.8) |
| **16** | Sequence — Audit Logging & Governance | `16_sequence_audit_governance.mmd` | `sequenceDiagram` | Security audit events, trust transition trails, and administrator investigation flows. | `akta/auth/`, `akta/vdr/models.py` | **Implemented** | Chapter 3 (3.9) |
| **17** | Database Entity-Relationship Diagram | `17_er_diagram.mmd` | `erDiagram` | Complete schema of all 13 SQLite tables, primary keys, foreign keys, and cardinalities. | `akta/vdr/models.py` | **Implemented** | Chapter 3 (3.10) |
| **18** | Subsystems & Domain Class Diagram | `18_class_diagram.mmd` | `classDiagram` | Core domain classes, enums, configuration objects, ORM models, and relationships. | `akta/trust_engine.py`, `akta/adaptive_auth.py`, `akta/vdr/models.py` | **Implemented** | Chapter 3 (3.2) |
| **19** | Complete End-to-End Project Workflow | `19_complete_project_workflow.mmd` | `flowchart TD` | Master macro workflow covering system boot, registration, discovery, execution, trust, and audit. | All backend & frontend modules | **Implemented** | Chapter 3 (3.1) / Chapter 4 |
| **20** | Agent Trust State Transition Machine | `20_agent_trust_state_machine.mmd` | `stateDiagram-v2` | Formal state machine detailing TRUSTED, SUSPICIOUS, QUARANTINED, and terminal REVOKED states. | `akta/trust_engine.py` | **Implemented** | Chapter 3 (3.4) |
| **21** | Agent Registration & DID Genesis Flow | `21_agent_registration_flow.mmd` | `flowchart TD` | Cryptographic key generation, multicodec prefixing, base58 encoding, and initial trust setup. | `akta/did.py`, `akta/vdr/registry_crud.py` | **Implemented** | Chapter 3 (3.3) |
| **22** | Defense-in-Depth Security Architecture | `22_security_architecture.mmd` | `flowchart LR` | Layered security controls: session defense, human RBAC, cryptographic identity, and trust policies. | `akta/auth/`, `akta/adaptive_auth.py`, `akta/credentials.py` | **Implemented** | Chapter 3 (3.9) |
| **23** | Authentication & RBAC Route Gating Flow | `23_authentication_rbac_flow.mmd` | `flowchart TD` | Request-level decision tree for Bearer tokens, lockout checks, and ADMIN/OPERATOR/VIEWER enforcement. | `akta/auth/dependencies.py` | **Implemented** | Chapter 3 (3.9) |
| **24** | Deployment Topology & Process Architecture | `24_deployment_architecture.mmd` | `flowchart TB` | Host deployment topology showing React Vite (5173), FastAPI Uvicorn (8050), and SQLite WAL. | `akta/server.py`, `frontend/vite.config.js` | **Implemented** | Chapter 3 (3.2) |
| **25** | End-to-End Tier Interaction (UI to DB) | `25_frontend_backend_database_flow.mmd` | `sequenceDiagram` | Detailed round-trip trace from React user action through Axios, FastAPI, ORM, and SQLite. | `frontend/src/`, `akta/server.py`, `akta/vdr/models.py` | **Implemented** | Chapter 3 (3.12) |

---

## Important Architectural Disclaimers & Grounding

1. **Verifiable Data Registry (VDR):**
   - Implemented as a local relational SQLite database (`vdr.db`) operating with Write-Ahead Logging (`WAL` mode).
   - It is **not** a decentralized blockchain or distributed ledger. Cross-organizational blockchain integration is marked as `PROPOSED / FUTURE SCOPE`.

2. **Agent Connector Execution Model:**
   - Implemented as `LocalAgentConnector`, which provides deterministic, capability-specific structured responses for tasks (research, analysis, coding, planning, verification), with optional outbound HTTP POST fallback.
   - It does **not** invoke live large language models (LLMs) via OpenAI/Anthropic/Gemini APIs in default testing. Live LLM API integration is marked as `FUTURE SCOPE`.

3. **Workflow Orchestration Patterns:**
   - The database schema supports `SEQUENTIAL` and `PARALLEL` patterns (`WorkflowModel.pattern`).
   - The operational engine and verified automated tests strictly execute the `SEQUENTIAL` pattern. Parallel execution is marked as `FUTURE SCOPE`.
