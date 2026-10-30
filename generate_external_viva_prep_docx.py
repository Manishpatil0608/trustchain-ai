# -*- coding: utf-8 -*-
"""
generate_external_viva_prep_docx.py
Generates the comprehensive external viva examination preparation manual:
TrustChain_AI_External_Viva_Prep.docx
Covers all 14 technical domains with 35 authoritative questions, examiner intents,
technical codebase anchors, and defense cautions.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCX_PATH = os.path.join(BASE_DIR, "docs", "presentation", "TrustChain_AI_External_Viva_Prep.docx")

HEX_NAVY = "081426"
HEX_CYAN = "00A3C4"
HEX_DARK_BLUE = "112240"
HEX_LIGHT_BLUE = "EAF3FF"
HEX_GREEN = "059669"
HEX_AMBER = "D97706"
HEX_RED = "DC2626"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, title, text, border_hex="00A3C4", bg_hex="F0F9FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"{title}: ")
    r1.bold = True
    r1.font.name = "Calibri"
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = RGBColor.from_string(border_hex)
    
    r2 = p.add_run(text)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor.from_string("1E293B")
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def build_viva_prep():
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "TrustChain-AI · External Examiner Viva Preparation Manual · SVKM's NMIMS MPSTME 2026–2027"
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.runs[0].font.name = "Calibri"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(148, 163, 184)

    # Document Header
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_after = Pt(2)
    r_uni = p_uni.add_run("SVKM'S NMIMS (DEEMED-TO-BE UNIVERSITY)\nMUKESH PATEL SCHOOL OF TECHNOLOGY MANAGEMENT & ENGINEERING\nDEPARTMENT OF COMPUTER ENGINEERING")
    r_uni.bold = True
    r_uni.font.name = "Calibri"
    r_uni.font.size = Pt(11)
    r_uni.font.color.rgb = RGBColor(71, 85, 105)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("TrustChain-AI: External Examiner Defense Manual & Viva Preparation Guide")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run("35 Authoritative Technical Questions & Examiner Traps Covering All 14 Architecture Domains\nAcademic Year 2026–2027 · Final-Year B.Tech Capstone Examination")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0, 163, 196)

    doc.add_heading("1. Viva Defense Philosophy & Answering Framework", level=1)
    p_intro = doc.add_paragraph(
        "External examiners at the B.Tech level evaluate two primary criteria: technical depth and intellectual honesty. "
        "Examiners frequently test candidates with deliberate trap questions to verify whether the architecture was genuinely "
        "designed and implemented or merely adapted from online tutorials. Candidates must structure every response using the "
        "4-Step Authoritative Response Framework:\n"
        "1. Direct Conceptual Answer: Immediate, unequivocal response to the core question (15 seconds).\n"
        "2. Mathematical & Algorithmic Grounding: Exact equations, weights, parameters, and algorithms (20 seconds).\n"
        "3. Technical Codebase Citation: Exact file names, functions, and database tables in the repository (15 seconds).\n"
        "4. Defense Caveat & Academic Boundary: Proactive acknowledgment of realistic engineering limitations (10 seconds)."
    )
    p_intro.paragraph_format.space_after = Pt(12)

    doc.add_heading("2. Complete 35-Question Technical Viva Defense Matrix", level=1)

    questions = [
        # Domain 1: System Architecture
        ("Q1: Walk me through the exact path of a task request from the React frontend to the database.",
         "Domain 1: System Architecture",
         "Testing end-to-end trace knowledge across all 5 tiers.",
         "When an operator initiates a task on the React 19 frontend (port 5173), an authenticated HTTP POST request is sent with an Authorization Bearer JWT to the FastAPI Gateway (port 8050). The gateway executes add_security_headers_and_request_id middleware, validates the JWT in get_current_user, and dispatches to collaboration_router.py. The CollaborationManager invokes AdaptivePolicyEnforcer.check_agent_authorization against the executing agent's live trust state. If T >= 0.80, the task payload is dispatched to LocalAgentConnector. Upon completion, the connector streams a TelemetryEvent to TrustEngine, which recalculates P_i(t) and updates T_i(t). Finally, an atomic transaction writes to stored_vcs, telemetry_logs, trust_audit_trails, and collaboration_events in the local SQLite WAL database.",
         "akta/server.py, akta/adaptive_auth.py, akta/trust_engine.py, akta/vdr/database.py",
         "Do not claim that the frontend talks directly to the database or that components communicate over WebSockets."),

        ("Q2: Why did you separate the system into 5 distinct tiers instead of a simpler monolithic script?",
         "Domain 1: System Architecture",
         "Evaluating architectural decomposition principles.",
         "A 5-tier architecture enforces separation of concerns and defense-in-depth security boundaries. Tier 1 (Presentation) is completely decoupled and untrusted. Tier 2 (Gateway) enforces network hygiene and human RBAC. Tier 3 (Trust Intelligence) contains pure mathematical algorithms independent of HTTP transport. Tier 4 (Cryptography) encapsulates keypair management and W3C standard encoding. Tier 5 (Storage) isolates relational persistence in SQLite WAL. This modularity allows swapping the local SQLite VDR for a distributed Byzantine ledger without modifying the trust scoring or gateway logic.",
         "docs/presentation/TrustChain_AI_Slide_Assets/architecture_diagram.png, akta/server.py",
         "Do not say it was just to make the architecture diagram look more complex."),

        ("Q3: What ports do your frontend and backend run on, and why are they configured that way?",
         "Domain 1: System Architecture",
         "Verifying actual runtime deployment configuration.",
         "The frontend runs on Vite's default development port 5173, configured in frontend/vite.config.js. The FastAPI backend runs on Uvicorn ASGI port 8050, specified in akta/server.py and settings.py. CORS middleware in server.py explicitly restricts cross-origin resource sharing to http://localhost:5173 with allow_credentials=True, preventing unauthorized cross-site scripting origins.",
         "akta/server.py (lines 135-143), frontend/vite.config.js",
         "Ensure you state port 8050 for the backend, NOT the standard port 8000."),

        # Domain 2: DID & Verifiable Credentials
        ("Q4: Explain the deterministic derivation of a W3C did:key identifier.",
         "Domain 2: DID & Verifiable Credentials",
         "Testing understanding of multicodec and multibase encoding standards.",
         "In did:key, an agent generates a 32-byte Ed25519 private key seed and derives its 32-byte public key using PyNaCl. We prepend the two-byte multicodec varint prefix 0xED01, which signifies an Ed25519 public key in the multiformats table. The resulting 34 bytes are encoded using the Bitcoin base58 alphabet, prefixed with the character 'z' to indicate base58-btc multibase encoding. The complete URI prefix 'did:key:' is prepended, yielding did:key:z6MkpTHR... Any peer can extract the raw 32-byte public key directly by stripping the prefix and decoding base58.",
         "akta/did.py (generate_did_key, resolve_did_key), tests/test_crypto.py",
         "Do not confuse did:key with did:ethr or did:ion which require external blockchain lookups."),

        ("Q5: Why did you choose did:key over did:ethr or did:web?",
         "Domain 2: DID & Verifiable Credentials",
         "Evaluating trade-offs between self-sovereignty and global registries.",
         "did:key is completely self-contained, self-sovereign, and offline-resolvable in sub-microsecond time. did:ethr requires making an RPC query to an Ethereum smart contract registry, introducing 2–15 second network latencies and gas fees. did:web depends on DNS infrastructure and web server uptime, creating centralized points of failure. For high-frequency autonomous agent messaging, did:key delivers maximum speed and decentralization.",
         "docs/blackbook/TrustChain_AI_Blackbook_Part1.md (Chapter 2), akta/did.py",
         "Acknowledge that did:key cannot support key rotation without changing the identifier itself."),

        ("Q6: How do you verify a W3C Verifiable Credential signed with Ed25519Signature2020?",
         "Domain 2: DID & Verifiable Credentials",
         "Checking cryptographic proof verification pipeline knowledge.",
         "Verification follows three rigorous steps: First, the credential's JSON-LD semantic graph is canonicalized into deterministic N-Quads using the URDNA2015 algorithm via PyLD, removing serialization discrepancies. Second, the proof options and canonicalized document are hashed using SHA-256 to create the verification digest. Third, the issuer's public key is extracted from the verificationMethod did:key string and used to verify the 64-byte Ed25519 cryptographic signature. Finally, stored_vcs is queried to confirm is_revoked is False.",
         "akta/vc.py (verify_verifiable_credential), tests/test_vc.py",
         "Do not claim that verifying the signature proves the agent is currently honest; it only proves credential validity."),

        # Domain 3: Cryptography & Ed25519
        ("Q7: Why use Ed25519 instead of RSA-2048 or ECDSA secp256k1?",
         "Domain 3: Cryptography & Verification",
         "Testing cryptographic primitive justification.",
         "Ed25519 offers three critical advantages: Performance: key generation and signing execute in 15–25 microseconds compared to 2–4ms for RSA. Compactness: 32-byte public keys and 64-byte signatures minimize HTTP header bandwidth. Security: Ed25519 operates deterministically over Twisted Edwards curves (Curve25519), eliminating side-channel cache-timing vulnerabilities and the catastrophic nonce-reuse flaws inherent to standard ECDSA.",
         "PyNaCl library binding, akta/did.py, tests/test_crypto.py",
         "Do not claim Ed25519 is quantum-resistant. It is based on elliptic curve discrete logs."),

        ("Q8: How does your implementation detect credential tampering?",
         "Domain 3: Cryptography & Verification",
         "Verifying negative test cases and cryptographic integrity.",
         "In test_vc.py, we deliberately mutate a single character in the credential subject payload (e.g., modifying capability from 'analysis' to 'admin') after issuance. When verify_verifiable_credential executes, the URDNA2015 canonicalization produces a different N-Quads digest, causing PyNaCl's VerifyKey.verify to raise a BadSignatureError, immediately rejecting the forged credential.",
         "akta/vc.py, tests/test_vc.py (test_tampered_credential_fails_verification)",
         "Offer to demonstrate this test live; it is validated in test_vc.py."),

        ("Q9: What happens if an agent's private key is leaked or stolen?",
         "Domain 3: Cryptography & Verification",
         "Testing incident response and revocation mechanisms.",
         "Because did:key binds identity immutably to the public key, key rotation requires generating a new keypair and did:key identifier. The administrator invokes POST /api/v1/registry/revoke, which immediately marks the compromised agent as REVOKED in stored_vcs and agent_trust_states, locking its trust score to 0.0 and terminating all active collaboration sessions.",
         "akta/vdr/registry_router.py (revoke_agent), akta/vdr/registry_crud.py",
         "Never state that the leaked key can be 'fixed'. The old DID must be permanently decommissioned."),

        # Domain 4: Behavioral Telemetry & Scoring
        ("Q10: What are the three telemetry metrics captured for every agent interaction?",
         "Domain 4: Behavioral Telemetry",
         "Evaluating runtime observability implementation.",
         "Every interaction captures a TelemetryEvent with three normalized metrics: 1. Success Factor S_i(t) in [0.0, 1.0], measuring functional correctness. 2. Policy Compliance Factor C_i(t) in [0.0, 1.0], validating schema adherence and security protocol conformance. 3. Latency Penalty L_i(t) = min(latency_ms / 2000, 1.0), penalizing execution times against our 2000ms SLA threshold.",
         "akta/trust_engine.py (compute_instantaneous_performance), akta/vdr/models.py (TelemetryLog)",
         "Be precise: latency is normalized against a 2000-millisecond threshold."),

        ("Q11: Why are the weights 0.6 for Success, 0.3 for Compliance, and 0.1 for Latency?",
         "Domain 4: Behavioral Telemetry",
         "Testing security prioritization reasoning.",
         "The weights reflect enterprise mission-critical priorities. Correctness (0.6) is paramount: an agent that returns wrong answers has zero utility. Security compliance (0.3) is vital: prompt leakage or protocol breaches must immediately degrade trust. Latency (0.1) is an operational efficiency factor: an agent that is slow but correct and secure should receive a mild penalty, but should never be quarantined solely due to high network traffic.",
         "akta/trust_engine.py, docs/presentation/TrustChain_AI_Slide_Assets/telemetry_pipeline.png",
         "Acknowledge that these weights are empirically established constants, not machine-learned."),

        ("Q12: How is telemetry data protected from agent spoofing?",
         "Domain 4: Behavioral Telemetry",
         "Testing sensor architecture security assumptions.",
         "Telemetry events are not self-reported by the worker agent. They are captured and signed by the API Gateway or supervisory proxy (LocalAgentConnector) that monitors the interaction. Each telemetry record in telemetry_logs includes the raw timestamp, input payload hash, and sensor signature.",
         "akta/vdr/models.py (TelemetryLog), akta/collaboration_router.py",
         "Acknowledge that compromised internal gateway sensors are treated as out of scope."),

        # Domain 5: EMA Trust Mathematics
        ("Q13: State the exact Exponential Moving Average equation implemented in TrustChain-AI.",
         "Domain 5: EMA Trust Mathematics",
         "Testing mathematical formula recall and precision.",
         "The temporal trust equation is: T_i(t) = 0.7 * T_i(t-1) + 0.3 * P_i(t), where T_i(0) = 1.00 is the initial optimistic trust prior, alpha = 0.7 is the historical memory weight, and beta = 0.3 is the instantaneous performance weight. P_i(t) is computed as 0.6*S + 0.3*C + 0.1*(1 - L).",
         "akta/trust_engine.py (update_trust_score, lines 85-115)",
         "Ensure you state alpha=0.7 and beta=0.3 clearly; they sum to exactly 1.0."),

        ("Q14: Exactly how many complete failures cause a fully trusted agent to be quarantined?",
         "Domain 5: EMA Trust Mathematics",
         "Mathematical stress-test verification.",
         "Exactly TWO complete failures (P=0.00). Round 0: T_0 = 1.000. Round 1: T_1 = 0.7(1.000) + 0.3(0.000) = 0.700 (enters SUSPICIOUS). Round 2: T_2 = 0.7(0.700) + 0.3(0.000) = 0.490. Since 0.490 is strictly below the 0.50 quarantine threshold, the agent is quarantined at Round 2.",
         "docs/presentation/TrustChain_AI_Slide_Assets/trust_timeline.png, tests/test_trust_engine.py",
         "Do not guess 3 or 4 rounds. State the exact mathematical values: 0.700 then 0.490."),

        ("Q15: How many consecutive successful rounds are required for a quarantined agent (T=0.409) to recover to TRUSTED?",
         "Domain 5: EMA Trust Mathematics",
         "Recovery math verification.",
         "An agent requires FOUR consecutive flawless canary rounds (P=0.993) to re-enter TRUSTED (T >= 0.80): Round 6: 0.584 (exits Quarantine to Suspicious). Round 7: 0.706. Round 8: 0.792. Round 9: 0.852 (crosses 0.80 into TRUSTED). A fifth round brings it to 0.895.",
         "docs/presentation/TrustChain_AI_Slide_Assets/trust_timeline.png",
         "Notice that recovery is harder than decay, preventing whitewashing attacks."),

        # Domain 6: Trust States & Lifecycle
        ("Q16: Name all four trust states and their exact numerical thresholds.",
         "Domain 6: Trust States & Lifecycle",
         "State machine threshold verification.",
         "1. TRUSTED: T_i(t) >= 0.80 (full operational privileges). 2. SUSPICIOUS: 0.50 <= T_i(t) < 0.80 (standard tasks allowed; privileged workflows blocked). 3. QUARANTINED: T_i(t) < 0.50 (automated isolation; all production execution blocked). 4. REVOKED: Terminal state, T locked at 0.0, non-recoverable.",
         "akta/trust_engine.py (TrustState enum, _determine_state)",
         "Never state that REVOKED has a numerical threshold; it is an administrative terminal lock."),

        ("Q17: Can an agent transition directly from TRUSTED to QUARANTINED in a single round?",
         "Domain 6: Trust States & Lifecycle",
         "Boundary condition edge testing.",
         "No, under our formula with T_0 = 1.00, the maximum possible single-round decay under total failure (P=0) is T_1 = 0.7*1.0 = 0.700, which lands in SUSPICIOUS. However, an administrative revocation immediately forces the state to REVOKED regardless of previous score.",
         "akta/trust_engine.py",
         "Explain that EMA deliberately buffers against single-round catastrophic false positives."),

        ("Q18: What is the purpose of the SUSPICIOUS state?",
         "Domain 6: Trust States & Lifecycle",
         "Operational security philosophy.",
         "SUSPICIOUS provides a graceful degradation zone. Rather than abruptly terminating an agent due to a temporary network blip or minor latency spike, the agent remains permitted to perform low-risk standard tasks (read, query) while shielding high-risk privileged workflows (delegation, execution).",
         "akta/adaptive_auth.py, docs/blackbook/TrustChain_AI_Blackbook_Part1.md",
         "Highlight the principle of least privilege."),

        # Domain 7: Authorization & RBAC vs ABAC
        ("Q19: Explain the difference between Human RBAC and Autonomous Agent ABAC in your architecture.",
         "Domain 7: Authorization & Security",
         "Evaluating dual-access control architecture.",
         "Human RBAC governs portal operators using static roles: ADMIN (full mutations and user management), OPERATOR (task dispatch and agent monitoring), and VIEWER (read-only audit observability), secured by Argon2id passwords and JWT tokens. Autonomous Agent ABAC dynamically evaluates runtime attributes: the agent's live trust score T_i(t), operational state, and the blast radius of the requested operation (STANDARD vs PRIVILEGED).",
         "akta/auth.py (require_role), akta/adaptive_auth.py (AdaptivePolicyEnforcer)",
         "Do not confuse human portal users with autonomous software agents."),

        ("Q20: What happens when an agent in SUSPICIOUS attempts to execute a workflow?",
         "Domain 7: Authorization & Security",
         "API gateway interception verification.",
         "AdaptivePolicyEnforcer intercepts the request. Because workflow:execute is classified as a PRIVILEGED operation, the enforcer blocks execution, logs a security audit record in security_audit_events with severity WARNING, and returns HTTP 403 Forbidden with detail 'Operation privileged:blocked for state SUSPICIOUS'.",
         "akta/adaptive_auth.py (evaluate_request), tests/test_adaptive_policy.py",
         "State HTTP 403 Forbidden specifically, not 401 Unauthorized."),

        ("Q21: How does your password security prevent brute-force attacks?",
         "Domain 7: Authorization & Security",
         "Security controls verification.",
         "We enforce Argon2id memory-hard password hashing (combining Argon2d for GPU resistance and Argon2i for side-channel resistance) and a 5-strike account lockout policy. After 5 consecutive failed passwords, the account is locked for 15 minutes, rejecting subsequent login attempts with HTTP 423 Locked.",
         "akta/auth/crud.py (authenticate_user), akta/vdr/models.py (User)",
         "Mention HTTP 423 Locked specifically."),

        # Domain 8: Discovery vs Matching
        ("Q22: What is the fundamental difference between Discovery and Matching?",
         "Domain 8: Discovery vs Matching",
         "System design distinction test.",
         "Discovery (/discovery) is an inventory search and availability tool: it evaluates the entire registry against capability tags, availability, and health, providing diagnostic rationales for why agents are eligible or excluded. Matching (/matching) is a task-driven optimization algorithm: it takes a specific task requirement and computes a composite MatchScore across eligible candidates to spotlight the single top recommended agent.",
         "akta/vdr/registry_router.py (/discover vs /match), frontend/src/components/",
         "Do not claim they do the same thing with different UI."),

        ("Q23: Why does Discovery show excluded agents instead of silently hiding them?",
         "Domain 8: Discovery vs Matching",
         "Explainable AI and transparency.",
         "In security operations, silent omission creates ambiguity: an operator cannot tell if an agent is missing, deleted, offline, or quarantined. TrustChain-AI explicitly lists excluded agents with transparent diagnostic rationales (e.g., 'Excluded: Trust score 0.65 below requested slider 0.80'), giving operators complete forensic visibility.",
         "frontend/src/components/DiscoveryCenter.jsx, tests/test_investigation_discovery_matching.py",
         "Explainability is a core requirement for SOC operators."),

        ("Q24: What are the four exclusion rationales surfaced by the Discovery engine?",
         "Domain 8: Discovery vs Matching",
         "Diagnostic engine verification.",
         "1. Policy Exclusion: agent is under behavioral quarantine (T < 0.50). 2. Threshold Exclusion: agent's trust score is below the operator's slider threshold. 3. Availability Exclusion: agent is currently BUSY on an active session. 4. Health Exclusion: agent endpoint probe returned UNHEALTHY or connection refused.",
         "akta/vdr/registry_router.py (discover_agents), DiscoveryCenter.jsx",
         "List all four exact rationale types."),

        # Domain 9: Matching Algorithm & Formulas
        ("Q25: State the composite MatchScore equation and all four of its weights.",
         "Domain 9: Matching Formulation",
         "Algorithmic precision test.",
         "MatchScore = 0.4*T + 0.3*(r/5.0) + 0.2*sigma + 0.1*(1 - lambda). Weights: 0.4 on temporal trust T [0,1]; 0.3 on peer reputation r normalized from [1,5] to [0.2,1.0]; 0.2 on historical success rate sigma [0,1]; 0.1 on latency bonus (1 - lambda), where lambda = min(latency_ms / 2000, 1.0).",
         "akta/vdr/registry_crud.py (find_best_agent_match), tests/test_platform_features.py",
         "Emphasize that the weights sum to exactly 1.0."),

        ("Q26: Why is historical peer reputation divided by 5.0?",
         "Domain 9: Matching Formulation",
         "Dimensional normalization awareness.",
         "Temporal trust, success rate, and latency bonus are all normalized within the unit interval [0.0, 1.0]. Because peer ratings follow standard 5-star ratings in [1.0, 5.0], dividing by 5.0 maps the reputation dimension into [0.2, 1.0], preserving intended mathematical proportionality.",
         "akta/vdr/registry_crud.py",
         "State that this is a classic multi-criteria decision making normalization step."),

        ("Q27: In your benchmark test, which candidate won the matching spotlight and what was its score?",
         "Domain 9: Matching Formulation",
         "Empirical benchmark data verification.",
         "Agent Alpha won the top recommendation spotlight with a composite MatchScore of 0.963 (Trust: 0.392, Reputation: 0.288, Success: 0.194, Latency: 0.089). Agent Beta scored 0.812, Agent Gamma scored 0.655, and Agent Delta was disqualified (score 0.000) due to active quarantine.",
         "docs/presentation/TrustChain_AI_Slide_Assets/matching_breakdown.png",
         "Cite Agent Alpha's exact score of 0.963."),

        # Domain 10: Database Schema & Auditability
        ("Q28: How many database tables exist in your SQLite VDR, and what are the five functional domains?",
         "Domain 10: Database & Storage",
         "Schema mastery verification.",
         "Exactly 13 SQLite tables partitioned across five domains: 1. Identity: stored_vcs, agents. 2. Trust: agent_trust_states, telemetry_logs, trust_audit_trails. 3. Collaboration: collaboration_sessions, collaboration_events, agent_ratings. 4. Workflows: workflows, workflow_nodes. 5. Security: users, refresh_tokens, security_audit_events.",
         "akta/vdr/models.py, docs/presentation/TrustChain_AI_Slide_Assets/database_er_diagram.png",
         "State the exact number: 13 tables."),

        ("Q29: What are the four independent audit streams maintained in the schema?",
         "Domain 10: Database & Storage",
         "Forensic auditability verification.",
         "1. stored_vcs: Credential issuance, claims, and cryptographic revocation status. 2. trust_audit_trails: Immutable state transitions (old_score, new_score, trigger_reason, timestamp). 3. telemetry_logs: Granular interaction telemetry records. 4. security_audit_events: Gateway security events (logins, lockouts, RBAC violations).",
         "akta/vdr/models.py",
         "List all four exact table names."),

        ("Q30: How does SQLite WAL mode achieve sub-5ms latency?",
         "Domain 10: Database & Storage",
         "Database performance engineering.",
         "Standard SQLite rollback journals lock the database during writes. By executing PRAGMA journal_mode=WAL and PRAGMA synchronous=NORMAL, SQLite writes changes to an append-only .wal file, allowing concurrent execution: readers never block writers, and writers never block readers, reducing transaction latencies from >45ms to <3ms.",
         "akta/vdr/database.py",
         "Confirm that WAL mode is active in the repository."),

        # Domain 11: Collaboration & Sequential Workflows
        ("Q31: What are the states in a collaboration session lifecycle?",
         "Domain 11: Collaboration & Workflows",
         "Bilateral state machine verification.",
         "Sessions progress through: PENDING (initiated, mutual did:key and VC exchange verified), ACTIVE (bilateral task payload execution and telemetry streaming), and either COMPLETED (task delivered, mutual ratings stored) or TERMINATED (forced abort upon trust decay or policy breach).",
         "akta/vdr/models.py (CollaborationSession), akta/collaboration_router.py",
         "Explain that state transitions are enforced at the backend."),

        ("Q32: Does your workflow engine support parallel branches?",
         "Domain 11: Collaboration & Workflows",
         "Concurrency boundary academic honesty.",
         "The database schema includes a depends_on field in workflow_nodes supporting DAG dependencies. However, in the current capstone implementation, execution is strictly sequential to guarantee deterministic audit verification. Asynchronous parallel DAG execution is identified as future work.",
         "akta/vdr/models.py (WorkflowNode), tests/test_collaboration.py",
         "Do not claim parallel execution is working in production. State clearly it is sequential."),

        # Domain 12: Testing & Verification Methodology
        ("Q33: How many automated tests exist in your pytest suite, and how fast do they execute?",
         "Domain 12: Testing & Verification",
         "Empirical verification metrics.",
         "Exactly 80 automated unit and integration tests passing in 11.82 seconds with zero failures and zero regressions under Python 3.12 and pytest 9.1.",
         "tests/ (8 test modules), pytest.ini, test logs",
         "State 80 passed in 11.82 seconds."),

        ("Q34: How long does the frontend production build take, and how many modules are bundled?",
         "Domain 12: Testing & Verification",
         "Frontend engineering metrics.",
         "Vite compiles 2,478 modules into an optimized production bundle in dist/ in exactly 19.99 seconds with zero syntax or packaging errors.",
         "frontend/package.json (npm run build), vite output log",
         "State 19.99 seconds and 2,478 modules."),

        # Domain 13 & 14: Threats to Validity & Future Scope
        ("Q35: What is the single biggest threat to validity in TrustChain-AI today?",
         "Domain 13: Threats to Validity",
         "Intellectual maturity and honesty.",
         "The reliance on deterministic simulation via LocalAgentConnector rather than live commercial LLMs. While essential for 100% reproducible testing without external API billing, real-world LLMs exhibit stochastic reasoning variance that remains to be evaluated in wild enterprise environments.",
         "docs/blackbook/TrustChain_AI_Blackbook_Part2.md (Chapter 6)",
         "Examiners deeply respect candidates who acknowledge their evaluation boundaries."),

        ("Q36: What are the four phases of your future research roadmap?",
         "Domain 14: Future Scope",
         "Strategic research roadmap.",
         "Phase 1: Distributed Byzantine VDR Integration (Hedera Hashgraph/Tendermint). Phase 2: Zero-Knowledge Telemetry Proofs (zk-SNARKs) to prove policy compliance without leaking proprietary model weights. Phase 3: Dynamic Reinforcement Learning for Adaptive Weight Tuning. Phase 4: Asynchronous Parallel DAG Workflow Engine.",
         "docs/presentation/TrustChain_AI_Slide_Assets/slides_png/Slide17.PNG",
         "Present the phases in clear sequential order.")
    ]

    for item in questions:
        q_text, domain, intent, answer, code_ref, trap = item
        
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(10)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q_text)
        r_q.bold = True
        r_q.font.name = "Calibri"
        r_q.font.size = Pt(11)
        r_q.font.color.rgb = RGBColor(15, 23, 42)

        p_cat = doc.add_paragraph()
        p_cat.paragraph_format.space_after = Pt(4)
        r_cat = p_cat.add_run(f"Domain: {domain}   |   Examiner Trap: {intent}")
        r_cat.font.name = "Calibri"
        r_cat.font.size = Pt(9)
        r_cat.font.italic = True
        r_cat.font.color.rgb = RGBColor(100, 116, 139)

        add_callout(doc, "Authoritative Response", answer, border_hex=HEX_GREEN, bg_hex="ECFDF5")

        p_ground = doc.add_paragraph()
        p_ground.paragraph_format.space_before = Pt(2)
        p_ground.paragraph_format.space_after = Pt(1)
        r_g = p_ground.add_run(f"Technical Codebase Anchor: {code_ref}")
        r_g.bold = True
        r_g.font.name = "Consolas"
        r_g.font.size = Pt(9)
        r_g.font.color.rgb = RGBColor(30, 41, 59)

        p_trap = doc.add_paragraph()
        p_trap.paragraph_format.space_after = Pt(8)
        r_t = p_trap.add_run(f"Defense Caution (What NOT to say): {trap}")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(9.5)
        r_t.font.italic = True
        r_t.font.color.rgb = RGBColor(185, 28, 28)

    doc.save(DOCX_PATH)
    print("TrustChain_AI_External_Viva_Prep.docx successfully created at:", DOCX_PATH)
    print("File size:", os.path.getsize(DOCX_PATH), "bytes")

if __name__ == "__main__":
    build_viva_prep()
