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
    "Messdaten B7 - 40°C (115.6 Ohm).csv",
    "Messdaten B7 - 50°C (119.23 Ohm).csv"
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))




for file_name in files:
    df = pd.read_csv(dir / file_name)
    label = file_name.split("-")[1].split("(")[0].strip()

    # Apply the unit conversion
    df["Optische Leistung P (nW)"] = df["Optische Leistung P"].apply(convert_to_nw)

    # Plot the I-V characteristic (Voltage vs. Current)
    ax1.semilogy(df["Diodenspannung V_D (mV)"], df["Diodenstrom I_D (mA)"], linestyle="-", label=label)

    # Plot the P-I characteristic (Current vs. Optical Power)
    ax2.plot(df["Diodenstrom I_D (mA)"], df["Optische Leistung P (nW)"], linestyle="-", label=label)

ax1.set_xlabel("Diodenspannung V_D (mV)")
ax1.set_ylabel("Diodenstrom I_D (mA)")
ax1.set_title("I-V Characteristic")
ax1.grid(True)
ax1.legend()

ax2.set_xlabel("Diodenstrom I_D (mA)")
ax2.set_ylabel("Optische Leistung P (nW)")
ax2.set_title("P-I Characteristic")
ax2.loglog()
ax2.set_xlim(10, 20)
ax2.grid(True)
ax2.legend()


# Adjust layout and render the figure
plt.tight_layout()
plt.savefig(fname=dir / "plots" / "temperature_dependence_2.pdf")
