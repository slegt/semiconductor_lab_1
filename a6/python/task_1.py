import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from config import SINGLE_COLUMN
from exporter import update_json_file
from parser import XRDMLParser
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from pathlib import Path

file_path = Path(__file__).resolve()
destination = file_path.parent.parent / "plots"

plt.rcParams.update(SINGLE_COLUMN)



def fit_func(phi, gamma, psi0):
    return theta + np.rad2deg(np.arctan(np.tan(np.deg2rad(gamma)) * np.cos(np.deg2rad(psi0 + phi))))

# import files
filepath0 = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task1_omega_scan_024_al2o3peak_1deg_.005ss_phi=0.xrdml"
filepath90 = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task1_omega_scan_024_al2o3peak_1deg_.005ss_phi=90.xrdml"
filepath180 = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task1_omega_scan_024_al2o3peak_1deg_.005ss_phi=180.xrdml"
filepath270 = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task1_omega_scan_024_al2o3peak_1deg_.005ss_phi=270.xrdml"
files = [filepath0, filepath90, filepath180, filepath270]


sessions = [XRDMLParser.parse_file(file) for file in files]
offset_omega = -0.2292
offset_2theta = 0.0487
angles = [0, 90, 180, 270]

# parse different scans
scans = [session.measurement.scan.get_plot_data() for session in sessions]
theta = (sessions[0].measurement.scan.positions[0].common_position - offset_2theta) / 2


# calculate quantities
omega_peaks = []
intensity_peaks = []

for index, scan in enumerate(scans):
    x_data = scan["omega"] - offset_omega
    y_data = scan["intensity"]

    max_index = find_peaks(y_data, height=1e6)[0][0]
    max_x = x_data[max_index]
    max_y = y_data[max_index]

    omega_peaks.append(max_x)
    intensity_peaks.append(max_y)
    scans[index]["omega"] = x_data

m, cov = curve_fit(f=fit_func, xdata=angles, ydata=omega_peaks, p0=[1, 1])
gamma = m[0]
delta_gamma = np.sqrt(cov[0][0])

# export quantities
exportable_data = {
    "theta": f"{theta:.2f}",
    "gamma": f"{gamma:.2f}",
    "delta_gamma": f"{delta_gamma:.2f}"
}
update_json_file(data_dict=exportable_data, key="task_1")

# plot
fig, ax = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
fig.subplots_adjust(left=0.18, right=0.95, top=0.99, bottom=0.15)

for scan, angle in zip(scans, angles):
    ax.plot(scan["omega"], scan["intensity"], label=str(angle) + "°")

for angle, intensity in zip(omega_peaks, intensity_peaks):
    ax.scatter(angle, intensity)
    ax.text(x=angle, y=intensity + 1e6, s=f"{angle:.2f} °", ha="center", va="bottom")

ax.set_yscale("log")
ax.set_xlim(26.05, 26.5)
ax.set_ylim(top=3e7)
ax.legend(loc="lower right")
ax.set_xlabel(r"$\Omega$ [deg]")
ax.set_ylabel(r"$I$ [arb. unit]")
fig.savefig(destination / "task1_1.pdf")
plt.close(fig)

fig, ax = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
# edge positions in figure-relative coords (0=left/bottom, 1=right/top)
fig.subplots_adjust(left=0.2, right=0.95, top=0.99, bottom=0.15)

ax.scatter(angles, omega_peaks, color="orange", zorder=10, label="measurement")
ax.plot(np.linspace(0, 360, 100), fit_func(np.linspace(0, 360, 100), *m), zorder=1, label="fit")
ax.text(
    x=0.5,
    y=0.5,
    s=rf"$\gamma={round(m[0], 2)}$",
    transform=ax.transAxes,
    horizontalalignment="center",
    verticalalignment="center",
)
ax.legend(loc="upper right")
ax.set_xlabel(r"$\varphi$ [deg]")
ax.set_ylabel(r"$\Omega$ [deg]")
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_minor_locator(MultipleLocator(0.05))
ax.xaxis.set_major_locator(MultipleLocator(100))
ax.xaxis.set_minor_locator(MultipleLocator(50))
fig.savefig(destination / "task1_2.pdf")
plt.close(fig)
