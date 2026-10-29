# Experiment 4: Measurement of Signal Strength vs Distance for a Wi-Fi Router

**Aim:** Measurement of signal strength vs distance for a Wi-Fi router.

**Lab Outcome:** MDL501.3

## Theory

### RSSI
**Received Signal Strength Indicator (RSSI)** is the power of the received radio signal, usually given in **dBm** (decibels relative to 1 mW):

$$P_{dBm} = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)$$

| RSSI | Quality |
|---|---|
| −30 to −50 dBm | Excellent |
| −50 to −67 dBm | Good (fine for streaming and VoIP) |
| −67 to −70 dBm | Fair |
| −70 to −80 dBm | Weak, unreliable |
| < −80 dBm | Unusable |

### Free-space path loss (Friis)
$$FSPL(dB) = 20\log_{10}(d) + 20\log_{10}(f) - 147.55$$

with d in metres and f in Hz. In free space, received power falls by **6 dB each time the distance doubles**.

### Log-distance path loss model
Real indoor environments have walls, furniture and people, so a general model is used:

$$RSSI(d) = RSSI(d_0) - 10\,n\,\log_{10}\left(\frac{d}{d_0}\right) + X_\sigma$$

- d₀: reference distance (1 m)
- n: path loss exponent (2 in free space, 1.6–1.8 in corridors, 2.5–4 in offices, 4–6 through walls)
- X_σ: shadowing, a Gaussian random variable in dB

Plotting RSSI against 10·log₁₀(d) gives a straight line with slope −n, so n can be estimated with **linear regression**.

### Factors that affect Wi-Fi signal strength
Distance, obstacles (walls, glass, metal), interference from other networks, the band (2.4 GHz travels further than 5 GHz), router antenna orientation, transmit power and people moving nearby.

## Procedure
1. Connect a laptop to the Wi-Fi router and stand 1 m from it, in line of sight.
2. Run `python wifi_rssi.py measure --distance 1`. It takes 10 samples and saves the average to `readings.csv`.
3. Move to 2, 3, 4, 5, 6, 8, 10, 12 and 15 m and repeat step 2 at each point.
   *(Alternative: read RSSI from a mobile app such as "WiFi Analyzer" and type the values into `readings.csv`.)*
4. Run `python wifi_rssi.py analyze --csv readings.csv` to fit the model and plot `rssi_vs_distance.png`.
5. To check the setup, run `python wifi_rssi.py analyze --csv sample_readings.csv`.

## Observation table
| Distance (m) | RSSI (dBm) | Signal quality |
|---|---|---|
| 1 | | |
| 2 | | |
| 4 | | |
| 8 | | |
| 15 | | |

Path loss exponent n = ______  RSSI at 1 m = ______ dBm

## Conclusion
RSSI falls logarithmically with distance from the router. The fitted path loss exponent is greater than the free-space value of 2, which shows the extra attenuation and multipath of an indoor environment.
