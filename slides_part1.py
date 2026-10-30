import os
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

from build_full_deck import (
    COLOR_BG, COLOR_PANEL, COLOR_PANEL_ALT, COLOR_BORDER, COLOR_CYAN,
    COLOR_GREEN, COLOR_AMBER, COLOR_RED, COLOR_PURPLE, COLOR_WHITE,
    COLOR_SLATE, COLOR_MUTED, FONT_TITLE, FONT_BODY, FONT_MONO,
    create_base_slide, add_card, add_textbox, add_para, attach_notes
)

def build_slides_1_to_6(prs, assets_dir):
    # ==========================================================================
    # SLIDE 1: Title Slide
    # ==========================================================================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG
    bg1.line.fill.background()

    # Brand / Track Pill
    pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(4.2), Inches(0.36))
    pill.fill.solid()
    pill.fill.fore_color.rgb = COLOR_PANEL
    pill.line.color.rgb = COLOR_CYAN
    pill.line.width = Pt(1)
    ptf = pill.text_frame
    ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
    pp = ptf.paragraphs[0]
    pp.text = "B.TECH CAPSTONE DEFENSE · ACADEMIC YEAR 2026–2027"
    pp.font.name = FONT_MONO
    pp.font.size = Pt(8.5)
    pp.font.bold = True
    pp.font.color.rgb = COLOR_CYAN
    pp.alignment = PP_ALIGN.CENTER

    # Main Project Title
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(2.0))
    ttf = t_box.text_frame
    ttf.word_wrap = True
    ttf.margin_left = ttf.margin_top = ttf.margin_right = ttf.margin_bottom = 0
    p_title = ttf.paragraphs[0]
    p_title.text = "TrustChain-AI"
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    p_sub = ttf.add_paragraph()
    p_sub.text = "A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration"
    p_sub.font.name = FONT_TITLE
    p_sub.font.size = Pt(17)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CYAN
    p_sub.space_before = Pt(6)

    p_desc = ttf.add_paragraph()
    p_desc.text = "Department of Computer Engineering · Mukesh Patel School of Technology Management & Engineering (MPSTME)\nSVKM's NMIMS (Deemed-to-be University), Mumbai"
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(11.5)
    p_desc.font.color.rgb = COLOR_SLATE
    p_desc.space_before = Pt(8)

    # 3 Framework Foundation Cards
    pillars = [
        ("01 · IDENTITY LAYER", "W3C did:key & Ed25519", "Decentralized cryptographic public-key identity generation without central CA dependency. W3C Verifiable Credentials with LD-Proofs.", COLOR_CYAN),
        ("02 · TRUST INTELLIGENCE", "Continuous Temporal EMA", "Multi-factor sensor telemetry (Success, Compliance, Latency). Mathematical Exponential Moving Average with 4 discrete states.", COLOR_GREEN),
        ("03 · ZERO-TRUST CONTROL", "Adaptive Policy Gateway", "Operation-level privilege isolation (Privileged vs Standard). Transparent multi-factor agent matching and React 19 SOC portal.", COLOR_PURPLE)
    ]
    for i, (tag, h, b, col) in enumerate(pillars):
        cx = Inches(0.8 + i * 4.0)
        c = add_card(slide1, cx, Inches(3.6), Inches(3.733), Inches(2.0), border_color=col)
        ctf = add_textbox(slide1, cx + Inches(0.2), Inches(3.75), Inches(3.333), Inches(1.7))
        add_para(ctf, tag, size=9, bold=True, color=col, mono=True)
        add_para(ctf, h, size=13, bold=True, color=COLOR_WHITE, space_before=3)
        add_para(ctf, b, size=10, color=COLOR_SLATE, space_before=5)

    # Student & Mentor Footer Card
    cred_card = add_card(slide1, Inches(0.8), Inches(5.85), Inches(11.733), Inches(1.05), fill_color=COLOR_PANEL_ALT)
    crtf = add_textbox(slide1, Inches(1.1), Inches(5.95), Inches(11.133), Inches(0.85))
    add_para(crtf, "PROJECT PRESENTERS & MENTORSHIP", size=9, bold=True, color=COLOR_CYAN, mono=True)
    add_para(crtf, "Submitted by: [STUDENT NAME 1] (Roll No: [ROLL NUMBER 1])  &  [STUDENT NAME 2] (Roll No: [ROLL NUMBER 2])", size=11, bold=True, color=COLOR_WHITE, space_before=2)
    add_para(crtf, "Project Mentor: [MENTOR NAME]   |   B.Tech Final-Year Capstone Project   |   Session 2026–2027", size=10, color=COLOR_SLATE, space_before=2)

    attach_notes(slide1, {
        'narrative': "Good morning respected members of the panel, our project guide, and external examiner. We present TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration. In modern multi-agent systems, agents autonomously exchange data, execute code, and delegate tasks across boundaries. Our work addresses a critical vulnerability: point-in-time cryptographic authentication verifies who an agent is at session start, but cannot verify how reliably or securely it behaves during runtime. TrustChain-AI bridges this gap by unifying W3C decentralized identity with continuous mathematical trust scoring.",
        'takeaway': "TrustChain-AI establishes a complete, closed-loop zero-trust framework combining W3C did:key identity, runtime behavioral telemetry, temporal EMA trust scoring, and adaptive policy gating.",
        'evidence': "docs/blackbook/TrustChain_AI_Final_Blackbook.docx, akta/did.py, akta/trust_engine.py, akta/server.py",
        'qa': "Q1: Why is this project relevant today?\nA1: As LLM agents gain tool execution and autonomous delegation privileges, compromised or hallucinating agents can propagate errors across systems. Static API keys fail to stop degraded agents once authenticated.\n\nQ2: What is the primary novelty?\nA2: The integration of W3C decentralized identity with continuous temporal EMA trust evaluation and operation-level adaptive gating.",
        'caveat': "Student and mentor names are represented as configurable placeholders per project blackbook formatting."
    })

    # ==========================================================================
    # SLIDE 2: Problem Statement and Motivation
    # ==========================================================================
    slide2 = create_base_slide("RESEARCH MOTIVATION · THE PROBLEM", "The Point-in-Time Security Failure in Multi-Agent Systems", 2)
    
    # Left Column: Failure Modes
    c2_left = add_card(slide2, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Three Critical Failure Modes of Static Authentication")
    tf2_l = add_textbox(slide2, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf2_l, "1. The Binary Point-of-Entry Fallacy", size=12, bold=True, color=COLOR_AMBER)
    add_para(tf2_l, "Traditional access control treats authentication as a one-time gate: an agent presents a valid credential or API key at t=0 and receives persistent operational access. However, validity at connection time provides zero guarantee of runtime execution safety.", size=10.5, color=COLOR_SLATE, space_before=2)
    
    add_para(tf2_l, "2. Post-Authentication Behavioral Drift", size=12, bold=True, color=COLOR_AMBER, space_before=8)
    add_para(tf2_l, "Autonomous agents are prone to model hallucination, API timeout degradation, configuration tampering, and prompt injection subversion. Once past the initial authentication barrier, a degraded agent continues executing privileged workloads undetected.", size=10.5, color=COLOR_SLATE, space_before=2)
    
    add_para(tf2_l, "3. Cascading Compromise in Multi-Agent Workflows", size=12, bold=True, color=COLOR_AMBER, space_before=8)
    add_para(tf2_l, "In sequential and collaborative pipelines (Agent A -> Agent B -> Agent C), output from an unmonitored degraded agent is consumed as trusted input by subsequent nodes, compounding errors and undermining systemic integrity.", size=10.5, color=COLOR_SLATE, space_before=2)

    # Right Column: Paradigm Comparison
    c2_right = add_card(slide2, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Security Paradigm Shift: Static vs. Continuous Zero-Trust")
    tf2_r = add_textbox(slide2, Inches(7.133), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf2_r, "TRADITIONAL PARADIGM: BLIND RUNTIME TRUST", size=11, bold=True, color=COLOR_RED, mono=True)
    add_para(tf2_r, "[Static API Key / Token]  ──>  [Access Granted (t=0)]  ──>  [Unchecked Execution]  ──>  [Silent Failure / Breach]", size=10, color=COLOR_SLATE, mono=True, space_before=3)
    add_para(tf2_r, "• Binary access: Agent is either 100% trusted or completely blocked.\n• No runtime behavioral monitoring or telemetry feedback loop.\n• Privileges persist even during catastrophic performance degradation.", size=10, color=COLOR_SLATE, space_before=4)
    
    add_para(tf2_r, "TRUSTCHAIN-AI PARADIGM: CONTINUOUS ZERO-TRUST", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=10)
    add_para(tf2_r, "[W3C did:key] ──> [Sensor Telemetry] ──> [EMA Trust Scoring] ──> [Adaptive Gating] ──> [Audit Trail]", size=10, color=COLOR_CYAN, mono=True, space_before=3)
    add_para(tf2_r, "• Multi-factor evaluation: Success rate (S), compliance (C), latency (L).\n• Temporal smoothing prevents single-event volatility: T(t) = 0.7·T(t-1) + 0.3·P(t).\n• Automatic dynamic isolation: Quarantines degraded agents (T < 0.50).", size=10, color=COLOR_SLATE, space_before=4)

    attach_notes(slide2, {
        'narrative': "To understand why TrustChain-AI is necessary, we must examine how security is currently handled in multi-agent architectures. In existing systems, agents authenticate using an API key or cryptographic signature. Once verified, access is treated as binary and permanent. However, an autonomous agent can experience severe drift: hallucinations, SLA latency breaches, or prompt injection compromises. If Agent A degrades, downstream agents consuming its output are poisoned. TrustChain-AI replaces blind runtime trust with continuous mathematical zero-trust governance.",
        'takeaway': "Static authentication confirms cryptographic identity at session start; it cannot evaluate whether an agent remains safe, compliant, or reliable during runtime execution.",
        'evidence': "docs/blackbook/TrustChain_AI_Blackbook_Part1.md (Chapter 1), akta/adaptive_auth.py, tests/test_adaptive_policy.py",
        'qa': "Q1: Why can't we just use standard OAuth2 or API rate limiting?\nA1: OAuth2 validates authorization at issuance time; it has no visibility into whether model reasoning succeeded, whether security protocols were respected, or whether output quality degraded.\n\nQ2: How does TrustChain-AI know an agent has degraded?\nA2: Through normalized sensor telemetry events capturing execution success, compliance breaches, and response latency.",
        'caveat': "Workflow comparisons represent systemic architectural paradigms verified across multi-agent system literature."
    })

    # ==========================================================================
    # SLIDE 3: Project Objectives and Scope
    # ==========================================================================
    slide3 = create_base_slide("PROJECT SPECIFICATION · BOUNDARIES", "Formal Engineering Objectives & Scope Governance", 3)
    
    c3_l = add_card(slide3, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.25), "Six Core Technical Objectives (Implemented & Verified)")
    tf3_l = add_textbox(slide3, Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.5))
    
    objectives = [
        ("Obj 1 · Cryptographic Identity Genesis", "Implement W3C did:key decentralized identifiers using Ed25519 elliptic-curve keypairs with multicodec encoding (0xED01)."),
        ("Obj 2 · Verifiable Credential Operations", "Formulate W3C JSON-LD Verifiable Credentials with URDNA2015 canonicalization and Ed25519Signature2020 proof verification."),
        ("Obj 3 · Multi-Factor Telemetry Ingestion", "Capture runtime sensor events evaluating task success rate S(t), policy compliance C(t), and SLA latency penalty L(t)."),
        ("Obj 4 · Temporal EMA Trust Engine", "Develop mathematical Exponential Moving Average smoothing T(t) = 0.7·T(t-1) + 0.3·P(t) across 4 discrete states."),
        ("Obj 5 · Adaptive Policy Enforcement", "Dynamically gate PRIVILEGED operations (workflow execution, delegation) vs STANDARD operations across trust states."),
        ("Obj 6 · Trust-Aware Discovery & Matching", "Implement capability discovery and task-aware matching algorithm: MatchScore = 0.4T + 0.3(r/5) + 0.2σ + 0.1(1-λ).")
    ]
    for tag, desc in objectives:
        add_para(tf3_l, tag, size=11, bold=True, color=COLOR_WHITE, space_before=4)
        add_para(tf3_l, desc, size=10, color=COLOR_SLATE, space_before=1)

    c3_r = add_card(slide3, Inches(7.133), Inches(1.65), Inches(5.4), Inches(5.25), "Implementation Scope vs. Explicit Non-Claims")
    tf3_r = add_textbox(slide3, Inches(7.383), Inches(2.2), Inches(4.9), Inches(4.5))
    
    add_para(tf3_r, "IN-SCOPE IMPLEMENTED CAPABILITIES", size=11, bold=True, color=COLOR_GREEN, mono=True)
    add_para(tf3_r, "• FastAPI backend with 10 routers, Pydantic v2 validation, and CORS.\n• Local SQLite Verifiable Data Registry (WAL mode) with 13 tables.\n• React 19 SOC operations dashboard with dark/light theme support.\n• 80 passing automated unit/integration tests executed via pytest.\n• Deterministic LocalAgentConnector for structured capability execution.", size=10, color=COLOR_SLATE, space_before=3)
    
    add_para(tf3_r, "EXPLICIT NON-CLAIMS & BOUNDARIES", size=11, bold=True, color=COLOR_AMBER, mono=True, space_before=10)
    add_para(tf3_r, "• No Distributed Blockchain: Local relational SQLite VDR; distributed ledger anchoring is identified as future scope.\n• No Live Commercial LLMs: Default test harness uses deterministic synthetic responses; live LLM APIs are future work.\n• Sequential Workflows Verified: The database schema models parallel nodes, but execution tests strictly validate sequential pipelines.", size=10, color=COLOR_SLATE, space_before=3)

    attach_notes(slide3, {
        'narrative': "Slide 3 defines the formal boundaries of our capstone project. We defined six concrete engineering objectives, covering decentralized identity, verifiable credentials, telemetry ingestion, temporal trust mathematics, adaptive zero-trust gating, and multi-factor matching. Crucially, we maintain strict academic honesty: our implementation utilizes a local SQLite Verifiable Data Registry in WAL mode, not a global blockchain. Our agent connector provides deterministic structured execution for reproducible testing rather than invoking live commercial LLMs.",
        'takeaway': "All six core technical objectives are fully implemented and verified with 80 automated pytest tests, backed by transparent engineering scope boundaries.",
        'evidence': "pytest tests/ (80 passed in 19.10s), akta/vdr/database.py, akta/agent_connector.py, docs/blackbook/FINAL_QA_CHECKLIST.md",
        'qa': "Q1: Is TrustChain-AI running on Ethereum or Hyperledger?\nA1: No. In this prototype, the Verifiable Data Registry is implemented as a local relational SQLite database running in WAL mode with ACID guarantees. Distributed ledger anchoring is proposed future work.\n\nQ2: Does the framework use real AI models?\nA2: The core implementation includes LocalAgentConnector, which deterministically generates structured responses for research, coding, and analysis to allow rigorous, reproducible test execution.",
        'caveat': "Parallel workflow orchestration is modeled in the relational schema but empirically validated in sequential execution mode."
    })

    # ==========================================================================
    # SLIDE 4: Research Gap and Related Work
    # ==========================================================================
    slide4 = create_base_slide("LITERATURE CONTEXT · THEORETICAL GAPS", "Literature Survey & Research Gap Analysis", 4)
    
    # Summary Box
    sum_card = add_card(slide4, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.85), fill_color=COLOR_PANEL_ALT)
    stf = add_textbox(slide4, Inches(1.05), Inches(1.75), Inches(11.233), Inches(0.65))
    add_para(stf, "THEMATIC LITERATURE SYNTHESIS (15 VERIFIED CITATIONS)", size=9.5, bold=True, color=COLOR_CYAN, mono=True)
    add_para(stf, "Surveying peer-reviewed literature across Self-Sovereign Identity (W3C, RFC 8037), Distributed Trust (EigenTrust, Jøsang), Zero Trust Architecture (NIST SP 800-207), and Multi-Agent Systems (FIPA).", size=10.5, color=COLOR_WHITE, space_before=2)

    # 4 Thematic Domain Cards
    domains = [
        ("1. SSI & DECENTRALIZED IDENTITY", "W3C DID Core (2022) [1]\nW3C VC Model (2022) [2]\nRFC 8037 Ed25519 (2017) [8]", "STRENGTH:\nCryptographic decentralization; user-controlled verifiable claims.\n\nLIMITATION:\nHuman-centric; static credentials lack runtime behavioral coupling.\n\nTRUSTCHAIN-AI CONTRIBUTION:\nCouples did:key with continuous behavioral telemetry scoring.", COLOR_CYAN),
        ("2. DISTRIBUTED TRUST SYSTEMS", "Jøsang et al. (2007) [3]\nEigenTrust / Kamvar (2003) [4]\nMui et al. (2002) [5]", "STRENGTH:\nReputation aggregation in distributed P2P topologies.\n\nLIMITATION:\nAssumes static peer relationships; lacks capability & SLA matching.\n\nTRUSTCHAIN-AI CONTRIBUTION:\nIntegrates success, compliance, and SLA latency into EMA trust.", COLOR_GREEN),
        ("3. ZERO TRUST ARCHITECTURE", "NIST SP 800-207 (2020) [15]\nZhang et al. (2020) [11]\nBernabe et al. (2019) [10]", "STRENGTH:\nContinuous verification; elimination of implicit network trust.\n\nLIMITATION:\nFocused on network microsegmentation, not agent reasoning.\n\nTRUSTCHAIN-AI CONTRIBUTION:\nOperationalizes ZTA for autonomous agent collaboration pipelines.", COLOR_AMBER),
        ("4. MULTI-AGENT COORDINATION", "FIPA Agent Mgmt (2004) [12]\nShoker (2017) [13]\nNitti et al. (2014) [6]", "STRENGTH:\nAgent Directory Facilitator (DF) capability registry.\n\nLIMITATION:\nNo runtime behavioral gating, quarantine, or revocation.\n\nTRUSTCHAIN-AI CONTRIBUTION:\nAdaptive gating separating Privileged vs Standard operations.", COLOR_PURPLE)
    ]
    for i, (dom, refs, body, col) in enumerate(domains):
        dx = Inches(0.8 + i * 3.0)
        c = add_card(slide4, dx, Inches(2.65), Inches(2.8), Inches(4.25), border_color=col)
        dtf = add_textbox(slide4, dx + Inches(0.18), Inches(2.78), Inches(2.44), Inches(3.95))
        add_para(dtf, dom, size=9, bold=True, color=col, mono=True)
        add_para(dtf, refs, size=8.5, color=COLOR_WHITE, space_before=3, mono=True)
        add_para(dtf, body, size=9, color=COLOR_SLATE, space_before=6)

    attach_notes(slide4, {
        'narrative': "In Slide 4, we position TrustChain-AI within the academic literature across four key domains. First, in Self-Sovereign Identity, the W3C standards establish verifiable identifiers, but credentials remain static. Second, in distributed trust systems, classic models like EigenTrust aggregate peer feedback in file-sharing networks, but ignore task latency and policy compliance. Third, NIST's Zero Trust Architecture articulates the need for continuous verification, but addresses network endpoints rather than autonomous agents. Fourth, FIPA standards provide agent directory lookups without behavioral trust gating. TrustChain-AI synthesizes these four pillars into a unified framework.",
        'takeaway': "TrustChain-AI addresses the identified gap where decentralized identity standards lack runtime behavioral verification, and trust algorithms lack operation-level privilege gating.",
        'evidence': "docs/blackbook/REFERENCES.md, NIST SP 800-207, W3C DID Core Recommendation 2022",
        'qa': "Q1: How does your trust model differ from EigenTrust?\nA1: EigenTrust computes global peer reputation via matrix iteration in P2P file networks. TrustChain-AI uses local temporal Exponential Moving Average tracking three explicit runtime metrics (success, compliance, latency) with hard zero-trust isolation boundaries.\n\nQ2: Did you invent the DID standard?\nA2: No. We strictly adopt the official W3C did:key v1.0 standard using Ed25519 cryptographic curves as the identity foundation.",
        'caveat': "Literature comparison focuses on architectural integration rather than empirical throughput benchmarking against external legacy repositories."
    })

    # ==========================================================================
    # SLIDE 5: Proposed Solution and Core Contributions
    # ==========================================================================
    slide5 = create_base_slide("SOLUTION OVERVIEW · NOVEL SYNTHESIS", "TrustChain-AI Architectural Paradigm & System Contributions", 5)
    
    # Left Column: The 7 Pillars
    c5_l = add_card(slide5, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.25), "The Seven Integrated Architectural Pillars")
    tf5_l = add_textbox(slide5, Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.5))
    
    pillars7 = [
        ("1. Identity Genesis", "Ed25519 keypair generation multicodec prefixed (0xED01) to form W3C did:key."),
        ("2. Verifiable Credentials", "JSON-LD credential issuance with URDNA2015 canonicalization & LD-proofs."),
        ("3. Runtime Telemetry Ingestion", "Event sensors capturing success, compliance breaches, and latency in milliseconds."),
        ("4. Trust Intelligence Core", "Mathematical sliding-window scoring Pi(t) coupled with temporal EMA smoothing Ti(t)."),
        ("5. Adaptive Policy Gateway", "Operation-level privilege isolation across TRUSTED, SUSPICIOUS, QUARANTINED, REVOKED."),
        ("6. Trust-Aware Discovery & Matching", "Multi-factor candidate ranking: MatchScore = 0.4T + 0.3(r/5) + 0.2σ + 0.1(1-λ)."),
        ("7. Quad-Dimensional Audit Trail", "Tamper-evident logs across user sessions, state changes, telemetry, and collaborations.")
    ]
    for tag, desc in pillars7:
        add_para(tf5_l, f"• {tag}:", size=10, bold=True, color=COLOR_WHITE, space_before=3)
        add_para(tf5_l, f"  {desc}", size=9.5, color=COLOR_SLATE, space_before=1)

    # Right Column: Principal Engineering Contributions
    c5_r = add_card(slide5, Inches(7.133), Inches(1.65), Inches(5.4), Inches(5.25), "Three Principal Engineering Contributions")
    tf5_r = add_textbox(slide5, Inches(7.383), Inches(2.2), Inches(4.9), Inches(4.5))
    
    add_para(tf5_r, "CONTRIBUTION 1: SSI + DYNAMIC TRUST SYNTHESIS", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf5_r, "Proves that decentralized cryptographic identity can be successfully coupled with dynamic behavioral telemetry to govern autonomous AI agents without relying on centralized identity providers.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf5_r, "CONTRIBUTION 2: ADAPTIVE ZERO-TRUST POLICY GATING", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf5_r, "Establishes a dual-layer access model: human role-based access control (ADMIN, OPERATOR, VIEWER) combined with autonomous agent runtime trust states that dynamically quarantine degraded agents.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf5_r, "CONTRIBUTION 3: EXPLAINABLE MULTI-FACTOR MATCHING", size=11, bold=True, color=COLOR_PURPLE, mono=True, space_before=8)
    add_para(tf5_r, "Formulates a transparent, verifiable candidate ranking equation balancing trust, historical reputation, task success, and latency, backed by a responsive React 19 SOC operations interface.", size=10, color=COLOR_SLATE, space_before=2)

    attach_notes(slide5, {
        'narrative': "Slide 5 presents the complete TrustChain-AI solution and our primary engineering contributions. Rather than claiming to have invented DIDs, Verifiable Credentials, or trust scoring in isolation, our fundamental contribution is the cohesive system integration. We engineered a closed-loop framework where an agent generates a cryptographic did:key, acquires Verifiable Credentials, executes tasks that stream sensor telemetry, updates its temporal trust score, and is subject to adaptive policy gating. If an agent misbehaves, it is automatically quarantined without requiring human intervention.",
        'takeaway': "The contribution of TrustChain-AI lies in the cohesive system integration of SSI identity, runtime telemetry, EMA trust mathematics, and adaptive zero-trust authorization.",
        'evidence': "docs/blackbook/TrustChain_AI_Blackbook_Part1.md (Chapter 3), akta/server.py, akta/trust_engine.py",
        'qa': "Q1: What prevents an agent from faking its telemetry?\nA1: In this prototype, telemetry is recorded by the execution harness/gateway, not self-reported by the agent. Securing decentralized telemetry reporting against gateway collusion is identified as a critical future research direction.\n\nQ2: What is the main benefit of the matching algorithm?\nA2: It ensures that an agent with high historical reputation but currently degraded live trust score cannot be selected for sensitive tasks.",
        'caveat': "The contribution is an architectural and engineering synthesis evaluated through automated integration test suites."
    })

    # ==========================================================================
    # SLIDE 6: Overall System Architecture
    # ==========================================================================
    slide6 = create_base_slide("ARCHITECTURE & DESIGN · SYSTEM STACK", "Five-Tier System Architecture & Operational Topology", 6)
    
    tiers = [
        ("TIER 1 · PRESENTATION TIER (PORT 5173)", "React 19 · Vite · Tailwind CSS · Recharts · Lucide Icons", "• SOC Security Dashboard: Fleet trust distribution, live health probes, telemetry volume visualizers.\n• Agent Explorer & Investigation Drawer: Real-time risk posture visualizers, deep audit transition inspections.\n• Capability Discovery Center: Multi-filter capability search, trust threshold slider, diagnostic eligibility rationales.\n• Task-Driven Matching Center: Workload prompt input, Top Match spotlight card, transparent score breakdown.", COLOR_CYAN),
        ("TIER 2 · API GATEWAY TIER (PORT 8050)", "FastAPI · Uvicorn ASGI · Pydantic v2 · JWT (HS256) · Argon2id", "• Security Headers Middleware: X-Request-ID tracing, nosniff, DENY clickjacking, strict referrer policies.\n• Dual Authentication Gate: Human session JWT tokens (Argon2id hashing) & Agent Bearer token verification.\n• RESTful Router Modules: /auth, /vdr (credentials), /trust (telemetry & state), /registry (discovery & matching).", COLOR_GREEN),
        ("TIER 3 · TRUST INTELLIGENCE TIER", "TrustEngine · AdaptivePolicyEnforcer · LocalAgentConnector", "• Trust Engine Core: Sliding-window evaluation (S, C, L), instantaneous score P(t), temporal EMA smoothing T(t).\n• Adaptive Policy Gateway: Operation-level authorization gating (Privileged vs Standard) across 4 trust states.\n• Local Agent Connector: Deterministic structured response engine & outbound HTTP POST collaboration bridge.", COLOR_AMBER),
        ("TIER 4 · IDENTITY & CREDENTIALS", "W3C did:key · PyNaCl Ed25519 · PyLD URDNA2015 · Base58", "• DID Generator: Ed25519 32-byte key generation, 0xED01 multicodec prefixing, base58 multibase encoding.\n• Verifiable Credentials: W3C JSON-LD credential issuance, URDNA2015 dataset normalization, Ed25519 proofs.", COLOR_PURPLE),
        ("TIER 5 · PERSISTENCE & VDR TIER", "SQLite 3 (WAL Mode) · SQLAlchemy 2.0 ORM · Relational VDR", "• Relational Verifiable Data Registry: 13 normalized tables storing credentials, trust states, telemetry, and audits.\n• ACID Guarantee & Concurrency: Write-Ahead Logging (WAL) mode supporting concurrent readers and sub-5ms probes.", COLOR_SLATE)
    ]
    for i, (tag, h, body, col) in enumerate(tiers):
        ty = Inches(1.65 + i * 1.05)
        c = add_card(slide6, Inches(0.8), ty, Inches(11.733), Inches(0.96), border_color=col)
        ttf = add_textbox(slide6, Inches(1.05), ty + Inches(0.08), Inches(11.233), Inches(0.82))
        add_para(ttf, f"{tag}   |   {h}", size=10, bold=True, color=col, mono=True)
        add_para(ttf, body, size=8.5, color=COLOR_WHITE, space_before=2)

    attach_notes(slide6, {
        'narrative': "Slide 6 details the complete five-tier system architecture. Tier 1 is our React 19 SOC operations interface, running on Vite at port 5173. Tier 2 is the FastAPI API Gateway at port 8050, enforcing security headers, request tracing, and human authentication. Tier 3 is the Trust Intelligence Tier, containing our TrustEngine, AdaptivePolicyEnforcer, and LocalAgentConnector. Tier 4 handles cryptographic identities, using PyNaCl for Ed25519 key generation and PyLD for URDNA2015 credential normalization. Finally, Tier 5 is our local Verifiable Data Registry, implemented in SQLite with Write-Ahead Logging for sub-5 millisecond response times.",
        'takeaway': "The architecture cleanly decouples presentation, API routing, mathematical trust evaluation, cryptographic identity generation, and ACID persistence.",
        'evidence': "akta/server.py, akta/config.py, akta/vdr/database.py, frontend/src/App.jsx, docs/blackbook/diagrams/01_system_architecture.svg",
        'qa': "Q1: How do the frontend and backend communicate?\nA1: Via an Axios client communicating over HTTP REST with JWT Bearer tokens and JSON payloads, configured with CORS protection and X-Request-ID headers.\n\nQ2: Where is the security boundary enforced?\nA2: At two levels: Tier 2 validates human session JWTs and route permissions; Tier 3 validates cryptographic DID signatures and evaluates runtime trust states before permitting operations.",
        'caveat': "The persistence layer is an authoritative local SQLite VDR operating in WAL mode, not a distributed blockchain."
    })

    print("Slides 1-6 built successfully.")
