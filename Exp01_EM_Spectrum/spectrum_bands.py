"""
Experiment 1: Study of electromagnetic spectrum allocation and wireless bands.

Prints the ITU radio band table and common wireless services, then draws a
log-scale chart of where each service sits in the spectrum.

Run:  python spectrum_bands.py
Output: spectrum_chart.png
"""
import matplotlib.pyplot as plt

# ITU radio bands: (name, full form, start Hz, end Hz, typical use)
ITU_BANDS = [
    ("ELF", "Extremely Low Frequency", 3, 30, "Submarine communication"),
    ("SLF", "Super Low Frequency", 30, 300, "Power grids, submarines"),
    ("ULF", "Ultra Low Frequency", 300, 3e3, "Mine communication"),
    ("VLF", "Very Low Frequency", 3e3, 30e3, "Navigation, time signals"),
    ("LF", "Low Frequency", 30e3, 300e3, "AM longwave, RFID (125 kHz)"),
    ("MF", "Medium Frequency", 300e3, 3e6, "AM broadcast radio"),
    ("HF", "High Frequency", 3e6, 30e6, "Shortwave, amateur radio, NFC (13.56 MHz)"),
    ("VHF", "Very High Frequency", 30e6, 300e6, "FM radio, TV, aviation"),
    ("UHF", "Ultra High Frequency", 300e6, 3e9, "Mobile, Wi-Fi 2.4 GHz, Bluetooth, GPS"),
    ("SHF", "Super High Frequency", 3e9, 30e9, "Wi-Fi 5/6 GHz, 5G FR1/FR2, satellite"),
    ("EHF", "Extremely High Frequency", 30e9, 300e9, "5G mmWave, radar, 60 GHz WiGig"),
]

# Wireless services: (name, start Hz, end Hz)
SERVICES = [
    ("AM Radio", 535e3, 1.705e6),
    ("NFC", 13.553e6, 13.567e6),
    ("FM Radio", 88e6, 108e6),
    ("GSM 900", 880e6, 960e6),
    ("GPS L1", 1.57542e9 - 1e6, 1.57542e9 + 1e6),
    ("GSM 1800 / LTE B3", 1.71e9, 1.88e9),
    ("LTE B40 (TDD)", 2.3e9, 2.4e9),
    ("Wi-Fi / Bluetooth 2.4 GHz (ISM)", 2.4e9, 2.4835e9),
    ("5G n78", 3.3e9, 3.8e9),
    ("Wi-Fi 5 GHz", 5.15e9, 5.875e9),
    ("Wi-Fi 6E (6 GHz)", 5.925e9, 7.125e9),
    ("Satellite Ku band", 12e9, 18e9),
    ("5G mmWave n257/n258", 24.25e9, 29.5e9),
    ("60 GHz WiGig", 57e9, 71e9),
]


def fmt(hz):
    for unit, scale in (("GHz", 1e9), ("MHz", 1e6), ("kHz", 1e3)):
        if hz >= scale:
            return f"{hz / scale:g} {unit}"
    return f"{hz:g} Hz"


def wavelength(hz):
    return 3e8 / hz


def main():
    print(f"{'Band':<5} {'Full form':<26} {'Range':<22} {'Wavelength':<20} Use")
    print("-" * 110)
    for name, full, lo, hi, use in ITU_BANDS:
        wl = f"{wavelength(hi):.3g} m - {wavelength(lo):.3g} m"
        print(f"{name:<5} {full:<26} {fmt(lo) + ' - ' + fmt(hi):<22} {wl:<20} {use}")

    print("\nCommon wireless services")
    print("-" * 60)
    for name, lo, hi in SERVICES:
        print(f"{name:<32} {fmt(lo):>10} - {fmt(hi):<10} BW = {fmt(hi - lo)}")

    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.tab20.colors
    for i, (name, _, lo, hi, _) in enumerate(ITU_BANDS):
        ax.axvspan(lo, hi, color=colors[i % 20], alpha=0.25)
        ax.text((lo * hi) ** 0.5, len(SERVICES) + 0.3, name, ha="center", fontsize=9, weight="bold")
    for i, (name, lo, hi) in enumerate(SERVICES):
        ax.barh(i, hi - lo, left=lo, height=0.6, color="tab:blue")
        ax.text(hi * 1.15, i, name, va="center", fontsize=8)
    ax.set_xscale("log")
    ax.set_xlim(1e5, 3e11)
    ax.set_ylim(-1, len(SERVICES) + 1)
    ax.set_yticks([])
    ax.set_xlabel("Frequency (Hz, log scale)")
    ax.set_title("Radio spectrum allocation and wireless services")
    fig.tight_layout()
    fig.savefig("spectrum_chart.png", dpi=150)
    print("\nSaved spectrum_chart.png")


if __name__ == "__main__":
    main()
