import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.constants import k, e
from scipy.optimize import curve_fit
import json

latex_column_width = 221.48395  # pt
pt_to_inch = latex_column_width / 72  # 1 inch = 72 points
a = pt_to_inch * 0.98

mpl.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "text.latex.preamble": r"\usepackage{siunitx}",
        "font.serif": ["Computer Modern"],
        "font.size": 10,
        "figure.figsize": (a, a),
    }
)


def linear(x, a, b):
    return a * x + b

def calculate_donor_energy(m):
    return - 2 * k * m / e * 1000 # in meV


# file location
file = pathlib.Path(__file__).parent.resolve()
latex_data = dict()

# Read the data from the csv file
data = pd.read_csv(filepath_or_buffer=file.parent / "data" / "ZnO.txt", sep="\t")
print(data.head())

T_1 = data["T2"].to_numpy()[:-2]
n = data["n"].to_numpy()[:-2]


reciprocal_T = 1 / T_1
n_over_t = np.log(n * T_1 ** (-3 / 4))

# Fit the data to a linear model
m, cov = curve_fit(linear, reciprocal_T[8:], n_over_t[8:])
latex_data["slope"] = round(m[0], 2)
latex_data["donor_energy"] = round(calculate_donor_energy(m[0]), 2)
latex_data["n_d"] = round(max(n), 2)

plt.scatter(reciprocal_T * 1000, n_over_t, label="Data", s=8)
plt.plot(
    reciprocal_T * 1000,
    linear(reciprocal_T, *m),
    color="black",
    linestyle="--",
    label="Fit",
)
plt.text(
    0.18,
    0.1,
    f"$y = {m[0]:.2f}x + {m[1]:.2f}$",
    transform=plt.gca().transAxes,
    color="black",
)
plt.xlabel(r"$\num{1000} T^{-1} \quad [\qty{1000}{K^{-1}}]$")
plt.ylabel(r"$\ln(nT^{-3/4}) \quad [\ln(\unit{m^{-3} K^{-3 / 4}}]$")
plt.tight_layout()
plt.legend()
plt.savefig(file.parent / "plots" / "task_2_n.pdf")
plt.close()


T_2 = data["T"].to_numpy()
mu = data["mu"].to_numpy()
T_2_log = np.log(T_2)
mu_log = np.log(mu)

m1, cov1 = curve_fit(linear, T_2_log[:10], mu_log[:10])
m2, cov2 = curve_fit(linear, T_2_log[14:21], mu_log[14:21])
m3, cov3 = curve_fit(linear, T_2_log[23:-8], mu_log[23:-8])
latex_data["mobility_1"] = round(m1[0], 2)
latex_data["mobility_2"] = round(m2[0], 2)
latex_data["mobility_3"] = round(m3[0], 2)

plt.scatter(T_2_log, mu_log, label="Data", s=8)
plt.plot(T_2_log[:12], linear(T_2_log[:12], *m1), color="black", linestyle="--", label="Fit")
plt.plot(T_2_log[12:23], linear(T_2_log[12:23], *m2), color="black", linestyle="--")
plt.plot(T_2_log[23:], linear(T_2_log[23:], *m3), color="black", linestyle="--")
plt.text(0.2, 0.1, r"$\text{slope:}$" + "\n" + f"{m1[0]:.2f}", transform=plt.gca().transAxes, ha="center")
plt.text(0.51, 0.1, r"$\text{slope:}$" + "\n" + f"{m2[0]:.2f}", transform=plt.gca().transAxes, ha="center")
plt.text(0.78, 0.1, r"$\text{slope:}$" + "\n" + f"{m3[0]:.2f}", transform=plt.gca().transAxes, ha="center")
plt.axvspan(T_2_log[12], T_2_log[23], color="black", alpha=0.1, lw=0)
plt.xlabel(r"$\ln(T) \quad [\ln(K)]$")
plt.ylabel(r"$\ln(\mu) \quad [\ln(\unit{cm^2/Vs})]$")
plt.tight_layout()
plt.legend()
plt.savefig(file.parent / "plots" / "task_2_mu.pdf")
plt.close()

with open(file.parent / "plots" / "task_2_data.json", "w") as f:
    json.dump(latex_data, f, indent=2)