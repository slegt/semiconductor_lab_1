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
filepath = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task2_006_rockingcurve2.xrdml"
session = XRDMLParser.parse_file(filepath)

data = session.measurement.scan.get_plot_data()
two_theta = session.measurement.scan.get_position("2Theta")
theta_B = two_theta / 2.0
wavelength = session.measurement.used_wavelength.k_alpha_1.value * 1e-10

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


def three_peaks(x, background, a1, c1, w1, e1, a2, c2, w2, e2, a3, c3, w3, e3):
    """The model we fit: a flat background plus three pseudo-Voigt peaks
    (substrate, film, and a third tilted domain / fringe)."""
    return (
        background + pseudo_voigt(x, a1, c1, w1, e1) + pseudo_voigt(x, a2, c2, w2, e2) + pseudo_voigt(x, a3, c3, w3, e3)
    )


# initial guess and limits
background_guess = np.median(intensity[omega > 20.95])
guesses = [
    # amplitude, center,  fwhm,  eta
    (38000.0, 20.873, 0.010, 0.3),
    (43000.0, 20.887, 0.012, 0.3),
    (35000.0, 20.899, 0.010, 0.3),
]

p0 = [background_guess]
for amplitude, center, fwhm, eta in guesses:
    p0 += [amplitude, center, fwhm, eta]

lower = [0.0] + [0.0, 20.80, 1e-4, 0.0] * 3
upper = [2000.0] + [1e6, 20.95, 0.05, 1.0] * 3

# fit routine and parameter readout
window = (omega > 20.80) & (omega < 20.95)
omega_fit = omega[window]
intensity_fit = intensity[window]


popt, pcov = curve_fit(three_peaks, omega_fit, intensity_fit, p0=p0, bounds=(lower, upper))
perr = np.sqrt(np.diag(pcov))

background = popt[0]
labels = ["peak_1", "peak_2", "peak_3"]
peaks = []
for i, label in enumerate(labels):
    amplitude, center, fwhm, eta = popt[1 + 4 * i : 5 + 4 * i]
    center_err = perr[2 + 4 * i]
    fwhm_err = perr[3 + 4 * i]
    peaks.append((label, center, center_err, fwhm, fwhm_err))

for label, center, center_err, fwhm, fwhm_err in peaks:
    print(f"{label}: omega = {center:.4f} +/- {center_err:.4f} deg   FWHM = {fwhm:.4f} +/- {fwhm_err:.4f} deg")

# calculate coherence length and screw type dislocation density
substrate_fwhm = peaks[1][3]
substrate_fwhm_err = peaks[1][4]
fwhm_rad = np.deg2rad(substrate_fwhm)
L = 0.9 * wavelength / (fwhm_rad * np.sin(np.deg2rad(theta_B)))
delta_L = L * (substrate_fwhm_err / substrate_fwhm)

c = 12.9907e-10
rho_screw = fwhm_rad**2 / (4.35 * c**2)


# export quantities
exportable_data = {}
for label, center, center_err, fwhm, fwhm_err in peaks:
    exportable_data[f"{label}_omega"] = f"{center:.4f}"
    exportable_data[f"{label}_fwhm"] = f"{fwhm:.4f}"
exportable_data["coherence_length"] = f"{L:.2e}"
exportable_data["coherence_length_delta"] = f"{delta_L:.2e}"
exportable_data["screw_dislocation_density"] = f"{rho_screw:.2e}"
update_json_file(data_dict=exportable_data, key="task_2_006")

# plot
fig, ax = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
fig.subplots_adjust(left=0.17, right=0.98, top=0.98, bottom=0.15)

omega_smooth = np.linspace(omega_fit.min(), omega_fit.max(), 2000)

ax.plot(omega, intensity, ".", ms=1, color="0.6", label="data", zorder=10, alpha=0.8)
ax.plot(omega_smooth, three_peaks(omega_smooth, *popt), color="k", lw=1.2, label="fit")

# draw each fitted peak on its own
for i, (label, _, _, _, _) in enumerate(peaks):
    amplitude, center, fwhm, eta = popt[1 + 4 * i : 5 + 4 * i]
    component = background + pseudo_voigt(omega_smooth, amplitude, center, fwhm, eta)
    ax.plot(omega_smooth, component, "--", lw=0.8, label=f"peak {i + 1}")

ax.set_yscale("log")
ax.set_xlim(20.80, 20.95)
ax.set_ylim(bottom=2e2)
ax.set_xlabel(r"$\Omega$ [deg]")
ax.set_ylabel(r"$I$ [arb. unit]")
ax.legend(loc="upper left", fontsize=7)
fig.savefig(destination / "task_2_1.pdf")
plt.close(fig)
