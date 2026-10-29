# Experiment 6: Study of Bluetooth Communication Using Mobile Devices

**Aim:** Study of Bluetooth communication using mobile devices (pairing, range testing).

**Lab Outcome:** MDL501.4

## Theory

### Bluetooth
Bluetooth (IEEE 802.15.1) is a short-range wireless technology for **Wireless Personal Area Networks (WPAN)**. It works in the unlicensed **2.4 GHz ISM band (2.400–2.4835 GHz)**.

| Feature | Bluetooth Classic (BR/EDR) | Bluetooth Low Energy (BLE) |
|---|---|---|
| Channels | 79 × 1 MHz | 40 × 2 MHz (3 advertising) |
| Data rate | 1–3 Mbps | 125 kbps – 2 Mbps |
| Range | ~10 m (Class 2) | 10–100 m (up to ~1 km with Coded PHY in BT 5) |
| Power | ~1 W peak | 0.01–0.5 W |
| Use | Audio, file transfer | Wearables, beacons, IoT |

### Frequency Hopping Spread Spectrum (FHSS)
Classic Bluetooth hops **1600 times per second** in a pseudo-random sequence across 79 channels. **Adaptive Frequency Hopping (AFH)** skips channels that are busy (for example with Wi-Fi), which reduces interference.

### Piconet and scatternet
- **Piconet:** one **central (master)** and up to **7 active peripherals (slaves)** share the master's clock and hopping sequence.
- **Scatternet:** several piconets linked through a device that belongs to more than one.

### Power classes
| Class | Max power | Range |
|---|---|---|
| 1 | 100 mW (20 dBm) | ~100 m |
| 2 | 2.5 mW (4 dBm) | ~10 m |
| 3 | 1 mW (0 dBm) | ~1 m |

### Pairing process
1. **Inquiry / discovery:** a device broadcasts inquiry packets, and discoverable devices respond with their address and name.
2. **Paging / connection:** a connection is set up with the selected device.
3. **Pairing:** keys are exchanged using **Secure Simple Pairing (SSP)** methods: *Just Works*, *Numeric Comparison*, *Passkey Entry* or *Out-of-Band (NFC)*.
4. **Bonding:** the link key is stored so the devices can reconnect automatically later.

### Bluetooth protocol stack
Radio → Baseband → Link Manager (LMP) → HCI → L2CAP → RFCOMM / SDP / ATT-GATT → Profiles (A2DP, HFP, OPP, HID)

### Distance estimation from RSSI
$$d = 10^{\frac{TxPower - RSSI}{10\,n}}$$

where TxPower is the RSSI at 1 m (about −59 dBm) and n is the path loss exponent.

## Procedure

### Part A: Pairing with two mobile phones
1. Turn on Bluetooth on both phones and make Phone B discoverable.
2. On Phone A, scan for devices and select Phone B.
3. Confirm that the same numeric code appears on both phones (Numeric Comparison).
4. Send a file (an image of known size) from A to B and note how long the transfer takes.
5. Data rate = file size × 8 / time.

### Part B: Range testing
1. Keep the paired phones 1 m apart and start the file transfer or play audio to a Bluetooth speaker.
2. Increase the distance in steps of 2 m (2, 4, 6, 8, 10, 12 m...) and note where audio breaks or the transfer fails.
3. Repeat with a wall or human body between the devices.
4. Using a laptop, run `python bluetooth_scan.py scan` to list nearby BLE devices and their RSSI.
5. Run `python bluetooth_scan.py watch --address <phone/beacon address> --label 2m` at each distance and compare the estimated distance with the real one. (An app such as *nRF Connect* can also show RSSI.)

## Observation table
| Distance (m) | Line of sight? | RSSI (dBm) | Transfer / audio status |
|---|---|---|---|
| 1 | Yes | | |
| 4 | Yes | | |
| 8 | Yes | | |
| 4 | Wall | | |

## Conclusion
Bluetooth devices discover, pair and bond securely within a short range. RSSI falls with distance and obstacles, and the link fails once the signal drops below receiver sensitivity (about −90 dBm). Range depends on power class, environment and interference.
