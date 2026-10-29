# Experiment 5: Throughput and Latency Measurement Using Network Tools

**Aim:** Throughput and latency measurement using network tools (e.g., ping, speed test).

**Lab Outcome:** MDL501.4

## Theory

### Performance metrics
| Metric | Definition | Unit |
|---|---|---|
| **Bandwidth** | Maximum theoretical capacity of a link | Mbps |
| **Throughput** | Data actually delivered per unit time | Mbps |
| **Latency (RTT)** | Time for a packet to reach the destination and return | ms |
| **Jitter** | Variation in latency between packets | ms |
| **Packet loss** | Percentage of packets that never arrive | % |

Throughput is always lower than bandwidth because of protocol overhead (headers, ACKs), retransmissions, congestion, interference and weak signal.

### Components of latency
$$\text{Latency} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$$
- **Processing delay:** time to examine headers and route the packet
- **Queuing delay:** time spent waiting in router buffers
- **Transmission delay:** L/R (packet length / link rate)
- **Propagation delay:** distance / speed of light in the medium

On wireless links, extra delay comes from **CSMA/CA** channel contention, retransmissions after collisions or fading, and power-saving modes.

### Tools
- **ping:** sends ICMP Echo Request packets and measures the round-trip time of each Echo Reply.
- **traceroute / tracert:** shows the per-hop delay along the path.
- **Speed test (speedtest.net, fast.com):** opens several TCP connections to a nearby server and measures download/upload throughput.
- **iperf3:** sends controlled TCP/UDP traffic between two hosts on a LAN to measure throughput.

### Typical values
| Application | Acceptable latency | Throughput needed |
|---|---|---|
| Web browsing | < 100 ms | 1–5 Mbps |
| VoIP | < 150 ms, jitter < 30 ms | 0.1 Mbps |
| Online gaming | < 50 ms | 3–6 Mbps |
| HD video streaming | < 200 ms | 5–8 Mbps |

## Procedure
1. Connect to Wi-Fi and run `python net_perf.py`.
2. Record the min/avg/max RTT, jitter, packet loss, and download/upload throughput.
3. Repeat (a) close to the router, (b) far from the router, (c) on mobile data, and (d) on the 2.4 GHz and 5 GHz bands.
4. Run `ping -c 20 <router IP>` and `ping -c 20 google.com`, and compare LAN latency with Internet latency.
5. Optional: run `iperf3 -s` on one machine and `iperf3 -c <server-ip>` on another to measure LAN throughput.
6. Cross-check against speedtest.net or fast.com.

## Observation table
| Condition | Avg RTT (ms) | Jitter (ms) | Loss (%) | Download (Mbps) | Upload (Mbps) |
|---|---|---|---|---|---|
| Near router | | | | | |
| Far from router | | | | | |
| Mobile data | | | | | |

## Conclusion
Throughput and latency depend on signal strength, distance, interference and network load. As the device moves away from the router, latency and jitter rise and throughput falls, because of lower data rates and more retransmissions.
