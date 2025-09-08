import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import patches, rc
import pathlib
from scipy.optimize import curve_fit

# Setup Fit
def func(x, a, vth):
    return np.where(x < vth, 0, a * (x - vth) ** 2)

# Configure matplotlib
rc("text", usetex=True)
rc("text.latex", preamble=r"\usepackage{siunitx}")
rc("font", size=10, family="serif")

width, height = 300, 120
file_path = pathlib.Path(__file__).parent.resolve()

fig, axs = plt.subplots(1, 2, figsize=(width / 72, height / 72))

# Plot V_G vs I_D
df_vg = pd.read_csv(file_path / "../data/I_D-V_G.csv", sep=";")
df_vg.columns = ["V_G", "I_D", "none"]
df_vg = df_vg.drop(columns=["none"])

v_g = df_vg["V_G"].to_numpy()
i_d = df_vg["I_D"].to_numpy() / 1000

# Fit data
popt, pcov = curve_fit(func, v_g, i_d, p0=(1, 2))

special_vg = [2, 4, 6, 8, 10]
special_id = [i_d[np.where(v_g == vg)[0][0]] for vg in special_vg]

axs[0].plot(v_g, i_d, lw=0.9)
axs[0].set_xlabel(r"$v_\mathrm{gate}$ in $\unit{V}$")
axs[0].set_ylabel(r"$i_\mathrm{drain}$ in $\unit{mA}$")

# Plot V_D vs I_D
df_vd = pd.read_csv(file_path / "../data/I_D-V_DS.csv", sep=";")
df_vd.columns = ["V_D", "I_D", "none"]
df_vd = df_vd.drop(columns=["none"])

v_ds = df_vd["V_D"].to_numpy()
i_ds = df_vd["I_D"].to_numpy() / 1000

id_segments, vd_segments = {}, {}
last_index, count = 0, 1

for index, entry in enumerate(v_ds):
    if entry == 10.0:
        id_segments[2 * count] = i_ds[last_index:index]
        vd_segments[2 * count] = v_ds[last_index:index]
        last_index = index + 1
        count += 1

colors = [f"#{hex(0x00FF00 - i * 0x003000)[2:].zfill(6)}" for i in range(5)]
for (i, v), color in zip(zip(id_segments.values(), vd_segments.values()), colors):
    axs[1].plot(v, i, color=color, lw=0.9)

axs[1].plot(
    vd_segments[2][:700],
    popt[0] * vd_segments[2][:700] ** 2,
    "--",
    color="red",
    label="Fit Extrapolation",
    lw=0.8,
    alpha=0.7,
)

axs[1].set_yticks([])
axs[1].set_xlabel(r"$v_\mathrm{drain}$ in $\unit{V}$")

# Adjust layout and remove unnecessary spines
plt.subplots_adjust(right=0.98, left=0.15, top=0.98, bottom=0.25)
for ax in axs:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Add connection patches
for vg, id in zip(special_vg, special_id):
    con = patches.ConnectionPatch(
        xyA=(vg, id),
        xyB=((id / popt[0]) ** (1 / 2), id),
        coordsA="data",
        coordsB="data",
        axesA=axs[0],
        axesB=axs[1],
        color="grey",
        lw=0.7,
        alpha=0.7,
        linestyle="--",
    )
    fig.add_artist(con)

plt.savefig(file_path / "../plots/cv_characteristics.pdf")
