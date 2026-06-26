from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from config import SINGLE_COLUMN
from exporter import update_json_file
from parser import XRDMLParser
from scipy.optimize import curve_fit

plt.rcParams.update(SINGLE_COLUMN)

file_path = Path(__file__).resolve()
destination = file_path.parent.parent / "plots"

# import files
filepath = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/task3_2theta_om_006.xrdml"
session = XRDMLParser.parse_file(filepath)

data = session.measurement.scan.get_plot_data()
two_theta = data["2theta"] - 0.0088
omega = data["omega"] - session.measurement.sample_offset[1].value
intensity = data["intensity"]

wavelength = session.measurement.used_wavelength.k_alpha_1.value * 1e-10  # [m]
spacing = two_theta[1] - two_theta[0]

# define peak functions
def pseudo_voigt(x, amplitude, center, fwhm, eta):
    """A single peak: a mix of a Gaussian and a Lorentzian that share the same
    width. ``eta`` (0..1) sets how Lorentzian the peak is (0 = pure Gaussian,
    1 = pure Lorentzian). This is the standard line shape for XRD peaks."""
    z = (x - center) / fwhm
    gaussian = np.exp(-4.0 * np.log(2.0) * z**2)
    lorentzian = 1.0 / (1.0 + 4.0 * z**2)
    return amplitude * (eta * lorentzian + (1.0 - eta) * gaussian)


def model(x, background, a1, c1, w1, e1, a2, c2, w2, e2):
    """The model we fit: a flat background plus single pseudo-Voigt peaks
    (substrate, film, and a third tilted domain / fringe)."""
    return (
        background + pseudo_voigt(x, a1, c1, w1, e1) + pseudo_voigt(x, a2, c2, w2, e2)
    )


# initial guess and limits
p0 = [2] + [19, 41.51, 0.01, 0.6] + [19500, 41.68, 0.01, 0.01]

lower = [1.0] +  [0.0, 41.4, 1e-4, 0.0] * 2
upper = [10.0]  + [1e5, 41.8, 0.5, 1.0] * 2

# fit routine and parameter readout
window = (two_theta > 41.4) & (two_theta < 41.8)
two_theta_fit = two_theta[window]
intensity_fit = intensity[window]

popt, pcov = curve_fit(
    model, two_theta_fit, intensity_fit, p0=p0, bounds=(lower, upper),
)
perr = np.sqrt(np.diag(pcov))

params = {}
background = popt[0]

for i in range(2):
    amplitude, center, fwhm, eta = popt[1 + 4* i:5 + 4 * i]
    center_err = perr[2 + 4 * i]
    fwhm_err = perr[3 + 4 * i]
    params[i] = {
        "amplitude": amplitude,
        "center": center,
        "center_err": center_err,
        "fwhm": fwhm,
        "eta": eta
    }

for i in range(2):
    n = 6
    theta = np.deg2rad(params[i]["center"]) / 2
    center_err = max(params[i]["center_err"], spacing / 2)
    theta_err = np.deg2rad(center_err) / 2
    c = n / 2 * wavelength / np.sin(theta)
    c_err = c / np.tan(theta) * theta_err
    params[i]["c"] = c
    params[i]["c_err"] = c_err



# export quantities
exportable_data = {}
for i in range(2):
    exportable_data[f"peak_{i}_2theta"] = f"{params[i]["center"]:.4f}"
    exportable_data[f"peak_{i}_fwhm"] = f"{params[i]["fwhm"]:.4f}"
    exportable_data[f"peak_{i}_c"] = f"{params[i]["c"]:.5e}"
    exportable_data[f"peak_{i}_c_err"] = f"{params[i]["c_err"]:.0e}"
# exportable_data["edge_dislocation_density"] = f"{rho_edge:.2e}"

update_json_file(data_dict=exportable_data, key="task_3_006")
# plot
fig, ax = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
fig.subplots_adjust(left=0.17, right=0.93, top=0.98, bottom=0.15)

two_theta_smooth = np.linspace(two_theta_fit.min(), two_theta_fit.max(), 2000)

ax.plot(two_theta, intensity, ".", ms=1, color="0.6", label="data", zorder=10, alpha=0.9)
ax.plot(two_theta_smooth, model(two_theta_smooth, *popt), color="k", lw=1.2, label="fit")

ax.set_yscale("log")
ax.set_xlim(41.4, 42)
ax.set_xlabel(r"$2\theta$ [deg]")
ax.set_ylabel(r"$I$ [arb. unit]")
ax.legend(loc="upper left", fontsize=7)
fig.savefig(destination / "task_3_006_2to.pdf")
plt.close(fig)
