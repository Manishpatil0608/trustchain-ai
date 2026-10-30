# -*- coding: utf-8 -*-
"""
generate_diagram_assets.py
Generates high-resolution visual diagrams and charts for TrustChain-AI presentation:
1. architecture_diagram.png (5-Tier Layered Architecture)
2. did_vc_lifecycle.png (DID & VC Cryptographic Lifecycle)
3. telemetry_pipeline.png (Telemetry Ingestion & Scoring Flow)
4. trust_state_machine.png (4-State Transition Diagram)
5. auth_matrix.png (RBAC & ABAC Security Gating)
6. discovery_flowchart.png (Discovery Eligibility Flowchart)
7. matching_flowchart.png (Matching & Ranking Flowchart)
8. collaboration_sequence.png (Bilateral Collaboration Sequence)
9. database_er_diagram.png (13-Table Schema ER Diagram)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs", "presentation", "TrustChain_AI_Slide_Assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Theme Colors
BG_DARK = "#080E1A"
PANEL_DARK = "#111C35"
PANEL_ALT = "#0C1426"
BORDER_BLUE = "#1E3A6E"
CYAN = "#00F0FF"
GREEN = "#00E676"
AMBER = "#FFB300"
RED = "#FF3D71"
PURPLE = "#9D4EDD"
WHITE = "#F8FAFC"
SLATE = "#94A3B8"

def save_fig(fig, filename):
    p = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(p, dpi=300, bbox_inches='tight', facecolor=BG_DARK, edgecolor='none')
    plt.close(fig)
    print(f"Generated: {filename} ({os.path.getsize(p)} bytes)")

# ------------------------------------------------------------------------------
# 1. 5-Tier Architecture Diagram
# ------------------------------------------------------------------------------
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    tiers = [
        ("TIER 1: PRESENTATION TIER (PORT 5173)", 
         "React 19 + Vite Frontend  ·  Tailwind CSS SOC Theme  ·  Lucide Icons  ·  Headless UI",
         "[Executive Dashboard]   [Agent Explorer]   [Discovery Center]   [Matching Center]   [User Admin]",
         CYAN, 5.8, 0.95),
        ("TIER 2: API GATEWAY & ROUTING (PORT 8050)",
         "FastAPI ASGI Server  ·  CORS Middleware  ·  JWT Token Verification  ·  Argon2id RBAC  ·  Security Headers",
         "[/api/v1/auth]       [/api/v1/registry]       [/api/v1/collaboration]       [/health (Probes)]",
         PURPLE, 4.4, 0.95),
        ("TIER 3: TRUST INTELLIGENCE & GOVERNANCE",
         "TrustEngine (EMA Math)  ·  AdaptivePolicyEnforcer (ABAC Gating)  ·  LocalAgentConnector (Simulation)",
         "[Instantaneous P_i(t)]       [Temporal EMA T_i(t)]       [Discrete State Engine: 4 States]",
         GREEN, 3.0, 0.95),
        ("TIER 4: CRYPTOGRAPHIC IDENTITY LAYER",
         "PyNaCl: Ed25519 32-byte Keypairs  ·  did:key Multicodec 0xED01  ·  PyLD: URDNA2015 JSON-LD Proofs",
         "[Algorithm-derived DIDs]       [Self-Sovereign Resolution]       [Ed25519Signature2020 Proofs]",
         CYAN, 1.6, 0.95),
        ("TIER 5: LOCAL VERIFIABLE DATA REGISTRY (VDR)",
         "SQLite 3 Engine in WAL Mode  ·  PRAGMA synchronous=NORMAL  ·  Exactly 13 Relational Tables",
         "[stored_vcs]   [agent_trust_states]   [telemetry_logs]   [trust_audit_trails]   [security_audit_events]",
         AMBER, 0.2, 0.95)
    ]

    for title, sub, comps, col, y, h in tiers:
        # Box
        rect = patches.FancyBboxPatch((0.5, y), 9.0, h, boxstyle="round,pad=0.1,rounding_size=0.12",
                                      facecolor=PANEL_DARK, edgecolor=col, linewidth=1.8)
        ax.add_patch(rect)
        # Title
        ax.text(0.75, y + h - 0.22, title, color=col, fontsize=10.5, fontweight='bold', fontfamily='sans-serif')
        # Subtitle
        ax.text(0.75, y + h - 0.48, sub, color=WHITE, fontsize=8.5, fontfamily='sans-serif')
        # Components
        ax.text(0.75, y + 0.16, comps, color=SLATE, fontsize=8, fontfamily='monospace')

        # Flow Arrow between tiers
        if y > 0.5:
            ax.annotate('', xy=(5.0, y - 0.05), xytext=(5.0, y - 0.25),
                        arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.5))

    save_fig(fig, "architecture_diagram.png")

# ------------------------------------------------------------------------------
# 2. DID & VC Lifecycle Diagram
# ------------------------------------------------------------------------------
def create_did_vc_lifecycle():
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    steps = [
        ("Step 1: Keypair Gen", "PyNaCl / libsodium\n32-byte Ed25519\nSeed & Public Key", 0.5, 3.2, CYAN),
        ("Step 2: Multicodec", "Prepend 0xED01\n(Ed25519 indicator)\nRaw 34-byte array", 2.4, 3.2, CYAN),
        ("Step 3: Base58-btc", "Encode via Base58\nPrefix with 'z'\ndid:key:z6Mkp...", 4.3, 3.2, CYAN),
        ("Step 4: VC Issuance", "W3C JSON-LD\nClaims & Capabilities\nIssuer Platform DID", 6.2, 3.2, GREEN),
        ("Step 5: Canonicalize", "PyLD: URDNA2015\nStandardized N-Quads\nSHA-256 Digest", 8.1, 3.2, GREEN),
    ]

    for title, desc, x, y, col in steps:
        box = patches.FancyBboxPatch((x, y), 1.5, 1.4, boxstyle="round,pad=0.08",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 0.75, y + 1.15, title, color=col, fontsize=9, fontweight='bold', ha='center')
        ax.text(x + 0.75, y + 0.55, desc, color=WHITE, fontsize=7.5, ha='center')

        # Forward Arrow
        if x < 8.0:
            ax.annotate('', xy=(x + 1.8, y + 0.7), xytext=(x + 1.5, y + 0.7),
                        arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.5))

    # Bottom Verification & Storage Block
    bot1 = patches.FancyBboxPatch((0.5, 0.6), 4.3, 1.8, boxstyle="round,pad=0.08",
                                  facecolor=PANEL_ALT, edgecolor=PURPLE, linewidth=1.5)
    ax.add_patch(bot1)
    ax.text(0.7, 2.05, "Step 6: Cryptographic Proof Signing", color=PURPLE, fontsize=10, fontweight='bold')
    ax.text(0.7, 1.6, "• Apply Ed25519Signature2020 using issuer private key\n• Embed proof object: type, created, verificationMethod, jws\n• Verifiable by any node without querying central CA", color=WHITE, fontsize=8)

    bot2 = patches.FancyBboxPatch((5.2, 0.6), 4.4, 1.8, boxstyle="round,pad=0.08",
                                  facecolor=PANEL_ALT, edgecolor=AMBER, linewidth=1.5)
    ax.add_patch(bot2)
    ax.text(5.4, 2.05, "Step 7: VDR Storage & Verification", color=AMBER, fontsize=10, fontweight='bold')
    ax.text(5.4, 1.6, "• Record in stored_vcs SQLite table with is_revoked=False\n• Runtime verification: extracts issuer public key from did:key\n• Checks cryptographic signature + local revocation status", color=WHITE, fontsize=8)

    save_fig(fig, "did_vc_lifecycle.png")

# ------------------------------------------------------------------------------
# 3. Telemetry Pipeline Diagram
# ------------------------------------------------------------------------------
def create_telemetry_pipeline():
    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Pipeline blocks
    nodes = [
        ("1. Task Execution Event", "Task payload processed\nResponse latency measured\nSchema compliance validated", 0.4, 2.8, 1.8, 1.5, CYAN),
        ("2. Multi-Factor Normalization", "Success: S in [0,1]\nCompliance: C in [0,1]\nLatency: L = min(ms/2000, 1)", 2.7, 2.8, 2.0, 1.5, CYAN),
        ("3. Instantaneous Performance", "P_i(t) = 0.6*S + 0.3*C + 0.1*(1 - L)\nWeights sum to 1.0\nStrict security bounds", 5.2, 2.8, 2.1, 1.5, GREEN),
        ("4. Temporal Smoothing", "T_i(t) = 0.7*T_{t-1} + 0.3*P_i(t)\nInitial prior T_0 = 1.00\nContinuous EMA score", 7.7, 2.8, 1.9, 1.5, GREEN),
    ]

    for title, desc, x, y, w, h, col in nodes:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.28, title, color=col, fontsize=8.5, fontweight='bold', ha='center')
        ax.text(x + w/2, y + 0.55, desc, color=WHITE, fontsize=7.5, ha='center')

        if x < 7.5:
            ax.annotate('', xy=(x + w + 0.25, y + h/2), xytext=(x + w, y + h/2),
                        arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.5))

    # Bottom State Output
    bot = patches.FancyBboxPatch((0.4, 0.5), 9.2, 1.6, boxstyle="round,pad=0.08",
                                 facecolor=PANEL_ALT, edgecolor=PURPLE, linewidth=1.5)
    ax.add_patch(bot)
    ax.text(0.7, 1.7, "5. Discrete State Classification & Policy Enforcement Action", color=PURPLE, fontsize=10, fontweight='bold')
    ax.text(0.7, 1.15, "• T >= 0.80  -> TRUSTED: Full standard & privileged operation authorization granted.\n• 0.50 <= T < 0.80 -> SUSPICIOUS: Standard tasks permitted; privileged workflows blocked (HTTP 403).\n• T < 0.50   -> QUARANTINED: All operational execution halted; isolated to supervised canary tasks.", color=WHITE, fontsize=8.5)

    save_fig(fig, "telemetry_pipeline.png")

# ------------------------------------------------------------------------------
# 4. Trust State Machine Diagram
# ------------------------------------------------------------------------------
def create_state_machine_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # 4 State Circles/Boxes
    states = [
        ("TRUSTED", "T >= 0.80\nBaseline Prior T_0 = 1.0\nAll Operations Allowed", 1.0, 3.2, 2.2, 1.5, GREEN),
        ("SUSPICIOUS", "0.50 <= T < 0.80\nPrivileged Blocked (403)\nStandard Allowed", 4.0, 3.2, 2.2, 1.5, AMBER),
        ("QUARANTINED", "T < 0.50\nTotal Operational Block\nSupervised Canary Only", 7.0, 3.2, 2.2, 1.5, RED),
        ("REVOKED", "T locked at 0.0\nCryptographic Compromise\nTerminal State (Non-Recoverable)", 4.0, 0.6, 2.8, 1.5, "#E11D48"),
    ]

    for name, desc, x, y, w, h, col in states:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=2.0)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.35, name, color=col, fontsize=11, fontweight='bold', ha='center')
        ax.text(x + w/2, y + 0.45, desc, color=WHITE, fontsize=8, ha='center')

    # Transitions (Arrows & Annotations)
    # Trusted -> Suspicious
    ax.annotate('', xy=(3.95, 4.1), xytext=(3.25, 4.1),
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=2.0))
    ax.text(3.6, 4.25, "Decay\nT < 0.80", color=AMBER, fontsize=7.5, ha='center')

    # Suspicious -> Quarantined
    ax.annotate('', xy=(6.95, 4.1), xytext=(6.25, 4.1),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))
    ax.text(6.6, 4.25, "Decay\nT < 0.50", color=RED, fontsize=7.5, ha='center')

    # Quarantined -> Suspicious (Recovery)
    ax.annotate('', xy=(6.25, 3.6), xytext=(6.95, 3.6),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0))
    ax.text(6.6, 3.35, "Canary\nT >= 0.50", color=GREEN, fontsize=7.5, ha='center')

    # Suspicious -> Trusted (Recovery)
    ax.annotate('', xy=(3.25, 3.6), xytext=(3.95, 3.6),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0))
    ax.text(3.6, 3.35, "Restored\nT >= 0.80", color=GREEN, fontsize=7.5, ha='center')

    # Any -> Revoked (Downward)
    for sx in [2.1, 5.1, 8.1]:
        ax.annotate('', xy=(5.4, 2.15), xytext=(sx, 3.15),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.2, ls="--"))
    ax.text(5.4, 2.4, "Manual Admin Revocation / Cryptographic Tampering Detected", color=RED, fontsize=8, ha='center', fontweight='bold')

    save_fig(fig, "trust_state_machine.png")

# ------------------------------------------------------------------------------
# 5. Database ER Diagram (13 Tables)
# ------------------------------------------------------------------------------
def create_database_er_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.2), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    domains = [
        ("DOMAIN 1: IDENTITY & VCS", 0.4, 3.5, 2.8, 2.4, CYAN, [
            ("stored_vcs", "vc_id, issuer_did, subject_did, claims, proof, is_revoked"),
            ("agents", "did, name, capabilities, endpoint_url, created_at")
        ]),
        ("DOMAIN 2: TRUST & METRICS", 3.6, 3.5, 3.0, 2.4, GREEN, [
            ("agent_trust_states", "did, trust_score, state, last_evaluated"),
            ("telemetry_logs", "log_id, agent_did, success, compliance, latency, signature"),
            ("trust_audit_trails", "trail_id, did, old_score, new_score, trigger_reason, ts")
        ]),
        ("DOMAIN 3: WORKFLOWS & NODES", 7.0, 3.5, 2.6, 2.4, PURPLE, [
            ("workflows", "workflow_id, name, status, created_at"),
            ("workflow_nodes", "node_id, workflow_id, step_order, agent_did, depends_on")
        ]),
        ("DOMAIN 4: COLLABORATION", 0.4, 0.4, 4.4, 2.6, AMBER, [
            ("collaboration_sessions", "session_id, initiator_did, target_did, status, token"),
            ("collaboration_events", "event_id, session_id, step_index, payload, signature"),
            ("agent_ratings", "rating_id, rater_did, rated_did, rating_score (1-5), comments")
        ]),
        ("DOMAIN 5: AUTH & SECURITY", 5.2, 0.4, 4.4, 2.6, RED, [
            ("users", "user_id, username, password_hash (Argon2id), role, locked_until"),
            ("refresh_tokens", "token_id, user_id, token_hash, expires_at, revoked"),
            ("security_audit_events", "event_id, event_type, severity, details, ip_address, ts")
        ])
    ]

    for title, x, y, w, h, col, tables in domains:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 0.15, y + h - 0.25, title, color=col, fontsize=9, fontweight='bold')

        ty = y + h - 0.55
        for tname, cols in tables:
            ax.text(x + 0.15, ty, f"• {tname}", color=WHITE, fontsize=8, fontweight='bold')
            ax.text(x + 0.25, ty - 0.22, cols, color=SLATE, fontsize=6.8, fontfamily='monospace')
            ty -= 0.55

    save_fig(fig, "database_er_diagram.png")

# ------------------------------------------------------------------------------
# 6. Collaboration Sequence Diagram
# ------------------------------------------------------------------------------
def create_collaboration_sequence():
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # Entities (Top lifelines)
    entities = [
        ("Agent A (Initiator)", 1.5, CYAN),
        ("FastAPI Gateway & Policy", 5.0, PURPLE),
        ("Agent B (Target Worker)", 8.5, GREEN)
    ]

    for name, x, col in entities:
        box = patches.FancyBboxPatch((x - 1.2, 4.8), 2.4, 0.5, boxstyle="round,pad=0.05",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, 5.05, name, color=col, fontsize=8.5, fontweight='bold', ha='center')
        # Lifeline
        ax.plot([x, x], [0.6, 4.75], color=BORDER_BLUE, lw=1.2, ls="--")

    # Sequence Steps
    steps = [
        (4.3, 1.5, 5.0, "1. POST /collaboration/initiate (signed session request)", CYAN, "->"),
        (3.8, 5.0, 5.0, "2. Verify DIDs, VCs & Live Trust States (T >= 0.80 required)", WHITE, "self"),
        (3.3, 5.0, 8.5, "3. Dispatch task payload with session token", PURPLE, "->"),
        (2.8, 8.5, 5.0, "4. Return task result & execution telemetry (ms)", GREEN, "->"),
        (2.3, 5.0, 5.0, "5. Update TrustEngine: compute P_i(t) & T_i(t)", AMBER, "self"),
        (1.8, 5.0, 5.0, "6. Check Mid-Session Boundary: if T < 0.50 -> HALT SESSION", RED, "self"),
        (1.3, 5.0, 1.5, "7. Deliver verified result & audit confirmation", CYAN, "->"),
        (0.8, 1.5, 5.0, "8. Submit peer rating r in [1, 5] -> stored in agent_ratings", AMBER, "->")
    ]

    for y, x1, x2, text, col, arrow_type in steps:
        if arrow_type == "self":
            # Self loop at gateway
            ax.annotate('', xy=(x1 + 0.1, y - 0.15), xytext=(x1 + 0.1, y + 0.15),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.5,
                                        connectionstyle="arc3,rad=-0.8"))
            ax.text(x1 + 0.5, y, text, color=col, fontsize=7.5, va='center')
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.5))
            ax.text((x1 + x2)/2, y + 0.12, text, color=col, fontsize=7.5, ha='center')

    save_fig(fig, "collaboration_sequence.png")

if __name__ == "__main__":
    create_architecture_diagram()
    create_did_vc_lifecycle()
    create_telemetry_pipeline()
    create_state_machine_diagram()
    create_database_er_diagram()
    create_collaboration_sequence()
    print("All visual diagrams generated successfully.")
