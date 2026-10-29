"""
Experiment 3: Demonstration of frequency reuse in cellular systems.

Draws a hexagonal cell layout coloured by channel group for a cluster size
N = i^2 + i*j + j^2, highlights the co-channel cells of the centre cell and
prints the co-channel reuse ratio Q = D/R and the signal-to-interference ratio
S/I = Q^n / i0 for common cluster sizes.

Run:  python frequency_reuse.py [--i 2 --j 1] [--rings 4] [--n 4]
Output: frequency_reuse_N<N>.png
"""
import argparse
from math import floor, log10, sqrt

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

R = 1.0  # cell radius


def axial_to_xy(q, r):
    return R * sqrt(3) * (q + r / 2), R * 1.5 * r


def cells_within(rings):
    return [(q, r) for q in range(-rings, rings + 1) for r in range(-rings, rings + 1)
            if abs(q + r) <= rings]


def channel_group(q, r, i, j):
    """Map a cell to its channel group by reducing it modulo the co-channel lattice."""
    a = (i, j)            # shift to the nearest co-channel cell
    b = (-j, i + j)       # the same shift rotated by 60 degrees
    det = a[0] * b[1] - a[1] * b[0]  # = N
    x = (q * b[1] - r * b[0]) / det
    y = (a[0] * r - a[1] * q) / det
    fx, fy = floor(x + 1e-9), floor(y + 1e-9)
    return (q - fx * a[0] - fy * b[0], r - fx * a[1] - fy * b[1])


def sir_db(n_cluster, path_loss_exp=4, interferers=6):
    q = sqrt(3 * n_cluster)
    return 10 * log10(q ** path_loss_exp / interferers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", type=int, default=2)
    parser.add_argument("--j", type=int, default=1)
    parser.add_argument("--rings", type=int, default=4)
    parser.add_argument("--n", type=float, default=4, help="path loss exponent")
    parser.add_argument("--channels", type=int, default=420, help="total duplex channels")
    args = parser.parse_args()
    i, j = args.i, args.j
    N = i * i + i * j + j * j

    print("Cluster size and interference (path loss exponent n = %g, 6 first-tier interferers)" % args.n)
    print(f"{'N':>3} {'(i,j)':>6} {'Q = D/R':>8} {'S/I (dB)':>9} {'Channels/cell':>14}")
    for (ii, jj) in [(1, 1), (2, 0), (2, 1), (3, 0), (2, 2), (3, 1)]:
        n_ = ii * ii + ii * jj + jj * jj
        print(f"{n_:>3} {str((ii, jj)):>6} {sqrt(3 * n_):>8.2f} {sir_db(n_, args.n):>9.2f} "
              f"{args.channels // n_:>14}")

    cells = cells_within(args.rings)
    groups = {channel_group(0, 0, i, j): 0}  # centre cell is group A
    for q, r in cells:
        groups.setdefault(channel_group(q, r, i, j), len(groups))
    centre_group = groups[channel_group(0, 0, i, j)]

    fig, ax = plt.subplots(figsize=(9, 9))
    cmap = plt.cm.tab20 if N > 10 else plt.cm.tab10
    for q, r in cells:
        g = groups[channel_group(q, r, i, j)]
        x, y = axial_to_xy(q, r)
        co_channel = g == centre_group
        ax.add_patch(RegularPolygon((x, y), 6, radius=R, facecolor=cmap(g % cmap.N),
                                    edgecolor="red" if co_channel else "k",
                                    linewidth=3 if co_channel else 0.8, alpha=0.75))
        ax.text(x, y, chr(65 + g) if g < 26 else str(g), ha="center", va="center",
                fontsize=10, weight="bold" if co_channel else "normal")

    D = R * sqrt(3 * N)
    ax.add_patch(plt.Circle((0, 0), D, fill=False, ls="--", color="red"))
    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")
    ax.set_title(f"Frequency reuse, cluster size N = {N} (i={i}, j={j})\n"
                 f"Co-channel cells (group A) outlined in red, D = {D:.2f}R, "
                 f"S/I = {sir_db(N, args.n):.1f} dB")
    out = f"frequency_reuse_N{N}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nCells drawn: {len(cells)}, channel groups: {len(groups)} (expected {N})")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
