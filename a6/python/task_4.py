from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle
from config import DOUBLE_COLUMN
from parser import XRDMLParser

plt.rcParams.update(DOUBLE_COLUMN)

file_path = Path(__file__).resolve()
destination = file_path.parent.parent / "plots"

# import file (frame-based reciprocal space map: many 2theta scans, each at a
# fixed omega, so session.measurement.scan is a list of Scan objects)
filepath = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/task4_RSM_frame_based_6deg_100sec_11.5min_1.xrdml"
session = XRDMLParser.parse_file(filepath)
scans = session.measurement.scan

wavelength = session.measurement.used_wavelength.k_alpha_1.value  # [Angstrom]
offset_2theta = session.measurement.sample_offset[0].value
offset_omega = session.measurement.sample_offset[1].value

# assemble the frames into curvilinear (n_frames, n_points) grids
two_theta = np.array([scan.get_plot_data()["2theta"] for scan in scans]) - offset_2theta
omega = np.array([scan.get_position("Omega") for scan in scans]) - offset_omega
omega = np.repeat(omega[:, None], two_theta.shape[1], axis=1)
intensity = np.array([scan.get_plot_data()["intensity"] for scan in scans])

# convert (omega, 2theta) to reciprocal space coordinates [1/Angstrom].
# Qx is in-plane, Qz out-of-plane; q = k_out - k_in with k = 2 pi / lambda,
# so |q| = 4 pi sin(theta) / lambda.
k = 2 * np.pi / wavelength
om = np.deg2rad(omega)
tt = np.deg2rad(two_theta)
q_x = k * (np.cos(tt - om) - np.cos(om))
q_z = k * (np.sin(tt - om) + np.sin(om))

# location of the intensity maximum (the reflection) in reciprocal space
max_idx = np.unravel_index(np.argmax(intensity), intensity.shape)
q_x_max = q_x[max_idx]
q_z_max = q_z[max_idx]
q_radius = np.hypot(q_x_max, q_z_max)

# plot
# zoom region (interesting reflection)
zoom_xlim = (-0.01, 0.03)
zoom_ylim = (3.5, 3.65)

fig, (ax_full, ax_zoom) = plt.subplots(
    1, 2, figsize=DOUBLE_COLUMN["figure.figsize"], constrained_layout=True
)

norm = LogNorm(vmin=1, vmax=intensity.max())
clipped = np.clip(intensity, 1, None)

for ax in (ax_full, ax_zoom):
    mesh = ax.pcolormesh(
        q_x, q_z, clipped, norm=norm, cmap="inferno",
        shading="gouraud", rasterized=True,
    )
    ax.set_xlabel(r"$q_\parallel$ [\AA$^{-1}$]")

ax_full.set_ylabel(r"$q_\perp$ [\AA$^{-1}$]")
ax_full.set_title("full map", fontsize=8)
ax_zoom.set_title("zoom", fontsize=8)

# zoom into the interesting region and mark it on the full map
ax_zoom.set_xlim(*zoom_xlim)
ax_zoom.set_ylim(*zoom_ylim)

# paths through the intensity maximum
ax_zoom.axhline(q_z_max, color="cyan", lw=0.8, label="horizontal")
ax_zoom.axvline(q_x_max, color="lime", lw=0.8, label="vertical")
# arc segment at constant |q| through the maximum: the mosaicity direction
ax_full.add_patch(
    Rectangle(
        (zoom_xlim[0], min(zoom_ylim)),
        zoom_xlim[1] - zoom_xlim[0],
        abs(zoom_ylim[1] - zoom_ylim[0]),
        fill=False, edgecolor="white", lw=0.8,
    )
)

cbar = fig.colorbar(mesh, ax=(ax_full, ax_zoom), pad=0.02)
cbar.set_label(r"$I$ [arb. unit]")

fig.savefig(destination / "task_4_rsm.pdf")
plt.close(fig)
