# Experiment 7: Study of Path Loss in an Indoor Environment

**Aim:** Study of path loss in an indoor environment (RSSI vs obstacles).

**Lab Outcome:** MDL501.5

## Theory

### Path loss
Path loss is the drop in signal power as a wave travels from transmitter to receiver:

$$PL(dB) = P_t(dBm) - P_r(dBm)$$

Indoor path loss is larger than free-space loss because of **absorption, reflection, diffraction and scattering** by walls, floors, furniture and people.

### Large-scale propagation models
**1. Free space (Friis):**
$$PL_{FS}(dB) = 20\log_{10} d + 20\log_{10} f - 147.55$$

**2. Log-distance:**
$$PL(d) = PL(d_0) + 10\,n\log_{10}(d/d_0) + X_\sigma$$

**3. Multi-wall (Motley–Keenan) indoor model:**
$$PL(d) = PL(d_0) + 10\,n\log_{10}(d) + \sum_{i} k_i L_{w,i} + \sum_j k_{f,j} L_{f,j}$$

where k_i is the number of walls of type i, L_w is the wall attenuation, and L_f is the floor attenuation.

### Typical attenuation at 2.4 GHz
| Obstacle | Attenuation |
|---|---|
| Glass window | 2–3 dB |
| Wooden door | 3–4 dB |
| Drywall / partition | 3–5 dB |
| Brick wall | 6–10 dB |
| Concrete wall | 10–15 dB |
| Metal door / elevator | 15–25 dB |
| Human body | 3–5 dB |
| Floor / ceiling (RCC) | 15–20 dB |

5 GHz signals lose more through each obstacle than 2.4 GHz signals do.

### Path loss exponent indoors
| Environment | n |
|---|---|
| Free space | 2 |
| Corridor (waveguide effect) | 1.6–1.8 |
| Open office, LOS | 2–2.5 |
| Office with partitions | 2.5–3.5 |
| Obstructed buildings | 4–6 |

## Procedure
1. Place the Wi-Fi router at a fixed point and note its transmit power (about 20 dBm).
2. Measure RSSI (using `../Exp04_WiFi_Signal_vs_Distance/wifi_rssi.py measure` or a Wi-Fi analyser app) at:
   - several distances in the same room (line of sight),
   - the next room (1 wall), two rooms away (2 walls), a corridor with the door closed, another floor.
3. For each point, record the location, distance, number of walls and RSSI in a CSV (same format as `sample_obstacles.csv`).
4. Run `python path_loss.py --csv your_data.csv`.
5. Note the fitted path loss exponent **n** and the **loss per wall**, and compare measured path loss with free-space loss.

## Observation table
| Location | Distance (m) | Walls | RSSI (dBm) | Path loss (dB) |
|---|---|---|---|---|
| | | | | |

## Conclusion
Indoor path loss is much higher than free-space loss. Each wall between the router and the receiver adds a roughly fixed attenuation (about 7–10 dB for brick walls), and the indoor path loss exponent is above 2. The multi-wall model predicts indoor RSSI well and helps decide where to place access points.
