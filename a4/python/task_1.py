import numpy as np
from numpy import cosh, exp, log
from scipy.constants import pi
from scipy.optimize import fsolve
from scipy.constants import e
import pandas as pd
import pathlib

file_directory = pathlib.Path(__file__).parent.resolve()

data = {
    "P_SI": {
        "T": np.array([300, 300, 300, 300]),
        "I": np.array([0.01, 0.01, 0.01, 0.01]),
        "U1": np.array([-5.69, -5.63, 5.86, 5.87]) * 10**-4,
        "U2": np.array([-3.92, -3.92, 3.99, 4.02]) * 10**-4,
        "U3": np.array([1.84, -1.77, -1.72, 1.87]) * 10**-4,
        "U4": np.array([1.90, -1.72, -1.78, 1.81]) * 10**-4,
        "d": 500e-6,
    },
    "ZnO": {
        "T": np.array([300, 300, 300, 300]),
        "I": np.array([4.3, 4.3, 4.3, 4.3]) * 10e-4,
        "U1": np.array([-3.09, -3.09, 3.09, 3.09]) * 10e-1,
        "U2": np.array([-3.25, -3.25, 3.25, 3.25]) * 10e-1,
        "U3": np.array([-1.59, 1.6, 1.59, -1.6]) * 10e-2,
        "U4": np.array([-1.76, 1.43, 1.76, -1.43]) * 10e-2,
        "d": 1e-6,
    },
    "ZTO": {
        "T": np.array([300, 300, 300, 300]),
        "I": np.array([8.5, 8.5, 8.5, 8.5]) * 10e-3,
        "U1": np.array([-2.75, -2.75, 2.75, 2.74]) * 10e-1,
        "U2": np.array([-2.87, -2.87, 2.87, 2.87]) * 10e-1,
        "U3": np.array([-1.26, 1.25, 1.23, -1.29]) * 10e-2,
        "U4": np.array([-1.33, 1.18, 1.3, -1.23]) * 10e-2,
        "d": 1.3e-6,
    },
    "CuI": {
        "T": np.array([300, 300, 300, 300]),
        "I": np.array([0.03, 0.03, 0.03, 0.03]),
        "U1": np.array([-1.7, -1.68, 1.75, 1.75]) * 10e-3,
        "U2": np.array([-1.19, -1.19, 1.17, 1.18]) * 10e-3,
        "U3": np.array([5.27, -5.52, -5.18, 5.45]) * 10e-4,
        "U4": np.array([5.45, -5.34, -5.36, 5.28]) * 10e-4,
        "d": 330e-9,
    },
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
    return np.array(rhos)


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
    return np.array(rhos)


def calculate_hall_concentration(hall_coefficient):
    return np.abs(1 / e * 1 / hall_coefficient)


def calculate_hall_mobility(hall_coefficient, resistivity):
    return hall_coefficient / resistivity


def float_format(x):
    formatted_value = "\\num{" + f"{x:.2e}" + "}"
    return formatted_value


if __name__ == "__main__":
    resistivities = {key: calculate_resistivities(value) for key, value in data.items()}
    hall_coefficients = {key: calculate_hall_coefficient(value) for key, value in data.items()}
    hall_mobility = {key: calculate_hall_mobility(hall_coefficients[key], resistivities[key]) for key in data.keys()}
    hall_concentration = {key: calculate_hall_concentration(hall_coefficients[key]) for key in data.keys()}

    df = pd.DataFrame(columns=["Property", "p-Si", "ZnO", "ZTO", "CuI"])

    for i in range(0, 4):
        table_resistivities = [resistivities[key][i] for key in data.keys()]
        df.loc[i] = [f"$\\rho_{{{i + 1}}}$", *table_resistivities]
    mean_resistivities = {key: np.mean(value) for key, value in resistivities.items()}
    std_resistivities = {key: np.std(value) for key, value in resistivities.items()}
    df.loc[4] = ["$\\rho_\\text{avg}$", *mean_resistivities.values()]
    df.loc[5] = ["$\\rho_\\text{std}$", *std_resistivities.values()]

    for i in range(6, 10):
        table_hall_coefficients = [hall_coefficients[key][i - 6] for key in data.keys()]
        df.loc[i] = [f"$R_{{\\mathrm{{H}},{i - 5}}}$", *table_hall_coefficients]
    mean_hall_coefficients = {key: np.mean(value) for key, value in hall_coefficients.items()}
    std_hall_coefficients = {key: np.std(value) for key, value in hall_coefficients.items()}
    df.loc[10] = ["$R_{\\mathrm{H},\\text{avg}}$", *mean_hall_coefficients.values()]
    df.loc[11] = ["$R_{\\mathrm{H},\\text{std}}$", *std_hall_coefficients.values()]

    for i in range(12, 16):
        table_hall_concentration = [hall_concentration[key][i - 12] for key in data.keys()]
        df.loc[i] = [f"$n_{{{i - 11}}}$", *table_hall_concentration]
    mean_hall_concentration = {key: np.mean(value) for key, value in hall_concentration.items()}
    std_hall_concentration = {key: np.std(value) for key, value in hall_concentration.items()}
    df.loc[16] = ["$n_\\text{avg}$", *mean_hall_concentration.values()]
    df.loc[17] = ["$n_\\text{std}$", *std_hall_concentration.values()]

    for i in range(18, 22):
        table_hall_mobility = [hall_mobility[key][i - 18] for key in data.keys()]
        df.loc[i] = [f"$\\mu_{{\\mathrm{{H}},{i - 17}}}$", *table_hall_mobility]
    mean_hall_mobility = {key: np.mean(value) for key, value in hall_mobility.items()}
    std_hall_mobility = {key: np.std(value) for key, value in hall_mobility.items()}
    df.loc[22] = ["$\\mu_{\\mathrm{H},\\text{avg}}$", *mean_hall_mobility.values()]
    df.loc[23] = ["$\\mu_{\\mathrm{H},\\text{std}}$", *std_hall_mobility.values()]

    save_path = file_directory.parent / "plots" / "resistivity_hall.tex"
    df.to_latex(
        buf=str(save_path),
        index=False,
        escape=False,
        float_format=float_format,
    )

    with open(save_path, "r") as file:
        lines = file.readlines()
        for index, line_index in enumerate([10,16,22]):
            lines.insert(line_index + index, "\\midrule\n")
    with open(save_path, "w") as file:
        file.writelines(lines)

shorted_df = df.iloc[[4,10,16,22]]
units = [r"\unit{\ohm\meter}", r"\unit{\meter^3 \per \coulomb}", r"\unit{m^{-3}}", r"\unit{\meter^2 \per \volt \per \second}"]
units = [f"({unit})" for unit in units]
shorted_df.loc[:, "Property"] = [text + " " + unit for text, unit in zip(shorted_df["Property"], units)]
shorted_df.to_latex(
    buf=str(file_directory.parent / "plots" / "resistivity_hall_short.tex"),
    index=False,
    escape=False,
    float_format=float_format,
)