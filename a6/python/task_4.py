import json
from pathlib import Path

import numpy as np
from config import DOUBLE_COLUMN
from exporter import update_json_file
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle
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
k_0 = 2 * np.pi / wavelength
om = np.deg2rad(omega)
tt = np.deg2rad(two_theta)
q_x = k_0 * (np.cos(tt - om) - np.cos(om))
q_z = k_0 * (np.sin(tt - om) + np.sin(om))

# locate the two prominent reflections in reciprocal space. Both sit at
# essentially the same in-plane q_parallel; they differ in q_perp: the
# stronger substrate peak near q_perp = 3.61 and the weaker thin-film peak
# near q_perp = 3.55. Search for the intensity maximum inside a q_perp band
# around each, restricted to the in-plane window of the zoom region.
zoom_xlim = (-0.01, 0.03)
zoom_ylim = (3.5, 3.65)

x_window = (q_x > zoom_xlim[0]) & (q_x < zoom_xlim[1])


def find_peak(q_perp_lo, q_perp_hi):
    """Return (q_x, q_z, intensity) of the maximum within a q_perp band."""
    band = x_window & (q_z > q_perp_lo) & (q_z < q_perp_hi)
    idx = np.unravel_index(np.argmax(np.where(band, intensity, -np.inf)), intensity.shape)
    return q_x[idx], q_z[idx], intensity[idx]


substrate = find_peak(3.58, 3.64)
film = find_peak(3.51, 3.58)

for name, (px, pz, pi) in [("substrate", substrate), ("film", film)]:
    print(f"{name:9s}: q_parallel = {px:.4f}  q_perp = {pz:.4f}  I = {pi:.0f}")


export_path = file_path.parent.parent / "plots" / "export.json"
with open(export_path, "r", encoding="utf-8") as f:
    export_data = json.load(f)

q_film = np.sqrt(film[0] ** 2 + film[1] ** 2)  * 1e10
c_film = float(export_data["task_3_006"]["peak_film_c"])
l = 4
k = 2

# literature lattice constants of the corundum-phase end members [m]
a_al2o3, c_al2o3 = 4.75925e-10, 12.9929e-10
a_ga2o3, c_ga2o3 = 4.98e-10, 13.43e-10


def lattice_a(q, c):
    """In-plane lattice parameter ``a`` from |G|^2 = k^2 b2^2 + l^2 b3^2 with
    b2 = 4 pi / (sqrt(3) a) and b3 = 2 pi / c."""
    b3 = 2 * np.pi / c
    b2 = np.sqrt((q**2 - l**2 * b3**2) / k**2)
    return 4 * np.pi / (np.sqrt(3) * b2)


def vegard(measured, pure_al2o3, pure_ga2o3):
    """Ga content x of an (Al_{1-x}Ga_x)_2O_3 alloy, from a linear interpolation
    of the given lattice constant between the two end members."""
    return (measured - pure_al2o3) / (pure_ga2o3 - pure_al2o3)


a_film = lattice_a(q_film, c_film)
x_ga_from_a = vegard(a_film, a_al2o3, a_ga2o3)
x_ga_from_c = vegard(c_film, c_al2o3, c_ga2o3)

print(f"a_film = {a_film * 1e10:.4f} Angstrom -> x_Ga = {x_ga_from_a:.3f}")
print(f"c_film = {c_film * 1e10:.4f} Angstrom -> x_Ga = {x_ga_from_c:.3f}")

# export peak positions
exportable_data = {
    "substrate_q_parallel": float(substrate[0]),
    "substrate_q_perp": float(substrate[1]),
    "film_q_parallel": float(film[0]),
    "film_q_perp": float(film[1]),
    "film_a": float(a_film),
    "film_x_ga_from_a": float(x_ga_from_a),
    "film_x_ga_from_c": float(x_ga_from_c),
}
update_json_file(data_dict=exportable_data, key="task_4")

fig, (ax_full, ax_zoom) = plt.subplots(1, 2, figsize=DOUBLE_COLUMN["figure.figsize"], constrained_layout=True)

norm = LogNorm(vmin=1, vmax=intensity.max())
clipped = np.clip(intensity, 1, None)

for ax in (ax_full, ax_zoom):
    mesh = ax.pcolormesh(
        q_x,
        q_z,
        clipped,
        norm=norm,
        cmap="inferno",
        shading="gouraud",
        rasterized=True,
    )
    ax.set_xlabel(r"$q_\parallel$ [\AA$^{-1}$]")

ax_full.set_ylabel(r"$q_\perp$ [\AA$^{-1}$]")
ax_full.set_title("full map", fontsize=8)
ax_zoom.set_title("zoom", fontsize=8)

# zoom into the interesting region and mark it on the full map
ax_zoom.set_xlim(*zoom_xlim)
ax_zoom.set_ylim(*zoom_ylim)

# mark the two prominent reflections in the zoom
for (px, pz, _), label, color in [
    (substrate, "substrate (024)", "cyan"),
    (film, "film (024)", "lime"),
]:
    ax_zoom.scatter(px, pz, s=30, facecolors="none", edgecolors=color, lw=1.0)
    ax_zoom.annotate(
        f"{label}\n$q_\\perp={pz:.3f}$",
        xy=(px, pz),
        xytext=(6, 0),
        textcoords="offset points",
        color=color,
        fontsize=6,
        va="center",
        ha="left",
    )
# mark the zoom region on the full map
ax_full.add_patch(
    Rectangle(
        (zoom_xlim[0], min(zoom_ylim)),
        zoom_xlim[1] - zoom_xlim[0],
        abs(zoom_ylim[1] - zoom_ylim[0]),
        fill=False,
        edgecolor="white",
        lw=0.8,
    )
)

cbar = fig.colorbar(mesh, ax=(ax_full, ax_zoom), pad=0.02)
cbar.set_label(r"$I$ [arb. unit]")

fig.savefig(destination / "task_4_rsm.pdf")
plt.close(fig)
