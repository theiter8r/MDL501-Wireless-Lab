"""
Experiment 7: Study of path loss in an indoor environment (RSSI vs obstacles).

Fits the multi-wall (Motley-Keenan) indoor path loss model to measured data

    RSSI = A - 10 * n * log10(d) - k * Lw

where A is the RSSI at 1 m, n is the path loss exponent, k is the number of walls
between router and receiver and Lw is the loss per wall. Collect RSSI
values with Exp04/wifi_rssi.py (or a Wi-Fi analyser app) and record them in a CSV
with columns: location, distance_m, walls, rssi_dbm

Run:  python path_loss.py --csv sample_obstacles.csv [--freq 2.4e9]
Output: path_loss.png
"""
import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np


def fspl_db(d, f):
    return 20 * np.log10(d) + 20 * np.log10(f) - 147.55


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="sample_obstacles.csv")
    parser.add_argument("--freq", type=float, default=2.4e9)
    parser.add_argument("--tx-dbm", type=float, default=20, help="router transmit power (EIRP)")
    args = parser.parse_args()

    rows = list(csv.DictReader(open(args.csv)))
    loc = [r["location"] for r in rows]
    d = np.array([float(r["distance_m"]) for r in rows])
    walls = np.array([int(r["walls"]) for r in rows])
    rssi = np.array([float(r["rssi_dbm"]) for r in rows])

    # Least squares: rssi = A + n * (-10 log10 d) + Lw * (-walls)
    X = np.column_stack([np.ones_like(d), -10 * np.log10(d), -walls])
    (A, n, Lw), *_ = np.linalg.lstsq(X, rssi, rcond=None)
    model = X @ np.array([A, n, Lw])
    rmse = np.sqrt(np.mean((rssi - model) ** 2))

    print(f"{'Location':<22} {'d (m)':>6} {'Walls':>6} {'RSSI':>7} {'Path loss':>10} "
          f"{'FSPL':>7} {'Model':>7}")
    for i in range(len(rows)):
        pl = args.tx_dbm - rssi[i]
        print(f"{loc[i]:<22} {d[i]:>6g} {walls[i]:>6} {rssi[i]:>7.1f} {pl:>10.1f} "
              f"{fspl_db(d[i], args.freq):>7.1f} {model[i]:>7.1f}")
    print(f"\nFitted model: RSSI = {A:.1f} - 10*{n:.2f}*log10(d) - {Lw:.1f}*walls")
    print(f"Path loss exponent n = {n:.2f}, loss per wall Lw = {Lw:.1f} dB, RMSE = {rmse:.2f} dB")

    plt.figure(figsize=(8, 5))
    dd = np.linspace(max(d.min(), 0.5), d.max(), 200)
    for k in sorted(set(walls)):
        sel = walls == k
        line = plt.plot(d[sel], rssi[sel], "o", label=f"Measured, {k} wall(s)")[0]
        plt.plot(dd, A - 10 * n * np.log10(dd) - k * Lw, "-", color=line.get_color(), alpha=0.6)
    plt.plot(dd, args.tx_dbm - fspl_db(dd, args.freq), "k--", label="Free space")
    plt.xscale("log")
    plt.xlabel("Distance (m, log scale)")
    plt.ylabel("RSSI (dBm)")
    plt.title(f"Indoor path loss: n = {n:.2f}, wall loss = {Lw:.1f} dB")
    plt.grid(alpha=0.4, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig("path_loss.png", dpi=150)
    print("Saved path_loss.png")


if __name__ == "__main__":
    main()
