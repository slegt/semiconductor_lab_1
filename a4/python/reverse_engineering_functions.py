import numpy as np
from numpy import log, cosh, exp
import pandas as pd
from scipy.constants import pi
from scipy.optimize import fsolve


# count lines of a file
def count_lines(file_path):
    with open(file_path, "r") as file:
        line_count = sum(1 for line in file)
    return line_count


# get value dicts from file
def get_meta_df(filepath):
    data = []
    entries = int(count_lines(filepath) / 9)

    for i in range(entries):
        df_meta = pd.read_csv(
            filepath_or_buffer=filepath,
            delimiter=r"\t",
            engine="python",
            skiprows=3 + i * 9,
            nrows=1,
            header=None,
            names=["current", "magnetic_field", "thickness", "Nothing", "comment"],
        )
        df = pd.read_csv(
            filepath_or_buffer=filepath,
            delimiter=r"\t",
            engine="python",
            skiprows=5 + i * 9,
            nrows=4,
            names=["T", "I", "U1", "U2", "U3", "U4", "error"],
        )
        data_dict = {
            "B": df_meta["magnetic_field"][0],
            "d": df_meta["thickness"][0] * 10**-6,
            "T": df["T"].to_numpy(),
            "I": df["I"].to_numpy(),
            "U1": df["U1"].to_numpy(),
            "U2": df["U2"].to_numpy(),
            "U3": df["U3"].to_numpy(),
            "U4": df["U4"].to_numpy(),
        }
        data.append(data_dict)
    return data


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
        r_1 = np.abs(u_1 / i_1)

        i_2 = measurement_dict["I"][index]
        u_2 = measurement_dict["U1"][index]
        r_2 = np.abs(u_2 / i_2)

        rho = pi * d / log(2) * (r_1 + r_2) / 2
        rho = rho * f(r_1 / r_2)
        rhos.append(rho)
    return rhos


# calculate hall coefficients
def calculate_hall_coefficient(measurement_dict):
    hall_coefficients = []
    d = 500e-6
    for index in range(0, 4):
        i = measurement_dict["I"][index]
        u_3 = measurement_dict["U3"][index]
        u_4 = measurement_dict["U4"][index]

        hall_coefficient = d / (i * B) * (u_3 - u_4)
        hall_coefficients.append(hall_coefficient)
    return hall_coefficients
