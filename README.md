# MDL501 – Wireless Technology Lab

Code and theory for the MDL501 lab experiments (Department of Computer Engineering, University of Mumbai syllabus).
Each folder has a `theory.md` (aim, lab outcome, theory, procedure, observation table, conclusion) and the code for that experiment. Sample output plots are included.

| No. | Experiment | LO | Code |
|---|---|---|---|
| 1 | [Study of electromagnetic spectrum allocation and wireless bands](Exp01_EM_Spectrum/theory.md) | MDL501.1 | `spectrum_bands.py` |
| 2 | [Simulation of basic communication system (Tx–Channel–Rx)](Exp02_Tx_Channel_Rx/theory.md) | MDL501.2 | `tx_channel_rx.py`, `tx_channel_rx.m` |
| 3 | [Demonstration of frequency reuse in cellular systems](Exp03_Frequency_Reuse/theory.md) | MDL501.2 | `frequency_reuse.py` |
| 4 | [Measurement of signal strength vs distance for Wi-Fi router](Exp04_WiFi_Signal_vs_Distance/theory.md) | MDL501.3 | `wifi_rssi.py` |
| 5 | [Throughput and latency measurement (ping, speed test)](Exp05_Throughput_Latency/theory.md) | MDL501.4 | `net_perf.py` |
| 6 | [Study of Bluetooth communication (pairing, range testing)](Exp06_Bluetooth/theory.md) | MDL501.4 | `bluetooth_scan.py` |
| 7 | [Study of path loss in an indoor environment (RSSI vs obstacles)](Exp07_Indoor_Path_Loss/theory.md) | MDL501.5 | `path_loss.py` |
| 8 | [Analysis of multipath effects (signal fluctuation)](Exp08_Multipath_Fading/theory.md) | MDL501.5 | `multipath.py` |
| 9 | [Noise and interference analysis in wireless communication](Exp09_Noise_Interference/theory.md) | MDL501.6 | `noise_interference.py` |
| 10 | [Introduction to network simulation tool (NS-3)](Exp10_NS3_Simulation/theory.md) | MDL501.6 | `wifi-basic.cc` |
| 11 | [Innovative: Cellular call setup and handover simulation](Exp11_Innovative_Handover/theory.md) | MDL501.1 | `handover_sim.py` |

## Setup

```bash
git clone https://github.com/theiter8r/MDL501-Wireless-Lab.git
cd MDL501-Wireless-Lab
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run any experiment from inside its folder, for example:

```bash
cd Exp02_Tx_Channel_Rx
python tx_channel_rx.py
```

- Experiments 4–9 that need real measurements also accept CSV data, and sample data is included so every script runs without hardware.
- Experiment 6 needs a Bluetooth adapter and `bleak`.
- Experiment 10 needs [NS-3](https://www.nsnam.org/) (Linux / WSL). See its theory file for build steps.
