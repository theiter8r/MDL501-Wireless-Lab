# Experiment 2: Simulation of a Basic Communication System (Tx – Channel – Rx)

**Aim:** Simulation of a basic communication system (Tx–Channel–Rx) using MATLAB / Python / online tools.

**Lab Outcome:** MDL501.2

## Theory

### Block diagram

```
 Source -> Source encoder -> Modulator -> [ Channel + Noise ] -> Demodulator -> Decoder -> Sink
 \_____________ Transmitter ___________/                       \___________ Receiver ________/
```

- **Transmitter:** turns information into a signal that suits the channel (source coding, channel coding, modulation, amplification).
- **Channel:** the medium (free space, cable, fibre). It attenuates the signal and adds **noise**, **interference** and **distortion**.
- **Receiver:** recovers the original message (filtering, demodulation, detection, decoding).

### BPSK modulation
In Binary Phase Shift Keying each bit changes the carrier's phase by 0° or 180°:

$$s(t) = \pm \sqrt{\tfrac{2E_b}{T_b}} \cos(2\pi f_c t)$$

At baseband this is bit 1 → +1 and bit 0 → −1.

### AWGN channel
Additive White Gaussian Noise is the standard channel model:
- **Additive:** r = s + n
- **White:** flat power spectral density N₀/2 across all frequencies
- **Gaussian:** noise amplitude follows a normal distribution with zero mean

### Bit error rate
BER = (number of bits received in error) / (total bits sent). For BPSK in AWGN:

$$P_b = \frac{1}{2}\,\text{erfc}\left(\sqrt{\frac{E_b}{N_0}}\right)$$

where E_b/N_0 is the energy per bit over the noise power spectral density (it is related to SNR). As E_b/N_0 rises, BER falls roughly exponentially.

## Procedure
1. Python: run `python tx_channel_rx.py`. MATLAB/Octave: run `tx_channel_rx.m`.
2. The program generates random bits, maps them to BPSK, adds AWGN for Eb/N0 = 0 to 10 dB and detects them.
3. Record the simulated and theoretical BER in the table.
4. Look at `ber_curve.png` and `constellation.png`. At low SNR the received points spread across the decision threshold.
5. *(Online option)* Repeat with any web BPSK simulator and compare.

## Observations (sample)
| Eb/N0 (dB) | Simulated BER | Theoretical BER |
|---|---|---|
| 0 | ≈ 7.9 × 10⁻² | 7.86 × 10⁻² |
| 4 | ≈ 1.25 × 10⁻² | 1.25 × 10⁻² |
| 8 | ≈ 2 × 10⁻⁴ | 1.91 × 10⁻⁴ |
| 10 | ≈ 4 × 10⁻⁶ | 3.87 × 10⁻⁶ |

## Conclusion
We simulated a complete Tx → AWGN channel → Rx chain. The simulated BER closely matches the theoretical BPSK curve, which shows that higher signal energy relative to noise means more reliable communication.
