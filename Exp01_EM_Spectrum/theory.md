# Experiment 1: Electromagnetic Spectrum Allocation and Wireless Bands

**Aim:** Study of electromagnetic spectrum allocation and wireless bands used in communication.

**Lab Outcome:** MDL501.1

## Theory

### Electromagnetic spectrum
The electromagnetic (EM) spectrum covers every frequency of EM radiation, from radio waves through microwaves, infrared, visible light, ultraviolet, X-rays and gamma rays. Frequency and wavelength are related by

$$\lambda = \frac{c}{f}, \qquad c = 3 \times 10^8 \text{ m/s}$$

Wireless communication mostly uses the **radio spectrum (3 Hz – 300 GHz)**, because radio waves travel long distances, pass through or bend around obstacles, and can be generated and received with cheap antennas.

### ITU frequency bands

| Band | Frequency range | Wavelength | Typical applications |
|---|---|---|---|
| VLF | 3 – 30 kHz | 100 – 10 km | Navigation, submarine links |
| LF | 30 – 300 kHz | 10 – 1 km | Longwave AM, RFID (125 kHz) |
| MF | 300 kHz – 3 MHz | 1 km – 100 m | AM broadcast |
| HF | 3 – 30 MHz | 100 – 10 m | Shortwave, amateur radio, NFC (13.56 MHz) |
| VHF | 30 – 300 MHz | 10 – 1 m | FM radio (88–108 MHz), TV, aircraft |
| UHF | 300 MHz – 3 GHz | 1 m – 10 cm | GSM, LTE, GPS, Wi-Fi 2.4 GHz, Bluetooth |
| SHF | 3 – 30 GHz | 10 – 1 cm | Wi-Fi 5/6 GHz, 5G, satellite, radar |
| EHF | 30 – 300 GHz | 10 – 1 mm | 5G mmWave, 60 GHz WiGig, radio astronomy |

### Spectrum allocation
Spectrum is limited and shared, so its use is regulated:
- **International:** the ITU (International Telecommunication Union) divides the world into 3 regions (India is in Region 3) and allocates bands to services at World Radio Conferences (WRC).
- **India:** the **Department of Telecommunications (DoT)**, through its **WPC Wing**, publishes the **National Frequency Allocation Plan (NFAP)**. **TRAI** recommends pricing and policy, and spectrum for mobile networks is sold by **auction**.

Kinds of spectrum:
- **Licensed:** exclusive use (cellular bands such as 700, 800, 900, 1800, 2100, 2300 MHz, 3.3–3.67 GHz and 26 GHz in India).
- **Unlicensed (ISM):** free to use within power limits (2.4 GHz and 5 GHz Wi-Fi, Bluetooth, Zigbee). In India 6 GHz (lower part) has also been de-licensed for Wi-Fi.
- **Shared/lightly licensed:** satellite, backhaul (E-band, V-band).

### Common wireless bands

| Technology | Band |
|---|---|
| GSM (2G) | 900 MHz, 1800 MHz |
| UMTS (3G) | 2100 MHz |
| LTE (4G) | 850, 1800, 2300 MHz (B5, B3, B40) |
| 5G NR FR1 | 3.3 – 3.8 GHz (n78), 700 MHz (n28) |
| 5G NR FR2 | 24.25 – 29.5 GHz (n257/n258) |
| Wi-Fi | 2.4 GHz, 5 GHz, 6 GHz |
| Bluetooth / BLE | 2.400 – 2.4835 GHz (79 × 1 MHz / 40 × 2 MHz channels) |
| GPS | L1 1575.42 MHz, L5 1176.45 MHz |
| NFC | 13.56 MHz |

### Trade-off between frequency bands
- **Low frequencies:** longer range, better penetration through walls, but little bandwidth (lower data rates).
- **High frequencies:** large bandwidth (high data rates), but higher path loss, weaker penetration and smaller cells.

## Procedure
1. Install the requirements: `pip install -r ../requirements.txt`
2. Run `python spectrum_bands.py`.
3. Note the band table and services printed in the terminal.
4. Open `spectrum_chart.png` and identify where cellular, Wi-Fi, Bluetooth and GPS lie.
5. Work out the wavelength of 900 MHz, 2.4 GHz and 28 GHz signals using λ = c/f.

## Observations
| Frequency | Wavelength (λ = c/f) | Band |
|---|---|---|
| 900 MHz | 33.3 cm | UHF |
| 2.4 GHz | 12.5 cm | UHF |
| 5 GHz | 6 cm | SHF |
| 28 GHz | 1.07 cm | EHF |

## Conclusion
We studied the EM spectrum, the ITU band classification and how spectrum is allocated internationally and in India. Lower bands give coverage and higher bands give capacity, which is why modern networks combine several bands.
