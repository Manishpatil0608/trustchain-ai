# -*- coding: utf-8 -*-
"""
generate_final_deliverables.py
Compiles:
1. docs/presentation/final/TrustChain_AI_Final_Presentation_Slide_Wise_Content.md
2. docs/presentation/final/TrustChain_AI_Final_Presentation_Slide_Wise_Content.docx
3. docs/presentation/final/TrustChain_AI_Final_Presentation_Notes.docx
with complete, professional, word-for-word spoken scripts and technical examiner Q&As.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs", "presentation", "final")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Include complete data for all 18 slides
SLIDES_DATA = [
    {
        "num": 1,
        "title": "Title Slide: Project Identification & Attributions",
        "tracker": "B.TECH CAPSTONE DEFENSE · ACADEMIC YEAR 2026–2027",
        "content": [
            "Project Title: TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration",
            "Institutional Affiliation: Department of Computer Engineering, Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Deemed-to-be University), Mumbai",
            "Student Presenters: [Presenter Names & Roll Numbers]",
            "Project Mentor / Guide: [Faculty Mentor / Guide Name]",
            "Three Core Architectural Pillars:",
            "  1. Decentralized Identity Anchor: W3C did:key algorithmic public keys & Verifiable Credentials without central CA.",
            "  2. Behavioral Trust Intelligence: Continuous temporal Exponential Moving Average evaluation of runtime telemetry.",
            "  3. Adaptive Zero-Trust Gating: Dynamic operation gating (HTTP 403 on Quarantine; privileged restriction on Suspicious)."
        ],
        "visual": "Styled dark navy SOC theme layout (#080E1A) with neon cyan track pill, crisp typography, and formal institutional attributions.",
        "evidence": "README.md, pyproject.toml, SVKM's NMIMS MPSTME B.Tech Capstone Guidelines 2026-2027.",
        "script": "Good morning, respected members of the evaluation committee, project guide, and external examiner. We are privileged to present our B.Tech final-year capstone project: TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration. In modern enterprise software, autonomous AI agents communicate, delegate sub-tasks, and execute privileged tools without human intervention. However, current systems suffer from a fatal security vulnerability: static point-in-time authentication verifies who an agent is when it connects, but has zero visibility into whether that agent remains safe, reliable, and compliant during execution. TrustChain-AI solves this fundamentally by unifying W3C decentralized public-key identity with continuous mathematical trust scoring and zero-trust policy gating. We have validated our architecture through 80 automated unit tests passing in 15.04 seconds and a full production React 19 SOC portal.",
        "qa": [
            ("Why did you choose autonomous AI agents rather than traditional microservices for this security framework?",
             "Traditional microservices execute static, deterministic code where static mTLS certificates and API tokens are sufficient. Autonomous AI agents, however, operate non-deterministically using Large Language Models and tool execution. They can suffer from prompt injection, goal drift, and reasoning hallucination post-authentication. This makes static point-in-time security obsolete and necessitates continuous behavioral trust intelligence.")
        ]
    },
    {
        "num": 2,
        "title": "Executive Summary & Research Motivation",
        "tracker": "RESEARCH MOTIVATION · THE PROBLEM",
        "content": [
            "1. The Core Vulnerability: Static Point-in-Time Security Failure in Multi-Agent Systems.",
            "   • Existing agent frameworks authenticate once at t=0 using API keys or TLS certificates, assuming perpetual trustworthiness.",
            "   • An authenticated agent can drift, hallucinate, suffer jailbreak attacks, or exceed resource limits at t > 0 without detection.",
            "2. Traditional Paradigm: Blind Runtime Trust",
            "   • Binary access: full trust or complete denial.",
            "   • Static API keys vulnerable to token theft, relay attacks, and lateral privilege escalation.",
            "   • Zero operational visibility into behavioral degradation post-handshake.",
            "3. TrustChain-AI Paradigm: Continuous Zero-Trust Governance",
            "   • Dynamic behavioral trust: evaluated continuously across task success, policy compliance, and SLA latency.",
            "   • Cryptographic identity bound to verifiable behavioral telemetry.",
            "   • Principle: 'Never trust, always verify — continuously at runtime'."
        ],
        "visual": "Dual-card architectural contrast layout comparing traditional static identity with TrustChain-AI continuous zero-trust evaluation.",
        "evidence": "docs/blackbook/TrustChain_AI_Blackbook_Part1.md (Chapter 1), NIST SP 800-207 Zero Trust Architecture.",
        "script": "Slide 2 establishes the core motivation behind TrustChain-AI. In multi-agent systems, agents are granted expansive access to databases, APIs, and external tools. The fundamental problem is what we term the Point-in-Time Security Failure. Once an agent authenticates at time t=0 using an API key or certificate, the system assumes it will remain trustworthy forever. But autonomous agents are stochastic: an agent can hallucinate, experience prompt injection, or degrade in latency. Under traditional architectures, this drift goes unnoticed until catastrophic damage occurs. TrustChain-AI introduces continuous zero-trust governance: we treat cryptographic identity merely as the initial baseline, while continually evaluating behavioral telemetry to gate access dynamically at runtime.",
        "qa": [
            ("What is the core vulnerability you are addressing in one sentence?",
             "We solve the Point-in-Time Security Failure, where existing frameworks verify who an agent is at initial connection (t=0) but remain completely blind when that agent degrades, hallucinates, or acts maliciously during runtime (t > 0).")
        ]
    },
    {
        "num": 3,
        "title": "Security Failures in Autonomous Multi-Agent Systems",
        "tracker": "FAILURE MODES · EMPIRICAL MOTIVATION",
        "content": [
            "1. Binary Point-of-Entry Failure [CRITICAL SEVERITY]",
            "   • Static credential validation verifies possession of private key or token at t=0, but has zero visibility into subsequent runtime behavior.",
            "   • Adversary leveraging a compromised credential gains unrestricted lifetime access with zero operational friction.",
            "2. Post-Authentication Behavioral Drift [HIGH SEVERITY]",
            "   • Stochastic model updates, adversarial prompt injection, or context poisoning cause agents to breach SLA compliance or execute unsafe tool calls.",
            "   • Binary access control cannot detect or throttle gradual behavioral degradation.",
            "3. Cascading Multi-Agent Compromise [CRITICAL SEVERITY]",
            "   • In collaborative pipelines, a compromised upstream agent propagates corrupted outputs to downstream peer agents.",
            "   • A single uncontained failure leads to catastrophic systemic compromise across the multi-agent cluster."
        ],
        "visual": "Three structured container cards with color-coded severity badges (CRITICAL, HIGH, CRITICAL) mapping out failure pathways.",
        "evidence": "akta/trust_engine.py (degradation math), tests/test_collaboration.py (canary abort verification).",
        "script": "On Slide 3, we detail the three critical failure modes that motivate our design. First is the Binary Point-of-Entry Failure: static validation checks keys at connection time, creating a blind spot once access is granted. Second is Post-Authentication Behavioral Drift: autonomous agents are subject to prompt injection and model drift. Even without an adversary, an agent's compliance can degrade over time. Third is Cascading Compromise: in collaborative pipelines, if Agent A is compromised and produces corrupted outputs, downstream Agent B consumes that data and fails as well, causing an uncontained domino effect across the enterprise. TrustChain-AI is specifically engineered to detect and isolate these failures before cascading occurs.",
        "qa": [
            ("How does cascading compromise happen in multi-agent workflows?",
             "In sequential or DAG pipelines, if Agent A is compromised and produces corrupted outputs, downstream Agent B consumes that untrusted output and produces further corrupted results, cascading failures across the enterprise. TrustChain-AI intercepts every inter-agent transition with canary telemetry, terminating the workflow before cascading damage occurs.")
        ]
    },
    {
        "num": 4,
        "title": "Literature Review, Theoretical Foundations & Research Gap",
        "tracker": "ACADEMIC FOUNDATIONS · STATE OF THE ART",
        "content": [
            "1. Self-Sovereign Identity (W3C DID v1.0, 2022 & VC v1.1, 2021)",
            "   • Provides tamper-evident cryptographic public-key identity without centralized certificate authorities.",
            "   • Limitation: Static identity assertions; no runtime telemetry or behavioral monitoring.",
            "2. Distributed Reputation Systems (Kamvar et al., EigenTrust, ACM WWW 2003)",
            "   • Mathematical peer rating aggregation in P2P networks using power iteration.",
            "   • Limitation: High computational latency; vulnerable to sybil collusion; lacks operation-level zero-trust access gating.",
            "3. Zero Trust Architecture (NIST Special Publication 800-207, 2020)",
            "   • Establishes core axiom: 'Never trust, always verify'. Requires continuous policy evaluation per session.",
            "   • Limitation: Designed for human enterprise IAM/microservices; lacks primitives for autonomous AI agent delegation.",
            "4. Multi-Agent Systems & FIPA Standards (FIPA Agent Management, 2002)",
            "   • Defines agent directory services, communication protocols (ACL), and task handshakes.",
            "   • Limitation: Assumes cooperative, non-adversarial environments with zero cryptographic identity anchors.",
            "SYNTHESIS RESEARCH GAP: No prior framework unifies W3C algorithmic public-key identity with continuous runtime sensor telemetry and operation-level zero-trust gating."
        ],
        "visual": "Multi-column comparative academic matrix contrasting prior standards with TrustChain-AI's unified architecture.",
        "evidence": "W3C DID Core 1.0; W3C VC Data Model 1.1; Kamvar et al. (WWW 2003); NIST SP 800-207.",
        "script": "Slide 4 contextualizes our work within academic literature across four domains. Self-Sovereign Identity provides tamper-evident public keys through W3C DIDs and Verifiable Credentials, but remains static. Distributed reputation systems, pioneered by Kamvar's EigenTrust in 2003, calculate peer reputation mathematically, but suffer from high computational latency and lack real-time access gating. NIST Special Publication 800-207 defines Zero Trust Architecture, but focuses on human IAM rather than autonomous agent tool delegation. Finally, legacy FIPA agent standards assume cooperative, benign environments. Our research gap is evident: no prior work combines algorithmic public-key identity with continuous behavioral telemetry and operation-level zero-trust gating.",
        "qa": [
            ("How does your trust model differ from the famous EigenTrust algorithm?",
             "EigenTrust computes stationary global reputation vectors in peer-to-peer file sharing using power iteration over peer ratings. However, it lacks real-time sensor telemetry, operates over static matrices, and provides no operation-level zero-trust access gating. TrustChain-AI combines temporal exponential moving average scoring with operation-level policy enforcement.")
        ]
    },
    {
        "num": 5,
        "title": "Research Objectives & Explicit Scope Boundaries",
        "tracker": "PROJECT SPECIFICATION · BOUNDARIES",
        "content": [
            "Six Implemented Engineering Objectives:",
            "  1. Algorithmic Identity: Implement W3C did:key using Ed25519 keypairs without central CA reliance.",
            "  2. Tamper-Evident Credentials: Build W3C JSON-LD VC issuance with URDNA2015 canonicalization.",
            "  3. Multi-Dimensional Telemetry: Ingest real-time execution signals: Success (S), Compliance (C), Latency (L).",
            "  4. Temporal Trust Scoring: Implement Exponential Moving Average trust scoring (T_i(t) = 0.7·T + 0.3·P).",
            "  5. Adaptive Policy Gateway: Enforce runtime ABAC (HTTP 403 on Quarantine; restrict privileged actions in Suspicious).",
            "  6. Explainable Discovery & Matching: Deliver multi-factor candidate ranking (MatchScore = 0.4T + 0.3(r/5) + 0.2σ + 0.1(1-λ)).",
            "Explicit Scope Boundaries (Academic Honesty):",
            "  • Local Relational Storage: Uses high-performance SQLite WAL; not a distributed Byzantine consensus ledger.",
            "  • Deterministic Connector: Multi-agent execution evaluated via LocalAgentConnector to avoid stochastic cloud API billing.",
            "  • Sequential Pipeline Execution: Multi-agent workflows execute sequentially; DAG parallel fork-join runtime is future scope."
        ],
        "visual": "Six numbered objective containers paired with an amber-bordered academic scope boundary card.",
        "evidence": "akta/ package structure, pyproject.toml, capstone project plan.",
        "script": "Slide 5 establishes our six core engineering objectives alongside our explicit scope boundaries. First, implement decentralized did:key identity. Second, issue tamper-evident Verifiable Credentials with JSON-LD canonicalization. Third, ingest real-time telemetry across success, compliance, and latency. Fourth, engineer an Exponential Moving Average trust engine. Fifth, build an adaptive policy gateway that enforces operation gating. Sixth, build an explainable candidate discovery and multi-factor matching engine. We maintain absolute academic honesty regarding our boundaries: our Verifiable Data Registry uses an optimized local SQLite engine with Write-Ahead Logging, agent execution is simulated via LocalAgentConnector, and workflow execution is sequential. These boundaries were chosen deliberately to ensure reproducible, sub-millisecond evaluation.",
        "qa": [
            ("Why did you limit the scope to a local SQLite VDR instead of deploying to Ethereum or Solana?",
             "Public blockchains introduce 2-to-15 second block confirmation latencies and variable gas costs per transaction, which is impractical for inter-agent communication operating at millisecond scale. SQLite WAL provides sub-5ms ACID transactions and zero operational overhead, while strictly satisfying the W3C VDR interface requirements.")
        ]
    },
    {
        "num": 6,
        "title": "System Architecture & 5-Tier Layered Design",
        "tracker": "SYSTEM ARCHITECTURE · 5-TIER LAYERED DESIGN",
        "content": [
            "1. Agent Layer: Autonomous AI Agents, did:key Ed25519 identity, LocalAgentConnector deterministic simulation.",
            "2. Gateway Layer: FastAPI ASGI Server (port 8050), AdaptivePolicyEnforcer, security headers, request ID tracing.",
            "3. Intelligence Layer: TrustEngine (EMA evaluation), AgentRegistry (Discovery/Matching), Collaboration Manager.",
            "4. Storage Layer: 13-Table SQLite WAL Verifiable Data Registry (sub-5ms query latency, ACID compliance).",
            "5. Presentation Layer: React 19 + Vite SOC Dashboard (port 5173), dark navy theme, AgentInvestigationDrawer.",
            "Inter-Tier Communication: Authenticated REST APIs over HTTP/TLS, JSON-LD payloads, Ed25519 detached signatures."
        ],
        "visual": "High-resolution architecture diagram (architecture_diagram.png) illustrating the 5 tiers, port bindings, and data flow paths.",
        "evidence": "akta/server.py (ports & routing), frontend/vite.config.js, docs/presentation/final/assets/architecture_diagram.png.",
        "script": "Slide 6 presents the 5-tier architecture of TrustChain-AI. At the foundation is the Agent Layer, where agents maintain self-sovereign did:key identities. Above it, the Gateway Layer operates on port 8050 using FastAPI, acting as the security gatekeeper through AdaptivePolicyEnforcer. The Intelligence Layer houses our TrustEngine, telemetry normalizer, and multi-factor candidate matchmaker. The Storage Layer implements our Verifiable Data Registry using SQLite with Write-Ahead Logging across 13 tables, delivering sub-5ms latency and full ACID guarantees. Finally, the Presentation Layer runs on port 5173 using React 19 and Vite, providing human security operators with an enterprise SOC dashboard and a forensic investigation drawer.",
        "qa": [
            ("What happens if Tier 3 (Trust Intelligence) fails or crashes?",
             "The Gateway Layer enforces fail-secure zero-trust policies: if trust state cannot be determined, agents default to SUSPICIOUS or QUARANTINED, denying privileged mutations while preserving system integrity.")
        ]
    },
    {
        "num": 7,
        "title": "Decentralized Identity (DID) & VC Lifecycle",
        "tracker": "CRYPTOGRAPHIC FOUNDATION · W3C SSI",
        "content": [
            "1. Decentralized Identifier (did:key) Generation:",
            "   • Generates 32-byte Ed25519 signing keypair using PyNaCl / libsodium.",
            "   • Appends multicodec two-byte prefix 0xED01 (Ed25519 public key).",
            "   • Encodes via base58-btc with prefix 'z' -> did:key:z6MkuT8g...",
            "   • Fully stateless resolution: public key decoded directly from DID string without registry lookup.",
            "2. Verifiable Credential Lifecycle:",
            "   • Minting: Drafts JSON-LD credential binding DID to certified capabilities, model name, and issuance date.",
            "   • Canonicalization: Normalizes RDF dataset using URDNA2015 algorithm, eliminating JSON formatting variance.",
            "   • Signing: Computes SHA-256 digest of canonicalized N-Quads and signs with issuer private key.",
            "   • Proof Attachment: Embeds Ed25519Signature2020 proof containing signature and verification method.",
            "   • Verification: Detaches proof, re-canonicalizes payload, and cryptographically asserts signature validity."
        ],
        "visual": "Cryptographic lifecycle diagram (did_vc_lifecycle.png) detailing keygen, canonicalization, signing, and verification.",
        "evidence": "akta/did.py, akta/vc.py, tests/commands/test_claim.py, tests/commands/test_keys.py.",
        "script": "Slide 7 details our cryptographic identity foundation. We implement the W3C did:key specification using Ed25519 elliptic curve keypairs. The public key is prefixed with multicodec byte 0xED01 and base58-btc encoded, yielding an identifier like did:key:z6M. This enables stateless verification: any node can decode the agent's public key directly from its DID string without querying a central directory. On top of this, we build W3C Verifiable Credentials. To sign a JSON credential securely, we must eliminate variations in whitespace and key ordering. We pass the credential subject through URDNA2015 RDF dataset canonicalization, generate a SHA-256 hash of the normalized N-Quads, and append an Ed25519 detached signature proof. If a single byte is altered in transit, verification fails cryptographically.",
        "qa": [
            ("What is URDNA2015 and why is canonicalization necessary before signing a JSON document?",
             "In JSON, whitespace, indentation, and key ordering can vary without changing semantic meaning, but any byte change alters a SHA-256 hash. URDNA2015 converts the JSON-LD document into standardized N-Quads, ensuring deterministic cryptographic hashing across different languages and platforms.")
        ]
    },
    {
        "num": 8,
        "title": "Dynamic Behavioral Telemetry & Trust Engine Formulation",
        "tracker": "INTELLIGENCE ENGINE · REAL-TIME TRUST EVALUATION",
        "content": [
            "1. Instantaneous Task Performance Metric P_i(t):",
            "   • P_i(t) = 0.6·S_i(t) + 0.3·C_i(t) + 0.1·(1 - L_i(t))",
            "   • S_i(t) ∈ {0, 1}: Binary task outcome (1 for success, 0 for failure; 60% weight).",
            "   • C_i(t) ∈ [0, 1]: Policy compliance score (1.0 for zero compliance violations; 30% weight).",
            "   • L_i(t) = min(latency_ms / 2000, 1.0): Latency penalty factor (10% weight; capped at 2000ms).",
            "2. Temporal Exponential Moving Average (EMA) Formulation:",
            "   • T_i(t) = 0.7·T_i(t-1) + 0.3·P_i(t)  with initial trust anchor T_i(0) = 1.000",
            "   • Decay Parameter λ = 0.7: Retains 70% historical inertia to absorb transient network jitter.",
            "   • Adaptation Weight (1-λ) = 0.3: Rapidly penalizes repeated failures while preventing single-event overreaction.",
            "3. Sensor Normalization: Robust clipping ensures all input metrics map strictly to [0.0, 1.0] unit interval."
        ],
        "visual": "Telemetry pipeline flowchart (telemetry_pipeline.png) showing sensor ingestion, normalization, EMA calculation, and state emission.",
        "evidence": "akta/trust_engine.py (TrustEngine, TrustConfig, calculate_behavioral_score), tests/test_trust_engine.py.",
        "script": "Slide 8 introduces the mathematical heart of TrustChain-AI: our dynamic trust engine. Raw telemetry cannot be evaluated naively; we compute an Instantaneous Performance Score, P_i(t), as a weighted sum: 60% weight on task success, 30% on policy compliance, and 10% on latency bonus. Latency is normalized and capped at 2000 milliseconds. To prevent single transient network hiccups from knocking an agent offline, we smooth P_i(t) using an Exponential Moving Average: T_i(t) equals 0.7 times previous trust plus 0.3 times current performance. Newly registered agents start with a baseline score of 1.0. This 70% historical memory provides stability, while the 30% update weight ensures that sustained non-compliance triggers decisive intervention.",
        "qa": [
            ("Why did you choose lambda = 0.7 for historical memory decay?",
             "A value of lambda = 0.7 strikes an optimal balance between responsiveness and stability: it retains 70% historical inertia, preventing transient network spikes from flipping an agent's trust state, while ensuring that two consecutive catastrophic failures will decisively drive trust below 0.50 into Quarantine.")
        ]
    },
    {
        "num": 9,
        "title": "Mathematical Trajectory Dynamics: Degradation & Recovery Timeline",
        "tracker": "CALCULATED SCENARIO · 10-ROUND TRUST TIMELINE",
        "content": [
            "10-Round Illustrative Scenario Calculations (T_0 = 1.000):",
            "  • R0: Baseline Prior: T_0 = 1.000 [State: TRUSTED]",
            "  • R1: Flawless Task (P=0.994): T_1 = 0.7(1.000) + 0.3(0.994) = 0.998 [State: TRUSTED]",
            "  • R2: Normal Execution (P=0.988): T_2 = 0.7(0.998) + 0.3(0.988) = 0.995 [State: TRUSTED]",
            "  • R3: Latency Spike (P=0.460): T_3 = 0.7(0.995) + 0.3(0.460) = 0.835 [State: TRUSTED]",
            "  • R4: Complete Failure (P=0.000): T_4 = 0.7(0.835) + 0.3(0.000) = 0.584 [State: SUSPICIOUS]",
            "  • R5: Repeated Failure (P=0.000): T_5 = 0.7(0.584) + 0.3(0.000) = 0.409 [State: QUARANTINED (T<0.50)]",
            "  • R6: Supervised Canary 1 (P=0.991): T_6 = 0.7(0.409) + 0.3(0.991) = 0.584 [State: SUSPICIOUS]",
            "  • R7: Supervised Canary 2 (P=0.992): T_7 = 0.7(0.584) + 0.3(0.992) = 0.706 [State: SUSPICIOUS]",
            "  • R8: Supervised Canary 3 (P=0.993): T_8 = 0.7(0.706) + 0.3(0.993) = 0.792 [State: SUSPICIOUS]",
            "  • R9: Supervised Canary 4 (P=0.993): T_9 = 0.7(0.792) + 0.3(0.993) = 0.852 [State: TRUSTED (T>=0.80)]",
            "  • R10: Restored Ops (P=0.994): T_10 = 0.7(0.852) + 0.3(0.994) = 0.895 [State: TRUSTED]",
            "CALCULATED ILLUSTRATIVE SCENARIO — NOT MEASURED PRODUCTION DATA:",
            "  • Rapid Quarantine: Isolated in exactly TWO complete failures (T_5 = 0.409 < 0.50).",
            "  • Inertial Recovery: Requires FOUR supervised canary rounds (P>0.99) to restore Trusted state (T_9 = 0.852 >= 0.80)."
        ],
        "visual": "Line graph (trust_timeline.png) plotting 10-round calculated trajectory with zone fills (Trusted >=0.80, Suspicious 0.50-0.80, Quarantine <0.50).",
        "evidence": "akta/trust_engine.py, generate_charts.py, docs/presentation/final/assets/trust_timeline.png.",
        "script": "Slide 9 demonstrates the mathematical behavior of our trust engine through a 10-round illustrative scenario. We emphasize that this is a calculated mathematical demonstration, not live production telemetry. Starting from a baseline of 1.0, rounds 1 and 2 maintain high trust. In round 3, a latency spike drops performance to 0.46, pulling trust down to 0.835, but remaining Trusted due to historical inertia. In round 4, a complete task failure drops trust to 0.584, triggering the Suspicious state. In round 5, a second consecutive failure drives trust down to 0.409, immediately breaching the 0.50 threshold into Quarantine. Notice the asymmetric recovery: because of historical inertia, returning to Trusted requires four consecutive flawless canary rounds. Trust is fast to lose and slow to regain.",
        "qa": [
            ("Why does recovery require four canary rounds while degradation only took two rounds?",
             "This asymmetric hysteresis is an intentional security design: trust must be difficult to rebuild and easy to lose. With lambda = 0.7, recovery from T=0.409 requires multiple consistent high-performance canary rounds (P approx 0.99) before crossing the T >= 0.80 threshold back into Trusted.")
        ]
    },
    {
        "num": 10,
        "title": "Adaptive Authorization & Zero-Trust Access Control",
        "tracker": "ACCESS CONTROL · ZERO-TRUST ENFORCEMENT",
        "content": [
            "1. Human Role Hierarchy (Portal Operators):",
            "   • ADMIN: Full mutation privileges, user account provisioning, manual trust override.",
            "   • OPERATOR: Workflow execution, candidate matching, discovery queries.",
            "   • VIEWER: Read-only access to dashboard, metrics, and audit logs; mutations blocked.",
            "   • Security: Argon2id password hashing, 5-strike account lockout (HTTP 423), JWT refresh rotation.",
            "2. Autonomous Agent Authorization (AdaptivePolicyEnforcer):",
            "   • TRUSTED (T >= 0.80): Full autonomous execution across standard & privileged workflows.",
            "   • SUSPICIOUS (0.50 <= T < 0.80): Standard queries permitted; privileged mutations blocked with HTTP 403.",
            "   • QUARANTINED (T < 0.50): Total isolation; all execution requests denied (HTTP 403).",
            "   • REVOKED: Administrative terminal state; cryptographically blacklisted with zero recovery.",
            "Backend Sole Authority: Frontend badges are UI conveniences; FastAPI backend is the sole enforcement boundary."
        ],
        "visual": "Dual-layer authorization matrix (auth_matrix.png) contrasting human RBAC with agent ABAC state enforcement.",
        "evidence": "akta/adaptive_auth.py, akta/auth/router.py, tests/test_adaptive_policy.py, tests/test_authentication.py.",
        "script": "Slide 10 details our defense-in-depth authorization model. We enforce a strict separation between human administrators and autonomous agents. For human operators, we implement Role-Based Access Control across ADMIN, OPERATOR, and VIEWER roles, secured with Argon2id password hashing, a five-strike brute-force lockout policy, and JWT token rotation. For autonomous agents, we implement Attribute-Based Access Control via AdaptivePolicyEnforcer. We classify operations into standard queries and privileged actions. When an agent is TRUSTED, it has full execution privileges. If it degrades into SUSPICIOUS, privileged mutations like workflow orchestration are blocked with HTTP 403. If it falls into QUARANTINED, all execution is blocked. All checks are enforced authoritatively on the backend.",
        "qa": [
            ("Can a malicious actor bypass role restrictions by modifying client-side JavaScript?",
             "No. Frontend role flags are strictly presentation aids. All security boundaries are authoritatively enforced on the FastAPI backend using JWT claims verified on every request.")
        ]
    },
    {
        "num": 11,
        "title": "Agent Capability Discovery & Diagnostic Eligibility",
        "tracker": "DISCOVERY ENGINE · TRANSPARENT GOVERNANCE",
        "content": [
            "1. Multi-Parametric Search Controls:",
            "   • Capability Tag Selector: Filters agents by certified skills (coding, security_audit, research, analysis).",
            "   • Dynamic Min Trust Slider: Real-time interactive slider (0.00 to 1.00 in steps of 0.05).",
            "   • Operational Availability Filter: AVAILABLE, BUSY, OFFLINE status toggles.",
            "   • Endpoint Health Probe Filter: Validates live HTTP 200 connectivity.",
            "2. Explainable Eligibility vs. Exclusion Engine:",
            "   • Rather than silently omitting excluded candidates, TrustChain-AI displays explicit diagnostic rationales:",
            "   • Quarantine Exclusion: 'Under behavioral quarantine (T = 0.42 < 0.50)'.",
            "   • Threshold Exclusion: 'Trust score (0.65) does not meet requested minimum slider (0.80)'.",
            "   • Availability Exclusion: 'Status is BUSY on active collaboration session'.",
            "Direct Operational Actions: One-click 'Investigate' drawer and 'Launch Session' actions."
        ],
        "visual": "Discovery eligibility flowchart (discovery_flowchart.png) showing multi-stage capability, trust, and health filtering.",
        "evidence": "frontend/src/components/DiscoveryCenter.jsx, akta/vdr/registry_router.py (/api/v1/registry/discover).",
        "script": "Slide 11 showcases our Agent Discovery Engine. It is vital to distinguish discovery from matching: discovery is an inventory exploration and eligibility tool. Operators filter agents by required capability, set a minimum trust threshold slider from 0.0 to 1.0, and filter by operational availability and endpoint health. Instead of silently hiding excluded agents, our engine evaluates every registered agent and returns explicit diagnostic rationales: explaining whether an agent was excluded due to quarantine, low trust, or busy status. Operators can click Investigate on any card to mount our forensic drawer instantly.",
        "qa": [
            ("What is the primary difference between Discovery and Matching?",
             "Discovery is an inventory exploration tool that evaluates capability, availability, and eligibility against operator filters. Matching is an algorithmic ranking engine that scores eligible agents for a specific task using a multi-factor equation.")
        ]
    },
    {
        "num": 12,
        "title": "Task-Driven Matchmaker & Explainable Multi-Factor Ranking",
        "tracker": "ALGORITHMIC MATCHMAKING · EXPLAINABLE AI",
        "content": [
            "1. Composite MatchScore Formulation:",
            "   • MatchScore = 0.4·T + 0.3·(r/5.0) + 0.2·σ + 0.1·(1 - λ)",
            "   • T: Normalized temporal trust score [0.0, 1.0] (40% weight).",
            "   • r: Historical peer reputation [1.0, 5.0] normalized by /5.0 (30% weight).",
            "   • σ: Historical task success rate (successes / total_tasks) (20% weight).",
            "   • λ: Latency penalty min(latency_ms / 2000, 1.0) -> (1-λ) is latency bonus (10% weight).",
            "2. Hard Zero-Trust Disqualification Gates:",
            "   • Immediate Disqualification: If state is QUARANTINED or REVOKED, MatchScore is forced to 0.000 with 'REJECTED BY POLICY'.",
            "3. Candidate Benchmark Breakdown (0.4·T + 0.3·r/5 + 0.2·σ + 0.1·[1-λ]):",
            "   • 1. Agent Alpha: 0.963 [TOP CANDIDATE SPOTLIGHT] (0.380 + 0.288 + 0.200 + 0.095)",
            "   • 2. Agent Beta:  0.812 [ELIGIBLE CANDIDATE] (0.340 + 0.252 + 0.170 + 0.050)",
            "   • 3. Agent Gamma: 0.655 [ELIGIBLE CANDIDATE] (0.260 + 0.210 + 0.150 + 0.035)",
            "   • 4. Agent Delta: 0.000 [DISQUALIFIED - UNDER QUARANTINE (T=0.42)]",
            "Note: Calculated illustrative benchmark scenario matching akta/vdr/registry_crud.py."
        ],
        "visual": "Stacked horizontal bar chart (matching_breakdown.png) showing multi-factor contributions and hard policy rejection for 4 candidate agents.",
        "evidence": "akta/vdr/registry_crud.py (find_best_agent_match), tests/test_investigation_discovery_matching.py.",
        "script": "Slide 12 covers our Task-Driven Matchmaker. When an operator submits a task description, capability requirement, and minimum trust score, the system ranks all eligible candidates using our multi-factor matching formula: 40% weight on temporal trust, 30% on historical reputation, 20% on success rate, and 10% on latency bonus. The chart on the right illustrates the transparent score contributions for four benchmark candidates. Agent Alpha achieves the top match with a score of 0.963. Notice Agent Delta: despite having a 5.0 reputation, because it is under Quarantine, our zero-trust policy gate immediately forces its MatchScore to zero with REJECTED BY POLICY.",
        "qa": [
            ("Why does Agent Delta receive a MatchScore of 0.000 despite having a 5.0 reputation?",
             "Our zero-trust policy gateway enforces hard disqualification: if an agent is in QUARANTINED or REVOKED state, its MatchScore is immediately forced to 0.000 with reason 'REJECTED BY POLICY', regardless of historical reputation.")
        ]
    },
    {
        "num": 13,
        "title": "Multi-Agent Collaboration Sessions & Sequential Pipeline",
        "tracker": "RUNTIME COLLABORATION · BILATERAL SESSION LIFECYCLE",
        "content": [
            "1. Bilateral Collaboration Session Lifecycle:",
            "   • PENDING: Session requested; mutual DIDs and Verifiable Credentials asserted.",
            "   • ACTIVE: Policy gateway verifies both agents are TRUSTED; delegation handshake established.",
            "   • COMPLETED: Task payload returned; execution metrics recorded in telemetry logs.",
            "   • TERMINATED: Session forcefully aborted if an agent degrades into Quarantine mid-execution.",
            "2. Sequential Workflow Pipeline Execution:",
            "   • Workflows structured as sequential chains across specialized agents (e.g. Planning -> Coding -> Review).",
            "   • Intermediate state transitions evaluated after every node execution.",
            "   • Canary Drift Abort: If any node exhibits policy violations or latency spikes, subsequent steps halt immediately.",
            "3. Closed-Loop Post-Task Feedback: Requester submits 1-to-5 star rating, dynamically updating agent reputation."
        ],
        "visual": "Collaboration sequence diagram (collaboration_sequence.png) illustrating bilateral request, validation, execution, and rating.",
        "evidence": "akta/vdr/registry_router.py (/collaboration/request, /sessions/{id}/step), tests/test_multi_agent.py, tests/test_platform_features.py.",
        "script": "Slide 13 details our multi-agent collaboration protocol. Agents do not collaborate blindly; sessions follow a strict finite-state lifecycle: PENDING, ACTIVE, COMPLETED, or TERMINATED. In step 1, mutual DIDs and credentials are exchanged. In step 2, the gateway verifies that both agents are in the Trusted state before activating the session. During multi-step sequential workflows—such as a planning agent delegating to a coding agent—telemetry is captured after every step. If an agent degrades during execution, our canary drift detection aborts the workflow immediately. Upon completion, peer ratings are recorded, feeding back into the agent's long-term reputation.",
        "qa": [
            ("What happens if an agent degrades mid-way through a multi-step collaboration?",
             "Telemetry is recorded after every step. If the target agent's trust drops into Quarantine, the gateway aborts the session immediately, marks status as TERMINATED, and logs an alert.")
        ]
    },
    {
        "num": 14,
        "title": "Local Relational VDR Architecture & Quad-Dimensional Auditability",
        "tracker": "DATA INTEGRITY · 13-TABLE VDR SCHEMA",
        "content": [
            "1. High-Performance SQLite WAL Storage Engine:",
            "   • W3C Verifiable Data Registry implemented via SQLite with Write-Ahead Logging (PRAGMA journal_mode=WAL;).",
            "   • Concurrent read/write access without database lock contention; query latency under 5 milliseconds.",
            "2. Exact 13 SQLite Tables across 5 Functional Domains:",
            "   • Identity & Credentials: stored_vcs",
            "   • Behavioral Trust: agent_trust_states, telemetry_logs, trust_audit_trails",
            "   • Agent Registry: agents, agent_ratings",
            "   • Collaboration & Workflows: collaboration_sessions, collaboration_events, workflows, workflow_nodes",
            "   • Access Control & Security: users, refresh_tokens, security_audit_events",
            "3. Quad-Dimensional Forensic Audit Trails:",
            "   • Credential Audit (stored_vcs) | Trust Transition Audit (trust_audit_trails)",
            "   • Interaction Telemetry (telemetry_logs) | Access Control Violations (security_audit_events)"
        ],
        "visual": "Entity-Relationship diagram (database_er_diagram.png) illustrating the 13 SQLite tables grouped across 5 functional domains.",
        "evidence": "akta/vdr/models.py, akta/vdr/database.py, tests/test_platform_features.py.",
        "script": "Slide 14 presents our Verifiable Data Registry. In W3C specifications, a VDR is an abstract interface, not necessarily a public blockchain. For TrustChain-AI, we engineered a high-throughput relational VDR using SQLite in Write-Ahead Logging mode. This guarantees atomic transactions and sub-5 millisecond response times without gas costs or consensus delays. The database consists of exactly 13 tables across five functional domains. To guarantee forensic accountability, we maintain four separate audit dimensions: stored_vcs for credential provenance, trust_audit_trails for state transitions, telemetry_logs for raw interaction metrics, and security_audit_events for access control violations. Every event is immutable and timestamped.",
        "qa": [
            ("Why is SQLite WAL sufficient for high-concurrency capstone evaluation?",
             "SQLite Write-Ahead Logging allows concurrent readers to access the database without blocking writers, maintaining sub-millisecond query latencies and complete ACID compliance for local registries.")
        ]
    },
    {
        "num": 15,
        "title": "Operational SOC Portal Demonstration & Interface Verification",
        "tracker": "FRONTEND IMPLEMENTATION · SECURITY OPERATIONS CENTER",
        "content": [
            "1. Modern Frontend Architecture & Five Operational Modules:",
            "   • React 19 + Vite 8.2: Production bundle built in 14.43s (2,478 modules transformed, zero errors).",
            "   • Dark Navy SOC Theme: #080E1A background, #111C35 containers, #00F0FF accents, with light mode toggle.",
            "   • Five Modules: Executive Dashboard, Agent Explorer (/agents), Discovery (/discovery), Matching (/matching), Admin (/admin/users).",
            "2. Agent Investigation Forensic Drawer (AgentInvestigationDrawer.jsx):",
            "   • Mounted immediately when clicking 'INVESTIGATE' in Agent Explorer; fetches live state via backend REST APIs.",
            "   • Identity & Specs: Agent DID, model provider, execution endpoint, and live 'Test Health' probe button.",
            "   • Real-Time KPI Cards: Trust Score T(t), Reputation r/5.0, Operational Status, and Endpoint Health.",
            "   • Workload Metrics: Total tasks, successes, failures, success rate %, and average latency ms.",
            "   • Trust Math Causality: Real-time P(t) = 0.6·S + 0.3·C + 0.1·(1-L) score breakdown from recent events.",
            "   • Interactive Sub-Tabs: Toggle between 'Recent Telemetry' (task IDs, compliance, latency) and 'Trust Transitions' (audit history).",
            "   • Deep-Dive Route: Direct 'Full View' action link to /agents/{did} (AgentDetails.jsx) with historical trend charts.",
            "3. Explainable Matching Interface: Mathematical breakdown chips (0.4·T + 0.3·r/5 + 0.2·σ + 0.1·[1-λ]) and policy rejection reasons."
        ],
        "visual": "Frontend component architecture and forensic drawer layout illustrating real-time telemetry inspection and model specs.",
        "evidence": "frontend/src/components/AgentExplorer.jsx, AgentInvestigationDrawer.jsx, AgentDetails.jsx, DiscoveryCenter.jsx, MatchingCenter.jsx.",
        "script": "Slide 15 showcases our Security Operations Center portal. Built with React 19 and Vite 8.2, the interface provides a unified cockpit for monitoring autonomous agents. The design follows enterprise SOC conventions with a dark navy palette, high-contrast cyan accents, and complete light mode compatibility. The portal features five dedicated views: Executive Dashboard, Agent Explorer, Discovery Center, Matching Center, and User Management. When an operator clicks 'Investigate' on any agent card, an asynchronous slide-over drawer mounts immediately. Rather than an ungrounded mockup, this drawer is fully wired to our backend endpoints: displaying live model specifications, KPI cards, workload metrics, our P(t) trust math causality breakdown, and dual sub-tabs for raw telemetry records and state transition audit logs, with a direct link to the full agent profile page.",
        "qa": [
            ("How does the Investigate button work on the frontend?",
             "Clicking 'Investigate' mounts AgentInvestigationDrawer.jsx, which makes concurrent asynchronous API calls to /registry/agents/{did}, /trust/state/{did}, /trust/telemetry/{did}, and /trust/audit/{did}, displaying live telemetry and audit history without page reloads.")
        ]
    },
    {
        "num": 16,
        "title": "Empirical Testing, Subsystem Health & Mathematical Verification",
        "tracker": "EMPIRICAL VALIDATION · 80/80 AUTOMATED TESTS PASSING",
        "content": [
            "1. Verified Pytest Automated Test Suite: 80 PASSED IN 15.04s (100% Pass Rate)",
            "   • test_claim.py & test_keys.py (15 tests): Ed25519 keygen, did:key multicodec 0xED01, base58-btc, VC verification.",
            "   • test_vdr.py & test_registry.py (10 tests): W3C VC schema validation, URDNA2015 canonicalization, tampering detection.",
            "   • test_adaptive_policy.py (7 tests): RBAC + ABAC enforcement, privileged vs standard action gating, HTTP 403 intercepts.",
            "   • test_authentication.py (28 tests): Argon2id hashing, JWT refresh rotation, 5-strike lockout, role matrices.",
            "   • test_e2e_lifecycle.py (3 tests): Complete agent onboarding, VC issuance, telemetry stream, and trust progression.",
            "   • test_investigation_discovery_matching.py (3 tests): Investigation drawer endpoints, discovery filters, exclusion rationales.",
            "   • test_multi_agent.py & test_platform_features.py (10 tests): Bilateral sessions, 13 SQLite tables, matching formula.",
            "   • test_system_health.py (4 tests): Live /health probe, database WAL latency check, trust math core verification.",
            "2. Frontend Production Build: Vite 8.2.2 bundle compiled in 14.43s (2,478 modules transformed, zero errors).",
            "3. Authoritative Live Health Probe (GET /health):",
            "   • Returns HTTP 200 OK: SQLite WAL latency < 5ms, TrustEngine in-process math core validated (P=1.000, T=1.000)."
        ],
        "visual": "Test distribution bar chart (test_results_chart.png) displaying 80 passing tests across 8 suites in 15.04s, plus live /health JSON card.",
        "evidence": "tests/ (80 passing tests), pytest.ini, frontend/package.json, akta/server.py (/health).",
        "script": "Slide 16 details our empirical testing and subsystem verification. In computer science capstone projects, implementation claims must be backed by reproducible evidence. We verified the complete framework against an 80-test automated pytest suite, achieving 100% pass rate in 15.04 seconds across eight distinct test modules in SQLite WAL mode. These tests cover cryptographic primitives, Verifiable Credential tampering, mathematical EMA boundary conditions, adaptive policy enforcement, collaboration lifecycles, and RBAC security. The chart on the upper right shows the distribution across the eight suites. On the frontend, Vite 8.2.2 compiles the production bundle in 14.43 seconds with zero syntax or packaging errors across 2,478 transformed modules. Finally, our live /health endpoint continuously confirms that the SQLite WAL database and trust math engine are operational with sub-millisecond query latency.",
        "qa": [
            ("How do you verify credential tampering in automated tests?",
             "In test_vc.py, we alter a single byte in the credentialSubject payload after cryptographic signing and assert that verify_credential raises a cryptographic verification exception.")
        ]
    },
    {
        "num": 17,
        "title": "Transparent Limitations, Threats to Validity & Research Roadmap",
        "tracker": "CRITICAL ANALYSIS · HONEST BOUNDARIES & FUTURE SCOPE",
        "content": [
            "Seven Frank Technical Limitations & Threats to Validity:",
            "  1. Local Relational Storage: Uses SQLite WAL rather than a distributed Byzantine consensus ledger (Ethereum/Hedera).",
            "  2. Deterministic Telemetry Emulation: Evaluated via LocalAgentConnector; wild LLM reasoning variance remains unmeasured.",
            "  3. Sensor Authenticity Assumption: Assumes local gateway sensors are uncompromised; internal sensor spoofing is out of scope.",
            "  4. Static Hyperparameter Weights: EMA weights (0.7/0.3) and matching weights (0.4/0.3/0.2/0.1) are fixed rather than learned.",
            "  5. Sequential Pipeline Boundary: Multi-agent workflows run sequentially; parallel DAG fork-join execution is future work.",
            "  6. Closed-World Evaluation Scale: Benchmarked with 8-10 agents; million-agent scale requires distributed DHT indexing.",
            "  7. False Positive Anomaly Risk: Transient network hiccups can cause brief latency penalties, temporarily nudging trust into Suspicious.",
            "Four-Phase Post-Capstone Research Roadmap:",
            "  • Phase 1: Distributed Byzantine VDR Integration (Hedera Hashgraph / Tendermint BFT).",
            "  • Phase 2: Zero-Knowledge Telemetry Proofs (zk-SNARKs for proprietary prompt & weight privacy).",
            "  • Phase 3: Dynamic Reinforcement Learning for Adaptive Weight & Threshold Tuning.",
            "  • Phase 4: Asynchronous Parallel DAG Workflow Runtime with Fork-Join Dependency Resolution."
        ],
        "visual": "Comparative two-card container layout contrasting 7 technical limitations with the 4-phase research roadmap.",
        "evidence": "Capstone Blackbook Chapter 6, research paper conclusions.",
        "script": "On Slide 17, we maintain academic rigor by transparently addressing seven technical limitations and outlining our future research roadmap. First, our VDR uses local SQLite WAL rather than a distributed Byzantine consensus network. Second, agent telemetry is deterministically simulated via LocalAgentConnector. Third, we assume gateway sensors are authentic. Fourth, our mathematical weights are static hyperparameters rather than dynamically learned via reinforcement learning. Fifth, our workflow engine executes sequentially rather than as an asynchronous parallel DAG. To address these limitations, our post-capstone roadmap outlines four concrete phases: integrating Hedera Hashgraph for decentralized consensus, implementing zk-SNARK proofs for model privacy, applying reinforcement learning for dynamic weight tuning, and building a full parallel DAG execution runtime.",
        "qa": [
            ("How will you handle privacy when agents share proprietary prompts or models?",
             "In Phase 2 of our roadmap, we plan to implement Zero-Knowledge Telemetry Proofs (zk-SNARKs), allowing agents to mathematically prove compliance without disclosing proprietary prompts or model weights.")
        ]
    },
    {
        "num": 18,
        "title": "Capstone Defense Conclusion, Core Contributions & Open Defense",
        "tracker": "PROJECT DEFENSE CONCLUSION · KEY CONTRIBUTIONS",
        "content": [
            "Summary of Three Core Research & Engineering Contributions:",
            "  1. Cryptographic Trust Anchor (W3C did:key & VCs): Engineered decentralized agent identity using Ed25519 keypairs and multicodec encoding without central CA reliance. Implemented W3C Verifiable Credentials with URDNA2015 canonicalization and Ed25519Signature2020 proofs.",
            "  2. Dynamic Behavioral Telemetry & Adaptive Zero-Trust Gating: Replaced static binary authentication with continuous Exponential Moving Average trust scoring (T = 0.7·T + 0.3·P). Coupled trust scores directly to operation-level adaptive gating (blocking privileged actions in Suspicious, total quarantine below 0.50).",
            "  3. Verifiable Traceability & Explainable Matching: Built a 13-table SQLite WAL Verifiable Data Registry with quad-dimensional auditability. Created an explainable multi-factor candidate matching engine (MatchScore = 0.4T + 0.3(r/5) + 0.2σ + 0.1(1-λ)) backed by a modern React 19 SOC portal.",
            "Empirical Validation: 80/80 passing pytest tests in 15.04s and 100% verified production Vite frontend build (14.43s).",
            "Academic Acknowledgments:",
            "  • Department of Computer Engineering, MPSTME, SVKM's NMIMS (Deemed-to-be University), Mumbai.",
            "  • Project Guide & Mentorship Committee for technical guidance throughout academic session 2026–2027.",
            "DEFENSE COMMITTEE Q&A SESSION: Thank you for your time and evaluation. We welcome questions from the examination committee."
        ],
        "visual": "Balanced closing defense synthesis layout with glowing neon cyan Q&A banner.",
        "evidence": "Entire repository codebase, 80 passing tests, and capstone blackbook.",
        "script": "To conclude our defense, TrustChain-AI successfully solves the point-in-time security failure in autonomous multi-agent systems. We have demonstrated three core contributions: a cryptographic trust anchor built on W3C did:key and Verifiable Credentials; dynamic behavioral telemetry coupled with an Exponential Moving Average trust engine and adaptive policy gating; and a high-performance 13-table SQLite WAL Verifiable Data Registry with quad-dimensional auditability and an explainable matching engine. All claims are backed by 80 automated unit tests passing in 15.04 seconds and a verified production frontend. We express our deepest gratitude to the Department of Computer Engineering at MPSTME, SVKM's NMIMS, our project guide, and the examination committee. We are now ready for your questions.",
        "qa": [
            ("What is the primary academic takeaway of TrustChain-AI?",
             "That static cryptographic identity is merely the baseline of security. In autonomous multi-agent systems, trust is a dynamic, continuously earned behavioral property that must directly govern runtime authorization.")
        ]
    }
]

# ==============================================================================
# 1. Generate Markdown File: TrustChain_AI_Final_Presentation_Slide_Wise_Content.md
# ==============================================================================
md_path = os.path.join(OUTPUT_DIR, "TrustChain_AI_Final_Presentation_Slide_Wise_Content.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# TrustChain-AI: Complete Slide-Wise Content, Spoken Scripts & Examiner Q&A Dossier\n\n")
    f.write("**Project Title:** TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration  \n")
    f.write("**Institution:** Department of Computer Engineering, MPSTME, SVKM's NMIMS (Deemed-to-be University), Mumbai  \n")
    f.write("**Evaluation Target:** Final-Year B.Tech Capstone Defense (18 Slides)  \n")
    f.write("**Academic Session:** 2026–2027  \n")
    f.write("**Verified Test Status:** 80 / 80 Passed in 15.04s | Vite Build: 14.43s (2,478 modules transformed)  \n\n")
    f.write("---\n\n")

    for slide in SLIDES_DATA:
        f.write(f"## Slide {slide['num']}: {slide['title']}\n\n")
        f.write(f"**Category Header / Tracker:** `{slide['tracker']}`  \n\n")
        f.write("### Exact Slide Content (On-Slide Bullet Points & Formulations)\n")
        for line in slide["content"]:
            f.write(f"{line}\n")
        f.write("\n")
        f.write(f"### Visual & Embedded Asset\n{slide['visual']}\n\n")
        f.write(f"### Codebase Grounding & Evidence Reference\n`{slide['evidence']}`\n\n")
        f.write("### Spoken Defense Script (~45–75 Seconds)\n")
        f.write(f"> \"{slide['script']}\"\n\n")
        f.write("### Likely Examiner Questions & Technically Defensible Answers\n")
        for q, a in slide["qa"]:
            f.write(f"* **Examiner Question:** *\"{q}\"*\n")
            f.write(f"  * **Defensible Technical Answer:** {a}\n\n")
        f.write("---\n\n")

print(f"Generated Markdown: {md_path}")

# ==============================================================================
# 2. Generate Word Document: TrustChain_AI_Final_Presentation_Slide_Wise_Content.docx
# ==============================================================================
docx_content_path = os.path.join(OUTPUT_DIR, "TrustChain_AI_Final_Presentation_Slide_Wise_Content.docx")
doc = Document()

# Page setup (Letter, 0.75 in margins)
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

# Styling palette
C_NAVY = RGBColor(11, 19, 43)
C_BLUE = RGBColor(42, 75, 141)
C_CYAN = RGBColor(0, 168, 181)
C_DARK = RGBColor(30, 41, 59)
C_SLATE = RGBColor(71, 85, 105)

# Document Title
p_title = doc.add_paragraph()
r_title = p_title.add_run("TrustChain-AI: Slide-Wise Content & Defense Guide")
r_title.bold = True
r_title.font.size = Pt(22)
r_title.font.color.rgb = C_NAVY
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("B.Tech Capstone Defense · 18 Slides Slide-by-Slide Content, Scripts, and Examiner Q&A")
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = C_BLUE
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_meta = doc.add_paragraph()
r_meta = p_meta.add_run("Department of Computer Engineering | MPSTME, SVKM's NMIMS | Academic Year 2026–2027\nAutomated Test Status: 80/80 Passing Tests in 15.04s | Vite Production Build: 14.43s")
r_meta.font.size = Pt(9.5)
r_meta.font.color.rgb = C_SLATE
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph().paragraph_format.space_after = Pt(10)

for slide in SLIDES_DATA:
    # Heading 1: Slide Title
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run(f"Slide {slide['num']}: {slide['title']}")
    r_h1.font.size = Pt(15)
    r_h1.font.color.rgb = C_NAVY
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(2)

    # Category Tracker
    p_tr = doc.add_paragraph()
    r_tr = p_tr.add_run(f"CATEGORY TRACKER: {slide['tracker']}")
    r_tr.font.size = Pt(9)
    r_tr.bold = True
    r_tr.font.color.rgb = C_CYAN
    p_tr.paragraph_format.space_after = Pt(6)

    # 1. Exact Slide Content
    h2_c = doc.add_heading(level=2)
    r_h2_c = h2_c.add_run("1. Exact On-Slide Content")
    r_h2_c.font.size = Pt(12)
    r_h2_c.font.color.rgb = C_BLUE
    h2_c.paragraph_format.space_after = Pt(3)

    for item in slide["content"]:
        p_item = doc.add_paragraph()
        r_item = p_item.add_run(item)
        r_item.font.size = Pt(10)
        r_item.font.color.rgb = C_DARK
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.15

    # 2. Visual & Embedded Asset
    h2_v = doc.add_heading(level=2)
    r_h2_v = h2_v.add_run("2. Visual Diagram & Embedded Asset")
    r_h2_v.font.size = Pt(12)
    r_h2_v.font.color.rgb = C_BLUE
    h2_v.paragraph_format.space_before = Pt(6)
    h2_v.paragraph_format.space_after = Pt(3)

    p_v = doc.add_paragraph()
    r_v = p_v.add_run(slide["visual"])
    r_v.font.size = Pt(10)
    r_v.font.color.rgb = C_DARK
    p_v.paragraph_format.space_after = Pt(4)

    # 3. Grounding & Evidence
    p_ev = doc.add_paragraph()
    r_ev_lbl = p_ev.add_run("Codebase Grounding & Evidence: ")
    r_ev_lbl.bold = True
    r_ev_lbl.font.size = Pt(9.5)
    r_ev_lbl.font.color.rgb = C_SLATE
    r_ev_val = p_ev.add_run(slide["evidence"])
    r_ev_val.font.size = Pt(9.5)
    r_ev_val.font.color.rgb = C_BLUE
    p_ev.paragraph_format.space_after = Pt(6)

    # 4. Spoken Script
    h2_s = doc.add_heading(level=2)
    r_h2_s = h2_s.add_run("3. Spoken Defense Script (~45–75 Seconds)")
    r_h2_s.font.size = Pt(12)
    r_h2_s.font.color.rgb = C_BLUE
    h2_s.paragraph_format.space_after = Pt(3)

    p_scr = doc.add_paragraph()
    p_scr.paragraph_format.left_indent = Inches(0.25)
    r_scr = p_scr.add_run(f'"{slide["script"]}"')
    r_scr.italic = True
    r_scr.font.size = Pt(10)
    r_scr.font.color.rgb = C_NAVY
    p_scr.paragraph_format.space_after = Pt(6)

    # 5. Examiner Q&A
    h2_q = doc.add_heading(level=2)
    r_h2_q = h2_q.add_run("4. Likely Examiner Questions & Technically Defensible Answers")
    r_h2_q.font.size = Pt(12)
    r_h2_q.font.color.rgb = C_BLUE
    h2_q.paragraph_format.space_after = Pt(3)

    for q, a in slide["qa"]:
        p_q = doc.add_paragraph()
        r_ql = p_q.add_run("Examiner Question: ")
        r_ql.bold = True
        r_ql.font.size = Pt(10)
        r_ql.font.color.rgb = RGBColor(180, 40, 40)
        r_qt = p_q.add_run(f'"{q}"')
        r_qt.bold = True
        r_qt.font.size = Pt(10)
        p_q.paragraph_format.space_after = Pt(2)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.left_indent = Inches(0.2)
        r_al = p_a.add_run("Defensible Technical Answer: ")
        r_al.bold = True
        r_al.font.size = Pt(9.5)
        r_al.font.color.rgb = RGBColor(20, 120, 60)
        r_at = p_a.add_run(a)
        r_at.font.size = Pt(9.5)
        r_at.font.color.rgb = C_DARK
        p_a.paragraph_format.space_after = Pt(6)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

doc.save(docx_content_path)
print(f"Generated DOCX Slide-Wise Content: {docx_content_path}")

# ==============================================================================
# 3. Generate Word Document: TrustChain_AI_Final_Presentation_Notes.docx
# ==============================================================================
docx_notes_path = os.path.join(OUTPUT_DIR, "TrustChain_AI_Final_Presentation_Notes.docx")
doc_n = Document()

for section in doc_n.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

p_ntitle = doc_n.add_paragraph()
r_ntitle = p_ntitle.add_run("TrustChain-AI: Capstone Defense Spoken Script & Speaker Notes")
r_ntitle.bold = True
r_ntitle.font.size = Pt(22)
r_ntitle.font.color.rgb = C_NAVY
p_ntitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_nsub = doc_n.add_paragraph()
r_nsub = p_nsub.add_run("Slide-by-Slide Word-for-Word Speaking Script, Timing Allocations, and Transition Cues")
r_nsub.font.size = Pt(11)
r_nsub.font.color.rgb = C_BLUE
p_nsub.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc_n.add_paragraph().paragraph_format.space_after = Pt(10)

for slide in SLIDES_DATA:
    h1 = doc_n.add_heading(level=1)
    r_h1 = h1.add_run(f"Slide {slide['num']}: {slide['title']}")
    r_h1.font.size = Pt(15)
    r_h1.font.color.rgb = C_NAVY

    p_meta = doc_n.add_paragraph()
    r_meta1 = p_meta.add_run(f"Tracker: {slide['tracker']}  |  Estimated Time: 50–70s\n")
    r_meta1.font.size = Pt(9)
    r_meta1.bold = True
    r_meta1.font.color.rgb = C_CYAN
    r_meta2 = p_meta.add_run(f"Evidence Base: {slide['evidence']}")
    r_meta2.font.size = Pt(9)
    r_meta2.font.color.rgb = C_SLATE

    h2_scr = doc_n.add_heading(level=2)
    r_h2_scr = h2_scr.add_run("Spoken Word-for-Word Script:")
    r_h2_scr.font.size = Pt(12)
    r_h2_scr.font.color.rgb = C_BLUE

    p_scr = doc_n.add_paragraph()
    p_scr.paragraph_format.left_indent = Inches(0.2)
    r_s = p_scr.add_run(f'"{slide["script"]}"')
    r_s.italic = True
    r_s.font.size = Pt(10.5)
    r_s.font.color.rgb = C_NAVY

    h2_qa = doc_n.add_heading(level=2)
    r_h2_qa = h2_qa.add_run("Key Examiner Defense Q&A:")
    r_h2_qa.font.size = Pt(12)
    r_h2_qa.font.color.rgb = C_BLUE

    for q, a in slide["qa"]:
        p_qa = doc_n.add_paragraph()
        r_q = p_qa.add_run(f"Q: {q}\n")
        r_q.bold = True
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = RGBColor(180, 40, 40)
        r_a = p_qa.add_run(f"A: {a}")
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = C_DARK

    doc_n.add_paragraph().paragraph_format.space_after = Pt(10)

doc_n.save(docx_notes_path)
print(f"Generated DOCX Presentation Notes: {docx_notes_path}")
