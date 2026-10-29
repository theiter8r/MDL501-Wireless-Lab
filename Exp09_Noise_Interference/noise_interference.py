"""
Experiment 9: Noise and interference analysis in wireless communication.

1. Thermal noise floor  N = -174 dBm/Hz + 10 log10(B) + NF  for common channel widths
2. BPSK link with AWGN plus a co-channel interferer at a given signal-to-interference
   ratio (SIR). Shows how BER flattens out (an "error floor") when interference
   dominates, and compares SNR with SINR.
3. Shannon capacity C = B log2(1 + SINR) for the same cases.

Run:  python noise_interference.py [--bits 200000]
Output: noise_interference.png
"""
import argparse
from math import erfc, log2, log10, sqrt

import matplotlib.pyplot as plt
import numpy as np


def noise_floor_dbm(bandwidth_hz, nf_db):
    return -174 + 10 * log10(bandwidth_hz) + nf_db


def simulate(ebn0_db, sir_db, n_bits, rng):
    bits = rng.integers(0, 2, n_bits)
    s = 2.0 * bits - 1
    noise = sqrt(1 / (2 * 10 ** (ebn0_db / 10))) * rng.standard_normal(n_bits)
    if np.isinf(sir_db):
        interference = 0.0
    else:
        amp = sqrt(10 ** (-sir_db / 10))
        interference = amp * (2.0 * rng.integers(0, 2, n_bits) - 1)  # co-channel BPSK user
    r = s + noise + interference
    return np.mean((r > 0) != bits)


def gaussian_approx_ber(ebn0_db, sir_db):
    n_var = 1 / (2 * 10 ** (ebn0_db / 10))
    i_pow = 0 if np.isinf(sir_db) else 10 ** (-sir_db / 10)
    return 0.5 * erfc(sqrt(1 / (2 * (n_var + i_pow))))


def sinr_db(snr_db, sir_db):
    snr, sir = 10 ** (snr_db / 10), (np.inf if np.isinf(sir_db) else 10 ** (sir_db / 10))
    return 10 * log10(1 / (1 / snr + 1 / sir))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=200_000)
    parser.add_argument("--nf", type=float, default=7, help="receiver noise figure (dB)")
    args = parser.parse_args()
    rng = np.random.default_rng(2)

    print("Thermal noise floor (NF = %g dB)" % args.nf)
    for name, bw in (("Bluetooth 1 MHz", 1e6), ("LTE RB 180 kHz", 180e3), ("Wi-Fi 20 MHz", 20e6),
                     ("Wi-Fi 40 MHz", 40e6), ("Wi-Fi 80 MHz", 80e6), ("5G 100 MHz", 100e6)):
        print(f"  {name:<18}: {noise_floor_dbm(bw, args.nf):7.1f} dBm")
    rx = -65
    print(f"\nExample: Rx power {rx} dBm on 20 MHz Wi-Fi -> SNR = "
          f"{rx - noise_floor_dbm(20e6, args.nf):.1f} dB")

    ebn0 = np.arange(0, 16)
    sirs = [np.inf, 20, 10, 6]
    plt.figure(figsize=(8, 5.5))
    for sir in sirs:
        sim = [max(simulate(e, sir, args.bits, rng), 1e-7) for e in ebn0]
        approx = [gaussian_approx_ber(e, sir) for e in ebn0]
        label = "No interference" if np.isinf(sir) else f"SIR = {sir} dB"
        line = plt.semilogy(ebn0, sim, "o", label=f"{label} (sim)")[0]
        plt.semilogy(ebn0, approx, "-", color=line.get_color(), alpha=0.6)
    plt.ylim(1e-6, 0.5)
    plt.grid(True, which="both", alpha=0.4)
    plt.xlabel("Eb/N0 (dB)")
    plt.ylabel("Bit Error Rate")
    plt.title("BPSK BER with noise and co-channel interference\n(markers: simulation, lines: Gaussian approximation)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("noise_interference.png", dpi=150)

    print(f"\n{'SNR (dB)':>8} {'SIR (dB)':>9} {'SINR (dB)':>10} {'Capacity @20MHz (Mbps)':>24}")
    for snr in (10, 20, 30):
        for sir in sirs:
            s = sinr_db(snr, sir)
            cap = 20e6 * log2(1 + 10 ** (s / 10)) / 1e6
            print(f"{snr:>8} {('inf' if np.isinf(sir) else sir):>9} {s:>10.2f} {cap:>24.1f}")
    print("\nSaved noise_interference.png")


if __name__ == "__main__":
    main()
