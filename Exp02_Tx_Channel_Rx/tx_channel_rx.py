"""
Experiment 2: Simulation of a basic communication system (Tx -> Channel -> Rx).

Transmitter : random bits -> BPSK mapping (0 -> -1, 1 -> +1)
Channel     : Additive White Gaussian Noise (AWGN)
Receiver    : threshold detector (> 0 -> 1)

Measures the bit error rate (BER) for a range of Eb/N0 values and compares
it with the theoretical BPSK curve  Pb = 0.5 * erfc(sqrt(Eb/N0)).

Run:  python tx_channel_rx.py [--bits 200000]
Output: ber_curve.png, constellation.png
"""
import argparse
from math import erfc, sqrt

import matplotlib.pyplot as plt
import numpy as np


def transmitter(n_bits, rng):
    bits = rng.integers(0, 2, n_bits)
    symbols = 2 * bits - 1  # BPSK
    return bits, symbols.astype(float)


def awgn_channel(symbols, ebn0_db, rng):
    ebn0 = 10 ** (ebn0_db / 10)
    noise_std = sqrt(1 / (2 * ebn0))  # Eb = 1 for BPSK
    return symbols + noise_std * rng.standard_normal(len(symbols))


def receiver(received):
    return (received > 0).astype(int)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=200_000)
    args = parser.parse_args()

    rng = np.random.default_rng(1)
    ebn0_range = np.arange(0, 11)
    sim_ber, theory_ber = [], []

    print(f"{'Eb/N0 (dB)':>10} {'Errors':>8} {'Simulated BER':>15} {'Theoretical BER':>16}")
    for ebn0_db in ebn0_range:
        bits, tx = transmitter(args.bits, rng)
        rx = awgn_channel(tx, ebn0_db, rng)
        errors = int(np.sum(receiver(rx) != bits))
        ber = errors / args.bits
        th = 0.5 * erfc(sqrt(10 ** (ebn0_db / 10)))
        sim_ber.append(max(ber, 1e-7))
        theory_ber.append(th)
        print(f"{ebn0_db:>10} {errors:>8} {ber:>15.2e} {th:>16.2e}")

    plt.figure(figsize=(7, 5))
    plt.semilogy(ebn0_range, theory_ber, "k-", label="Theoretical BPSK")
    plt.semilogy(ebn0_range, sim_ber, "ro", label="Simulated")
    plt.grid(True, which="both", alpha=0.4)
    plt.xlabel("Eb/N0 (dB)")
    plt.ylabel("Bit Error Rate")
    plt.title("BPSK over AWGN: Tx-Channel-Rx")
    plt.legend()
    plt.tight_layout()
    plt.savefig("ber_curve.png", dpi=150)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, snr in zip(axes, (0, 5, 10)):
        _, tx = transmitter(2000, rng)
        rx = awgn_channel(tx, snr, rng)
        ax.scatter(rx, np.zeros_like(rx) + 0.05 * rng.standard_normal(len(rx)), s=3, alpha=0.4)
        ax.axvline(0, color="r", ls="--")
        ax.set_title(f"Received symbols, Eb/N0 = {snr} dB")
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig("constellation.png", dpi=150)
    print("\nSaved ber_curve.png and constellation.png")


if __name__ == "__main__":
    main()
