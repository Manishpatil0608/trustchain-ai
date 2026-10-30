# -*- coding: utf-8 -*-
"""
upgraded_slides_7_to_12.py
Constructs upgraded Slides 7 to 12 with larger readable fonts, cleaner visual hierarchy,
embedded high-resolution diagram and chart assets, and comprehensive 6-part speaker notes.
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

def build_slides_7_to_12(prs, assets_dir):
    # ==========================================================================
    # SLIDE 7: DID, Cryptographic Identity, and Verifiable Credentials
    # ==========================================================================
    slide7 = create_base_slide("IDENTITY LAYER · W3C SPECIFICATIONS", "Cryptographic Agent Identity & Verifiable Credentials Lifecycle", 7)
    
    # Left Column: Algorithmic Architecture
    c7_l = add_card(slide7, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.25), "W3C did:key Decentralized Architecture")
    tf7_l = add_textbox(slide7, Inches(1.05), Inches(2.2), Inches(4.8), Inches(4.5))
    
    add_para(tf7_l, "1. Algorithmic Identity Construction", size=12, bold=True, color=COLOR_CYAN)
    add_para(tf7_l, "• Raw Keypair: Generates 32-byte Ed25519 seed & public key via libsodium (PyNaCl library).\n• Multicodec Prefix: Prepends 2-byte varint 0xED01 indicating Ed25519 public key.\n• Base58 Encoding: Encodes prefixed bytes with Bitcoin base58 alphabet, prefixed with 'z'.\n• Formal Format: did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRo...", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf7_l, "2. Self-Sovereign Decentralization", size=12, bold=True, color=COLOR_CYAN, space_before=8)
    add_para(tf7_l, "• No Central Authority: Identifiers are generated algorithmically without requiring DNS registration, central certificate authorities, or registration fees.\n• Deterministic Resolution: Any node in the network resolves public key directly from the DID string itself without querying an external registry.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf7_l, "3. Identity vs. Trust Boundary Axiom", size=12, bold=True, color=COLOR_AMBER, space_before=8)
    add_para(tf7_l, "Possessing a valid cryptographic did:key proves private key ownership; it provides ZERO guarantee of runtime correctness, safety, or compliance.", size=10, color=COLOR_WHITE, space_before=2)

    # Right Column: Embedded Lifecycle Diagram
    diag7_img = os.path.join(assets_dir, "did_vc_lifecycle.png")
    if os.path.exists(diag7_img):
        slide7.shapes.add_picture(diag7_img, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25))
    else:
        c7_r = add_card(slide7, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25), "DID & VC Lifecycle Diagram")

    attach_notes(slide7, {
        'narrative': "Slide 7 presents the identity and credential layer. Every agent generates an Ed25519 keypair using PyNaCl. The 32-byte public key is prefixed with the multicodec byte sequence 0xED01 and encoded in base58-btc to produce a deterministic W3C did:key identifier. This provides self-sovereign identity without a centralized CA. For verifiable claims, such as authorized capabilities, we issue W3C Verifiable Credentials. Because JSON keys can change order, we apply the URDNA2015 canonicalization algorithm using PyLD before hashing with SHA-256 and signing with Ed25519. Crucially, we emphasize that possessing a valid DID proves identity ownership, but does not prove operational trustworthiness.",
        'takeaway': "Algorithmic W3C did:key identity eliminates central CA dependency, while URDNA2015 canonicalization prevents JSON signature forgery.",
        'evidence': "akta/did.py (generate_did_key, verify_did_key), akta/vc.py (issue_verifiable_credential, canonicalize_credential), tests/test_crypto.py, tests/test_vc.py",
        'transition': "Let us now examine how runtime telemetry is ingested and converted into trust metrics on Slide 8.",
        'qa': "Q1: What happens if an agent's private key is compromised?\nA1: The administrator invokes the administrative revocation endpoint (/api/v1/registry/revoke), which marks the agent as REVOKED in stored_vcs and agent_trust_states, permanently blocking it from the network.\n\nQ2: Why URDNA2015 instead of standard JSON sorting?\nA2: URDNA2015 standardizes RDF graph structures into N-Quads, handling blank node labeling that lexical sorting cannot normalize.",
        'caveat': "did:key format strictly adheres to the W3C DID Core 1.0 Candidate Recommendation."
    })

    # ==========================================================================
    # SLIDE 8: Dynamic Trust Engine: Mathematical Formulation & Telemetry
    # ==========================================================================
    slide8 = create_base_slide("TRUST ENGINE · MATHEMATICAL FORMULATION", "Behavioral Telemetry Processing & Temporal EMA Trust Formulation", 8)
    
    # Left Column: Mathematical Formulation
    c8_l = add_card(slide8, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.25), "Mathematical Formulations & Sensor Weights")
    tf8_l = add_textbox(slide8, Inches(1.05), Inches(2.2), Inches(4.8), Inches(4.5))
    
    add_para(tf8_l, "1. INSTANTANEOUS PERFORMANCE EQUATION", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf8_l, "P_i(t) = 0.6 · S_i(t) + 0.3 · C_i(t) + 0.1 · (1 - L_i(t))", size=12.5, bold=True, color=COLOR_WHITE, mono=True, space_before=2)
    add_para(tf8_l, "• S_i(t) ∈ [0.0, 1.0]: Functional correctness and task success rate.\n• C_i(t) ∈ [0.0, 1.0]: Policy compliance (schema validity, zero prompt leaks).\n• L_i(t) = min(latency_ms / 2000, 1.0): Latency penalty against 2000ms SLA ceiling.\n• Weighting Rationale: Correctness (0.6) and Safety (0.3) are critical enterprise invariants; Latency (0.1) provides marginal optimization.", size=9.5, color=COLOR_SLATE, space_before=3)
    
    add_para(tf8_l, "2. TEMPORAL EMA TRUST EQUATION", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf8_l, "T_i(t) = 0.7 · T_i(t-1) + 0.3 · P_i(t)    [Initial Prior T_0 = 1.00]", size=12.5, bold=True, color=COLOR_CYAN, mono=True, space_before=2)
    add_para(tf8_l, "• α = 0.7: Historical memory retention parameter.\n• β = 0.3: Instantaneous performance responsiveness parameter.\n• Prevents single-event volatility while guaranteeing rapid quarantine in 2 consecutive complete failures.", size=9.5, color=COLOR_SLATE, space_before=3)

    # Right Column: Embedded Pipeline Diagram
    diag8_img = os.path.join(assets_dir, "telemetry_pipeline.png")
    if os.path.exists(diag8_img):
        slide8.shapes.add_picture(diag8_img, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25))
    else:
        c8_r = add_card(slide8, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25), "Telemetry Pipeline Flow")

    attach_notes(slide8, {
        'narrative': "Slide 8 details how runtime behavior is translated into mathematical metrics. When an agent executes a task, the gateway captures a TelemetryEvent containing success, compliance, and response latency. Across a sliding window of the last 10 observations, we compute three normalized factors: S_i for success rate, C_i for policy compliance, and L_i for latency penalty benchmarked against a 2000-millisecond SLA threshold. We then formulate the instantaneous performance score P_i(t) as a weighted linear combination: 0.6 for success, 0.3 for compliance, and 0.1 for latency efficiency. These weights reflect security priorities: correctness is primary, protocol safety is vital, and performance speed provides marginal optimization.",
        'takeaway': "Trust is modeled as a continuous mathematical metric combining success (0.6), compliance (0.3), and latency (0.1) smoothed via 0.7/0.3 EMA.",
        'evidence': "akta/trust_engine.py (TrustEngine, compute_instantaneous_performance, update_trust_score), tests/test_trust_engine.py",
        'transition': "Let us observe this mathematical formula in action across a 10-round empirical stress test on Slide 9.",
        'qa': "Q1: Why is latency weighted at only 0.1 while success is 0.6?\nA1: In enterprise multi-agent systems, functional correctness and security compliance are critical invariants. A slow but correct response is vastly preferable to an instantaneous hallucination or breach.\n\nQ2: What happens if an agent submits no tasks for an hour?\nA2: Trust score remains stable at its last evaluated state until new telemetry is received or an administrative heartbeat decay is applied.",
        'caveat': "Sliding window size is configured to 10 observations with max latency SLA clamp at 2000ms."
    })

    # ==========================================================================
    # SLIDE 9: Mathematical Trajectory Dynamics: Degradation & Recovery Timeline
    # ==========================================================================
    slide9 = create_base_slide("CALCULATED SCENARIO · 10-ROUND TRUST TIMELINE", "Mathematical Trajectory Dynamics: Degradation & Recovery", 9)
    
    # Left Column: Step-by-Step Data Card
    c9_l = add_card(slide9, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.25), "10-Round Illustrative Scenario Calculations (T_0 = 1.000)")
    tf9_l = add_textbox(slide9, Inches(1.05), Inches(2.2), Inches(4.8), Inches(4.5))
    
    rounds_data = [
        ("R0: Baseline Prior", "T_0 = 1.000", "State: TRUSTED", COLOR_GREEN),
        ("R1: Flawless Task (P=0.994)", "T_1 = 0.7(1.000) + 0.3(0.994) = 0.998", "State: TRUSTED", COLOR_GREEN),
        ("R2: Normal Execution (P=0.988)", "T_2 = 0.7(0.998) + 0.3(0.988) = 0.995", "State: TRUSTED", COLOR_GREEN),
        ("R3: Latency Spike (P=0.460)", "T_3 = 0.7(0.995) + 0.3(0.460) = 0.835", "State: TRUSTED", COLOR_GREEN),
        ("R4: Complete Failure (P=0.000)", "T_4 = 0.7(0.835) + 0.3(0.000) = 0.584", "State: SUSPICIOUS", COLOR_AMBER),
        ("R5: Repeated Failure (P=0.000)", "T_5 = 0.7(0.584) + 0.3(0.000) = 0.409", "State: QUARANTINED (T<0.50)", COLOR_RED),
        ("R6: Supervised Canary 1 (P=0.991)", "T_6 = 0.7(0.409) + 0.3(0.991) = 0.584", "State: SUSPICIOUS", COLOR_AMBER),
        ("R7: Supervised Canary 2 (P=0.992)", "T_7 = 0.7(0.584) + 0.3(0.992) = 0.706", "State: SUSPICIOUS", COLOR_AMBER),
        ("R8: Supervised Canary 3 (P=0.993)", "T_8 = 0.7(0.706) + 0.3(0.993) = 0.792", "State: SUSPICIOUS", COLOR_AMBER),
        ("R9: Supervised Canary 4 (P=0.993)", "T_9 = 0.7(0.792) + 0.3(0.993) = 0.852", "State: TRUSTED (T>=0.80)", COLOR_GREEN),
        ("R10: Restored Ops (P=0.994)", "T_10 = 0.7(0.852) + 0.3(0.994) = 0.895", "State: TRUSTED", COLOR_GREEN),
    ]
    for r_title, r_math, r_st, r_col in rounds_data:
        add_para(tf9_l, f"{r_title}: {r_math}  [{r_st}]", size=8.5, color=r_col, space_before=1)

    add_para(tf9_l, "CALCULATED ILLUSTRATIVE SCENARIO — NOT MEASURED PRODUCTION DATA:", size=9.5, bold=True, color=COLOR_CYAN, space_before=5)
    add_para(tf9_l, "• Rapid Quarantine: Isolated in exactly TWO complete failures (T_5 = 0.409 < 0.50).\n• Inertial Recovery: Requires FOUR supervised canary rounds (P>0.99) to restore Trusted state (T_9 = 0.852 >= 0.80).", size=9, color=COLOR_SLATE, space_before=2)

    # Right Column: Embedded Chart
    chart_img = os.path.join(assets_dir, "trust_timeline.png")
    if os.path.exists(chart_img):
        slide9.shapes.add_picture(chart_img, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25))
    else:
        c9_r = add_card(slide9, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25), "Trust Timeline Chart")

    attach_notes(slide9, {
        'narrative': "Slide 9 presents our temporal trust algorithm and state machine dynamics using an illustrative worked scenario. To prevent single transient errors from abruptly knocking agents offline, we apply an Exponential Moving Average: T_i(t) equals 0.7 times previous trust plus 0.3 times current performance. Newly registered agents start with an initial baseline score of 1.0. As shown in the chart on the right, if an agent experiences degradation, its trust decays smoothly across our discrete states: TRUSTED at or above 0.8, SUSPICIOUS between 0.5 and 0.8, and QUARANTINED below 0.5. Notice that an agent can recover from Quarantine if supervised canary telemetry proves restored reliability. However, REVOKED is an administrative terminal state that can never recover via telemetry.",
        'takeaway': "Mathematical trajectory analysis proves that EMA smoothing prevents transient oscillations while guaranteeing rapid quarantine isolation within 2 consecutive complete failure rounds.",
        'evidence': "docs/presentation/TrustChain_AI_Slide_Assets/trust_timeline.png, akta/trust_engine.py, tests/test_trust_engine.py",
        'transition': "Let us see how these discrete trust states directly drive runtime authorization on Slide 10.",
        'qa': "Q1: Can a quarantined agent recover on its own?\nA1: An agent under quarantine is blocked from unsupervised execution. It can only recover if an operator or automated supervisor submits verified recovery telemetry showing successful remediation.\n\nQ2: What is the exact formula for Round 5?\nA2: T_5 = 0.7 * 0.584 + 0.3 * 0.000 = 0.4088 ~ 0.409, crossing the 0.50 threshold into Quarantine.",
        'caveat': "Rounds represent sequential telemetry update epochs evaluated in test_trust_engine.py."
    })

    # ==========================================================================
    # SLIDE 10: Adaptive Authorization & Zero-Trust Access Control
    # ==========================================================================
    slide10 = create_base_slide("ACCESS CONTROL · ZERO-TRUST ENFORCEMENT", "Defense-in-Depth: Human RBAC & Autonomous Agent ABAC", 10)
    
    # Left Column: Human RBAC & Security
    c10_l = add_card(slide10, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.25), "Human RBAC & Defense-in-Depth Security")
    tf10_l = add_textbox(slide10, Inches(1.05), Inches(2.2), Inches(4.8), Inches(4.5))
    
    add_para(tf10_l, "1. Argon2id Password Hashing", size=12, bold=True, color=COLOR_CYAN)
    add_para(tf10_l, "• Memory-Hard Algorithm: Combines Argon2d (GPU/ASIC resistance) and Argon2i (side-channel resistance). OWASP recommended.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf10_l, "2. Five-Strike Account Lockout Policy", size=12, bold=True, color=COLOR_CYAN, space_before=8)
    add_para(tf10_l, "• 5 consecutive incorrect passwords trigger an automatic 15-minute lockout (HTTP 423 Locked), mitigating CPU exhaustion brute-forcing.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf10_l, "3. Human Role Hierarchy (Portal Operators)", size=12, bold=True, color=COLOR_PURPLE, space_before=8)
    add_para(tf10_l, "• ADMIN: Full mutations, user management, manual trust adjustments.\n• OPERATOR: Workflow execution, discovery search, task matching.\n• VIEWER: Complete read-only observability; mutation controls disabled.\n• Frontend badges are UI conveniences; FastAPI backend is SOLE boundary.", size=9.5, color=COLOR_WHITE, space_before=2)

    # Right Column: Embedded Auth Matrix Diagram
    diag10_img = os.path.join(assets_dir, "auth_matrix.png")
    if os.path.exists(diag10_img):
        slide10.shapes.add_picture(diag10_img, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25))
    else:
        c10_r = add_card(slide10, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25), "Auth Gating Matrix")

    attach_notes(slide10, {
        'narrative': "Slide 10 illustrates our defense-in-depth model. We maintain a clear separation between human administration and agent execution. For humans, we enforce RBAC across ADMIN, OPERATOR, and VIEWER roles, secured with Argon2id password hashing, five-strike account lockout, and refresh token rotation. For autonomous agents, we implement AdaptivePolicyEnforcer. We classify operations into STANDARD tasks and PRIVILEGED pipelines. If an agent enters the SUSPICIOUS state, it can still perform standard queries, but privileged operations like workflow orchestration are strictly blocked with HTTP 403. If it degrades into QUARANTINED, all execution is blocked.",
        'takeaway': "Zero-trust policy enforcement gates operations dynamically: suspicious agents lose privileged access, while quarantined agents are totally blocked.",
        'evidence': "akta/adaptive_auth.py (AdaptivePolicyEnforcer, evaluate_request), akta/auth.py, tests/test_adaptive_auth.py, tests/test_auth_rbac.py",
        'transition': "Next, let us examine how verified agents are discovered and classified on Slide 11.",
        'qa': "Q1: What happens when an agent in SUSPICIOUS attempts to execute a workflow?\nA1: The gateway intercepts the request, logs a security audit event in security_audit_events, and immediately returns HTTP 403 Forbidden with detail 'Operation privileged:blocked for state SUSPICIOUS'.\n\nQ2: Can a client bypass security by tampering with the React frontend?\nA2: No. The client is completely untrusted; all security rules are authoritatively enforced by the FastAPI backend.",
        'caveat': "Backend RBAC and ABAC checks execute independently of frontend UI state."
    })

    # ==========================================================================
    # SLIDE 11: Agent Capability Discovery & Diagnostic Eligibility
    # ==========================================================================
    slide11 = create_base_slide("DISCOVERY ENGINE · TRANSPARENT GOVERNANCE", "Inventory Exploration, Health Probing & Explainable Rationales", 11)
    
    # Left Column: Discovery Controls & Rationales
    c11_l = add_card(slide11, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.25), "Discovery Controls & Explainable Rationales")
    tf11_l = add_textbox(slide11, Inches(1.05), Inches(2.2), Inches(4.8), Inches(4.5))
    
    add_para(tf11_l, "1. Multi-Parametric Search Controls", size=12, bold=True, color=COLOR_CYAN)
    add_para(tf11_l, "• Capability Tag Selector: Filters by verified credentials (analysis, coding, research, planning, verification).\n• Dynamic Min Trust Slider: Real-time slider (0.00 to 1.00 in steps of 0.05).\n• Operational Availability Filter: AVAILABLE, BUSY, OFFLINE status.\n• Endpoint Health Probe Filter: Live ping confirming HTTP 200 reachable.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf11_l, "2. Explainable Eligibility vs. Exclusion Engine", size=12, bold=True, color=COLOR_AMBER, space_before=8)
    add_para(tf11_l, "Unlike opaque directories that silently hide excluded agents, TrustChain-AI explicitly evaluates every registered candidate and displays transparent rationales:\n• Quarantine Exclusion: 'Under behavioral quarantine (T = 0.42 < 0.50)'\n• Threshold Exclusion: 'Trust score (0.65) below requested slider (0.80)'\n• Availability Exclusion: 'Status is BUSY on active collaboration session'", size=9.5, color=COLOR_WHITE, space_before=2)
    
    add_para(tf11_l, "Direct Action Integration: Direct one-click 'Investigate' drawer and 'Engage in Collaboration' buttons.", size=10, color=COLOR_CYAN, space_before=8)

    # Right Column: Embedded Discovery Flowchart
    diag11_img = os.path.join(assets_dir, "discovery_flowchart.png")
    if os.path.exists(diag11_img):
        slide11.shapes.add_picture(diag11_img, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25))
    else:
        c11_r = add_card(slide11, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25), "Discovery Eligibility Flowchart")

    attach_notes(slide11, {
        'narrative': "Slide 11 covers our Agent Discovery Engine. It is vital to distinguish discovery from matching. Discovery is an inventory search and availability tool. An operator filters agents by required capability, sets a minimum trust threshold slider between 0.0 and 1.0, and filters by operational availability and endpoint health. Instead of silently omitting excluded agents, our engine evaluates every agent and presents explicit diagnostic rationales: for instance, explaining whether an agent was excluded because its trust score fell below the slider threshold, because it is under quarantine, or because it is currently busy. Operators can click Investigate to open the slide-over drawer immediately.",
        'takeaway': "Discovery provides transparent inventory search with explicit eligibility and exclusion rationales across capability, health, and trust filters.",
        'evidence': "frontend/src/components/DiscoveryCenter.jsx, akta/vdr/registry_router.py (/api/v1/registry/discover), tests/test_investigation_discovery_matching.py",
        'transition': "While Discovery checks inventory eligibility, Slide 12 presents our Task-Driven Matchmaker for optimal assignment.",
        'qa': "Q1: Does discovery perform task ranking?\nA1: No. Discovery verifies eligibility and availability. Ranking candidates for a specific workload is the distinct responsibility of the Matching Engine.\n\nQ2: What is the backend endpoint for discovery?\nA2: GET /api/v1/registry/discover with optional capability and min_trust query parameters.",
        'caveat': "Discovery evaluations are performed dynamically against live registry state."
    })

    # ==========================================================================
    # SLIDE 12: Task-Driven Matchmaker & Explainable Multi-Factor Ranking
    # ==========================================================================
    slide12 = create_base_slide("ALGORITHMIC MATCHMAKING · EXPLAINABLE AI", "Task-Driven Matchmaker & Explainable Multi-Factor Ranking", 12)
    
    # Left Column: Mathematical Formulation & Candidate Ranking
    c12_l = add_card(slide12, Inches(0.8), Inches(1.65), Inches(5.3), Inches(5.25), "Multi-Factor Matching Algorithm Formulation")
    tf12_l = add_textbox(slide12, Inches(1.05), Inches(2.2), Inches(4.8), Inches(4.5))
    
    add_para(tf12_l, "COMPOSITE MATCHSCORE EQUATION", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf12_l, "MatchScore = 0.4·T + 0.3·(r/5.0) + 0.2·σ + 0.1·(1 - λ)", size=12.5, bold=True, color=COLOR_WHITE, mono=True, space_before=2)
    add_para(tf12_l, "• T: Normalized temporal trust score [0.0, 1.0] (40% weight).\n• r: Historical peer reputation [1.0, 5.0] normalized by /5.0 (30% weight).\n• σ: Historical task success rate (successes / total_tasks) (20% weight).\n• λ: Latency penalty min(latency_ms / 2000, 1.0) -> (1-λ) is latency bonus (10%).", size=9.5, color=COLOR_SLATE, space_before=2)
    
    add_para(tf12_l, "HARD ZERO-TRUST DISQUALIFICATION GATES", size=11, bold=True, color=COLOR_RED, mono=True, space_before=6)
    add_para(tf12_l, "• Immediate Disqualification: If state is QUARANTINED or REVOKED, MatchScore is forced to 0.0 with 'REJECTED BY POLICY', regardless of high reputation.\n• Candidate Benchmark Breakdown (0.4·T + 0.3·r/5 + 0.2·σ + 0.1·[1-λ]):\n  1. Agent Alpha: 0.963 [TOP CANDIDATE SPOTLIGHT] (0.380 + 0.288 + 0.200 + 0.095)\n  2. Agent Beta:  0.812 [ELIGIBLE CANDIDATE] (0.340 + 0.252 + 0.170 + 0.050)\n  3. Agent Gamma: 0.655 [ELIGIBLE CANDIDATE] (0.260 + 0.210 + 0.150 + 0.035)\n  4. Agent Delta: 0.000 [DISQUALIFIED - UNDER QUARANTINE (T=0.42)]\n• Calculated illustrative benchmark matching akta/vdr/registry_crud.py.", size=9, color=COLOR_WHITE, space_before=2)

    # Right Column: Embedded Matching Chart
    chart12_img = os.path.join(assets_dir, "matching_breakdown.png")
    if os.path.exists(chart12_img):
        slide12.shapes.add_picture(chart12_img, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25))
    else:
        c12_r = add_card(slide12, Inches(6.3), Inches(1.65), Inches(6.233), Inches(5.25), "Matching Breakdown Chart")

    attach_notes(slide12, {
        'narrative': "Slide 12 covers our Task-Driven Matching Engine. When an operator inputs a specific task description, required capability, and minimum trust score, the system ranks all eligible agents using our multi-factor matching formula: 40% weight on temporal trust, 30% on historical reputation, 20% on success rate, and 10% on latency bonus. The chart on the right visualizes the exact score contributions. Notice how Agent Alpha achieves the top match with a score of 0.963. Crucially, our algorithm enforces hard security boundaries: an agent in Quarantine receives a MatchScore of zero, even if its historical reputation is 5.0 out of 5.0.",
        'takeaway': "The matching algorithm combines trust, reputation, success, and latency into an explainable score with hard zero-trust disqualification boundaries.",
        'evidence': "akta/vdr/registry_crud.py (find_best_agent_match), frontend/src/components/MatchingCenter.jsx, tests/test_investigation_discovery_matching.py",
        'transition': "Once agents are matched, they execute bilateral collaborations and workflows as detailed on Slide 13.",
        'qa': "Q1: Why is trust weighted at 0.4 while reputation is 0.3?\nA1: Temporal trust reflects recent, verified runtime behavior, whereas reputation is historical. In zero-trust systems, recent verified telemetry takes precedence over historical accolades.\n\nQ2: What is the purpose of dividing reputation by 5.0?\nA2: Peer ratings follow a 1-to-5 star scale; dividing by 5.0 normalizes reputation to the [0.2, 1.0] unit interval matching other terms.",
        'caveat': "Weights are configured in registry_crud.py and validated in test_platform_features.py."
    })

    print("Upgraded Slides 7-12 built successfully.")
