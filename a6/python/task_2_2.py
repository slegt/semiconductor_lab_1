from pathlib import Path

import numpy as np
from config import SINGLE_COLUMN
from exporter import update_json_file
from matplotlib import pyplot as plt
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
    return background + pseudo_voigt(x, a, c, w, e)


a = 4.7577e-10
c = 12.9907e-10


def get_lattice_vector(u, v, w):
    a1 = a / 2 * np.array([np.sqrt(3), 1, 0])
    a2 = a / 2 * np.array([np.sqrt(3), -1, 0])
    a3 = c * np.array([0, 0, 1])
    return u * a1 + v * a2 + w * a3


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
    model,
    omega_fit,
    intensity_fit,
    p0=p0,
    bounds=(lower, upper),
)
perr = np.sqrt(np.diag(pcov))

background = popt[0]
amplitude, center, fwhm, eta = popt[1:5]
center_err = perr[2]
fwhm_err = perr[3]

# calculate edge type dislocations

fwhm_rad = np.deg2rad(fwhm)
b_para = np.linalg.norm(get_lattice_vector(2, 4, 1))

rho_screw = (fwhm_rad) ** 2 / (4.35 * b_para**2)

# calculate lateral coherence length from the symmetric (024) rocking curve.
# On r-sapphire the (024) is the surface-parallel reflection, so its rocking
# width maps cleanly to the in-plane coherence length (unlike the inclined 006).
L = 0.9 * wavelength / (2 * fwhm_rad * np.sin(np.deg2rad(theta_B)))
delta_L = L * (fwhm_err / fwhm)

# export quantities
exportable_data = {}
exportable_data["peak_omega"] = center
exportable_data["peak_fwhm"] = fwhm
exportable_data["eta"] = eta
exportable_data["b_para"] = b_para
exportable_data["screw_dislocation_density"] = rho_screw
exportable_data["coherence_length"] = L
exportable_data["coherence_length_delta"] = delta_L
exportable_data["theta"] = theta_B
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
