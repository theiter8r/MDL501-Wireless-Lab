"""
Experiment 4: Measurement of signal strength vs distance for a Wi-Fi router.

measure : read the current Wi-Fi RSSI several times at one distance and
          append the average to a CSV file
analyze : fit the log-distance path loss model
          RSSI(d) = RSSI(d0) - 10 * n * log10(d / d0)
          and plot measured vs fitted RSSI

Run:
  python wifi_rssi.py measure --distance 1 --samples 10
  python wifi_rssi.py measure --distance 2
  ...
  python wifi_rssi.py analyze --csv readings.csv
  python wifi_rssi.py analyze --csv sample_readings.csv   # demo data

Supports macOS, Linux (iw / nmcli) and Windows (netsh).
"""
import argparse
import csv
import os
import platform
import re
import statistics
import subprocess
import time


def read_rssi_dbm():
    system = platform.system()
    if system == "Darwin":
        out = subprocess.run(["system_profiler", "SPAirPortDataType"],
                             capture_output=True, text=True).stdout
        m = re.search(r"Signal / Noise:\s*(-?\d+) dBm", out)
        if m:
            return int(m.group(1))
    elif system == "Linux":
        try:
            out = subprocess.run(["iw", "dev"], capture_output=True, text=True).stdout
            for iface in re.findall(r"Interface (\S+)", out):
                link = subprocess.run(["iw", "dev", iface, "link"],
                                      capture_output=True, text=True).stdout
                m = re.search(r"signal:\s*(-?\d+) dBm", link)
                if m:
                    return int(m.group(1))
        except FileNotFoundError:
            pass
        out = subprocess.run(["nmcli", "-t", "-f", "ACTIVE,SIGNAL", "dev", "wifi"],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            if line.startswith("yes:"):
                return int(line.split(":")[1]) // 2 - 100  # % -> approx dBm
    elif system == "Windows":
        out = subprocess.run(["netsh", "wlan", "show", "interfaces"],
                             capture_output=True, text=True).stdout
        m = re.search(r"Signal\s*:\s*(\d+)%", out)
        if m:
            return int(m.group(1)) // 2 - 100
    raise RuntimeError("Could not read Wi-Fi RSSI. Are you connected to Wi-Fi?")


def measure(args):
    readings = []
    for k in range(args.samples):
        rssi = read_rssi_dbm()
        readings.append(rssi)
        print(f"  sample {k + 1}/{args.samples}: {rssi} dBm")
        time.sleep(args.interval)
    avg = statistics.mean(readings)
    new_file = not os.path.exists(args.csv)
    with open(args.csv, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["distance_m", "rssi_dbm", "std_db", "samples"])
        w.writerow([args.distance, round(avg, 2), round(statistics.pstdev(readings), 2), len(readings)])
    print(f"Distance {args.distance} m -> average RSSI {avg:.1f} dBm (saved to {args.csv})")


def analyze(args):
    import matplotlib.pyplot as plt
    import numpy as np

    d, rssi = [], []
    with open(args.csv) as f:
        for row in csv.DictReader(f):
            d.append(float(row["distance_m"]))
            rssi.append(float(row["rssi_dbm"]))
    d, rssi = np.array(d), np.array(rssi)

    # Linear fit of RSSI against 10*log10(d): slope = -n, intercept = RSSI at 1 m
    x = 10 * np.log10(d)
    slope, intercept = np.polyfit(x, rssi, 1)
    n = -slope
    fitted = intercept + slope * x
    rmse = np.sqrt(np.mean((rssi - fitted) ** 2))

    print(f"{'Distance (m)':>12} {'Measured (dBm)':>15} {'Model (dBm)':>12}")
    for di, ri, fi in zip(d, rssi, fitted):
        print(f"{di:>12g} {ri:>15.1f} {fi:>12.1f}")
    print(f"\nRSSI at 1 m (A)        : {intercept:.1f} dBm")
    print(f"Path loss exponent (n) : {n:.2f}  (free space = 2, indoor 2.5-4)")
    print(f"RMSE                   : {rmse:.2f} dB")

    dd = np.linspace(d.min(), d.max(), 200)
    plt.figure(figsize=(7, 5))
    plt.plot(d, rssi, "o", label="Measured")
    plt.plot(dd, intercept - 10 * n * np.log10(dd), "-", label=f"Log-distance fit (n = {n:.2f})")
    plt.plot(dd, intercept - 20 * np.log10(dd), "--", label="Free space (n = 2)")
    plt.xlabel("Distance from router (m)")
    plt.ylabel("RSSI (dBm)")
    plt.title("Wi-Fi signal strength vs distance")
    plt.grid(alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig("rssi_vs_distance.png", dpi=150)
    print("Saved rssi_vs_distance.png")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("--distance", type=float, required=True)
    m.add_argument("--samples", type=int, default=10)
    m.add_argument("--interval", type=float, default=1.0)
    m.add_argument("--csv", default="readings.csv")
    a = sub.add_parser("analyze")
    a.add_argument("--csv", default="readings.csv")
    args = parser.parse_args()
    measure(args) if args.cmd == "measure" else analyze(args)


if __name__ == "__main__":
    main()
