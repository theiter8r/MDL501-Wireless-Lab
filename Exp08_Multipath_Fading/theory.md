# Experiment 8: Analysis of Multipath Effects

**Aim:** Analysis of multipath effects (signal fluctuation observation).

**Lab Outcome:** MDL501.5

## Theory

### Multipath propagation
In a real environment a transmitted signal reaches the receiver along **many paths**. These include the direct (LOS) path and copies created by:
- **Reflection** from large smooth surfaces (walls, floors, buildings)
- **Diffraction** around sharp edges (corners, rooftops)
- **Scattering** from rough or small objects (foliage, furniture)

Each copy arrives with a different **amplitude, phase and delay**. Copies that add in phase **reinforce** the signal, and copies that are out of phase **cancel** it. The result is rapid changes in received power called **small-scale (fast) fading**.

### Small-scale fading parameters
- **Doppler shift:** f_d = v/λ · cos θ. Motion causes the fading to vary over time.
- **Coherence time:** T_c ≈ 0.423 / f_d, the time over which the channel stays roughly constant.
- **Delay spread (σ_τ):** the spread of arrival times of the multipath copies.
- **Coherence bandwidth:** B_c ≈ 1 / (5σ_τ). If the signal bandwidth is greater than B_c, fading is **frequency selective**, which causes inter-symbol interference (ISI).
- Deep fades are roughly **λ/2 apart** in space (6.25 cm at 2.4 GHz).

### Statistical models
**Rayleigh fading** (no LOS, many scattered paths): the envelope r follows

$$p(r) = \frac{r}{\sigma^2} e^{-r^2/2\sigma^2}$$

Fades of 20–30 dB or more are common.

**Rician fading** (dominant LOS path plus scattered paths): described by the **K-factor** = LOS power / scattered power. K = 0 gives Rayleigh, and a larger K means milder fading.

### Types of fading
| Basis | Types |
|---|---|
| Delay spread | Flat fading / frequency-selective fading |
| Doppler spread | Slow fading / fast fading |

### Ways to reduce multipath effects
Diversity (space, frequency, time, polarisation), MIMO antennas, OFDM (used in Wi-Fi, LTE and 5G), equalisation, RAKE receivers (CDMA), and channel coding with interleaving.

## Procedure

### Part A: Simulation
1. Run `python multipath.py --speed 1.5 --freq 2.4e9 --k 5`.
2. Look at `multipath_fading.png`. The Rayleigh envelope shows deep fades; the Rician envelope (with LOS) is smoother.
3. Change the speed (0.5, 1.5, 10 m/s) and note how the Doppler shift and fade rate change.
4. Note the Doppler shift, coherence time and fading statistics printed in the terminal.

### Part B: Observation with real hardware
1. Stand still and log Wi-Fi RSSI every 0.5 s for 1 minute (Wi-Fi analyser app or Exp04 script), saving a CSV with column `rssi_dbm`.
2. Repeat while moving the laptop or phone slowly by a few centimetres, then while someone walks between it and the router.
3. Run `python multipath.py --csv your_log.csv` and compare the standard deviation and peak-to-peak variation of each case.

## Observation table
| Condition | Mean RSSI (dBm) | Std dev (dB) | Peak-to-peak (dB) |
|---|---|---|---|
| Stationary | | | |
| Moving device | | | |
| People moving nearby | | | |

## Conclusion
Multipath makes the received signal fluctuate quickly, even when the distance barely changes. Without line of sight, fading follows a Rayleigh distribution with deep fades. A strong LOS path (Rician) reduces the fluctuation. Movement increases the Doppler shift and the fading rate.
