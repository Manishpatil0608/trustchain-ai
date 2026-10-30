# -*- coding: utf-8 -*-
"""
upgraded_slides_1_to_6.py
Constructs upgraded Slides 1 to 6 with larger readable fonts, cleaner visual hierarchy,
embedded high-resolution architecture diagram, and comprehensive 6-part speaker notes.
"""

import os
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

from build_upgraded_presentation import (
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

    # Track Pill
    pill = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(4.5), Inches(0.4))
    pill.fill.solid()
    pill.fill.fore_color.rgb = COLOR_PANEL
    pill.line.color.rgb = COLOR_CYAN
    pill.line.width = Pt(1.2)
    ptf = pill.text_frame
    ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
    pp = ptf.paragraphs[0]
    pp.text = "B.TECH CAPSTONE DEFENSE · ACADEMIC YEAR 2026–2027"
    pp.font.name = FONT_MONO
    pp.font.size = Pt(9.5)
    pp.font.bold = True
    pp.font.color.rgb = COLOR_CYAN
    pp.alignment = PP_ALIGN.CENTER

    # Main Project Title
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.733), Inches(2.2))
    ttf = t_box.text_frame
    ttf.word_wrap = True
    ttf.margin_left = ttf.margin_top = ttf.margin_right = ttf.margin_bottom = 0
    p_title = ttf.paragraphs[0]
    p_title.text = "TrustChain-AI"
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    p_sub = ttf.add_paragraph()
    p_sub.text = "A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration"
    p_sub.font.name = FONT_TITLE
    p_sub.font.size = Pt(19)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CYAN
    p_sub.space_before = Pt(6)

    p_desc = ttf.add_paragraph()
    p_desc.text = "Department of Computer Engineering · Mukesh Patel School of Technology Management & Engineering (MPSTME)\nSVKM's NMIMS (Deemed-to-be University), Mumbai"
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(12)
    p_desc.font.color.rgb = COLOR_SLATE
    p_desc.space_before = Pt(8)

    # 3 Foundation Pillar Cards
    pillars = [
        ("01 · IDENTITY LAYER", "W3C did:key & Ed25519", "Decentralized cryptographic public-key identity generation without central CA dependency. W3C Verifiable Credentials with URDNA2015 LD-Proofs.", COLOR_CYAN),
        ("02 · TRUST INTELLIGENCE", "Continuous Temporal EMA", "Multi-factor runtime telemetry (Success: 60%, Compliance: 30%, Latency: 10%). Mathematical Exponential Moving Average with 4 discrete states.", COLOR_GREEN),
        ("03 · ZERO-TRUST CONTROL", "Adaptive Policy Gateway", "Operation-level privilege isolation (Standard vs Privileged). Explainable multi-factor candidate matching and modern React 19 SOC portal.", COLOR_PURPLE)
    ]
    for i, (tag, h, b, col) in enumerate(pillars):
        cx = Inches(0.8 + i * 4.0)
        c = add_card(slide1, cx, Inches(3.65), Inches(3.733), Inches(2.1), border_color=col)
        ctf = add_textbox(slide1, cx + Inches(0.25), Inches(3.8), Inches(3.233), Inches(1.8))
        add_para(ctf, tag, size=10, bold=True, color=col, mono=True)
        add_para(ctf, h, size=14, bold=True, color=COLOR_WHITE, space_before=4)
        add_para(ctf, b, size=11, color=COLOR_SLATE, space_before=5)

    # Presenters & Mentorship Card
    cred_card = add_card(slide1, Inches(0.8), Inches(5.95), Inches(11.733), Inches(1.05), fill_color=COLOR_PANEL_ALT)
    crtf = add_textbox(slide1, Inches(1.1), Inches(6.05), Inches(11.133), Inches(0.85))
    add_para(crtf, "PROJECT PRESENTERS & MENTORSHIP", size=9.5, bold=True, color=COLOR_CYAN, mono=True)
    add_para(crtf, "Submitted by: Candidate Presenters (B.Tech Computer Engineering)   |   Mentor & Guide: Project Mentorship Panel", size=11.5, bold=True, color=COLOR_WHITE, space_before=2)
    add_para(crtf, "Mukesh Patel School of Technology Management & Engineering (MPSTME), Mumbai   |   Final Capstone Defense 2026–2027", size=10.5, color=COLOR_SLATE, space_before=2)

    attach_notes(slide1, {
        'narrative': "Good morning respected members of the evaluation committee, project guide, and external examiner. We present TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration. In modern multi-agent systems, autonomous AI agents communicate, delegate sub-tasks, and execute sensitive tools without human intervention. However, current systems suffer from a fatal security vulnerability: point-in-time cryptographic authentication verifies who an agent is at session start, but cannot verify how reliably or securely it behaves during runtime. TrustChain-AI bridges this gap by unifying W3C decentralized identity with continuous mathematical trust scoring.",
        'takeaway': "TrustChain-AI establishes a complete, closed-loop zero-trust framework combining W3C did:key identity, runtime behavioral telemetry, temporal EMA trust scoring, and adaptive policy gating.",
        'evidence': "docs/blackbook/TrustChain_AI_Final_Blackbook.docx, akta/server.py, akta/did.py, akta/trust_engine.py",
        'transition': "Let us examine why traditional security architectures fail in autonomous multi-agent environments on Slide 2.",
        'qa': "Q1: Why is this project relevant today?\nA1: As LLM agents gain tool execution and autonomous delegation privileges, compromised or hallucinating agents can propagate errors across systems. Static API keys fail to stop degraded agents once authenticated.\n\nQ2: What is the primary novelty?\nA2: The integration of W3C decentralized identity with continuous temporal EMA trust evaluation and operation-level adaptive gating.",
        'caveat': "Institutional attributions follow approved SVKM's NMIMS MPSTME capstone project specifications."
    })

    # ==========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================================================
    slide2 = create_base_slide("RESEARCH MOTIVATION · THE PROBLEM", "The Point-in-Time Security Failure in Multi-Agent Systems", 2)
    
    # Left Column: Failure Modes
    c2_l = add_card(slide2, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Three Critical Failure Modes of Static Authentication")
    tf2_l = add_textbox(slide2, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf2_l, "1. The Binary Point-of-Entry Fallacy", size=13, bold=True, color=COLOR_AMBER)
    add_para(tf2_l, "Traditional access control treats authentication as a one-time gate: an agent presents a valid credential or API key at t=0 and receives persistent operational access. However, validity at connection time provides zero guarantee of runtime execution safety.", size=11, color=COLOR_SLATE, space_before=3)
    
    add_para(tf2_l, "2. Post-Authentication Behavioral Drift", size=13, bold=True, color=COLOR_AMBER, space_before=10)
    add_para(tf2_l, "Autonomous agents are prone to model hallucination, API timeout degradation, configuration tampering, and prompt injection subversion. Once past the initial authentication barrier, a degraded agent continues executing privileged workloads undetected.", size=11, color=COLOR_SLATE, space_before=3)
    
    add_para(tf2_l, "3. Cascading Compromise in Multi-Agent Workflows", size=13, bold=True, color=COLOR_AMBER, space_before=10)
    add_para(tf2_l, "In sequential and collaborative pipelines (Agent A -> Agent B -> Agent C), output from an unmonitored degraded agent is consumed as trusted input by subsequent nodes, compounding errors and undermining systemic integrity.", size=11, color=COLOR_SLATE, space_before=3)

    # Right Column: Paradigm Comparison
    c2_r = add_card(slide2, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Security Paradigm Shift: Static vs. Continuous Zero-Trust")
    tf2_r = add_textbox(slide2, Inches(7.133), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf2_r, "TRADITIONAL PARADIGM: BLIND RUNTIME TRUST", size=12, bold=True, color=COLOR_RED, mono=True)
    add_para(tf2_r, "[Static API Key] -> [Access Granted (t=0)] -> [Unchecked Execution] -> [Cascading Breach]", size=10.5, color=COLOR_WHITE, mono=True, space_before=4)
    add_para(tf2_r, "• Binary access: Agent is either 100% trusted or completely blocked.\n• No runtime behavioral monitoring or telemetry feedback loop.\n• Privileges persist even during catastrophic performance degradation.", size=10.5, color=COLOR_SLATE, space_before=4)
    
    add_para(tf2_r, "TRUSTCHAIN-AI PARADIGM: CONTINUOUS ZERO-TRUST", size=12, bold=True, color=COLOR_GREEN, mono=True, space_before=12)
    add_para(tf2_r, "[W3C did:key] -> [Sensor Telemetry] -> [EMA Trust Scoring] -> [Adaptive Gating] -> [Audit]", size=10.5, color=COLOR_CYAN, mono=True, space_before=4)
    add_para(tf2_r, "• Multi-factor evaluation: Success rate (S), compliance (C), latency (L).\n• Temporal smoothing prevents single-event volatility: T(t) = 0.7*T(t-1) + 0.3*P(t).\n• Automatic dynamic isolation: Quarantines degraded agents (T < 0.50).", size=10.5, color=COLOR_SLATE, space_before=4)

    attach_notes(slide2, {
        'narrative': "To understand why TrustChain-AI is necessary, we must examine how security is currently handled in multi-agent architectures. In existing systems, agents authenticate using an API key or cryptographic signature. Once verified, access is treated as binary and permanent. However, an autonomous agent can experience severe drift: hallucinations, SLA latency breaches, or prompt injection compromises. If Agent A degrades, downstream agents consuming its output are poisoned. TrustChain-AI replaces blind runtime trust with continuous mathematical zero-trust governance.",
        'takeaway': "Static authentication confirms cryptographic identity at session start; it cannot evaluate whether an agent remains safe, compliant, or reliable during runtime execution.",
        'evidence': "docs/blackbook/TrustChain_AI_Blackbook_Part1.md (Chapter 1), akta/adaptive_auth.py, tests/test_adaptive_policy.py",
        'transition': "Let us now examine the specific threat vectors and concrete security failure modes in Slide 3.",
        'qa': "Q1: Why can't we just use standard OAuth2 or API rate limiting?\nA1: OAuth2 validates authorization at issuance time; it has no visibility into whether model reasoning succeeded, whether security protocols were respected, or whether output quality degraded.\n\nQ2: How does TrustChain-AI know an agent has degraded?\nA2: Through normalized sensor telemetry events capturing execution success, compliance breaches, and response latency.",
        'caveat': "Workflow comparisons represent systemic architectural paradigms verified across multi-agent system literature."
    })

    # ==========================================================================
    # SLIDE 3: Threat Vectors & Security Failures
    # ==========================================================================
    slide3 = create_base_slide("FAILURE MODES · EMPIRICAL MOTIVATION", "Concrete Vulnerabilities & Threat Vectors in Autonomous Agent Networks", 3)
    
    threats = [
        ("1. RUNTIME DRIFT & HALLUCINATION", 
         "Stochastic Model Degradation: Output schemas mutate unexpectedly.\nPrompt Injection Subversion: Malicious prompts leak data.\nTrustChain Defense: Compliance factor C_i(t) drops to 0.0 upon schema breaches, triggering rapid quarantine.",
         Inches(0.8), Inches(1.65), Inches(5.65), Inches(2.45), COLOR_RED),
        ("2. SLA LATENCY & TIMEOUT BREACHES", 
         "Network Latency Spikes: Microservice stalls cause pipeline timeouts.\nSilent Hangs: Failing agents continue accepting tasks without delivery.\nTrustChain Defense: Latency factor L_i(t) enforces normalized SLA penalties against a 2000ms threshold ceiling.",
         Inches(6.883), Inches(1.65), Inches(5.65), Inches(2.45), COLOR_AMBER),
        ("3. CASCADING PIPELINE POISONING", 
         "Blast Radius Amplification: Node 1 failure propagates to Node 2.\nByzantine Deception: Degraded agent claims success with bad payload.\nTrustChain Defense: Sequential pipeline re-checks live trust at every node and halts immediately if an agent degrades.",
         Inches(0.8), Inches(4.35), Inches(5.65), Inches(2.55), COLOR_PURPLE),
        ("4. OVER-PRIVILEGED AGENT DELEGATION", 
         "Unchecked Delegation: Standard agents requesting state-altering tools.\nIdentity Replay: Stolen keys used to execute administrative pipelines.\nTrustChain Defense: Cryptographic Ed25519 signatures combined with ABAC: privileged actions strictly blocked in Suspicious/Quarantine.",
         Inches(6.883), Inches(4.35), Inches(5.65), Inches(2.55), COLOR_CYAN)
    ]

    for title, desc, x, y, w, h, col in threats:
        c = add_card(slide3, x, y, w, h, border_color=col)
        tf = add_textbox(slide3, x + Inches(0.25), y + Inches(0.18), w - Inches(0.5), h - Inches(0.35))
        add_para(tf, title, size=12.5, bold=True, color=col, mono=True)
        for line in desc.split("\n"):
            lead = line.split(":")[0] + ":" if ":" in line else "•"
            body = line.split(":", 1)[1] if ":" in line else line
            add_para(tf, f"{lead}{body}", size=10.5, color=COLOR_WHITE if "Defense" in lead else COLOR_SLATE, space_before=4)

    attach_notes(slide3, {
        'narrative': "Slide 3 categorizes the concrete threat vectors that compromise autonomous agent networks today. First is Runtime Drift and Hallucination: an agent may produce invalid schemas or leak sensitive data when exposed to indirect prompt injections. In TrustChain-AI, our compliance sensor immediately drops C(t) to zero upon policy violation. Second is SLA Latency Breaches: network stalls and hanging processes cascade through multi-agent pipelines; our latency sensor penalizes responses exceeding our 2000-millisecond SLA threshold. Third is Cascading Pipeline Poisoning: in sequential workflows, corrupted data from one node poisons downstream reasoning; our orchestrator verifies live trust before every node and halts execution upon anomaly detection. Fourth is Privilege Escalation: our adaptive access control strictly blocks privileged operations like workflow orchestration unless an agent maintains an active TRUSTED state.",
        'takeaway': "Unmonitored runtime execution creates cascading systemic vulnerabilities; TrustChain-AI provides continuous sensor telemetry and automatic quarantine.",
        'evidence': "akta/trust_engine.py, akta/collaboration_router.py, tests/test_collaboration.py",
        'transition': "Having identified these failure modes, let us review existing academic foundations on Slide 4.",
        'qa': "Q1: How do you detect an agent's failure if it doesn't crash?\nA1: Through multi-factor telemetry. An agent might return HTTP 200, but if its payload violates policy compliance C(t)=0.0 or breaches latency SLA L(t)=1.0, its performance score drops immediately.\n\nQ2: What is the threshold for a latency penalty?\nA2: A 2000ms SLA ceiling is enforced; any response taking >= 2000ms incurs the maximum latency penalty L=1.0.",
        'caveat': "Failure scenarios assume gateway sensors accurately intercept execution events."
    })

    # ==========================================================================
    # SLIDE 4: Literature Review & Research Gap
    # ==========================================================================
    slide4 = create_base_slide("ACADEMIC FOUNDATIONS · STATE OF THE ART", "Theoretical Foundations & Research Synthesis Across Four Domains", 4)
    
    # 4 Quadrants Matrix
    quads = [
        ("DOMAIN 1: SELF-SOVEREIGN IDENTITY", "W3C DID Core 1.0 & Verifiable Credentials (2021-2022)", 
         "• Strengths: Decentralized public-key identifiers (did:key) without central CA dependency.\n• Limitation: Credentials are static point-in-time attestations; zero visibility into runtime behavioral drift.\n• Relevance: TrustChain-AI adopts W3C did:key and URDNA2015 JSON-LD credentials as its identity baseline.",
         Inches(0.8), Inches(1.65), Inches(5.65), Inches(2.35), COLOR_CYAN),
        ("DOMAIN 2: DISTRIBUTED REPUTATION SYSTEMS", "EigenTrust (Kamvar 2003) & Beta Reputation (Jøsang 2002)", 
         "• Strengths: Peer ratings aggregation and historical reliability evaluation in distributed networks.\n• Limitation: Classic models ignore SLA execution latency, security compliance, and dynamic API access gating.\n• Relevance: TrustChain-AI integrates peer ratings into multi-factor matching, but prioritizes recent telemetry.",
         Inches(6.883), Inches(1.65), Inches(5.65), Inches(2.35), COLOR_GREEN),
        ("DOMAIN 3: ZERO TRUST ARCHITECTURES", "NIST SP 800-207 Zero Trust Architecture (2020)", 
         "• Strengths: 'Never trust, always verify' paradigm for network perimeters and continuous validation.\n• Limitation: Formulated for human enterprise users and network devices; lacks autonomous agent behavioral math.\n• Relevance: TrustChain-AI extends Zero Trust to autonomous AI agents via continuous mathematical trust scoring.",
         Inches(0.8), Inches(4.15), Inches(5.65), Inches(2.2), COLOR_AMBER),
        ("DOMAIN 4: MULTI-AGENT DIRECTORIES", "FIPA Agent Management Specification (SC00023J)", 
         "• Strengths: Standardized Directory Facilitator (DF) yellow-pages agent capability lookups.\n• Limitation: Static capability matching without runtime trust scoring, health verification, or explainability.\n• Relevance: TrustChain-AI replaces static directories with dynamic discovery and explainable candidate matching.",
         Inches(6.883), Inches(4.15), Inches(5.65), Inches(2.2), COLOR_PURPLE)
    ]

    for dom, cite, desc, x, y, w, h, col in quads:
        c = add_card(slide4, x, y, w, h, border_color=col)
        tf = add_textbox(slide4, x + Inches(0.2), y + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
        add_para(tf, dom, size=11, bold=True, color=col, mono=True)
        add_para(tf, cite, size=10, bold=True, color=COLOR_WHITE, space_before=2)
        for line in desc.split("\n"):
            add_para(tf, line, size=9.5, color=COLOR_SLATE, space_before=2)

    # Synthesis Banner Card
    syn_card = add_card(slide4, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.55), fill_color=COLOR_PANEL_ALT, border_color=COLOR_CYAN)
    stf = add_textbox(slide4, Inches(1.0), Inches(6.5), Inches(11.333), Inches(0.45))
    add_para(stf, "THE RESEARCH GAP: No prior system unifies W3C decentralized identity, continuous temporal EMA trust evaluation, quad-dimensional audit logging, and adaptive operation-level access control into a closed loop.", size=10.5, bold=True, color=COLOR_CYAN)

    attach_notes(slide4, {
        'narrative': "In Slide 4, we position TrustChain-AI across four established bodies of academic literature. First, in W3C Self-Sovereign Identity, standards like did:key and Verifiable Credentials provide decentralized identity, but credentials are fundamentally static snapshots. Second, in distributed reputation systems like Kamvar's EigenTrust and Jøsang's Beta Reputation, peer feedback is aggregated, but classic models ignore execution latency, schema compliance, and real-time operational gating. Third, in NIST's SP 800-207 Zero Trust Architecture, the principle of 'never trust, always verify' is established, but it lacks agent-specific behavioral formulations. Fourth, FIPA standards specify agent directories without trust-aware matching. The research gap is clear: no prior system unifies W3C decentralized identity with continuous mathematical trust scoring and operation-level adaptive gating. TrustChain-AI synthesizes these four pillars into a unified framework.",
        'takeaway': "TrustChain-AI bridges the gap between static W3C cryptographic identity and continuous runtime zero-trust behavioral governance.",
        'evidence': "docs/blackbook/REFERENCES.md (Citations [1]-[12]), W3C DID Core 1.0, NIST SP 800-207, Kamvar et al. (2003)",
        'transition': "Based on these foundations, Slide 5 details our formal research objectives and scope governance.",
        'qa': "Q1: How does your trust model differ from EigenTrust?\nA1: EigenTrust calculates global reputation via power-iteration on peer ratings in P2P file networks. TrustChain-AI evaluates multi-factor runtime sensor telemetry (success, compliance, latency) with temporal EMA smoothing and couples it directly to API authorization gates.\n\nQ2: What is the primary academic reference for Zero Trust?\nA2: NIST Special Publication 800-207 (2020), which establishes continuous verification requirements.",
        'caveat': "Literature survey covers peer-reviewed standards and papers through 2024–2026."
    })

    # ==========================================================================
    # SLIDE 5: Research Objectives & Scope Boundary
    # ==========================================================================
    slide5 = create_base_slide("PROJECT SPECIFICATION · BOUNDARIES", "Formal Engineering Objectives & Scope Governance", 5)
    
    # Left Column: 6 Implemented Objectives
    c5_l = add_card(slide5, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.25), "Six Core Technical Objectives (Implemented & Verified)")
    tf5_l = add_textbox(slide5, Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.5))
    
    objectives = [
        ("Obj 1 · Cryptographic Identity Genesis", "Implement W3C did:key decentralized identifiers using Ed25519 elliptic-curve keypairs with multicodec encoding (0xED01)."),
        ("Obj 2 · Verifiable Credential Operations", "Formulate W3C JSON-LD Verifiable Credentials with URDNA2015 canonicalization and Ed25519Signature2020 proof verification."),
        ("Obj 3 · Multi-Factor Telemetry Ingestion", "Capture runtime sensor events evaluating task success rate S_i(t), policy compliance C_i(t), and SLA latency penalty L_i(t)."),
        ("Obj 4 · Temporal EMA Trust Engine", "Develop mathematical Exponential Moving Average smoothing T_i(t) = 0.7*T_i(t-1) + 0.3*P_i(t) across 4 discrete states."),
        ("Obj 5 · Adaptive Policy Enforcement", "Dynamically gate PRIVILEGED operations (workflow execution, delegation) vs STANDARD operations across trust states."),
        ("Obj 6 · Trust-Aware Discovery & Matching", "Implement capability discovery and task-aware matching algorithm: MatchScore = 0.4T + 0.3(r/5) + 0.2*sigma + 0.1*(1-lambda).")
    ]
    for tag, desc in objectives:
        add_para(tf5_l, f"✓ {tag}", size=11, bold=True, color=COLOR_CYAN, space_before=3)
        add_para(tf5_l, f"   {desc}", size=10, color=COLOR_SLATE, space_before=1)

    # Right Column: Scope Boundaries
    c5_r = add_card(slide5, Inches(7.0), Inches(1.65), Inches(5.533), Inches(5.25), "Rigorous Scope Boundaries & Academic Honesty")
    tf5_r = add_textbox(slide5, Inches(7.25), Inches(2.2), Inches(5.033), Inches(4.5))
    
    add_para(tf5_r, "IMPLEMENTATION BOUNDARY DECLARATIONS", size=11.5, bold=True, color=COLOR_AMBER, mono=True)
    add_para(tf5_r, "In accordance with scientific integrity, TrustChain-AI explicitly defines its engineering boundaries:", size=10.5, color=COLOR_SLATE, space_before=3)
    
    boundaries = [
        ("1. Local Relational Storage (Non-Blockchain)", "The Verifiable Data Registry conforms to W3C VDR specifications via SQLite WAL mode for sub-5ms latency and zero gas fees, rather than a public blockchain."),
        ("2. Deterministic Agent Simulation", "Agent execution is evaluated using LocalAgentConnector for deterministic reproducibility, avoiding external LLM billing costs and stochastic jitter."),
        ("3. Sequential Pipeline Orchestration", "Workflows execute sequentially through ordered nodes. DAG parallel fork-join execution is modeled in schema but reserved for future work."),
        ("4. Closed-World Evaluation Scale", "Tested and validated with 8-10 registered agents; million-agent scale requires distributed DHT indexing.")
    ]
    for b_title, b_desc in boundaries:
        add_para(tf5_r, f"• {b_title}:", size=11, bold=True, color=COLOR_WHITE, space_before=6)
        add_para(tf5_r, f"  {b_desc}", size=10, color=COLOR_SLATE, space_before=1)

    attach_notes(slide5, {
        'narrative': "Slide 5 defines the formal boundaries of our capstone project. We defined six concrete engineering objectives, covering decentralized identity, verifiable credentials, telemetry ingestion, temporal trust mathematics, adaptive zero-trust gating, and multi-factor matching. Crucially, we maintain strict academic honesty: our implementation utilizes a local SQLite Verifiable Data Registry in WAL mode, not a global blockchain. Our agent connector provides deterministic structured execution for reproducible testing rather than invoking live commercial LLMs.",
        'takeaway': "Six verifiable technical objectives executed cleanly with realistic local performance guarantees and zero fabricated capabilities.",
        'evidence': "docs/blackbook/TrustChain_AI_Blackbook_Part1.md (Chapter 1.4), pytest.ini, tests/ (80 passing tests)",
        'transition': "Let us now examine the five-tier layered system architecture on Slide 6.",
        'qa': "Q1: Why did you choose SQLite over an external database or blockchain?\nA1: SQLite in WAL mode gives us atomic ACID compliance, sub-5ms latency, and zero deployment overhead, while perfectly conforming to the W3C VDR interface specification.\n\nQ2: How is agent simulation handled?\nA2: LocalAgentConnector simulates realistic response delays, parameterized payloads, and fault injections deterministically.",
        'caveat': "Scope boundaries are strictly aligned with Chapter 1.4 and Chapter 6 of the project blackbook."
    })

    # ==========================================================================
    # SLIDE 6: System Architecture & Layered Security Model
    # ==========================================================================
    slide6 = create_base_slide("SYSTEM DESIGN · FIVE-TIER MODEL", "Five-Tier Security Architecture & Request-Response Dataflow", 6)
    
    # Left Column: Description & Security Boundaries
    c6_l = add_card(slide6, Inches(0.8), Inches(1.65), Inches(5.2), Inches(5.25), "Layered Architectural Decomposition")
    tf6_l = add_textbox(slide6, Inches(1.05), Inches(2.2), Inches(4.7), Inches(4.5))
    
    tiers = [
        ("Tier 1 · Presentation Tier (Port 5173)", "React 19 + Vite frontend styled with Tailwind CSS SOC theme. Provides Dashboard, Agent Explorer, Discovery, Matching, and Admin views."),
        ("Tier 2 · API Gateway (Port 8050)", "FastAPI ASGI application enforcing CORS middleware, JWT authentication, Argon2id passwords, and security headers (nosniff, DENY)."),
        ("Tier 3 · Trust Intelligence Core", "In-process TrustEngine (EMA scoring), AdaptivePolicyEnforcer (RBAC/ABAC gating), and LocalAgentConnector simulation harness."),
        ("Tier 4 · Cryptographic Identity", "PyNaCl for 32-byte Ed25519 keypairs and did:key generation. PyLD for URDNA2015 JSON-LD credential canonicalization."),
        ("Tier 5 · Relational VDR Storage", "SQLite in WAL mode (PRAGMA synchronous=NORMAL) across 13 relational tables with sub-5ms read/write latency.")
    ]
    for t_name, t_desc in tiers:
        add_para(tf6_l, t_name, size=11.5, bold=True, color=COLOR_CYAN, space_before=4)
        add_para(tf6_l, t_desc, size=10, color=COLOR_SLATE, space_before=1)

    # Right Column: Embedded Architecture Diagram
    arch_img = os.path.join(assets_dir, "architecture_diagram.png")
    if os.path.exists(arch_img):
        slide6.shapes.add_picture(arch_img, Inches(6.2), Inches(1.65), Inches(6.333), Inches(5.25))
    else:
        c6_r = add_card(slide6, Inches(6.2), Inches(1.65), Inches(6.333), Inches(5.25), "5-Tier System Architecture Diagram")

    attach_notes(slide6, {
        'narrative': "Slide 6 details the complete five-tier system architecture. Tier 1 is our React 19 SOC operations interface, running on Vite at port 5173. Tier 2 is the FastAPI API Gateway at port 8050, enforcing security headers, request tracing, and human authentication. Tier 3 is the Trust Intelligence Tier, containing our TrustEngine, AdaptivePolicyEnforcer, and LocalAgentConnector. Tier 4 handles cryptographic identities, using PyNaCl for Ed25519 key generation and PyLD for URDNA2015 credential normalization. Finally, Tier 5 is our local Verifiable Data Registry, implemented in SQLite with Write-Ahead Logging for sub-5 millisecond response times.",
        'takeaway': "A modular 5-tier architecture separating presentation, API routing, trust evaluation, cryptography, and tamper-evident relational storage.",
        'evidence': "akta/server.py, akta/trust_engine.py, akta/adaptive_auth.py, akta/did.py, akta/vdr/models.py, frontend/src/App.jsx",
        'transition': "Let us now inspect Tier 4: the cryptographic identity and credential layer on Slide 7.",
        'qa': "Q1: How do the tiers communicate?\nA1: Tier 1 talks to Tier 2 via RESTful JSON APIs over HTTP. Tiers 2, 3, 4, and 5 run within the same high-performance Python ASGI backend process with clean module separation.\n\nQ2: What is the benefit of SQLite WAL mode in Tier 5?\nA2: WAL mode allows concurrent readers without blocking writers, achieving sub-5ms transaction speed.",
        'caveat': "Port 8050 for FastAPI backend and 5173 for Vite frontend reflect verified runtime configurations."
    })

    print("Upgraded Slides 1-6 built successfully.")
