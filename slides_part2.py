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

def build_slides_7_to_12(prs, assets_dir):
    # ==========================================================================
    # SLIDE 7: DID, Cryptographic Identity, and Verifiable Credentials
    # ==========================================================================
    slide7 = create_base_slide("IDENTITY LAYER · W3C SPECIFICATIONS", "Cryptographic Agent Identity & Verifiable Credentials Lifecycle", 7)
    
    # Left Column: W3C did:key Architecture
    c7_l = add_card(slide7, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "W3C did:key Decentralized Identifier Architecture")
    tf7_l = add_textbox(slide7, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf7_l, "1. Algorithmic Identity Construction", size=12, bold=True, color=COLOR_CYAN)
    add_para(tf7_l, "• Public Key Cryptography: Generates raw 32-byte Ed25519 keypair using libsodium via PyNaCl library.\n• Multicodec Prefix: Prepends 2-byte varint 0xED01 indicating Ed25519 public key.\n• Base58 Encoding: Encodes prefixed bytes with Bitcoin base58 alphabet, prefixed with 'z'.\n• Formal Format: did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRo...", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf7_l, "2. Self-Sovereign Decentralization", size=12, bold=True, color=COLOR_CYAN, space_before=8)
    add_para(tf7_l, "• No Central Authority: Identifiers are generated algorithmically without requiring DNS registration, central certificate authorities, or proprietary registration fees.\n• Deterministic Resolution: Any node in the network resolves public key directly from the DID string itself without querying an external registry.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf7_l, "3. Identity vs. Trust Boundary", size=12, bold=True, color=COLOR_AMBER, space_before=8)
    add_para(tf7_l, "• Critical Principle: Possession of a valid did:key proves cryptographic ownership of the private key. It does NOT prove current behavioral trustworthiness.", size=10, color=COLOR_WHITE, space_before=2)

    # Right Column: Verifiable Credentials & Lifecycle
    c7_r = add_card(slide7, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "W3C Verifiable Credentials & LD-Proof Lifecycle")
    tf7_r = add_textbox(slide7, Inches(7.133), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf7_r, "W3C JSON-LD CREDENTIAL STRUCTURE", size=11, bold=True, color=COLOR_GREEN, mono=True)
    add_para(tf7_r, "{\n  \"@context\": [\"https://www.w3.org/2018/credentials/v1\"],\n  \"id\": \"urn:uuid:7f3b4c12-...\",\n  \"type\": [\"VerifiableCredential\", \"AgentCapabilityCredential\"],\n  \"issuer\": \"did:key:z6Mku...\" (Authority DID),\n  \"credentialSubject\": { \"id\": \"did:key:...\", \"capabilities\": [\"analysis\"] },\n  \"proof\": { \"type\": \"Ed25519Signature2020\", \"proofValue\": \"...\" }\n}", size=8.5, color=COLOR_CYAN, mono=True, space_before=2)
    
    add_para(tf7_r, "CANONICALIZATION & CRYPTOGRAPHIC PROOF", size=11, bold=True, color=COLOR_PURPLE, mono=True, space_before=8)
    add_para(tf7_r, "• URDNA2015 Normalization: Uses PyLD to transform JSON-LD into deterministic N-Quads dataset prior to hashing, resolving JSON key reordering issues.\n• Ed25519Signature2020: Hashes normalized string via SHA-256 and signs with issuer private key; verifies against issuer's resolved public key.", size=9.5, color=COLOR_SLATE, space_before=2)
    
    add_para(tf7_r, "CREDENTIAL LIFECYCLE PIPELINE", size=11, bold=True, color=COLOR_WHITE, mono=True, space_before=8)
    add_para(tf7_r, "[Keypair Gen] ──> [DID Creation] ──> [VC Issuance] ──> [VDR Storage] ──> [Verification]", size=9.5, color=COLOR_SLATE, mono=True, space_before=2)

    attach_notes(slide7, {
        'narrative': "Slide 7 presents the identity and credential layer. Every agent generates an Ed25519 keypair using PyNaCl. The 32-byte public key is prefixed with the multicodec byte sequence 0xED01 and encoded in base58-btc to produce a deterministic W3C did:key identifier. This provides self-sovereign identity without a centralized CA. For verifiable claims, such as authorized capabilities, we issue W3C Verifiable Credentials. Because JSON keys can change order, we apply the URDNA2015 canonicalization algorithm using PyLD before hashing with SHA-256 and signing with Ed25519. Crucially, we emphasize that possessing a valid DID proves identity ownership, but does not prove operational trustworthiness.",
        'takeaway': "TrustChain-AI strictly implements W3C did:key and JSON-LD Verifiable Credentials with URDNA2015 canonicalization and Ed25519 cryptographic signatures.",
        'evidence': "akta/did.py, akta/credentials.py, akta/vdr/router.py, tests/commands/test_keys.py, tests/commands/test_claim.py",
        'qa': "Q1: Why did you choose did:key over did:ethr or did:ion?\nA1: did:key is fully deterministic and self-resolving. It requires no blockchain transactions or ledger lookup to extract the public verification key, making it lightweight and highly performant for autonomous agent microservices.\n\nQ2: What is URDNA2015 and why is it needed?\nA2: URDNA2015 is the RDF Dataset Normalization standard. In JSON-LD, dictionaries are unordered. Canonicalization standardizes statement ordering so the SHA-256 hash remains invariant regardless of key serialization order.",
        'caveat': "Verifiable credentials are stored and verified against the local SQLite VDR database."
    })

    # ==========================================================================
    # SLIDE 8: Behavioral Telemetry and Trust Evaluation
    # ==========================================================================
    slide8 = create_base_slide("TRUST MATHEMATICS · METRIC FORMULATION", "Runtime Sensor Telemetry & Instantaneous Behavioral Scoring", 8)
    
    # Left Column: Telemetry Signals
    c8_l = add_card(slide8, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Runtime Telemetry Sensor Ingestion Model")
    tf8_l = add_textbox(slide8, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf8_l, "STANDARDIZED TELEMETRY EVENT SCHEMA", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf8_l, "TelemetryEvent(\n  agent_did: str,          # Target agent identifier\n  task_id: str,            # Unique execution UUID\n  success: bool,           # Boolean task completion flag\n  compliance_event: str,   # Policy breach descriptor (None if OK)\n  latency_ms: int,         # Measured execution duration\n  timestamp: datetime      # UTC observation timestamp\n)", size=8.5, color=COLOR_WHITE, mono=True, space_before=2)
    
    add_para(tf8_l, "THREE EVALUATED BEHAVIORAL METRICS (SLIDING WINDOW W=10)", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf8_l, "1. Task Success Rate S_i(t) ∈ [0.0, 1.0]:\n   Ratio of successful executions over the sliding observation window.", size=10, color=COLOR_SLATE, space_before=2)
    add_para(tf8_l, "2. Protocol Compliance Rate C_i(t) ∈ [0.0, 1.0]:\n   Ratio of events with zero compliance breaches or protocol violations.", size=10, color=COLOR_SLATE, space_before=2)
    add_para(tf8_l, "3. Normalized Latency Penalty L_i(t) ∈ [0.0, 1.0]:\n   Normalized response duration: min(avg_latency / 2000ms, 1.0).", size=10, color=COLOR_SLATE, space_before=2)

    # Right Column: Instantaneous Score Math
    c8_r = add_card(slide8, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Instantaneous Performance Score Formulation P_i(t)")
    tf8_r = add_textbox(slide8, Inches(7.133), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf8_r, "THE INSTANTANEOUS BEHAVIORAL EQUATION", size=11, bold=True, color=COLOR_AMBER, mono=True)
    add_para(tf8_r, "P_i(t) = 0.6 · S_i(t) + 0.3 · C_i(t) + 0.1 · (1.0 - L_i(t))", size=14, bold=True, color=COLOR_CYAN, mono=True, space_before=4)
    add_para(tf8_r, "Constraints: w1 + w2 + w3 = 1.0  |  w1, w2, w3 ∈ [0, 1]  |  P_i(t) ∈ [0.0, 1.0]", size=9.5, color=COLOR_SLATE, mono=True, space_before=2)
    
    add_para(tf8_r, "PARAMETER WEIGHTING RATIONALE", size=11, bold=True, color=COLOR_WHITE, mono=True, space_before=10)
    add_para(tf8_r, "• Task Success Weight (w1 = 0.60):\n  Functional correctness is the paramount requirement. If an agent fails to complete reasoning orimplementation tasks, trust must degrade substantially.", size=9.5, color=COLOR_SLATE, space_before=2)
    add_para(tf8_r, "• Protocol Compliance Weight (w2 = 0.30):\n  Enforces safety boundaries, API protocol conformance, and non-repudiation. Compliance violations trigger acute trust reductions.", size=9.5, color=COLOR_SLATE, space_before=3)
    add_para(tf8_r, "• Latency Penalty Weight (w3 = 0.10):\n  Encourages operational efficiency. Benchmarked against a 2000ms SLA threshold; responses exceeding 2000ms receive zero latency bonus.", size=9.5, color=COLOR_SLATE, space_before=3)

    attach_notes(slide8, {
        'narrative': "Slide 8 details how runtime behavior is translated into mathematical metrics. When an agent executes a task, the gateway captures a TelemetryEvent containing success, compliance, and response latency. Across a sliding window of the last 10 observations, we compute three normalized factors: S_i for success rate, C_i for policy compliance, and L_i for latency penalty benchmarked against a 2000-millisecond SLA threshold. We then formulate the instantaneous performance score P_i(t) as a weighted linear combination: 0.6 for success, 0.3 for compliance, and 0.1 for latency efficiency. These weights reflect security priorities: correctness is primary, protocol safety is vital, and performance speed provides marginal optimization.",
        'takeaway': "The instantaneous score P_i(t) cleanly integrates functional success, security compliance, and latency performance into a bounded score between 0.0 and 1.0.",
        'evidence': "akta/telemetry.py, akta/trust_engine.py (lines 14-68), tests/test_adaptive_policy.py",
        'qa': "Q1: Why is the latency SLA fixed at 2000ms?\nA1: 2000ms represents the maximum acceptable timeout for real-time autonomous micro-delegations. It is configurable in TrustConfig.max_latency_ms.\n\nQ2: What happens if an agent submits no telemetry?\nA2: If no events exist, the system initializes S=1.0, C=1.0, L=0.0 to grant initial operational baseline trust under the principle of optimism.",
        'caveat': "The 10-event sliding window and weight constants are verified defaults configured in TrustConfig."
    })

    # ==========================================================================
    # SLIDE 9: Dynamic Trust Algorithm and Trust-State Lifecycle
    # ==========================================================================
    slide9 = create_base_slide("DYNAMIC TRUST ALGORITHM · STATE MACHINE", "Temporal EMA Smoothing & Behavioral State Transition Machine", 9)
    
    # Left Column: EMA Formula & State Thresholds
    c9_l = add_card(slide9, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Temporal Exponential Moving Average (EMA)")
    tf9_l = add_textbox(slide9, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf9_l, "TEMPORAL UPDATE FORMULATION", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf9_l, "T_i(t) = λ · T_i(t-1) + (1.0 - λ) · P_i(t)", size=13, bold=True, color=COLOR_WHITE, mono=True, space_before=3)
    add_para(tf9_l, "With verified default λ = 0.70:\nT_i(t) = 0.7 · T_i(t-1) + 0.3 · P_i(t)", size=12, bold=True, color=COLOR_CYAN, mono=True, space_before=2)
    add_para(tf9_l, "• Initial Baseline: T_i(0) = 1.00 (Optimistic initial trust).\n• Historical Memory Factor (λ = 0.70): Prevents single anomalous errors from destabilizing operational networks while ensuring sustained degradation triggers isolation.", size=10, color=COLOR_SLATE, space_before=3)
    
    add_para(tf9_l, "FOUR DISCRETE BEHAVIORAL STATES", size=11, bold=True, color=COLOR_AMBER, mono=True, space_before=8)
    add_para(tf9_l, "• TRUSTED (T >= 0.80): Full authorization for standard & privileged tasks.\n• SUSPICIOUS (0.50 <= T < 0.80): Warning state; privileged actions blocked.\n• QUARANTINED (T < 0.50): Automated isolation; all actions denied (HTTP 403).\n• REVOKED (Terminal): Administrative kill-switch; cannot recover via telemetry.", size=9.5, color=COLOR_WHITE, space_before=3)

    # Right Column: Chart Image
    chart1_img = os.path.join(assets_dir, "trust_timeline.png")
    if os.path.exists(chart1_img):
        slide9.shapes.add_picture(chart1_img, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25))
    else:
        c9_r = add_card(slide9, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Trust Score Degradation Timeline")

    attach_notes(slide9, {
        'narrative': "Slide 9 presents our temporal trust algorithm and state machine. To prevent single transient errors from abruptly knocking agents offline, we apply an Exponential Moving Average: T_i(t) equals 0.7 times previous trust plus 0.3 times current performance. Newly registered agents start with a baseline score of 1.0. As shown in the chart on the right, if an agent repeatedly fails or breaches compliance, its trust decays smoothly across our four states: TRUSTED at or above 0.8, SUSPICIOUS between 0.5 and 0.8, and QUARANTINED below 0.5. Notice that if an agent is quarantined, it can recover if supervised telemetry proves restored reliability. However, REVOKED is an administrative terminal state that can never recover via telemetry.",
        'takeaway': "The temporal EMA algorithm balances historical memory with adaptive responsiveness, mapping continuous scores into four rigorous operational states.",
        'evidence': "akta/trust_engine.py (lines 69-84), tests/test_adaptive_policy.py, tests/test_e2e_lifecycle.py",
        'qa': "Q1: Why is lambda set to 0.7?\nA1: A lambda of 0.7 places 70% weight on accumulated history and 30% on new observations. It requires approximately 3 consecutive failures to enter quarantine from 1.0, effectively filtering out momentary network glitches.\n\nQ2: What is the difference between Quarantine and Revocation?\nA2: Quarantine is an automated, score-driven temporary isolation state that can self-heal. Revocation is a permanent administrative terminal command executed by an ADMIN.",
        'caveat': "Chart displays an illustrative worked calculation following the exact mathematical equation implemented in the codebase."
    })

    # ==========================================================================
    # SLIDE 10: Trust-Aware Authorization and Security Enforcement
    # ==========================================================================
    slide10 = create_base_slide("ACCESS CONTROL · ZERO-TRUST ENFORCEMENT", "Dual-Layer Defense: Human RBAC & Agent Trust-State Gating", 10)
    
    # Left Column: Dual Layer Governance
    c10_l = add_card(slide10, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Dual-Layer Governance: Human RBAC vs. Agent Trust")
    tf10_l = add_textbox(slide10, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf10_l, "LAYER 1: HUMAN ROLE-BASED ACCESS CONTROL (RBAC)", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf10_l, "• ADMIN: Full platform governance, user management, policy updates, terminal agent revocation.\n• OPERATOR: Operational execution, initiating workflows, requesting agent matches, monitoring logs.\n• VIEWER: Read-only inspection of fleet posture, telemetry charts, and security audit trails.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf10_l, "LAYER 2: AUTONOMOUS AGENT RUNTIME TRUST GATING", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf10_l, "• Independent of Credentials: An agent with a valid cryptographic credential is still blocked if its behavioral trust score has degraded.\n• Continuous Decision Gate: Access decisions are re-evaluated dynamically on every single API invocation.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf10_l, "SESSION DEFENSE & CREDENTIAL INTEGRITY", size=11, bold=True, color=COLOR_PURPLE, mono=True, space_before=8)
    add_para(tf10_l, "• Password Security: Argon2id hashing algorithm with salt generation.\n• Lockout Defense: 5 consecutive failed attempts locks account for 15 minutes.\n• Token Rotation: Refresh token rotation with cryptographic hash reuse detection.", size=10, color=COLOR_SLATE, space_before=2)

    # Right Column: Operation Classification Matrix
    c10_r = add_card(slide10, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Operation Privilege Gating Matrix")
    tf10_r = add_textbox(slide10, Inches(7.133), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf10_r, "OPERATION CLASSIFICATION TAXONOMY", size=11, bold=True, color=COLOR_AMBER, mono=True)
    add_para(tf10_r, "• PRIVILEGED OPERATIONS:\n  workflow:execute, workflow:orchestrate, agent:delegate,\n  credential:issue, admin:revoke, admin:manage, sensitive:execute\n• STANDARD OPERATIONS:\n  read, query, map:generate, task:execute, collaboration:step", size=9.5, color=COLOR_WHITE, mono=True, space_before=2)
    
    add_para(tf10_r, "DYNAMIC DECISION MATRIX ACROSS TRUST STATES", size=11, bold=True, color=COLOR_WHITE, mono=True, space_before=8)
    add_para(tf10_r, "STATE          STANDARD OP       PRIVILEGED OP      GATEWAY DECISION", size=9, bold=True, color=COLOR_CYAN, mono=True, space_before=2)
    add_para(tf10_r, "TRUSTED        ALLOWED           ALLOWED            HTTP 200 (Permit)", size=9, color=COLOR_GREEN, mono=True)
    add_para(tf10_r, "SUSPICIOUS     ALLOWED (Audited) DENIED (Policy)    HTTP 403 (Restricted)", size=9, color=COLOR_AMBER, mono=True)
    add_para(tf10_r, "QUARANTINED    DENIED (403)      DENIED (403)       HTTP 403 (Quarantine)", size=9, color=COLOR_RED, mono=True)
    add_para(tf10_r, "REVOKED        DENIED (403)      DENIED (403)       HTTP 403 (Terminal)", size=9, color=COLOR_RED, mono=True)
    
    add_para(tf10_r, "Zero-Trust Guarantee: A compromised key cannot execute privileged actions once behavioral degradation trips the Suspicious or Quarantined boundaries.", size=9.5, color=COLOR_SLATE, space_before=8)

    attach_notes(slide10, {
        'narrative': "Slide 10 illustrates our defense-in-depth model. We maintain a clear separation between human administration and agent execution. For humans, we enforce RBAC across ADMIN, OPERATOR, and VIEWER roles, secured with Argon2id password hashing, five-strike account lockout, and refresh token rotation. For autonomous agents, we implement AdaptivePolicyEnforcer. We classify operations into STANDARD tasks and PRIVILEGED pipelines. If an agent enters the SUSPICIOUS state, it can still perform standard queries, but privileged operations like workflow orchestration are strictly blocked with HTTP 403. If it degrades into QUARANTINED, all execution is blocked.",
        'takeaway': "Adaptive authorization dynamically restricts privileges based on real-time trust state, implementing true zero-trust gating for autonomous AI agents.",
        'evidence': "akta/adaptive_auth.py, akta/auth/router.py, akta/auth/dependencies.py, tests/test_adaptive_policy.py, tests/test_authentication.py",
        'qa': "Q1: What happens when an agent in SUSPICIOUS requests a privileged operation?\nA1: The gateway immediately intercepts the request, blocks execution with an HTTP 403 Forbidden, and records a security policy violation event in the trust audit trail.\n\nQ2: How does refresh token reuse detection work?\nA2: When a refresh token is used, its unique JTI is invalidated. If a token with an already-revoked JTI is presented again, the system detects replay/theft, revokes all user sessions, and logs a security audit alert.",
        'caveat': "Operation classification is defined centrally in AdaptivePolicyEnforcer."
    })

    # ==========================================================================
    # SLIDE 11: Agent Discovery and Eligibility
    # ==========================================================================
    slide11 = create_base_slide("SERVICE DISCOVERY · AVAILABILITY SEARCH", "Agent Capability Discovery & Pre-Execution Eligibility Filter", 11)
    
    # Left Column: Discovery Purpose & Filters
    c11_l = add_card(slide11, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Discovery Engine Architecture & Filters")
    tf11_l = add_textbox(slide11, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf11_l, "DOMAIN ROLE: CAPABILITY & AVAILABILITY SEARCH", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf11_l, "The Discovery Engine provides broad inventory search and pre-execution filtering. It answers: 'Which candidate agents exist in the registry that possess the required capability, are currently online, and meet baseline trust criteria?'", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf11_l, "VERIFIED DISCOVERY CONTROLS & FILTERS", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf11_l, "1. Capability Selector:\n   Filters by verified tags (analysis, research, coding, planning, verification, compute).\n2. Minimum Trust Threshold Slider:\n   Dynamic real-time slider (0.00 to 1.00 in steps of 0.05).\n3. Operational Availability Filter:\n   AVAILABLE, BUSY, OFFLINE status filtering.\n4. Endpoint Health Probe Filter:\n   HEALTHY, UNHEALTHY, OFFLINE status verification.\n5. Search Query Input:\n   Instant filtering by DID prefix or agent display name.", size=9.5, color=COLOR_SLATE, space_before=2)

    # Right Column: Eligibility vs Exclusion Rationale
    c11_r = add_card(slide11, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Diagnostic Eligibility & Exclusion Rationale Engine")
    tf11_r = add_textbox(slide11, Inches(7.133), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf11_r, "EXPLAINABLE ELIGIBILITY CLASSIFICATION", size=11, bold=True, color=COLOR_AMBER, mono=True)
    add_para(tf11_r, "Unlike opaque registries that silently hide agents, TrustChain-AI explicitly evaluates every candidate against policy and surfaces clear diagnostic rationales.", size=10, color=COLOR_SLATE, space_before=2)
    
    add_para(tf11_r, "ELIGIBLE CANDIDATE STATUS PILL", size=10.5, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf11_r, "• Status: [ ELIGIBLE ]\n• Rationale: 'Eligible: Meets capability, trust threshold, operational status & health criteria.'", size=9.5, color=COLOR_WHITE, space_before=2)
    
    add_para(tf11_r, "EXCLUSION DIAGNOSTIC EXAMPLES", size=10.5, bold=True, color=COLOR_RED, mono=True, space_before=8)
    add_para(tf11_r, "• Policy Exclusion:\n  'Excluded: Under behavioral quarantine (T = 0.42 < 0.50).'\n• Threshold Exclusion:\n  'Excluded: Trust score (0.65) is below requested minimum (0.80).'\n• Availability Exclusion:\n  'Excluded: Operational status is BUSY on active collaboration.'\n• Health Exclusion:\n  'Excluded: Endpoint health probe returned UNHEALTHY.'", size=9, color=COLOR_SLATE, space_before=2)
    
    add_para(tf11_r, "Action Shortcuts: Direct one-click 'Investigate' drawer and 'Engage in Collaboration' buttons.", size=9.5, color=COLOR_CYAN, space_before=8)

    attach_notes(slide11, {
        'narrative': "Slide 11 covers our Agent Discovery Engine. It is vital to distinguish discovery from matching. Discovery is an inventory search and availability tool. An operator filters agents by required capability, sets a minimum trust threshold slider between 0.0 and 1.0, and filters by operational availability and endpoint health. Instead of silently omitting excluded agents, our engine evaluates every agent and presents explicit diagnostic rationales: for instance, explaining whether an agent was excluded because its trust score fell below the slider threshold, because it is under quarantine, or because it is currently busy. Operators can click Investigate to open the slide-over drawer immediately.",
        'takeaway': "Discovery provides transparent inventory search with explicit eligibility and exclusion rationales across capability, health, and trust filters.",
        'evidence': "frontend/src/components/DiscoveryCenter.jsx, akta/vdr/registry_router.py (/api/v1/registry/discover), tests/test_investigation_discovery_matching.py",
        'qa': "Q1: Does discovery perform task ranking?\nA1: No. Discovery verifies eligibility and availability. Ranking candidates for a specific workload is the distinct responsibility of the Matching Engine.\n\nQ2: What is the backend endpoint for discovery?\nA2: GET /api/v1/registry/discover with optional capability and min_trust query parameters.",
        'caveat': "Discovery evaluations are performed dynamically against the live registry state."
    })

    # ==========================================================================
    # SLIDE 12: Task-Aware Matching and Recommendation
    # ==========================================================================
    slide12 = create_base_slide("ALGORITHMIC MATCHMAKING · EXPLAINABLE AI", "Task-Driven Matchmaker & Explainable Multi-Factor Ranking", 12)
    
    # Left Column: Formulation & Spotlight
    c12_l = add_card(slide12, Inches(0.8), Inches(1.65), Inches(5.65), Inches(5.25), "Multi-Factor Matching Algorithm Formulation")
    tf12_l = add_textbox(slide12, Inches(1.05), Inches(2.2), Inches(5.15), Inches(4.5))
    
    add_para(tf12_l, "THE COMPOSITE MATCH SCORE EQUATION", size=11, bold=True, color=COLOR_CYAN, mono=True)
    add_para(tf12_l, "MatchScore = 0.4·T + 0.3·(r/5.0) + 0.2·σ + 0.1·(1 - λ)", size=12, bold=True, color=COLOR_WHITE, mono=True, space_before=3)
    add_para(tf12_l, "• T: Normalized temporal trust score [0.0, 1.0].\n• r: Historical peer reputation rating [1.0, 5.0] normalized by /5.0.\n• σ: Historical task success rate [0.0, 1.0] (successes / total_tasks).\n• λ: Normalized latency penalty min(latency_ms / 2000, 1.0).", size=9.5, color=COLOR_SLATE, space_before=2)
    
    add_para(tf12_l, "ZERO-TRUST HARD BOUNDARY ENFORCEMENT", size=11, bold=True, color=COLOR_RED, mono=True, space_before=8)
    add_para(tf12_l, "• Immediate Policy Disqualification: If an agent is in QUARANTINED or REVOKED state, MatchScore is forced to 0.0 with 'REJECTED BY POLICY', regardless of high historical reputation.\n• Privileged Restriction: If state is SUSPICIOUS and task is privileged, candidate is disqualified.", size=9.5, color=COLOR_SLATE, space_before=2)
    
    add_para(tf12_l, "TOP MATCH RECOMMENDATION SPOTLIGHT", size=11, bold=True, color=COLOR_GREEN, mono=True, space_before=8)
    add_para(tf12_l, "Highlights the highest-scoring candidate with a glowing cyan banner, mathematical breakdown chips, recommendation rationale, and one-click 'Assign Task' button.", size=9.5, color=COLOR_WHITE, space_before=2)

    # Right Column: Chart Image
    chart2_img = os.path.join(assets_dir, "matching_breakdown.png")
    if os.path.exists(chart2_img):
        slide12.shapes.add_picture(chart2_img, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25))
    else:
        c12_r = add_card(slide12, Inches(6.883), Inches(1.65), Inches(5.65), Inches(5.25), "Matching Score Comparison Chart")

    attach_notes(slide12, {
        'narrative': "Slide 12 covers our Task-Driven Matching Engine. When an operator inputs a specific task description, required capability, and minimum trust score, the system ranks all eligible agents using our multi-factor matching formula: 40% weight on temporal trust, 30% on historical reputation, 20% on success rate, and 10% on latency bonus. The chart on the right visualizes the exact score contributions. Notice how Agent Alpha achieves the top match with a score of 0.963. Crucially, our algorithm enforces hard security boundaries: an agent in Quarantine receives a MatchScore of zero, even if its historical reputation is 5.0 out of 5.0.",
        'takeaway': "The matching algorithm combines trust, reputation, success, and latency into an explainable score with hard zero-trust disqualification boundaries.",
        'evidence': "akta/vdr/registry_crud.py (find_best_agent_match), frontend/src/components/MatchingCenter.jsx, tests/test_investigation_discovery_matching.py",
        'qa': "Q1: Why is trust weighted at 0.4 while reputation is 0.3?\nA1: Temporal trust reflects recent, verified runtime behavior, whereas reputation is historical. In zero-trust systems, recent verified telemetry takes precedence over historical accolades.\n\nQ2: What is the purpose of the Ineligible Candidates accordion?\nA2: It provides explainability, showing operators exactly why other agents were disqualified (e.g. missing capability, low trust, or active quarantine).",
        'caveat': "Weights are configured in registry_crud.py and validated in test_platform_features.py."
    })

    print("Slides 7-12 built successfully.")
