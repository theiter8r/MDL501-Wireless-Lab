"""
Experiment 8: Analysis of multipath effects (signal fluctuation observation).

Simulation : Rayleigh (no line of sight) and Rician (with line of sight)
             fading using the Clarke / Jakes sum-of-sinusoids model for
             a receiver moving at speed v. Plots the envelope in dB over time and
             the envelope histogram against the theoretical Rayleigh pdf.
Measured   : with --csv, analyses an RSSI log (column rssi_dbm) captured
             while standing still / walking, and reports the fluctuation statistics.

Run:
  python multipath.py --speed 1.5 --freq 2.4e9 --k 5
  python multipath.py --csv my_rssi_log.csv
Output: multipath_fading.png
"""
import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np


def clarke_fading(fd, t, n_paths=64, rng=None):
    """Complex Rayleigh fading gain with unit average power."""
    rng = rng or np.random.default_rng(0)
    alpha = rng.uniform(0, 2 * np.pi, n_paths)   # arrival angles
    phi = rng.uniform(0, 2 * np.pi, n_paths)     # random phases
    h = np.exp(1j * (2 * np.pi * fd * np.cos(alpha)[:, None] * t + phi[:, None])).sum(axis=0)
    return h / np.sqrt(n_paths)


def stats(env_db):
    mean = env_db.mean()
    return {"mean (dB)": mean, "std dev (dB)": env_db.std(),
            "max fade below mean (dB)": mean - env_db.min(),
            "peak-to-peak (dB)": env_db.max() - env_db.min()}


def analyze_csv(path):
    rssi = np.array([float(r["rssi_dbm"]) for r in csv.DictReader(open(path))])
    print(f"Samples: {len(rssi)}")
    for k, v in stats(rssi).items():
        print(f"  {k:<26}: {v:.2f}")
    plt.plot(rssi, ".-")
    plt.xlabel("Sample")
    plt.ylabel("RSSI (dBm)")
    plt.title("Measured RSSI fluctuation")
    plt.grid(alpha=0.4)
    plt.savefig("measured_fluctuation.png", dpi=150)
    print("Saved measured_fluctuation.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=float, default=1.5, help="receiver speed (m/s)")
    parser.add_argument("--freq", type=float, default=2.4e9)
    parser.add_argument("--k", type=float, default=5, help="Rician K-factor (linear)")
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--csv", help="analyse a measured RSSI log instead")
    args = parser.parse_args()
    if args.csv:
        return analyze_csv(args.csv)

    wavelength = 3e8 / args.freq
    fd = args.speed / wavelength
    fs = 50 * fd
    t = np.arange(0, args.duration, 1 / fs)
    h = clarke_fading(fd, t)
    K = args.k
    h_rice = np.sqrt(K / (K + 1)) + np.sqrt(1 / (K + 1)) * h   # LOS + scattered

    ray_db = 20 * np.log10(np.abs(h))
    rice_db = 20 * np.log10(np.abs(h_rice))
    coherence_time = 0.423 / fd

    print(f"Wavelength        : {wavelength * 100:.2f} cm")
    print(f"Max Doppler shift : {fd:.2f} Hz")
    print(f"Coherence time    : {coherence_time * 1000:.1f} ms")
    print(f"Fade spacing      : ~lambda/2 = {wavelength * 50:.2f} cm")
    for name, env in (("Rayleigh (NLOS)", ray_db), (f"Rician K={K:g} (LOS)", rice_db)):
        print(f"\n{name}")
        for k, v in stats(env).items():
            print(f"  {k:<26}: {v:.2f}")
    p_deep = np.mean(ray_db < -10) * 100
    print(f"\nRayleigh: {p_deep:.1f}% of time more than 10 dB below the mean (theory ~9.5%)")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.5))
    a1.plot(t * 1000, ray_db, label="Rayleigh (NLOS)")
    a1.plot(t * 1000, rice_db, label=f"Rician K={K:g} (LOS)", alpha=0.8)
    a1.set_xlabel("Time (ms)")
    a1.set_ylabel("Envelope relative to mean power (dB)")
    a1.set_title(f"Multipath fading, v = {args.speed} m/s, f = {args.freq / 1e9:g} GHz")
    a1.grid(alpha=0.4)
    a1.legend()

    r = np.abs(h)
    a2.hist(r, bins=60, density=True, alpha=0.6, label="Simulated envelope")
    x = np.linspace(0, r.max(), 200)
    sigma2 = np.mean(r ** 2) / 2
    a2.plot(x, x / sigma2 * np.exp(-x ** 2 / (2 * sigma2)), "r", label="Rayleigh pdf")
    a2.set_xlabel("Envelope amplitude")
    a2.set_title("Envelope distribution")
    a2.legend()
    fig.tight_layout()
    fig.savefig("multipath_fading.png", dpi=150)
    print("Saved multipath_fading.png")


if __name__ == "__main__":
    main()
