"""
Experiment 6: Study of Bluetooth communication (discovery and range testing).

scan  : discover nearby Bluetooth Low Energy devices with their RSSI
watch : log the RSSI of one device over time while you walk away from it,
        and estimate distance with d = 10 ^ ((TxPower - RSSI) / (10 * n))

Requires:  pip install bleak
Run:
  python bluetooth_scan.py scan --timeout 8
  python bluetooth_scan.py watch --address <ADDRESS> --label 2m --csv bt_range.csv
"""
import argparse
import asyncio
import csv
import os
import time

from bleak import BleakScanner


def estimate_distance(rssi, tx_power=-59, n=2.0):
    """tx_power is the expected RSSI at 1 m."""
    return 10 ** ((tx_power - rssi) / (10 * n))


async def scan(timeout):
    found = await BleakScanner.discover(timeout=timeout, return_adv=True)
    rows = sorted(found.values(), key=lambda da: da[1].rssi, reverse=True)
    print(f"{'Address':<40} {'Name':<25} {'RSSI':>5} {'Est. dist (m)':>14}")
    for device, adv in rows:
        name = adv.local_name or device.name or "(unknown)"
        print(f"{device.address:<40} {name[:25]:<25} {adv.rssi:>5} {estimate_distance(adv.rssi):>14.2f}")
    print(f"\n{len(rows)} device(s) found")


async def watch(address, duration, label, csv_path, tx_power, n):
    samples = []

    def on_adv(device, adv):
        if device.address.lower() == address.lower():
            samples.append(adv.rssi)
            print(f"  RSSI {adv.rssi} dBm  ->  ~{estimate_distance(adv.rssi, tx_power, n):.2f} m")

    async with BleakScanner(detection_callback=on_adv):
        await asyncio.sleep(duration)

    if not samples:
        print("Device not seen. Check the address and that it is advertising.")
        return
    avg = sum(samples) / len(samples)
    new_file = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["time", "label", "avg_rssi_dbm", "samples", "est_distance_m"])
        w.writerow([time.strftime("%H:%M:%S"), label, round(avg, 1), len(samples),
                    round(estimate_distance(avg, tx_power, n), 2)])
    print(f"[{label}] average RSSI {avg:.1f} dBm over {len(samples)} samples -> saved to {csv_path}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("--timeout", type=float, default=8)
    w = sub.add_parser("watch")
    w.add_argument("--address", required=True)
    w.add_argument("--duration", type=float, default=15)
    w.add_argument("--label", default="")
    w.add_argument("--csv", default="bt_range.csv")
    w.add_argument("--tx-power", type=float, default=-59)
    w.add_argument("--n", type=float, default=2.0)
    args = parser.parse_args()
    if args.cmd == "scan":
        asyncio.run(scan(args.timeout))
    else:
        asyncio.run(watch(args.address, args.duration, args.label, args.csv, args.tx_power, args.n))


if __name__ == "__main__":
    main()
