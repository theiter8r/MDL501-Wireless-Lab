# Experiment 11 (Innovative): Cellular Call Setup and Handover Simulation

**Aim:** Simulate call setup and handover between two base stations for a moving user, and study the effect of hysteresis and time-to-trigger on the number of handovers and ping-pong handovers.

**Lab Outcome:** MDL501.1 (simulate and analyze basic cellular network operations such as call setup and handover)

## Theory

### Call setup (mobile-originated, simplified)
1. **Cell search and selection:** the mobile measures the pilot/reference signals (RSRP) of nearby cells and camps on the strongest suitable cell.
2. **Random access:** the mobile sends a RACH preamble and receives a timing advance and a temporary ID.
3. **RRC connection setup:** a signalling connection is set up with the base station (eNB/gNB).
4. **Authentication and security:** the core network (MME/AMF with HSS/UDM) authenticates the SIM and activates ciphering.
5. **Bearer / traffic channel setup:** a dedicated channel is assigned and the call connects.

A call is **blocked** if no channel is free or the signal is below the minimum level, and **dropped** if the link fails during the call.

### Handover
**Handover (handoff)** transfers an ongoing call from one cell to another without interrupting it, as the user moves.

| Type | Description |
|---|---|
| **Hard handover** (break-before-make) | The old link is released before the new one is set up. Used in GSM and LTE. |
| **Soft handover** (make-before-break) | The mobile connects to several cells at once. Used in CDMA/UMTS. |
| Intra-cell / inter-cell / inter-system | Same cell (other channel), different cells, or different technologies (LTE ↔ 3G) |

### Handover decision
The mobile reports measurements and the network decides. The LTE **event A3** condition is:

$$RSRP_{neighbour} > RSRP_{serving} + H \quad \text{held for TTT}$$

- **Hysteresis margin (H):** stops handovers caused by small fluctuations.
- **Time-to-trigger (TTT):** the condition must hold for this long (for example 320 ms).
- **Ping-pong effect:** with a small H, shadowing makes the call bounce back and forth between cells, which wastes signalling.
- **Too large an H** delays the handover, and the call may **drop** before it happens.

### Channel model used
$$P_r = P_t - PL(1\,m) - 10\,n\log_{10}d + X_\sigma$$

Here X_σ is log-normal shadowing (σ = 6 dB) correlated over about 50 m (Gudmundson model).

### Handover priority
Guard channels reserve some channels for handover calls, because dropping an ongoing call is worse than blocking a new one.

## Procedure
1. Run `python handover_sim.py`.
2. Note where the call was set up, when each handover happened, and the ping-pong count.
3. Look at `handover.png`: the dashed lines mark handover points, and the bar chart shows handovers against hysteresis.
4. Repeat with `--hyst 0`, `--hyst 6`, `--hyst 10`, and with `--ttt 0` and `--ttt 1`.
5. Change the speed (`--speed 3` for a pedestrian, `--speed 30` for a car) and the seed (`--seed 1..5`) and compare.

## Observation table
| Hysteresis (dB) | TTT (s) | Handovers | Ping-pong | Call status |
|---|---|---|---|---|
| 0 | 0.32 | | | |
| 3 | 0.32 | | | |
| 6 | 0.32 | | | |
| 10 | 0.32 | | | |

## Conclusion
The simulation shows call setup on the strongest cell and handover as the user moves between cells. A small hysteresis or TTT causes many unnecessary ping-pong handovers because of shadowing. Too large a value delays the handover and risks dropping the call. A moderate hysteresis (2–4 dB) with a suitable TTT balances the two.
