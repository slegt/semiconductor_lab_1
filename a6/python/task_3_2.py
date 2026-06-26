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
filepath = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/task3_036_2theta_omega.xrdml"
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


def model(x, background, a, c, w, e):
    """The model we fit: a flat background plus single pseudo-Voigt peaks
    (substrate, film, and a third tilted domain / fringe)."""
    return (
        background +  pseudo_voigt(x, a, c, w, e)
    )


# initial guess and limits
p0 = [1] + [3.2e4, 83.21, 0.03, 0.007]

lower = [1.0] +  [0.0, 80.0, 1e-4, 0.0]
upper = [10.0]  + [1e5, 84.0, 1, 1.0]

# fit routine and parameter readout
window = (two_theta > 83.1) & (two_theta < 83.3)
two_theta_fit = two_theta[window]
intensity_fit = intensity[window]

popt, pcov = curve_fit(
    model, two_theta_fit, intensity_fit, p0=p0, bounds=(lower, upper),
)
perr = np.sqrt(np.diag(pcov))

params = {}
background = popt[0]

amplitude, center, fwhm, eta = popt[1:5]
center_err = perr[2]
fwhm_err = perr[3]

# caclulating quantities
k = 3
l = 6
center_err = max(perr[2], spacing / 2)
theta = np.deg2rad(center) / 2
theta_err = np.deg2rad(center_err) / 2
c = 1.29930e-09
denom = 4 * np.sin(theta)**2 / wavelength**2 - l**2 / c**2
a = np.sqrt(4 / 3 * k**2 / denom)
a_err = a / (2 * denom) * 4 * np.sin(2 * theta) / wavelength**2 * theta_err

# export quantities
exportable_data = {
    "peak_2theta": f"{center}",
    "a": f"{a}",
    "a_err": f"{a_err}"
}

update_json_file(data_dict=exportable_data, key="task_3_036")

# plot
fig, ax = plt.subplots(figsize=SINGLE_COLUMN["figure.figsize"])
fig.subplots_adjust(left=0.17, right=0.93, top=0.98, bottom=0.15)

two_theta_smooth = np.linspace(two_theta_fit.min(), two_theta_fit.max(), 2000)

ax.plot(two_theta, intensity, ".", ms=1, color="0.6", label="data", zorder=10, alpha=0.9)
ax.plot(two_theta_smooth, model(two_theta_smooth, *popt), color="k", lw=1.2, label="fit")

ax.set_yscale("log")
ax.set_xlim(83.0, 83.4)
ax.set_xlabel(r"$2\theta$ [deg]")
ax.set_ylabel(r"$I$ [arb. unit]")
ax.legend(loc="upper left", fontsize=7)
fig.savefig(destination / "task_3_036_2to.pdf")
plt.close(fig)
