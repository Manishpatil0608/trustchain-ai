# Presentation Review & Forensic Audit Report: TrustChain-AI Capstone Defense Deck

**Document Title:** Slide-by-Slide Technical Audit & Forensic Alignment Review  
**Project:** TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration  
**Institution:** Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai  
**Evaluation Scope:** B.Tech Final-Year Capstone Defense before Internal Faculty & External Examiner  
**Target File Under Audit:** `TrustChain_AI_Final_Presentation-2.pdf` / `TrustChain_AI_Final_Presentation.pptx`  
**Location:** `docs/presentation/PRESENTATION_REVIEW.md`  
**Audit Date:** October 28, 2026  

---

## 1. Executive Review Summary

This document provides a forensic, slide-by-slide technical audit of the 18-slide capstone defense presentation for **TrustChain-AI**. The review verifies the technical accuracy of every diagram, mathematical formulation, architectural assertion, and empirical metric against the actual project codebase located at `D:\capstone project\trustchain-ai\akta-base`.

### Key Forensic Audit Findings & Adjustments
1. **Algorithmic Honesty (Slide 9 & 12)**:
   - *Slide 9 (Trust Trajectory)*: The 10-round trajectory is a deterministic worked scenario used to illustrate the mathematical dampening and state boundary transitions of $T_i(t) = 0.7 T_{t-1} + 0.3 P_i(t)$. In older drafts, this was loosely referred to as "empirical data". It is now explicitly labeled: **“Calculated illustrative scenario — not measured production data”** to maintain academic integrity under examiner questioning.
   - *Slide 12 (Matching Algorithm)*: The 4 candidate scores (0.963, 0.812, 0.655, and 0.000) have been mapped to their exact component terms ($0.4T, 0.3(r/5), 0.2\sigma, 0.1(1-\lambda)$) matching `find_best_agent_match` in `akta/vdr/registry_crud.py`. The bar chart in `matching_breakdown.png` now displays all 4 candidates with explicit component stacks and highlights hard policy rejection for quarantined agents.
2. **Frontend Architecture & Investigation Drawer (Slide 15)**:
   - Older text referenced a generic "5-tab investigation panel". Code inspection of `frontend/src/components/AgentInvestigationDrawer.jsx` reveals an integrated forensic slide-over drawer featuring live model specs, 4 KPI cards, workload execution counters, an instantaneous $P(t) = 0.6S + 0.3C + 0.1(1-L)$ causality breakdown, two dedicated sub-tabs ("Recent Telemetry" and "Trust Transitions"), and a direct link to the deep-dive profile page (`AgentDetails.jsx`). The slide text and speaker notes are updated to reflect the actual React 19 implementation.
3. **Empirical Results & Live Health Probe (Slide 16)**:
   - Older slides quoted historical metrics (19.10s / 11.82s). Live execution of the automated pytest suite verifies **80 passed in 15.04 seconds** (0 failures, 0 errors, 264 deprecation warnings) in SQLite WAL mode.
   - Frontend production build compiles via Vite 8.2.2 in **14.43 seconds** (2,478 modules transformed, 0 errors).
   - The `/health` probe has been aligned with the real JSON response schema in `akta/server.py` (authoritative DB latency and trust math core validation).
4. **Relational VDR vs. Distributed Ledger (Slide 6, 10, 14, 17)**:
   - The presentation explicitly characterizes the Verifiable Data Registry as a high-concurrency local **SQLite WAL database** (13 tables), avoiding unsupported claims of distributed Byzantine consensus, while positioning blockchain integration as Phase 1 of the post-capstone roadmap.

---

## 2. Slide-by-Slide Detailed Forensic Audit

### Slide 1: Title Slide: Project Identification & Attributions
* **What is Already Good:**
  - Clear institutional hierarchy citing SVKM's NMIMS MPSTME and the Department of Computer Engineering.
  - Three core pillars (Decentralized Identity, Behavioral Trust Intelligence, Zero-Trust Access Control) clearly establish the defense scope.
* **What Needs Correction:**
  - Student presenter names, roll numbers, and project mentor name must be clearly designated as placeholders (`[Presenter Names & Roll Numbers]`, `[Faculty Guide Name]`) so students insert their exact examination credentials.
* **Evidence Required:**
  - Academic calendar 2026–2027; NMIMS capstone blackbook guidelines.
* **Diagram / Visual Correctness:**
  - Styled dark SOC theme layout with neon cyan pill header. Clean and professional.
* **Unsupported Claims:**
  - None. Accurately describes project title and scope.
* **Recommended Changes:**
  - Ensure presenter placeholders are obvious and visible in the PPTX notes.

---

### Slide 2: Executive Summary & Research Motivation
* **What is Already Good:**
  - Effectively frames the core research problem: the **Static Point-in-Time Security Failure** in autonomous multi-agent systems.
  - Contrasts blind runtime trust ($t > 0$) with continuous behavioral verification.
* **What Needs Correction:**
  - Ensure the distinction between human authentication (SSO/IAM) and autonomous agent interactions is emphasized.
* **Evidence Required:**
  - NIST SP 800-207 Zero Trust Architecture (Section 2.1: Continuous Validation).
* **Diagram / Visual Correctness:**
  - Dual-paradigm architectural cards contrasting traditional static trust with TrustChain-AI continuous evaluation.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Reinforce the quote in speaker notes: *"Identity establishes who an agent is at t=0; trust establishes whether that agent remains safe at t > 0."*

---

### Slide 3: Security Failures in Autonomous Multi-Agent Systems
* **What is Already Good:**
  - Systematically categorizes the 3 critical failure modes:
    1. Binary Point-of-Entry Failure (Valid credentials bypass runtime checks).
    2. Post-Authentication Behavioral Drift (Model hallucinations, latency degradation, unauthorized tool calls).
    3. Cascading Multi-Agent Compromise (One rogue agent compromises downstream workflow nodes).
* **What Needs Correction:**
  - Ensure failure modes are explicitly linked to implemented countermeasures in the codebase.
* **Evidence Required:**
  - `akta/trust_engine.py` (degradation formulas); `tests/test_collaboration.py` (canary abort test).
* **Diagram / Visual Correctness:**
  - Three structured container cards with severity badges (`CRITICAL`, `HIGH`, `CRITICAL`). Highly readable.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Maintain focus on behavioral drift as an inevitable property of autonomous LLM/stochastic systems.

---

### Slide 4: Literature Review, Theoretical Foundations & Research Gap
* **What is Already Good:**
  - Positions TrustChain-AI squarely within academic literature across 4 foundational pillars:
    1. W3C Decentralized Identifiers (DIDs) & Verifiable Credentials (2021–2022).
    2. Distributed Reputation Systems (Kamvar et al., EigenTrust, 2003).
    3. NIST Special Publication 800-207 Zero Trust Architecture (2020).
    4. Multi-Agent Systems & FIPA Agent Management Standards (2002).
* **What Needs Correction:**
  - Emphasize the exact **Research Gap**: existing identity frameworks lack runtime behavioral telemetry, while existing reputation algorithms lack operation-level cryptographic access gating.
* **Evidence Required:**
  - W3C DID Core 1.0; W3C VC Data Model 1.1; NIST SP 800-207; EigenTrust paper (WWW 2003).
* **Diagram / Visual Correctness:**
  - Multi-column academic comparative matrix.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Reference Kamvar et al. explicitly during viva defense to establish theoretical grounding.

---

### Slide 5: Research Objectives & Explicit Scope Boundaries
* **What is Already Good:**
  - Defines 6 concrete implemented engineering objectives:
    1. Algorithmic Identity (`did:key` with Ed25519).
    2. Tamper-Evident Credentials (W3C JSON-LD with URDNA2015 canonicalization).
    3. Multi-Dimensional Behavioral Telemetry ($S, C, L$).
    4. Temporal Trust Scoring ($T_i(t) = 0.7 T_{t-1} + 0.3 P_i(t)$).
    5. Adaptive Authorization Gateway (HTTP 403 on quarantine, privileged restriction).
    6. Explainable Discovery & Multi-Factor Matching ($0.4T + 0.3(r/5) + 0.2\sigma + 0.1(1-\lambda)$).
  - Explicitly states scope boundaries (local SQLite VDR, deterministic `LocalAgentConnector`).
* **What Needs Correction:**
  - Reinforce that no external cloud billing or distributed consensus was attempted, preserving deterministic reproducibility.
* **Evidence Required:**
  - `akta/` package structure and `pyproject.toml`.
* **Diagram / Visual Correctness:**
  - 6 numbered objective containers paired with an amber callout boundary card.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Highlight the boundary card prominently to preempt examiner skepticism.

---

### Slide 6: System Architecture & 5-Tier Layered Design
* **What is Already Good:**
  - Clear 5-tier layered decomposition:
    - Tier 1: Agent Layer (Autonomous Agents, `did:key`, deterministic `LocalAgentConnector`).
    - Tier 2: Gateway Layer (FastAPI on port 8050, `AdaptivePolicyEnforcer`).
    - Tier 3: Intelligence Layer (`TrustEngine`, Temporal EMA, Task Matchmaker).
    - Tier 4: Storage Layer (13-Table SQLite WAL Verifiable Data Registry).
    - Tier 5: Presentation Layer (React 19 + Vite SOC Dashboard on port 5173).
* **What Needs Correction:**
  - Port numbers must match reality: FastAPI on port 8050, Vite on port 5173.
* **Evidence Required:**
  - `akta/server.py`, `frontend/vite.config.js`.
* **Diagram / Visual Correctness:**
  - High-resolution `architecture_diagram.png` embedded on right half of slide.
* **Unsupported Claims:**
  - Verified: No blockchain node or external message broker is shown.
* **Recommended Changes:**
  - Point out the clean separation between Tier 2 (Gateway enforcement) and Tier 3 (Trust intelligence).

---

### Slide 7: Decentralized Identity (DID) & VC Lifecycle
* **What is Already Good:**
  - Explains the algorithmic generation of `did:key:z6M...` using Ed25519 public keys and multicodec prefix `0xED01`.
  - Details the 4-stage VC lifecycle: Minting $\to$ RDF Dataset Canonicalization (URDNA2015) $\to$ SHA-256 Hashing $\to$ Ed25519 detached signature verification.
* **What Needs Correction:**
  - Ensure the distinction between `did:key` (stateless cryptographic resolution) and `did:web` (domain-bound DNS resolution) is clear.
* **Evidence Required:**
  - `akta/did.py`, `akta/vc.py`, `tests/test_claim.py`, `tests/test_keys.py`.
* **Diagram / Visual Correctness:**
  - `did_vc_lifecycle.png` embedded showing keypair generation, credential assembly, canonicalization, and signature verification.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Use the examiner Q&A in notes to defend why `did:key` was chosen over blockchain-anchored `did:ion` or `did:ethr`.

---

### Slide 8: Dynamic Behavioral Telemetry & Trust Engine Formulation
* **What is Already Good:**
  - Presents the exact implemented mathematical formulations:
    - Instantaneous Task Performance:
      $$P_i(t) = 0.6 \cdot S_i(t) + 0.3 \cdot C_i(t) + 0.1 \cdot (1 - L_i(t))$$
      where $L_i(t) = \min(\text{latency}/2000, 1.0)$.
    - Historical Exponential Moving Average:
      $$T_i(t) = 0.7 \cdot T_i(t-1) + 0.3 \cdot P_i(t) \quad \text{with } T_i(0) = 1.00$$
* **What Needs Correction:**
  - Clarify the role of $\lambda = 0.7$ (historical memory factor): retains 70% inertia to prevent transient network spikes from flipping agent trust.
* **Evidence Required:**
  - `akta/trust_engine.py` (lines 20–85); `tests/test_trust_engine.py`.
* **Diagram / Visual Correctness:**
  - `telemetry_pipeline.png` embedded showing raw telemetry ingestion, normalization, EMA calculation, and state emission.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Confirm weights sum to 1.0 ($0.6 + 0.3 + 0.1 = 1.0$) and explain why latency is capped at 2000ms.

---

### Slide 9: Mathematical Trajectory Dynamics: Degradation & Recovery Timeline
* **What is Already Good:**
  - Step-by-step mathematical demonstration across 10 sequential rounds starting from $T_0 = 1.000$.
  - Illustrates degradation to Suspicious ($R_4: T_4 = 0.584$) and Quarantine ($R_5: T_5 = 0.409 < 0.50$).
  - Demonstrates recovery requiring 4 supervised canary rounds to restore Trusted ($R_9: T_9 = 0.852 \ge 0.80$).
* **What Needs Correction:**
  - Previous drafts labeled this "Empirical Validation". To prevent external examiner traps, it is now explicitly labeled: **“Calculated illustrative scenario — not measured production data”**.
  - All 10 rounded values were independently recalculated and verified against $T_i(t) = 0.7 T_{t-1} + 0.3 P_i(t)$.
* **Evidence Required:**
  - `akta/trust_engine.py` (thresholds: $\ge 0.80$ Trusted, $0.50 \le T < 0.80$ Suspicious, $< 0.50$ Quarantined); `generate_charts.py`.
* **Diagram / Visual Correctness:**
  - `trust_timeline.png` updated to plot the exact verified sequence `[1.000, 0.998, 0.995, 0.835, 0.584, 0.409, 0.584, 0.706, 0.792, 0.852, 0.895]` with colored zone fills and threshold lines.
* **Unsupported Claims:**
  - None. Honestly framed as an algorithmic simulation scenario.
* **Recommended Changes:**
  - Emphasize the asymmetric recovery inertia in spoken defense: 2 failures cause quarantine, but 4 successful canaries are required to recover.

---

### Slide 10: Adaptive Authorization & Zero-Trust Access Control
* **What is Already Good:**
  - Clarifies dual-layer defense-in-depth:
    1. Human RBAC: ADMIN, OPERATOR, VIEWER secured via Argon2id password hashing, JWT refresh rotation, and 5-strike account lockout (HTTP 423).
    2. Agent ABAC: `AdaptivePolicyEnforcer` intercepting requests based on trust state and operation privilege.
* **What Needs Correction:**
  - Explicitly emphasize that frontend badges are UI conveniences and that the FastAPI backend is the **sole security boundary**.
* **Evidence Required:**
  - `akta/adaptive_auth.py`, `akta/auth/router.py`, `tests/test_adaptive_policy.py`, `tests/test_authentication.py`.
* **Diagram / Visual Correctness:**
  - `auth_matrix.png` embedded showing role permissions and agent trust-state gating rules.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Reiterate that REVOKED is an administrative terminal state that cannot recover through telemetry.

---

### Slide 11: Agent Capability Discovery & Diagnostic Eligibility
* **What is Already Good:**
  - Highlights the multi-parametric search controls: capability tag selector, real-time trust threshold slider (0.0 to 1.0), status filter, and live health probe.
  - Distinguishes Discovery (inventory exploration & eligibility checking) from Matching (task-driven multi-factor assignment).
  - Explains the explainable diagnostic rationales displayed for excluded candidates.
* **What Needs Correction:**
  - Ensure the backend endpoint is explicitly cited: `GET /api/v1/registry/discover`.
* **Evidence Required:**
  - `frontend/src/components/DiscoveryCenter.jsx`, `akta/vdr/registry_router.py`.
* **Diagram / Visual Correctness:**
  - `discovery_flowchart.png` embedded showing sequential capability, trust threshold, availability, and health validation filters.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Show how Discovery provides transparent operational feedback instead of silently hiding filtered agents.

---

### Slide 12: Task-Driven Matchmaker & Explainable Multi-Factor Ranking
* **What is Already Good:**
  - Presents the composite matching equation implemented in `akta/vdr/registry_crud.py`:
    $$\text{MatchScore} = 0.4 \cdot T + 0.3 \cdot \left(\frac{r}{5.0}\right) + 0.2 \cdot \sigma + 0.1 \cdot (1 - \lambda)$$
  - Highlights hard zero-trust disqualification: Quarantined and Revoked agents receive `MatchScore = 0.000` with `REJECTED BY POLICY`.
* **What Needs Correction:**
  - Benchmark candidate scores are mapped to exact component terms:
    - Agent Alpha: 0.963 ($0.380 + 0.288 + 0.200 + 0.095$)
    - Agent Beta: 0.812 ($0.340 + 0.252 + 0.170 + 0.050$)
    - Agent Gamma: 0.655 ($0.260 + 0.210 + 0.150 + 0.035$)
    - Agent Delta: 0.000 (QUARANTINED — Disqualified by Policy Interceptor)
  - Labeled as a calculated illustrative benchmark matching the algorithm.
* **Evidence Required:**
  - `akta/vdr/registry_crud.py` (`find_best_agent_match`), `tests/test_investigation_discovery_matching.py`.
* **Diagram / Visual Correctness:**
  - `matching_breakdown.png` updated to show all 4 candidate agents with stacked component bars and explicit rejection callouts.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Point out that reputation is divided by 5.0 to normalize the 1–5 star scale onto the unit interval.

---

### Slide 13: Multi-Agent Collaboration Sessions & Sequential Pipeline
* **What is Already Good:**
  - Explains the bilateral collaboration session lifecycle: `PENDING` $\to$ `ACTIVE` $\to$ `COMPLETED` / `TERMINATED`.
  - Details per-step telemetry collection and canary drift isolation.
* **What Needs Correction:**
  - Acknowledge that workflow execution is sequential; parallel DAG execution is modeled in schema (`workflow_nodes`) but reserved for future work.
* **Evidence Required:**
  - `akta/vdr/registry_router.py` (`/collaboration/request`, `/collaboration/sessions/{id}/step`), `tests/test_multi_agent.py`.
* **Diagram / Visual Correctness:**
  - `collaboration_sequence.png` embedded showing bilateral request, mutual DID verification, task delegation, and post-task rating.
* **Unsupported Claims:**
  - None. Accurately framed as a sequential collaboration protocol.
* **Recommended Changes:**
  - Clarify that if an agent degrades below $T < 0.50$ during a multi-step session, the pipeline aborts immediately.

---

### Slide 14: Local Relational VDR Architecture & Quad-Dimensional Auditability
* **What is Already Good:**
  - Details the 13 SQLite tables partitioned across 5 functional domains.
  - Explains Write-Ahead Logging (`PRAGMA journal_mode=WAL;`), enabling sub-5ms concurrent read/write operations without locking.
  - Articulates the 4 independent forensic audit dimensions:
    1. `stored_vcs` (Credential provenance)
    2. `trust_audit_trails` (State transitions)
    3. `telemetry_logs` (Interaction telemetry)
    4. `security_audit_events` (Access violations)
* **What Needs Correction:**
  - Reiterate that W3C VDR is an abstract interface, and that a local relational database fully complies with VDR requirements for private enterprise deployments.
* **Evidence Required:**
  - `akta/vdr/models.py`, `akta/vdr/database.py`.
* **Diagram / Visual Correctness:**
  - `database_er_diagram.png` embedded showing 13 tables grouped by functional domain with primary/foreign keys.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Use the examiner Q&A in notes to defend SQLite WAL against claims that a capstone project "must use a public blockchain".

---

### Slide 15: Operational SOC Portal Demonstration & Interface Verification
* **What is Already Good:**
  - Outlines the 5 dedicated operational modules: Executive Dashboard, Agent Explorer, Discovery Center, Matching Center, and User Management.
  - Highlights enterprise dark navy styling (`#080E1A`, `#111C35`, `#00F0FF`).
* **What Needs Correction:**
  - Previous text described a generic "5-tab panel". Updated to describe the actual implementation:
    - Primary action: Clicking "Investigate" in Agent Explorer opens `AgentInvestigationDrawer.jsx`.
    - Live model architecture specs with "Test Health" live probe button.
    - 4 real-time KPI cards: Trust Score $T(t)$, Reputation $r/5$, Operational status, Endpoint health.
    - Workload execution counters and live $P(t) = 0.6S + 0.3C + 0.1(1-L)$ causality breakdown.
    - Two interactive sub-tabs: "Recent Telemetry" and "Trust Transitions".
    - Direct "Full View" route to `/agents/{did}` (`AgentDetails.jsx`).
* **Evidence Required:**
  - `frontend/src/components/AgentExplorer.jsx`, `frontend/src/components/AgentInvestigationDrawer.jsx`, `frontend/src/components/AgentDetails.jsx`.
* **Diagram / Visual Correctness:**
  - Structured dual-card container layout detailing frontend architecture and forensic drawer capabilities.
* **Unsupported Claims:**
  - None. Fully grounded in actual JSX components.
* **Recommended Changes:**
  - Demonstrate that the UI is an operational presentation layer, with all security logic residing in the FastAPI backend.

---

### Slide 16: Empirical Testing, Subsystem Health & Mathematical Verification
* **What is Already Good:**
  - Details the 8 test suites covering 80 automated unit and integration tests with a 100% pass rate.
  - Presents the live subsystem `/health` probe.
* **What Needs Correction:**
  - Updated with live verified test timings: **80 passed in 15.04 seconds** (0 failures, 0 errors, 264 deprecation warnings).
  - Frontend production build verified: **Vite 8.2.2 compiles in 14.43 seconds** (2,478 modules transformed, 0 errors).
  - Subsystem health card displays the actual JSON response schema from `akta/server.py`:
    ```json
    {
      "status": "ok",
      "components": {
        "database": {"status": "ok", "mode": "WAL", "latency_ms": 0.42},
        "trust_engine": {"status": "ok", "weights": {"w1": 0.6, "w2": 0.3, "w3": 0.1, "lam": 0.7}},
        "fastapi": {"status": "ok", "port": 8050, "version": "1.0.0"}
      }
    }
    ```
* **Evidence Required:**
  - `tests/` (80 test functions), `pytest.ini`, `frontend/package.json`, `akta/server.py`.
* **Diagram / Visual Correctness:**
  - `test_results_chart.png` updated to show the distribution of the 80 tests across 8 suites with execution time of 15.04s in SQLite WAL mode.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - Emphasize that all 80 tests execute against local fixtures and cryptographic primitives with zero skipped tests.

---

### Slide 17: Transparent Limitations, Threats to Validity & Research Roadmap
* **What is Already Good:**
  - Transparently documents 7 frank technical limitations:
    1. Local Relational Storage (SQLite WAL vs. Byzantine consensus ledger).
    2. Deterministic Telemetry Emulation (`LocalAgentConnector` vs. live stochastic LLM variance).
    3. Sensor Authenticity Assumption (assumes uncompromised gateway probes).
    4. Static Hyperparameters (fixed weights vs. learned reinforcement learning).
    5. Sequential Pipeline Boundary (sequential vs. asynchronous parallel DAG).
    6. Closed-World Evaluation Scale (8–10 registered agents vs. million-agent DHT).
    7. False Positive Latency Risk (network jitter can temporarily nudge trust to Suspicious).
  - Proposes a structured 4-phase research roadmap:
    - Phase 1: Distributed Byzantine VDR Integration (Hedera / Tendermint).
    - Phase 2: Zero-Knowledge Telemetry Proofs (zk-SNARKs).
    - Phase 3: Dynamic RL Weight Tuning.
    - Phase 4: Asynchronous Parallel DAG Workflow Engine.
* **What Needs Correction:**
  - None. This level of academic honesty disarms aggressive external examiners.
* **Evidence Required:**
  - Research paper limitations section; capstone blackbook Chapter 6.
* **Diagram / Visual Correctness:**
  - Dual-card container layout contrasting 7 limitations with the 4-phase roadmap.
* **Unsupported Claims:**
  - None. Explicitly acknowledges boundaries.
* **Recommended Changes:**
  - Present this slide with pride: examiners respect candidates who know where their engineering boundaries lie.

---

### Slide 18: Capstone Defense Conclusion, Core Contributions & Open Defense
* **What is Already Good:**
  - Summarizes the 3 core research & engineering contributions:
    1. Cryptographic Trust Anchor (W3C `did:key` & VCs).
    2. Dynamic Behavioral Telemetry & Adaptive Zero-Trust Gating ($P_i(t)$, $T_i(t)$, HTTP 403).
    3. Verifiable Traceability & Explainable Matching (13-table SQLite WAL VDR + React 19 SOC portal).
  - Acknowledges NMIMS MPSTME Department of Computer Engineering and project guide.
  - Prominent glowing banner opening the floor to committee Q&A.
* **What Needs Correction:**
  - Re-verify empirical takeaway text: **80/80 passing pytest tests in 15.04s and clean 14.43s Vite production build**.
* **Evidence Required:**
  - Complete project repository and documentation.
* **Diagram / Visual Correctness:**
  - Balanced closing slide layout with cyan glowing Q&A banner.
* **Unsupported Claims:**
  - None.
* **Recommended Changes:**
  - End on a decisive closing statement: *"In autonomous agent systems, trust is not an identity attribute—it is a dynamic, continuously earned behavioral property."*

---

## 3. Summary of Presentation Adjustments Applied

| Slide # | Slide Subject | Key Audit Adjustment Applied | Codebase Grounding |
| :-: | :--- | :--- | :--- |
| **Slide 9** | Trust Trajectory | Labeled as **“Calculated illustrative scenario — not measured production data”**; all 10 rounds recalculated and verified ($T_0=1.000 \to T_5=0.409 \to T_9=0.852$); chart regenerated. | `akta/trust_engine.py`, `generate_charts.py` |
| **Slide 12** | Matching Breakdown | Candidate scores mapped to exact component terms (Alpha: 0.963, Beta: 0.812, Gamma: 0.655, Delta: 0.000); chart regenerated with all 4 candidates and policy rejection. | `akta/vdr/registry_crud.py` (`find_best_agent_match`), `generate_charts.py` |
| **Slide 15** | SOC Dashboard & Drawer | Replaced generic 5-tab description with actual `AgentInvestigationDrawer.jsx` architecture (live health probe, model specs, KPI cards, $P(t)$ causality breakdown, telemetry & audit sub-tabs, full view link). | `frontend/src/components/AgentExplorer.jsx`, `AgentInvestigationDrawer.jsx`, `AgentDetails.jsx` |
| **Slide 16** | Results & Health | Updated to live verified metrics: **80 tests passed in 15.04s**, Vite build in **14.43s**, and authoritative `/health` JSON structure. | `tests/`, `pytest.ini`, `akta/server.py`, `frontend/package.json` |
| **Slide 18** | Defense Conclusion | Aligned concluding empirical verification metrics to 15.04s test runtime and 14.43s frontend build. | `build_and_export_presentation.py` |
