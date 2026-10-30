# -*- coding: utf-8 -*-
"""
generate_charts.py
Generates high-resolution publication-quality matplotlib charts for TrustChain-AI Presentation.
Includes:
1. Chart 1: Trust Degradation & Recovery Timeline (Slide 9) - Exactly recalculated 10 rounds, labeled illustrative.
2. Chart 2: Matching Score Multi-Factor Breakdown (Slide 12) - Transparent breakdown for Alpha (0.963), Beta (0.812), Gamma (0.655), Delta (0.000).
3. Chart 3: Verified Test Suite Results Distribution (Slide 16) - 80/80 passing tests in 15.04s.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_dirs = [
    os.path.join(BASE_DIR, "docs", "presentation", "TrustChain_AI_Slide_Assets"),
    os.path.join(BASE_DIR, "docs", "presentation", "final", "assets")
]

for d in output_dirs:
    os.makedirs(d, exist_ok=True)

# Common styling
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['axes.edgecolor'] = '#2A4B8D'
plt.rcParams['axes.linewidth'] = 1.2

# ==============================================================================
# Chart 1: Trust Degradation & Recovery Timeline (Slide 9)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.5, 4.4), facecolor='#0B132B')
ax.set_facecolor('#080E1A')

rounds = np.arange(0, 11)
# Exactly recalculated with Ti(t) = 0.7 * Ti(t-1) + 0.3 * Pi(t)
# R0: 1.000
# R1: P=0.994 -> 0.998
# R2: P=0.988 -> 0.995
# R3: P=0.460 (latency spike) -> 0.835
# R4: P=0.000 (failure 1) -> 0.584 (Suspicious)
# R5: P=0.000 (failure 2) -> 0.409 (Quarantined, T < 0.50)
# R6: P=0.991 (canary 1) -> 0.584 (Suspicious, exits quarantine)
# R7: P=0.992 (canary 2) -> 0.706
# R8: P=0.993 (canary 3) -> 0.792
# R9: P=0.993 (canary 4) -> 0.852 (Trusted, T >= 0.80)
# R10: P=0.994 (restored) -> 0.895
trust_scores = [1.000, 0.998, 0.995, 0.835, 0.584, 0.409, 0.584, 0.706, 0.792, 0.852, 0.895]

# Zone fills
ax.axhspan(0.8, 1.05, color='#00E676', alpha=0.15, label='TRUSTED Zone (T >= 0.80)')
ax.axhspan(0.5, 0.8, color='#FFB300', alpha=0.15, label='SUSPICIOUS Zone (0.50 <= T < 0.80)')
ax.axhspan(0.0, 0.5, color='#FF3D71', alpha=0.15, label='QUARANTINED Zone (T < 0.50)')

# Threshold lines
ax.axhline(0.8, color='#00E676', linestyle='--', linewidth=1.5, alpha=0.8)
ax.axhline(0.5, color='#FFB300', linestyle='--', linewidth=1.5, alpha=0.8)

# Plot line and points
ax.plot(rounds, trust_scores, color='#00F0FF', linewidth=3, marker='o', markersize=7, 
        markerfacecolor='#FFFFFF', markeredgecolor='#00F0FF', markeredgewidth=2, label='Temporal Trust Ti(t)')

# Annotations
ax.annotate('Initial State\nT=1.000', xy=(0, 1.0), xytext=(0.4, 1.02),
            color='#FFFFFF', fontsize=8.5, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#00F0FF', lw=1.2))

ax.annotate('Quarantine Breach\n(T_5 = 0.409 < 0.50)', xy=(5, 0.409), xytext=(3.4, 0.22),
            color='#FF3D71', fontsize=8.5, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#FF3D71', lw=1.5))

ax.annotate('Canary Recovery Begins\n(R6: T_6 = 0.584, exits quarantine)', xy=(6, 0.584), xytext=(5.3, 0.70),
            color='#FFB300', fontsize=8.5, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#FFB300', lw=1.5))

ax.annotate('Restored to Trusted\n(R9: T_9 = 0.852 >= 0.80)', xy=(9, 0.852), xytext=(7.4, 0.98),
            color='#00E676', fontsize=8.5, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#00E676', lw=1.5))

ax.set_title('Temporal Trust Score Dynamics: Degradation & Recovery Timeline\n[ Ti(t) = 0.7·Ti(t-1) + 0.3·Pi(t)  |  Calculated Illustrative Scenario — Not Measured Production Data ]', 
             fontsize=10.5, color='#FFFFFF', fontweight='bold', pad=12)
ax.set_xlabel('Telemetry Observation Round (t)', color='#94A3B8', fontsize=10, labelpad=8)
ax.set_ylabel('Temporal Trust Score Ti(t)', color='#94A3B8', fontsize=10, labelpad=8)
ax.set_xlim(-0.3, 10.3)
ax.set_ylim(0.0, 1.08)
ax.set_xticks(rounds)
ax.tick_params(colors='#94A3B8', labelsize=9)
ax.grid(color='#1E3A6E', linestyle=':', linewidth=0.8, alpha=0.6)

legend = ax.legend(loc='lower left', facecolor='#111C35', edgecolor='#2A4B8D', fontsize=8)
for text in legend.get_texts():
    text.set_color('#CBD5E1')

plt.tight_layout()
for d in output_dirs:
    c1_path = os.path.join(d, "trust_timeline.png")
    plt.savefig(c1_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved Chart 1: trust_timeline.png")

# ==============================================================================
# Chart 2: Matching Score Multi-Factor Breakdown (Slide 12)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.5, 4.4), facecolor='#0B132B')
ax.set_facecolor('#080E1A')

# 4 Candidate Agents displayed bottom-to-top: Delta (Quarantined), Gamma (#3), Beta (#2), Alpha (Top Match)
candidates = [
    'Agent Delta\n[QUARANTINED]',
    'Agent Gamma\n[ELIGIBLE #3]',
    'Agent Beta\n[ELIGIBLE #2]',
    'Agent Alpha\n[TOP MATCH]'
]

# Breakdown components: [Trust (w=0.4), Reputation (w=0.3), Success Rate (w=0.2), Latency Bonus (w=0.1)]
# Alpha: T=0.95 (0.380) + r=4.8/5 (0.288) + succ=1.0 (0.200) + lat=100ms (0.095) = 0.963
# Beta:  T=0.85 (0.340) + r=4.2/5 (0.252) + succ=0.85 (0.170) + lat=1000ms (0.050) = 0.812
# Gamma: T=0.65 (0.260) + r=3.5/5 (0.210) + succ=0.75 (0.150) + lat=1300ms (0.035) = 0.655
# Delta: Quarantined -> All contributions forced to 0.000 by Policy Gateway Interceptor
trust_comp = np.array([0.000, 0.260, 0.340, 0.380])
rep_comp   = np.array([0.000, 0.210, 0.252, 0.288])
succ_comp  = np.array([0.000, 0.150, 0.170, 0.200])
lat_comp   = np.array([0.000, 0.035, 0.050, 0.095])

width = 0.55
y_pos = np.arange(len(candidates))

p1 = ax.barh(y_pos, trust_comp, width, label='Trust (0.4 · T)', color='#00F0FF', edgecolor='#080E1A')
p2 = ax.barh(y_pos, rep_comp, width, left=trust_comp, label='Reputation (0.3 · r/5)', color='#FFB300', edgecolor='#080E1A')
p3 = ax.barh(y_pos, succ_comp, width, left=trust_comp + rep_comp, label='Success Rate (0.2 · σ)', color='#00E676', edgecolor='#080E1A')
p4 = ax.barh(y_pos, lat_comp, width, left=trust_comp + rep_comp + succ_comp, label='Latency Bonus (0.1 · [1 - λ])', color='#9D4EDD', edgecolor='#080E1A')

totals = [0.000, 0.655, 0.812, 0.963]
labels = [
    "0.000 (REJECTED BY POLICY: QUARANTINED)",
    "Score: 0.655 (0.260 + 0.210 + 0.150 + 0.035)",
    "Score: 0.812 (0.340 + 0.252 + 0.170 + 0.050)",
    "Score: 0.963 (0.380 + 0.288 + 0.200 + 0.095)"
]

for i, (tot, lbl) in enumerate(zip(totals, labels)):
    offset = 0.02 if tot > 0 else 0.02
    color = '#FF3D71' if tot == 0 else '#FFFFFF'
    ax.text(tot + offset, i, lbl, va='center', color=color, fontweight='bold', fontsize=8.5)

ax.set_title('Transparent Matching Score Breakdown Across Candidate Agents\n[ MatchScore = 0.4·T + 0.3·(r/5.0) + 0.2·σ + 0.1·(1 - λ) | Calculated Illustrative Benchmark Scenario ]', 
             fontsize=10, color='#FFFFFF', fontweight='bold', pad=12)
ax.set_xlabel('Composite Match Score Contribution', color='#94A3B8', fontsize=10, labelpad=8)
ax.set_yticks(y_pos)
ax.set_yticklabels(candidates, color='#FFFFFF', fontsize=9, fontweight='bold')
ax.set_xlim(0, 1.35)
ax.tick_params(colors='#94A3B8', labelsize=9)
ax.grid(axis='x', color='#1E3A6E', linestyle=':', linewidth=0.8, alpha=0.6)

legend = ax.legend(loc='lower right', facecolor='#111C35', edgecolor='#2A4B8D', fontsize=8)
for text in legend.get_texts():
    text.set_color('#CBD5E1')

plt.tight_layout()
for d in output_dirs:
    c2_path = os.path.join(d, "matching_breakdown.png")
    plt.savefig(c2_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved Chart 2: matching_breakdown.png")

# ==============================================================================
# Chart 3: Test Suite Results & Coverage Distribution (Slide 16)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.5, 4.4), facecolor='#0B132B')
ax.set_facecolor('#080E1A')

suites = [
    'Auth & RBAC (28)',
    'CLI Commands (28)',
    'Adaptive Policy (7)',
    'Health Probes (4)',
    'Inv/Disc/Match (3)',
    'E2E Lifecycles (3)',
    'Multi-Agent (2)',
    'Platform/VDR (5)'
]
test_counts = [28, 28, 7, 4, 3, 3, 2, 5]  # Total = exactly 80 tests

colors = ['#00F0FF', '#00D2E0', '#00E676', '#38EF7D', '#FFB300', '#FF9100', '#9D4EDD', '#7B2CBF']
bars = ax.bar(suites, test_counts, color=colors, width=0.6, edgecolor='#2A4B8D', linewidth=1)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2., height + 0.6,
            f"{int(height)}", ha='center', va='bottom', color='#FFFFFF', fontweight='bold', fontsize=9)

ax.set_title('Verified Test Suite Distribution — 80 / 80 Tests Passing (100% Pass Rate)\n[ Verified via pytest · Total Execution Time: 15.04s in SQLite WAL Mode ]', 
             fontsize=10.5, color='#FFFFFF', fontweight='bold', pad=12)
ax.set_ylabel('Automated Tests Count', color='#94A3B8', fontsize=10, labelpad=8)
ax.set_ylim(0, 33)
ax.tick_params(colors='#94A3B8', labelsize=8)
plt.xticks(rotation=22, ha='right', color='#CBD5E1', fontweight='medium')
ax.grid(axis='y', color='#1E3A6E', linestyle=':', linewidth=0.8, alpha=0.6)

plt.tight_layout()
for d in output_dirs:
    c3_path = os.path.join(d, "test_results_chart.png")
    plt.savefig(c3_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved Chart 3: test_results_chart.png")
