# Experiment 10: Introduction to the Network Simulation Tool (NS-3)

**Aim:** Introduction to a network simulation tool (NS-3 / any GUI-based simulator), basic experiment.

**Lab Outcome:** MDL501.6

## Theory

### Network simulation
A network simulator models the behaviour of a network (nodes, links, protocols, traffic) in software. Simulation lets us study large or expensive networks, repeat experiments exactly, and test new protocols without real hardware.

### NS-3
**NS-3** is an open-source **discrete-event network simulator** written in **C++** with Python bindings. It is widely used in research and teaching for wired, wireless (Wi-Fi, LTE, 5G NR via 5G-LENA), ad hoc (AODV, OLSR) and IoT networks.

**Discrete-event simulation:** the simulator keeps a queue of time-stamped events (packet sent, packet received, timer expired) and processes them in order, jumping straight from one event to the next.

### Key NS-3 abstractions
| Abstraction | Description |
|---|---|
| **Node** | A computer, phone, router or AP (an empty shell to which devices and stacks are added) |
| **NetDevice** | A network interface card (WifiNetDevice, CsmaNetDevice, PointToPointNetDevice) |
| **Channel** | The medium connecting devices (YansWifiChannel, CsmaChannel) |
| **Protocol stack** | InternetStackHelper installs IPv4/IPv6, TCP, UDP and routing |
| **Application** | Traffic generators and sinks (OnOff, BulkSend, UdpEcho, PacketSink) |
| **Helpers** | Classes that configure many objects at once (WifiHelper, MobilityHelper) |
| **Mobility model** | Node positions and movement (ConstantPosition, RandomWalk2d) |

### Wi-Fi model in NS-3
- **PHY:** `YansWifiPhy` (or `SpectrumWifiPhy`) with propagation loss (LogDistance, Friis) and delay models.
- **MAC:** `ApWifiMac` (AP sends beacons), `StaWifiMac` (station associates), `AdhocWifiMac`.
- **Rate control:** Constant, Minstrel, Ideal and others.
- **Standards:** 802.11a/b/g/n/ac/ax/be.

### Output and analysis tools
- **FlowMonitor:** per-flow throughput, delay, jitter and loss
- **pcap traces:** open in **Wireshark**
- **ASCII traces** and logging (`NS_LOG`)
- **NetAnim:** animation of node movement and packets
- GUI-based alternatives: **Cisco Packet Tracer**, **OMNeT++**, **GNS3**, **NetSim**

## Procedure
1. Install NS-3 (Ubuntu / WSL):
   ```bash
   sudo apt install g++ python3 cmake ninja-build git
   git clone https://gitlab.com/nsnam/ns-3-dev.git && cd ns-3-dev
   ./ns3 configure --enable-examples && ./ns3 build
   ```
2. Copy `wifi-basic.cc` into `ns-3-dev/scratch/`.
3. Run `./ns3 run "scratch/wifi-basic --nSta=3 --distance=10 --dataRate=5Mbps"`.
4. Record per-flow throughput, delay and loss from the output.
5. Repeat for distance = 10, 30, 50, 80 m and nSta = 1, 3, 5, 10, and note how performance changes.
6. Open `wifi-basic-ap-*.pcap` in Wireshark to see beacons, association, ACKs and UDP data frames.

*GUI alternative:* in Cisco Packet Tracer, place a wireless router and 3 laptops with wireless NICs, set the SSID/WPA2 key, assign IPs with DHCP and test connectivity with ping in simulation mode.

## Observation table
| Stations | Distance (m) | Aggregate throughput (Mbps) | Avg delay (ms) | Loss (%) |
|---|---|---|---|---|
| 3 | 10 | | | |
| 3 | 50 | | | |
| 10 | 10 | | | |

## Conclusion
We learned NS-3's basic building blocks (nodes, devices, channels, stacks, applications) and simulated an infrastructure Wi-Fi network. Throughput falls and delay and loss rise as the distance grows (lower data rates) and as more stations share the medium (CSMA/CA contention).
