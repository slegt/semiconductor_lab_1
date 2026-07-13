import pathlib

import pandas as pd
import matplotlib.pyplot as plt


# Define a function to standardize optical power units to nanowatts (nW)
def convert_to_nw(val):
    if pd.isna(val):
        return val
    val_str = str(val).strip()
    if "nW" in val_str:
        return float(val_str.replace("nW", "").strip())
    elif "uW" in val_str:
        return float(val_str.replace("uW", "").strip()) * 1000
    else:
        return float(val_str)


dir = pathlib.Path(__file__).parent.resolve()

# Load the dataset
files = [
    "Messdaten B7 - Raumtemperatur (108.48 Ohm).csv",
    "Messdaten B7 - 15°C (105.7 Ohm).csv",
    "Messdaten B7 - 30°C (111.6 Ohm).csv",
    "Messdaten B7 - 40°C (115.6 Ohm).csv"
]
for file_name in files:
    df = pd.read_csv(dir / file_name)

    # Apply the unit conversion
    df["Optische Leistung P (nW)"] = df["Optische Leistung P"].apply(convert_to_nw)

    # Initialize the plot layout
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot the I-V characteristic (Voltage vs. Current)
    ax1.semilogy(df["Diodenspannung V_D (mV)"], df["Diodenstrom I_D (mA)"], marker="o", linestyle="-")
    ax1.set_xlabel("Diodenspannung V_D (mV)")
    ax1.set_ylabel("Diodenstrom I_D (mA)")
    ax1.set_title("I-V Characteristic")
    ax1.grid(True)

    # Plot the P-I characteristic (Current vs. Optical Power)
    ax2.plot(df["Diodenstrom I_D (mA)"], df["Optische Leistung P (nW)"], marker="s", linestyle="-", color="r")
    ax2.set_xlabel("Diodenstrom I_D (mA)")
    ax2.set_ylabel("Optische Leistung P (nW)")
    ax2.set_title("P-I Characteristic")
    ax2.loglog()
    ax2.grid(True)

    # Adjust layout and render the figure
    plt.tight_layout()
    filename_without_ending = file_name.rsplit(".", maxsplit=1)[0]
    plt.savefig(fname=dir / "plots" / (filename_without_ending + ".pdf"))
