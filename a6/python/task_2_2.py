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
filepath = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task2_rockingcurve_024_al2o3_phi270.xrdml"
session = XRDMLParser.parse_file(filepath)

data = session.measurement.scan.get_plot_data()
two_theta = session.measurement.scan.get_position("2Theta")
theta_B = two_theta / 2.0
wavelength = session.measurement.used_wavelength.k_alpha_1.value * 1e-10  # [m]

omega = data["omega"]
intensity = data["intensity"].astype(float)

# define peak functions
def pseudo_voigt(x, amplitude, center, fwhm, eta):
    """A single peak: a mix of a Gaussian and a Lorentzian that share the same
    width. ``eta`` (0..1) sets how Lorentzian the peak is (0 = pure Gaussian,
    1 = pure Lorentzian). This is the standard line shape for XRD peaks."""
    z = (x - center) / fwhm
    gaussian = np.exp(-4.0 * np.log(2.0) * z**2)
    lorentzian = 1.0 / (1.0 + 4.0 * z**2)
    return amplitude * (eta * lorentzian + (1.0 - eta) * gaussian)


def model(x, background, a, c, w, e):
    """The model we fit: a flat background plus single pseudo-Voigt peaks
    (substrate, film, and a third tilted domain / fringe)."""
    return (
        background + pseudo_voigt(x, a, c, w, e)
    )


# initial guess and limits
background_guess = np.median(intensity[omega > 26.5])  # flat tail
p0 = [background_guess, 6e6, 26.3, 0.01, 0.4]

lower = [0.0, 0.0, 20.80, 1e-4, 0.0]
upper = [1e4, 1e8, 28.95, 0.05, 1.0]

# fit routine and parameter readout
window = (omega > 26.2) & (omega < 26.40)
omega_fit = omega[window]
intensity_fit = intensity[window]

popt, pcov = curve_fit(
    model, omega_fit, intensity_fit, p0=p0, bounds=(lower, upper),
)
perr = np.sqrt(np.diag(pcov))

background = popt[0]
amplitude, center, fwhm, eta = popt[1:5]
center_err = perr[2]
fwhm_err = perr[3]

# calculate edge type dislocations
a = 4.7577e-10
fwhm_rad = np.deg2rad(fwhm)

rho_edge = (fwhm_rad * 4 / 3) **2 / (4.35 * a**2)

# export quantities
exportable_data = {}
exportable_data["peak_omega"] = f"{center:.4f}"
exportable_data["peak_fwhm"] = f"{fwhm:.4f}"
exportable_data["eta"] = f"{eta:.4f}"
exportable_data["edge_dislocation_density"] = f"{rho_edge:.2e}"
update_json_file(data_dict=exportable_data, key="task_2_024")

# plot
fig, ax = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
fig.subplots_adjust(left=0.17, right=0.93, top=0.98, bottom=0.15)

omega_smooth = np.linspace(omega_fit.min(), omega_fit.max(), 2000)

ax.plot(omega, intensity, ".", ms=1, color="0.6", label="data", zorder=10, alpha=0.8)
ax.plot(omega_smooth, model(omega_smooth, *popt), color="k", lw=1.2, label="fit")

ax.set_yscale("log")
ax.set_ylim(bottom=2e2)
ax.set_xlim(25.5, 26.5)
ax.set_xlabel(r"$\Omega$ [deg]")
ax.set_ylabel(r"$I$ [arb. unit]")
ax.legend(loc="upper left", fontsize=7)
fig.savefig(destination / "task_2_024_omega.pdf")
plt.close(fig)
