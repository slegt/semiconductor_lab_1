import numpy as np
from numpy import cosh, exp, log
from scipy.constants import pi
from scipy.optimize import fsolve
from scipy.constants import e
import pandas as pd
import pathlib

file_directory = pathlib.Path(__file__).parent.resolve()

P_SI = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([0.01, 0.01, 0.01, 0.01]),
    "U1": np.array([-5.69, -5.63, 5.86, 5.87]) * 10**-4,
    "U2": np.array([-3.92, -3.92, 3.99, 4.02]) * 10**-4,
    "U3": np.array([1.84, -1.77, -1.72, 1.87]) * 10**-4,
    "U4": np.array([1.90, -1.72, -1.78, 1.81]) * 10**-4,
    "d": 500e-6,
}

CuI = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([0.03, 0.03, 0.03, 0.03]),
    "U1": np.array([-1.7, -1.68, 1.75, 1.75]) * 10e-3,
    "U2": np.array([-1.19, -1.19, 1.17, 1.18]) * 10e-3,
    "U3": np.array([5.27, -5.52, -5.18, 5.45]) * 10e-4,
    "U4": np.array([5.45, -5.34, -5.36, 5.28]) * 10e-4,
    "d": 330e-9,
}

ZTO = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([8.5, 8.5, 8.5, 8.5]) * 10e-3,
    "U1": np.array([-2.75, -2.75, 2.75, 2.74]) * 10e-1,
    "U2": np.array([-2.87, -2.87, 2.87, 2.87]) * 10e-1,
    "U3": np.array([-1.26, 1.25, 1.23, -1.29]) * 10e-2,
    "U4": np.array([-1.33, 1.18, 1.3, -1.23]) * 10e-2,
    "d": 1.3e-6,
}

ZnO = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([4.3, 4.3, 4.3, 4.3]) * 10e-4,
    "U1": np.array([-3.09, -3.09, 3.09, 3.09]) * 10e-1,
    "U2": np.array([-3.25, -3.25, 3.25, 3.25]) * 10e-1,
    "U3": np.array([-1.59, 1.6, 1.59, -1.6]) * 10e-2,
    "U4": np.array([-1.76, 1.43, 1.76, -1.43]) * 10e-2,
    "d": 1e-6,
}

B = 0.43
resistivity_correction = [-1, -1, 1, 1]
hall_correction = [-1, -1, 1, 1]


# calculate implicit correction function
def correction_function(f, r):
    return cosh((r - 1) / (r + 1) * log(2) / f) - 1 / 2 * exp(log(2) / f)


# calculate explicit correction function
def f(r):
    correction_function_fixed = lambda f: correction_function(f, r)
    result = fsolve(func=correction_function_fixed, x0=0.6)[0]
    return result


# calculate resistivities
def calculate_resistivities(measurement_dict):
    rhos = []
    d = measurement_dict["d"]
    for index in range(0, 4):
        i_1 = measurement_dict["I"][index]
        u_1 = measurement_dict["U1"][index]
        r_1 = u_1 / i_1

        i_2 = measurement_dict["I"][index]
        u_2 = measurement_dict["U2"][index]
        r_2 = u_2 / i_2

        rho = pi * d / log(2) * (r_1 + r_2) / 2
        rho = rho * f(r_1 / r_2)
        rhos.append(float(rho))

    rhos = [a * b for a, b in zip(rhos, resistivity_correction)]
    return rhos


def calculate_hall_coefficient(measurement_dict):
    halls = []
    d = measurement_dict["d"]
    for index in range(0, 4):
        i_1 = measurement_dict["I"][index]
        u_1 = measurement_dict["U3"][index]
        u_2 = measurement_dict["U4"][index]
        hall = d * (u_1 - u_2) / (B * i_1)
        halls.append(hall)

    rhos = [a * b for a, b in zip(halls, hall_correction)]
    return rhos


def float_format(x):
    formatted_value = "\\num{" + f"{x:.2e}" + "}"
    return formatted_value


if __name__ == "__main__":
    p_si_r = np.array(calculate_resistivities(P_SI))
    zno_r = np.array(calculate_resistivities(ZnO))
    zto_r = np.array(calculate_resistivities(ZTO))
    cui_r = np.array(calculate_resistivities(CuI))

    df = pd.DataFrame(columns=["property", "P-Si", "ZnO", "ZTO", "CuI"])
    for i in range(0, 4):
        df.loc[i] = [f"\\rho_{{{i + 1}}}", p_si_r[i], zno_r[i], zto_r[i], cui_r[i]]
    df.loc[4] = ["\\rho_\\text{avg}", np.mean(p_si_r), np.mean(zno_r), np.mean(zto_r), np.mean(cui_r)]
    df.loc[5] = ["\\rho_\\text{std}", np.std(p_si_r), np.std(zno_r), np.std(zto_r), np.std(cui_r)]

    p_si_h = np.array(calculate_hall_coefficient(P_SI))
    zno_h = np.array(calculate_hall_coefficient(ZnO))
    zto_h = np.array(calculate_hall_coefficient(ZTO))
    cui_h = np.array(calculate_hall_coefficient(CuI))

    for i in range(6, 10):
        df.loc[i] = [f"R_\\mathrm{{H}},{i - 5}", p_si_h[i - 6], zno_h[i - 6], zto_h[i - 6], cui_h[i - 6]]
    df.loc[10] = ["R_{\\mathrm{H},\\text{avg}}", np.mean(p_si_h), np.mean(zno_h), np.mean(zto_h), np.mean(cui_h)]
    df.loc[11] = ["R_{\\mathrm{H},\\text{std}}", np.std(p_si_h), np.std(zno_h), np.std(zto_h), np.std(cui_h)]

    p_si_m = p_si_h / p_si_r
    zno_m = zno_h / zno_r
    zto_m = zto_h / zto_r
    cui_m = cui_h / cui_r

    for i in range(12, 16):
        df.loc[i] = [f"\\mu_{{{i - 11}}}", p_si_m[i - 12], zno_m[i - 12], zto_m[i - 12], cui_m[i - 12]]
    df.loc[16] = ["\\mu_\\text{avg}", np.mean(p_si_m), np.mean(zno_m), np.mean(zto_m), np.mean(cui_m)]
    df.loc[17] = ["\\mu_\\text{std}", np.std(p_si_m), np.std(zno_m), np.std(zto_m), np.std(cui_m)]

    p_si_n = np.abs(1 / e * 1 /p_si_h)
    zno_n = np.abs(1 / e * 1 /zno_h)
    zto_n = np.abs(1 / e * 1 /zto_h)
    cui_n = np.abs(1 / e * 1 /cui_h)

    for i in range(18, 22):
        df.loc[i] = [f"n_{{{i - 17}}}", p_si_n[i - 18], zno_n[i - 18], zto_n[i - 18], cui_n[i - 18]]
    df.loc[22] = ["n_\\text{avg}", np.mean(p_si_n), np.mean(zno_n), np.mean(zto_n), np.mean(cui_n)]
    df.loc[23] = ["n_\\text{std}", np.std(p_si_n), np.std(zno_n), np.std(zto_n), np.std(cui_n)]

    df.to_latex(
        file_directory / ".." / "plots" / "resistivity_hall.tex",
        index=False,
        escape=False,
        float_format=float_format,
    )
