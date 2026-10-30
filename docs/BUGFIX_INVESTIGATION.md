# TrustChain-AI — Bug Investigation & Root Cause Analysis

**Date:** 2026-10-21  
**Project:** TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration  
**Environment:** React 19 + Vite (Frontend), FastAPI + SQLite VDR (Backend)

---

## Executive Summary

This investigation diagnoses two user-reported defects in the TrustChain-AI operations portal:
1. **Bug 1:** On `/agents`, clicking the **INVESTIGATE** button produces no visible response or interactive inspection experience.
2. **Bug 2:** `/discovery` and `/matching` routes appear almost identical and lack distinct, functional operational workflows.

---

## 1. Bug 1 Analysis: `/agents` INVESTIGATE Button

### 1.1 Symptoms & Observed Behavior
- Navigating to `/agents` (`AgentExplorer.jsx`) presents an Agent Inventory table with DID, Trust Score, Risk Visualizer, Behavioral State, and an "Investigate" action button.
- Clicking "Investigate" on an agent row does not open an interactive modal, side panel, or responsive investigation drawer within the inventory view.
- When following the underlying `<Link to="/agents/:did">` route:
  - The `Sidebar` active state highlights nothing because it performs strict equality matching on `location.pathname === '/agents'`.
  - The destination component `AgentDetails.jsx` only queries `/trust/state/{did}` and `/trust/telemetry/{did}`.
  - Crucial agent metadata is completely absent:
    - Display Name
    - Model Name & Model Provider
    - Endpoint URL & Endpoint Health
    - Operational Status (`AVAILABLE`, `BUSY`, `OFFLINE`)
    - Capability badges/tags
    - Reputation score ($r \in [1, 5]$)
    - Task execution metrics: Total tasks, Successful tasks, Failed tasks
  - Several UI elements use hardcoded dark-mode classes (e.g., `text-slate-100`), causing low contrast or near-invisible text in light mode.

### 1.2 Root Cause
1. **No In-Page Investigation Pattern:** `AgentExplorer.jsx` lacked an embedded slide-over drawer or modal component to immediately act on the clicked row and inspect the selected agent without disrupting inventory review.
2. **Missing Backend Metadata Integration:** Neither `AgentExplorer` nor `AgentDetails` queried the authoritative `/api/v1/registry/agents/{did_or_id}` endpoint. As a result, agent registration metadata was never fetched or bound to the view.
3. **Incomplete Error & State Handling:** If an agent profile failed to load or had no historical telemetry, no recovery mechanism or fallback was provided.

---

## 2. Bug 2 Analysis: `/discovery` and `/matching` Duplication

### 2.1 Symptoms & Observed Behavior
- In `frontend/src/App.jsx` (lines 213–214):
  ```jsx
  <Route path="/discovery" element={<DiscoveryMatching />} />
  <Route path="/matching" element={<DiscoveryMatching />} />
  ```
- Both routes mount the exact same component `<DiscoveryMatching />`.
- Clicking either sidebar item ("Discovery" or "Matching") presents the identical UI, identical filters ("Required Capability", "Min Trust Threshold"), and identical Candidate Ranking table.

### 2.2 Domain Separation Analysis
The TrustChain-AI framework specifies two fundamentally different operational activities:
1. **Agent Discovery (`/discovery`):**
   - **Domain Purpose:** Inventory search and capability-based availability filtering.
   - **Core Workflow:** An operator searches for available agents by capability, sets a minimum trust threshold filter, and checks operational status (`AVAILABLE`, `BUSY`, `OFFLINE`) and health check status (`HEALTHY`, `UNHEALTHY`, `OFFLINE`).
   - **Key Visual Output:** Clear inventory of matching agents with status badges, trust scores, capability tags, and explicit eligibility/exclusion reasons (e.g., "Excluded: Trust score below threshold", "Excluded: Quarantined", "Eligible: Meets all criteria").
   - **Execution Behavior:** Discovery is a read-only query/exploration tool, not an auto-executing task matcher.
2. **Task-Driven Agent Matching (`/matching`):**
   - **Domain Purpose:** Multi-factor algorithmic matchmaking for a specific task prompt or workload.
   - **Core Workflow:** Given a task description/prompt, required capability, and minimum trust requirement, compute candidate compatibility using the formal TrustChain-AI matching formula:
     $$\text{MatchScore} = 0.4 \cdot T + 0.3 \cdot \frac{r}{5.0} + 0.2 \cdot \sigma + 0.1 \cdot (1 - \lambda)$$
   - **Key Visual Output:** Ranked recommendation list with a prominent "Best Match" highlight for the top eligible candidate, full score breakdowns (trust, reputation, success rate, latency penalty), and an expandable section for ineligible candidates showing policy rejection reasons.
   - **Execution Behavior:** Direct action to assign the task or initiate collaboration with the selected agent.

### 2.3 Root Cause
1. **Shared Route Target:** Both `/discovery` and `/matching` were mapped to `<DiscoveryMatching />`.
2. **Monolithic Component:** `<DiscoveryMatching.jsx>` collapsed both concepts into a single table without dedicated views, distinct filters, or role-specific workflows.

---

## 3. Implementation Plan

### Step 1: Fix Bug 1 (`/agents` Investigation Experience)
- Build an interactive, animated Slide-Over Investigation Drawer in `AgentExplorer.jsx`.
- When clicking "Investigate" on any agent row:
  - Immediately open the drawer and load:
    - Profile from `GET /api/v1/registry/agents/{did_or_id}`
    - Live Trust State from `GET /api/v1/trust/state/{did}`
    - Telemetry history from `GET /api/v1/trust/telemetry/{did}`
    - Trust audit trail from `GET /api/v1/trust/audit/{did}`
  - Display all required fields: DID, Name, Model, Provider, Endpoint, Health Status, Operational Status, Trust Score, Trust State Badge, Reputation Score, Capabilities tags, Task Execution counts (total, successful, failed), and recent Telemetry/Audit records.
  - Provide a clean close button (and ESC key / backdrop click support).
  - Also enhance `AgentDetails.jsx` so `/agents/:did` route displays the same comprehensive information if visited directly.

### Step 2: Fix Bug 2 (Separate `/discovery` and `/matching`)
- Create `DiscoveryCenter.jsx`:
  - Dedicated capability filter, minimum trust threshold slider, operational status filter, and health filter.
  - Discovered agents grid/table with capability badges, trust state, and clear eligibility/exclusion reasons.
  - Action buttons: "Investigate Agent" (opens investigation drawer) and "Initiate Collaboration".
- Create `MatchingCenter.jsx`:
  - Dedicated task description/prompt input, required capability selector, and minimum trust score threshold.
  - Highlighted "Best Match" / Top Candidate card with selection rationale.
  - Ranked candidate cards with transparent mathematical score breakdowns ($0.4 \cdot T$, $0.3 \cdot (r/5)$, $0.2 \cdot \sigma$, $0.1 \cdot (1-\lambda)$).
  - Expandable/collapsible "Ineligible Candidates" section with exact rejection reasons.
  - Direct action: "Initiate Collaboration with Best Match".
- Update `App.jsx` to route `/discovery` $\to$ `<DiscoveryCenter />` and `/matching` $\to$ `<MatchingCenter />`.

### Step 3: Backend & API Client Alignment
- Ensure `registry_crud.py` includes score breakdown fields in `find_best_agent_match`.
- Support optional `min_trust` parameter in `discover_free_agents` (`/api/v1/registry/discover`).
- Add `registryApi` helpers to `frontend/src/api.js`.

### Step 4: Verification & Automated Tests
- Run backend pytest suite (`pytest tests/`).
- Add new test cases for discovery filtering and matching score breakdown.
- Verify frontend production build (`npm run build`).
- Verify light and dark theme contrast.
