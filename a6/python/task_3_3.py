from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from config import SINGLE_COLUMN
from parser import XRDMLParser

plt.rcParams.update(SINGLE_COLUMN)

file_path = Path(__file__).resolve()
destination = file_path.parent.parent / "plots"

# import files
filepaths = {
    "(006)": "/home/simon/ProjectsTex/semiconductor_lab/a6/data/task3_omega_006.xrdml",
    "(036)": "/home/simon/ProjectsTex/semiconductor_lab/a6/data/task3_036_omega.xrdml",
}

scans = {}
for label, filepath in filepaths.items():
    session = XRDMLParser.parse_file(filepath)
    data = session.measurement.scan.get_plot_data()
    omega = data["omega"] - session.measurement.sample_offset[1].value
    intensity = data["intensity"]
    scans[label] = (omega, intensity)

# The two rocking curves are centred at very different omega (~21 deg for the
# (006) reflection vs ~41.6 deg for the (036) reflection), so they cannot share
# a single x-axis. Plot both on one axes but give each its own omega scale:
# (006) on the bottom axis, (036) on a twinned top axis.
fig, ax_006 = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
fig.subplots_adjust(left=0.17, right=0.93, top=0.86, bottom=0.15)
ax_036 = ax_006.twiny()

color_006 = "C0"
color_036 = "C3"

omega_006, intensity_006 = scans["(006)"]
omega_036, intensity_036 = scans["(036)"]

(line_006,) = ax_006.plot(
    omega_006, intensity_006, "-", lw=1.0, color=color_006, label=r"(006)"
)
(line_036,) = ax_036.plot(
    omega_036, intensity_036, "-", lw=1.0, color=color_036, label=r"(036)"
)

ax_006.set_yscale("log")

# single shared x-axis label in black; colour only the ticks to match curves
ax_006.set_xlabel(r"$\omega$ [deg]")
ax_006.tick_params(axis="x", colors=color_006)
ax_036.tick_params(axis="x", colors=color_036)

ax_006.set_ylabel(r"$I$ [arb. unit]")

ax_006.legend(handles=[line_006, line_036], loc="upper left", fontsize=7)

fig.savefig(destination / "task_3_3.pdf")
plt.close(fig)
