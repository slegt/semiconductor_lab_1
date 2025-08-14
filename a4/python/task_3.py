import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pathlib
from scipy.optimize import curve_fit

from task_2 import calculate_donor_energy


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


# file location
file = pathlib.Path(__file__).parent.resolve()
latex_data = dict()

# Read the data from the csv file
data = pd.read_csv(filepath_or_buffer=file.parent / "data" / "E771_Imax.txt", sep="\t")
print(data.head())

T = data["T"].to_numpy()
n = data["n"].to_numpy()
mu = data["mu"].to_numpy()

n_2 = n[0]
mu_2 = mu[0]

T = T[1:]
n = n[1:]
mu = mu[1:]

n_1 = (mu * n - mu_2 * n_2) ** 2 / (mu**2 * n - mu_2**2 * n_2)
mu_1 = (mu**2 * n - mu_2**2 * n_2) / (mu * n - mu_2 * n_2)

reciprocal_T = 1 / T
n_over_t_uncorrected = np.log(n * T ** (-3 / 4))
n_over_t = np.log(n_1 * T ** (-3 / 4))

# Fit the data to a linear model
m, cov = curve_fit(linear, reciprocal_T[8:21], n_over_t[8:21])
latex_data["concentration"] = round(m[0], 2)
latex_data["donor_energy"] = round(calculate_donor_energy(m[0]), 2)

plt.scatter(reciprocal_T * 1000, n_over_t_uncorrected, label=" Uncorrected", s=8)
plt.scatter(reciprocal_T * 1000, n_over_t, label="Corrected", s=8)
plt.plot(
    reciprocal_T[6:31] * 1000,
    linear(reciprocal_T[6:31], *m),
    color="black",
    linestyle="--",
    label="Fit",
)
plt.text(
    0.15,
    0.03,
    f"$y = {m[0]:.2f}x + {m[1]:.2f}$",
    transform=plt.gca().transAxes,
    color="black",
)
plt.xlabel(r"$\num{1000} T^{-1} \quad [\qty{1000}{K^{-1}}]$")
plt.ylabel(r"$\ln(nT^{-3/4}) \quad [\ln(\unit{m^{-3} K^{-3 / 4}})]$")
plt.tight_layout()
plt.legend()
plt.savefig(file.parent / "plots" / "task_3_n.pdf")
plt.close()

mu_1 = (mu**2 * n - mu_2**2 * n_2) / (mu * n - mu_2 * n_2)
T_log = np.log(T)
mu_1_log = np.log(mu_1)
mu_log = np.log(mu)

m1, cov1 = curve_fit(linear, T_log[2:12], mu_1_log[2:12])
m3, cov3 = curve_fit(linear, T_log[25:], mu_1_log[25:])
latex_data["mobility_1"] = round(m1[0], 2)
latex_data["mobility_3"] = round(m3[0], 2)

plt.scatter(T_log, mu_log, label="Uncorrected", s=8)
plt.scatter(T_log, mu_1_log, label="Corrected", s=8)
plt.plot(
T_log[2:11], linear(T_log[2:11], *m1), color="black", linestyle="--", label="Fit")
plt.plot(T_log[18:], linear(T_log[18:], *m3), color="black", linestyle="--")
plt.text(
    0.325,
    0.04,
    r"$\text{slope:}$" + "\n" + f"{m1[0]:.2f}",
    transform=plt.gca().transAxes,
    ha="center",
)
plt.text(
    0.85,
    0.04,
    r"$\text{slope:}$" + "\n" + f"{m3[0]:.2f}",
    transform=plt.gca().transAxes,
    ha="center",
)
plt.axvspan(T_log[18], 6, color="black", alpha=0.1, lw=0)
plt.axvspan(T_log[2], T_log[11], color="black", alpha=0.1, lw=0)
plt.xlabel(r"$\ln(T) \quad [\ln(K)]$")
plt.ylabel(r"$\ln(\mu) \quad [\ln(\unit{cm^2/Vs})]$")
plt.tight_layout()
plt.xlim(3, 5.9)
plt.ylim(3.0, 6.2)
plt.legend(bbox_to_anchor=(0.4, 0.5), bbox_transform=plt.gca().transAxes)
plt.savefig(file.parent / "plots" / "task_3_mu.pdf")
plt.close()

with open(file.parent / "plots" / "task_3_data.json", "w") as f:
    json.dump(latex_data, f, indent=2)