"""
Experiment 5: Throughput and latency measurement using network tools.

Latency    : runs the system `ping` and reports min / avg / max RTT,
             jitter (mean change between consecutive RTTs) and packet loss
Throughput : downloads and uploads test data over HTTP
             (Cloudflare speed test endpoints) and reports Mbps

Run:
  python net_perf.py                       # ping 8.8.8.8 + speed test
  python net_perf.py --host google.com --count 20
  python net_perf.py --no-speed            # latency only
"""
import argparse
import platform
import re
import statistics
import subprocess
import time
import urllib.request

DOWN_URL = "https://speed.cloudflare.com/__down?bytes={}"
UP_URL = "https://speed.cloudflare.com/__up"


def ping(host, count):
    flag = "-n" if platform.system() == "Windows" else "-c"
    out = subprocess.run(["ping", flag, str(count), host], capture_output=True, text=True).stdout
    rtts = [float(x) for x in re.findall(r"time[=<]\s*([\d.]+)\s*ms", out)]
    loss = 100 * (count - len(rtts)) / count
    return rtts, loss


def download_mbps(n_bytes):
    req = urllib.request.Request(DOWN_URL.format(n_bytes), headers={"User-Agent": "mdl501-lab"})
    start = time.perf_counter()
    received = 0
    with urllib.request.urlopen(req, timeout=60) as resp:
        while chunk := resp.read(64 * 1024):
            received += len(chunk)
    elapsed = time.perf_counter() - start
    return received * 8 / elapsed / 1e6, received, elapsed


def upload_mbps(n_bytes):
    data = b"0" * n_bytes
    req = urllib.request.Request(UP_URL, data=data, method="POST",
                                 headers={"User-Agent": "mdl501-lab",
                                          "Content-Type": "application/octet-stream"})
    start = time.perf_counter()
    with urllib.request.urlopen(req, timeout=60) as resp:
        resp.read()
    elapsed = time.perf_counter() - start
    return n_bytes * 8 / elapsed / 1e6, elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="8.8.8.8")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--down-mb", type=float, default=25)
    parser.add_argument("--up-mb", type=float, default=5)
    parser.add_argument("--no-speed", action="store_true")
    args = parser.parse_args()

    print(f"--- Latency: ping {args.host} x {args.count} ---")
    rtts, loss = ping(args.host, args.count)
    if rtts:
        jitter = statistics.mean(abs(a - b) for a, b in zip(rtts, rtts[1:])) if len(rtts) > 1 else 0.0
        print("RTTs (ms):", ", ".join(f"{r:g}" for r in rtts))
        print(f"Min / Avg / Max RTT : {min(rtts):.2f} / {statistics.mean(rtts):.2f} / {max(rtts):.2f} ms")
        print(f"Jitter              : {jitter:.2f} ms")
    print(f"Packet loss         : {loss:.1f} %")

    if args.no_speed:
        return
    print("\n--- Throughput ---")
    try:
        mbps, received, elapsed = download_mbps(int(args.down_mb * 1e6))
        print(f"Download : {mbps:.2f} Mbps ({received / 1e6:.1f} MB in {elapsed:.2f} s)")
        mbps, elapsed = upload_mbps(int(args.up_mb * 1e6))
        print(f"Upload   : {mbps:.2f} Mbps ({args.up_mb:.1f} MB in {elapsed:.2f} s)")
    except Exception as e:  # network may block the test server
        print(f"Speed test failed: {e}. Use speedtest.net / fast.com and record values manually.")


if __name__ == "__main__":
    main()
