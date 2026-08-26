# Trust Model

## Telemetry Components

**1. Task Success Rate $S_i(t)$**
```math
S_i(t) = \frac{\text{successful\_tasks}}{\text{total\_tasks}}
```
Evaluates raw binary outcome of the requested objective.

**2. Protocol Compliance $C_i(t)$**
```math
C_i(t) = \frac{\text{compliant\_events}}{\text{total\_events}}
```
Evaluates adherence to expected parameters, payload formats, and semantic boundaries.

**3. Normalized Latency $L_i(t)$**
```math
L_i(t) = \max\left(0, \min\left(1, \frac{\text{average\_latency}}{\text{MAX\_LATENCY\_MS}}\right)\right)
```
Evaluates execution speed to penalize unusually slow responses indicative of exhaustion or delay tactics.

## Behavioral Score $P_i(t)$
A weighted linear combination of the immediate telemetry signals.
```math
P_i(t) = w_1 S_i(t) + w_2 C_i(t) + w_3 (1 - L_i(t))
```
**Current experimental configuration:**
- $w_1 = 0.6$
- $w_2 = 0.3$
- $w_3 = 0.1$

*(Note: These parameters are experimental configuration values and are NOT claimed to be universally optimal.)*

## Temporal Trust $T_i(t)$
An exponential moving average allowing trust to decay or recover smoothly over successive events.
```math
T_i(t) = \lambda T_i(t-1) + (1-\lambda)P_i(t)
```
**Current experimental configuration:**
- $\lambda = 0.7$

*(Note: These parameters are experimental configuration values and are NOT claimed to be universally optimal.)*

## Trust State Lifecycle
The calculated temporal trust strictly governs the state machine.

- **TRUSTED**: $T_i \ge 0.8$
- **SUSPICIOUS**: $0.5 \le T_i < 0.8$
- **QUARANTINED**: $T_i < 0.5$
  - Behavioral authorization denied.
  - Cryptographic VC may remain valid.
  - Recovery is possible through consistent behavioral improvement.
- **REVOKED**: (Manual Override)
  - Administrative security action.
  - Terminal state.
  - Behavioral recovery cannot restore authorization.
  
**CRITICAL DISTINCTION:** `QUARANTINED` $\neq$ `REVOKED`. Quarantined agents can recover trust via good behavior over time; revoked agents are permanently burned.
