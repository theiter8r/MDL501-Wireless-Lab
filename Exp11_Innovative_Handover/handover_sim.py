"""
Experiment 11 (Innovative): Cellular call setup and handover simulation.

A mobile user moves in a straight line from base station BS1 to BS2. The
received power from each BS follows a log-distance path loss with correlated
log-normal shadowing. The simulation:
  * sets up the call on the strongest BS (if it is above the minimum signal level)
  * hands over when the neighbour is stronger than the serving BS by the
    hysteresis margin H for the whole time-to-trigger (TTT)  (LTE event A3)
  * drops the call if the serving signal stays below the drop threshold
  * counts handovers and ping-pong handovers for several hysteresis values

Run:  python handover_sim.py [--speed 15] [--hyst 3] [--ttt 0.32]
Output: handover.png
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

PT_DBM = 43          # BS transmit power
PL_1M = 38           # path loss at 1 m (dB), 2 GHz
N_EXP = 3.5          # path loss exponent (urban)
SIGMA = 6            # shadowing std dev (dB)
D_CORR = 50          # shadowing decorrelation distance (m)
MIN_SETUP_DBM = -105
DROP_DBM = -115
PING_PONG_WINDOW = 5.0  # s: return to the previous cell within this time = ping-pong


def correlated_shadowing(x, rng):
    s = np.empty(len(x))
    s[0] = rng.normal(0, SIGMA)
    for k in range(1, len(x)):
        rho = np.exp(-abs(x[k] - x[k - 1]) / D_CORR)
        s[k] = rho * s[k - 1] + np.sqrt(1 - rho ** 2) * rng.normal(0, SIGMA)
    return s


def rx_power(d, shadow):
    return PT_DBM - PL_1M - 10 * N_EXP * np.log10(np.maximum(d, 1)) + shadow


def run(p1, p2, t, hyst, ttt):
    dt = t[1] - t[0]
    serving = 0 if p1[0] >= p2[0] else 1
    if max(p1[0], p2[0]) < MIN_SETUP_DBM:
        return None, [], 0, "call setup failed (no coverage)"
    p = (p1, p2)
    serving_trace = np.empty(len(t), dtype=int)
    events, timer, low_timer, ping_pong = [], 0.0, 0.0, 0
    status = "call completed"
    for k in range(len(t)):
        other = 1 - serving
        timer = timer + dt if p[other][k] > p[serving][k] + hyst else 0.0
        if timer >= ttt:
            # ping-pong: going back to the cell we left in the previous handover
            if events and events[-1][1] == serving and t[k] - events[-1][0] < PING_PONG_WINDOW:
                ping_pong += 1
            serving = other
            events.append((t[k], serving))
            timer = 0.0
        low_timer = low_timer + dt if p[serving][k] < DROP_DBM else 0.0
        if low_timer >= 1.0:
            status = f"call dropped at t = {t[k]:.1f} s"
            serving_trace[k:] = -1
            break
        serving_trace[k] = serving
    return serving_trace, events, ping_pong, status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--distance", type=float, default=2000, help="BS1-BS2 distance (m)")
    parser.add_argument("--speed", type=float, default=15, help="user speed (m/s)")
    parser.add_argument("--hyst", type=float, default=3, help="hysteresis margin (dB)")
    parser.add_argument("--ttt", type=float, default=0.32, help="time to trigger (s)")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    dt = 0.04
    t = np.arange(0, args.distance / args.speed, dt)
    x = args.speed * t
    p1 = rx_power(x, correlated_shadowing(x, rng))
    p2 = rx_power(args.distance - x, correlated_shadowing(x, rng))

    trace, events, pp, status = run(p1, p2, t, args.hyst, args.ttt)
    print(f"Call setup on BS{trace[0] + 1}: RSSI BS1 = {p1[0]:.1f} dBm, BS2 = {p2[0]:.1f} dBm")
    for te, to in events:
        print(f"  Handover at t = {te:6.2f} s, x = {args.speed * te:7.1f} m -> BS{to + 1}")
    print(f"Handovers: {len(events)}, ping-pong: {pp}, result: {status}")

    print(f"\n{'Hysteresis (dB)':>15} {'Handovers':>10} {'Ping-pong':>10} {'First HO at (m)':>16}")
    hysts = [0, 1, 2, 3, 4, 6, 8, 10]
    counts = []
    for h in hysts:
        _, ev, pp_h, _ = run(p1, p2, t, h, args.ttt)
        counts.append(len(ev))
        first = f"{args.speed * ev[0][0]:.0f}" if ev else "-"
        print(f"{h:>15} {len(ev):>10} {pp_h:>10} {first:>16}")

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [3, 1.3]})
    a1.plot(x, p1, label="RSSI from BS1")
    a1.plot(x, p2, label="RSSI from BS2")
    a1.axhline(DROP_DBM, color="r", ls=":", label="Call drop threshold")
    for te, to in events:
        a1.axvline(args.speed * te, color="k", ls="--", alpha=0.6)
    a1.step(x, np.where(trace == 0, p1, p2), "k", lw=0.8, alpha=0.5, label="Serving cell RSSI")
    a1.set_xlabel("Distance from BS1 (m)")
    a1.set_ylabel("Received power (dBm)")
    a1.set_title(f"Handover: H = {args.hyst} dB, TTT = {args.ttt} s, v = {args.speed} m/s "
                 f"({len(events)} handovers, {pp} ping-pong)")
    a1.grid(alpha=0.4)
    a1.legend(fontsize=8)
    a2.bar([str(h) for h in hysts], counts, color="tab:purple")
    a2.set_xlabel("Hysteresis margin (dB)")
    a2.set_ylabel("No. of handovers")
    fig.tight_layout()
    fig.savefig("handover.png", dpi=150)
    print("\nSaved handover.png")


if __name__ == "__main__":
    main()
