# Experiment 3: Demonstration of Frequency Reuse in Cellular Systems

**Aim:** Demonstration of the frequency reuse concept in cellular systems (simulation/visualization).

**Lab Outcome:** MDL501.2

## Theory

### Cellular concept
A cellular system splits the service area into small regions called **cells**. Each cell has its own base station using low transmit power. Cells are drawn as **hexagons** because hexagons tile a plane without gaps and are the closest tiling shape to a circular coverage area.

### Frequency reuse
Spectrum is limited, so the same set of channels is **reused** in cells far enough apart that they do not interfere badly.
- The total channels **S** are split among **N** cells that form a **cluster**. Each cell gets k = S/N channels.
- The cluster is repeated across the area. Cells that use the same channel set are **co-channel cells**.
- Capacity: C = M·k·N = M·S, where M is how many times the cluster repeats.

### Cluster size
For a hexagonal geometry the cluster size can only take the values

$$N = i^2 + ij + j^2 \qquad (i, j = 0, 1, 2, \dots)$$

which gives N = 1, 3, 4, 7, 9, 12, 13, 19, ...

To find the nearest co-channel cell: move **i** cells along a chain of hexagons, turn 60° anticlockwise, then move **j** cells.

### Co-channel reuse ratio
$$Q = \frac{D}{R} = \sqrt{3N}$$

where D is the distance between co-channel cell centres and R is the cell radius.

### Signal-to-interference ratio
With i₀ = 6 first-tier co-channel interferers and path loss exponent n:

$$\frac{S}{I} = \frac{(\sqrt{3N})^n}{i_0}$$

| N | Q | S/I (n = 4) |
|---|---|---|
| 3 | 3.00 | 11.3 dB |
| 4 | 3.46 | 13.8 dB |
| 7 | 4.58 | 18.7 dB |
| 12 | 6.00 | 23.3 dB |

GSM-style systems need S/I ≥ 18 dB, so **N = 7** is the classic choice.

### Trade-off
- **Small N:** more channels per cell and more capacity, but co-channel cells are closer, so there is more interference.
- **Large N:** less interference, but fewer channels per cell and less capacity.

## Procedure
1. Run `python frequency_reuse.py --i 2 --j 1` (N = 7).
2. Look at `frequency_reuse_N7.png`: each letter is a channel group, and every cell labelled **A** reuses the centre cell's channels.
3. Repeat with `--i 1 --j 1` (N = 3), `--i 2 --j 0` (N = 4) and `--i 2 --j 2` (N = 12).
4. Record Q and S/I from the terminal output and compare the interference distance across cluster sizes.

## Conclusion
Frequency reuse lets a limited spectrum serve a large area. A larger cluster size increases the co-channel distance and S/I, but reduces the channels available per cell. Choosing N is a trade-off between capacity and interference.
