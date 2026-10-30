# -*- coding: utf-8 -*-
"""
generate_flowcharts.py
Generates the Discovery Flowchart, Matching Flowchart, and Auth Matrix assets.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs", "presentation", "TrustChain_AI_Slide_Assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

# 1. Discovery Flowchart
def create_discovery_flowchart():
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    steps = [
        ("Query & Tag Filter", "Operator inputs capability\n(e.g., 'analysis', 'coding')\nFilter against stored_vcs", 0.5, 3.2, CYAN),
        ("Threshold Slider", "Set minimum trust slider\nRange: 0.00 to 1.00\nEvaluates live T_i(t)", 2.8, 3.2, CYAN),
        ("Availability Probe", "Verify operational state:\nAVAILABLE vs BUSY\nPrevents double booking", 5.1, 3.2, AMBER),
        ("Endpoint Health Ping", "Probe agent HTTP URL\nVerify 200 OK & latency\nChecks reachable status", 7.4, 3.2, GREEN)
    ]

    for title, desc, x, y, col in steps:
        box = patches.FancyBboxPatch((x, y), 2.0, 1.4, boxstyle="round,pad=0.08",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 1.0, y + 1.15, title, color=col, fontsize=8.5, fontweight='bold', ha='center')
        ax.text(x + 1.0, y + 0.5, desc, color=WHITE, fontsize=7.5, ha='center')

        if x < 7.0:
            ax.annotate('', xy=(x + 2.3, y + 0.7), xytext=(x + 2.0, y + 0.7),
                        arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.5))

    # Bottom Explainable Decisions
    bot_l = patches.FancyBboxPatch((0.5, 0.6), 4.3, 1.8, boxstyle="round,pad=0.08",
                                  facecolor=PANEL_ALT, edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(bot_l)
    ax.text(0.7, 2.05, "ELIGIBLE CANDIDATE CLASSIFICATION", color=GREEN, fontsize=9.5, fontweight='bold')
    ax.text(0.7, 1.1, "• Status Pill: [ ELIGIBLE ]\n• Rationale: 'Meets capability, trust threshold, operational\n  status, and endpoint health criteria.'\n• Action: Enabled 'Investigate' drawer & 'Engage' buttons.", color=WHITE, fontsize=8)

    bot_r = patches.FancyBboxPatch((5.1, 0.6), 4.4, 1.8, boxstyle="round,pad=0.08",
                                  facecolor=PANEL_ALT, edgecolor=RED, linewidth=1.5)
    ax.add_patch(bot_r)
    ax.text(5.3, 2.05, "EXCLUDED CANDIDATE DIAGNOSTICS", color=RED, fontsize=9.5, fontweight='bold')
    ax.text(5.3, 1.1, "• Quarantine: 'Under behavioral quarantine (T = 0.42 < 0.50)'\n• Threshold: 'Trust score (0.65) below requested slider (0.80)'\n• Availability: 'Operational status is BUSY on active session'\n• Health: 'Endpoint probe returned UNHEALTHY (timeout)'", color=WHITE, fontsize=7.8)

    save_fig(fig, "discovery_flowchart.png")

# 2. Matching Flowchart
def create_matching_flowchart():
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    stages = [
        ("1. Task Requirements", "Operator task description\nRequired capability tag\nRequested min trust T_min", 0.4, 3.2, 2.0, CYAN),
        ("2. Eligibility Filter", "Filter out busy agents\nFilter out state < T_min\nExclude quarantined agents", 2.8, 3.2, 2.0, AMBER),
        ("3. Multi-Factor Formula", "MatchScore = 0.4*T\n+ 0.3*(r/5) + 0.2*sigma\n+ 0.1*(1 - lambda)", 5.2, 3.2, 2.1, GREEN),
        ("4. Candidate Ranking", "Sort by MatchScore desc\nGenerate score chips\nSelect top recommendation", 7.6, 3.2, 2.0, PURPLE)
    ]

    for title, desc, x, y, w, col in stages:
        box = patches.FancyBboxPatch((x, y), w, 1.5, boxstyle="round,pad=0.08",
                                     facecolor=PANEL_DARK, edgecolor=col, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + 1.2, title, color=col, fontsize=8.5, fontweight='bold', ha='center')
        ax.text(x + w/2, y + 0.5, desc, color=WHITE, fontsize=7.5, ha='center')

        if x < 7.0:
            ax.annotate('', xy=(x + w + 0.3, y + 0.75), xytext=(x + w, y + 0.75),
                        arrowprops=dict(arrowstyle="->", color=WHITE, lw=1.5))

    # Bottom Result Box
    bot = patches.FancyBboxPatch((0.4, 0.5), 9.2, 1.9, boxstyle="round,pad=0.08",
                                 facecolor=PANEL_ALT, edgecolor=CYAN, linewidth=1.5)
    ax.add_patch(bot)
    ax.text(0.65, 2.05, "TOP CANDIDATE RECOMMENDATION SPOTLIGHT CARD", color=CYAN, fontsize=10, fontweight='bold')
    ax.text(0.65, 1.5, "• Glowing Recommendation Card: Agent Alpha (MatchScore: 0.963 / 1.000)\n• Explainability Chips: [Trust: 0.392 (40%)]  [Rep: 0.288 (30%)]  [Success: 0.194 (20%)]  [Latency: 0.089 (10%)]\n• Zero-Trust Disqualification: Quarantined agents forced to 0.0 ('REJECTED BY POLICY') regardless of reputation.", color=WHITE, fontsize=8)
    ax.text(0.65, 0.8, "• One-Click Action: Instant 'Assign Workload' initiates secure bilateral session handshake.", color=GREEN, fontsize=8, fontweight='bold')

    save_fig(fig, "matching_flowchart.png")

# 3. Auth Matrix
def create_auth_matrix():
    fig, ax = plt.subplots(figsize=(10, 5.2), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    # Left: Human RBAC
    box_l = patches.FancyBboxPatch((0.4, 0.5), 4.3, 4.2, boxstyle="round,pad=0.08",
                                  facecolor=PANEL_DARK, edgecolor=PURPLE, linewidth=1.5)
    ax.add_patch(box_l)
    ax.text(0.6, 4.3, "HUMAN OPERATOR RBAC (JWT + ARGON2ID)", color=PURPLE, fontsize=9.5, fontweight='bold')
    ax.text(0.6, 3.8, "• ADMIN Role:\n  Full access: user management, manual trust\n  adjustment, policy configuration, system metrics.", color=WHITE, fontsize=8)
    ax.text(0.6, 2.9, "• OPERATOR Role:\n  Agent execution, task dispatch, discovery filtering,\n  matching review, collaboration monitoring.", color=WHITE, fontsize=8)
    ax.text(0.6, 2.0, "• VIEWER Role:\n  Read-only observability: metrics, audit logs,\n  trust history. Mutation actions disabled in UI.", color=WHITE, fontsize=8)
    ax.text(0.6, 1.1, "• 5-Strike Lockout Policy:\n  5 failed login attempts -> 15-minute lock.\n  Argon2id memory-hard password protection.", color=AMBER, fontsize=7.8)

    # Right: Agent ABAC
    box_r = patches.FancyBboxPatch((5.1, 0.5), 4.5, 4.2, boxstyle="round,pad=0.08",
                                  facecolor=PANEL_DARK, edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(box_r)
    ax.text(5.3, 4.3, "AUTONOMOUS AGENT ABAC (DYNAMIC GATING)", color=GREEN, fontsize=9.5, fontweight='bold')
    ax.text(5.3, 3.8, "• TRUSTED (T >= 0.80):\n  ALLOWED: Standard tasks & Privileged workflows.", color=GREEN, fontsize=8)
    ax.text(5.3, 3.0, "• SUSPICIOUS (0.50 <= T < 0.80):\n  ALLOWED: Standard tasks (read, query, map).\n  BLOCKED (HTTP 403): Privileged workflows.", color=AMBER, fontsize=8)
    ax.text(5.3, 2.1, "• QUARANTINED (T < 0.50):\n  BLOCKED (HTTP 403): All production execution.\n  ALLOWED: Supervised canary remediation tasks.", color=RED, fontsize=8)
    ax.text(5.3, 1.2, "• REVOKED (Terminal):\n  BLOCKED (HTTP 403): Total permanent exclusion.\n  T locked at 0.0; non-recoverable via telemetry.", color="#E11D48", fontsize=8)

    save_fig(fig, "auth_matrix.png")

if __name__ == "__main__":
    create_discovery_flowchart()
    create_matching_flowchart()
    create_auth_matrix()
    print("Flowcharts and matrix assets created.")
