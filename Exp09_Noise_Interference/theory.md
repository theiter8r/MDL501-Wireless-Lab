# Experiment 9: Noise and Interference Analysis in Wireless Communication

**Aim:** Noise and interference analysis in wireless communication.

**Lab Outcome:** MDL501.6

## Theory

### Noise
Noise is any unwanted random signal that corrupts the wanted signal.

| Type | Source |
|---|---|
| **Thermal (Johnson) noise** | Random motion of electrons in conductors. It is white and Gaussian. |
| **Shot noise** | Discrete flow of charge carriers in semiconductors |
| **Flicker (1/f) noise** | Low-frequency noise in active devices |
| **Atmospheric / cosmic noise** | Lightning, the sun, the galaxy |
| **Man-made noise** | Motors, ignition systems, power lines, switching supplies |

**Thermal noise power:**
$$N = kTB \;\Rightarrow\; N(dBm) = -174 + 10\log_{10}B + NF$$

where k = 1.38 × 10⁻²³ J/K, T = 290 K, B is the bandwidth in Hz, and NF is the receiver noise figure. For 20 MHz Wi-Fi with NF = 7 dB, the noise floor is about **−94 dBm**.

**Signal-to-noise ratio:** SNR(dB) = P_signal(dBm) − N(dBm)

### Interference
Interference is unwanted signal from **other transmitters**:
- **Co-channel interference (CCI):** other cells or APs using the same frequency, for example Wi-Fi networks on the same channel. This is the main limit in cellular systems with frequency reuse.
- **Adjacent-channel interference (ACI):** energy leaking from neighbouring channels, caused by imperfect filters or overlapping 2.4 GHz Wi-Fi channels (only 1, 6 and 11 do not overlap).
- **Inter-symbol interference (ISI):** caused by multipath delay spread.
- **Cross-technology interference:** Bluetooth, Zigbee and microwave ovens in the 2.4 GHz band.

### SINR
$$SINR = \frac{S}{I + N}$$

When I is much smaller than N the link is **noise-limited**; when I is much larger than N it is **interference-limited**. In the interference-limited case, raising transmit power does not help, because the interference rises as well. BER then reaches an **error floor**.

### Shannon capacity
$$C = B\log_2(1 + SINR)$$

Capacity grows linearly with bandwidth but only logarithmically with SINR.

### Ways to reduce noise and interference
Proper channel planning (1/6/11), the 5 GHz band, power control, directional antennas and beamforming, frequency hopping (Bluetooth), spread spectrum, error-correcting codes, filtering, and low-noise amplifiers (LNAs).

## Procedure
### Part A: Simulation
1. Run `python noise_interference.py`.
2. Record the noise floor for each bandwidth.
3. Look at `noise_interference.png`. With interference, BER curves level off at an error floor however high Eb/N0 goes.
4. Record SINR and capacity from the table and identify noise-limited and interference-limited cases.

### Part B: Practical observation
1. Use a Wi-Fi analyser app (Android "WiFi Analyzer" / macOS Wireless Diagnostics) to list nearby networks and their channels.
2. Note how many APs share your router's channel (co-channel) and overlap with it (adjacent channel).
3. Note the noise level (macOS: Option-click the Wi-Fi icon → *Noise*) and work out SNR = RSSI − Noise.
4. Run the Exp05 throughput test, switch the router to a less crowded channel or to 5 GHz, and run it again.

## Observation table
| Channel | No. of APs on channel | RSSI (dBm) | Noise (dBm) | SNR (dB) | Throughput (Mbps) |
|---|---|---|---|---|---|
| | | | | | |

## Conclusion
Thermal noise sets the minimum receivable signal, and interference from other transmitters often limits wireless performance more than noise does. SINR, not SNR alone, determines BER and capacity. Interference creates an error floor that extra power cannot remove, so channel planning and interference control are essential.
