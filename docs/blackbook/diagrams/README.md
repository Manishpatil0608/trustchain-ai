# TrustChain-AI — Mermaid Diagrams Guide

This directory contains the complete collection of 25 standalone Mermaid diagrams (`.mmd` files) illustrating the architecture, security models, data flows, workflows, and database schema of **TrustChain-AI: A Decentralized Trust Intelligence Framework for Secure Autonomous AI Agent Collaboration**.

---

## Directory Contents

- `00_diagram_index.md` — Complete master index of all 25 diagrams with metadata, sources, and target report chapters.
- `IMPLEMENTATION_MAPPING.md` — Detailed mapping of every diagram node, edge, and formula to the real codebase.
- `01_system_architecture.mmd` through `25_frontend_backend_database_flow.mmd` — 25 standalone Mermaid files.

---

## How to Render the Diagrams

### Option 1: Mermaid Live Editor (Browser — No Installation Required)

1. Open your web browser and navigate to the official [Mermaid Live Editor](https://mermaid.live).
2. Open any `.mmd` file in this directory (e.g., in VS Code, Notepad, or any text editor).
3. Copy the entire contents of the `.mmd` file.
4. Paste the code into the left code editor pane in Mermaid Live Editor.
5. The diagram renders instantly in the right preview pane.
6. Click **Actions** → **Download PNG** or **Download SVG** for inclusion in documents or presentations.

### Option 2: Mermaid CLI (`mmdc` via Node.js / npx)

If you have Node.js installed, you can render any diagram locally to SVG, PNG, or PDF using `@mermaid-js/mermaid-cli`.

#### Render a Single Diagram to SVG:
```bash
npx --yes @mermaid-js/mermaid-cli -i 01_system_architecture.mmd -o 01_system_architecture.svg
```

#### Render a Single Diagram to PNG (High Resolution):
```bash
npx --yes @mermaid-js/mermaid-cli -i 01_system_architecture.mmd -o 01_system_architecture.png -w 2400 -H 1600 -s 2
```

#### Batch Render All 25 Diagrams to SVG (PowerShell):
From within `docs/blackbook/diagrams`:
```powershell
Get-ChildItem -Filter "*.mmd" | ForEach-Object {
    $outFile = $_.BaseName + ".svg"
    Write-Host "Rendering $($_.Name) -> $outFile"
    npx --yes @mermaid-js/mermaid-cli -i $_.FullName -o $outFile -q
}
```

#### Batch Render All 25 Diagrams to PNG (PowerShell):
```powershell
Get-ChildItem -Filter "*.mmd" | ForEach-Object {
    $outFile = $_.BaseName + ".png"
    Write-Host "Rendering $($_.Name) -> $outFile"
    npx --yes @mermaid-js/mermaid-cli -i $_.FullName -o $outFile -w 2000 -H 1400 -s 2 -q
}
```

---

## Mathematical Notation Reference

Every diagram reflecting trust evaluation and matching uses the verified mathematical model of TrustChain-AI:

1. **Sliding Window Normalization (n = 10 events):**
   - Success Rate: $S_i(t) = \frac{\sum \text{success}}{n}$
   - Compliance Rate: $C_i(t) = \frac{\sum (\text{compliance\_event} == \text{None})}{n}$
   - Latency Penalty: $L_i(t) = \min\left(\frac{\bar{\ell}_i}{2000\text{ ms}}, 1.0\right)$

2. **Composite Performance Score:**
   $$P_i(t) = 0.6 \cdot S_i(t) + 0.3 \cdot C_i(t) + 0.1 \cdot (1 - L_i(t))$$

3. **Temporal Exponential Moving Average (EMA):**
   $$T_i(t) = 0.7 \cdot P_i(t) + 0.3 \cdot T_i(t-1)$$
   - Decay Factor: $\lambda = 0.7$
   - Genesis Baseline: $T_i(0) = 1.0$ (Benefit of the doubt)

4. **Trust State Thresholds:**
   - $\text{TRUSTED}$: $T_i(t) \ge 0.8$
   - $\text{SUSPICIOUS}$: $0.5 \le T_i(t) < 0.8$
   - $\text{QUARANTINED}$: $T_i(t) < 0.5$
   - $\text{REVOKED}$: Terminal administrative action (irreversible via telemetry)

5. **Discovery Match Score:**
   $$\text{match\_score}_i = 0.4 \cdot T_i + 0.3 \cdot \left(\frac{r_i}{5.0}\right) + 0.2 \cdot \sigma_i + 0.1 \cdot (1 - \lambda_i)$$
   - $r_i$: Reputation score ($1.0 - 5.0$ scale)
   - $\sigma_i$: Historical task success rate
   - $\lambda_i$: Normalized latency penalty
