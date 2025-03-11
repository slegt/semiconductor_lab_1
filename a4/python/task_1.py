import numpy as np
from numpy import log, cosh, exp
from scipy.constants import pi
from scipy.optimize import fsolve

B = 0.43  # T

P_SI = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([0.01, 0.01, 0.01, 0.01]),
    "U1": np.array([-5.69, -5.63, 5.86, 5.87]) * 10**-4,
    "U2": np.array([-3.92, -3.92, 3.99, 4.02]) * 10**-4,
    "U3": np.array([1.84, -1.77, -1.72, 1.87]) * 10**-4,
    "U4": np.array([1.90, -1.72, -1.78, 1.81]) * 10**-4,
}

M_2 = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([0.03, 0.03, 0.03, 0.03]),
    "U1": np.array([-1.7, -1.68, 1.75, 1.75]) * 10e-3,
    "U2": np.array([-1.19, -1.19, 1.17, 1.18]) * 10e-3,
    "U3": np.array([5.27, -5.52, -5.18, 5.45]) * 10e-4,
    "U4": np.array([5.45, -5.34, -5.36, 5.28]) * 10e-4,
}

M_3 = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([8.5, 8.5, 8.5, 8.5]) * 10e-3,
    "U1": np.array([-2.75, -2.75, 2.75, 2.74]) * 10e-1,
    "U2": np.array([-2.87, -2.87, 2.87, 2.87]) * 10e-1,
    "U3": np.array([-1.26, 1.25, 1.23, -1.29]) * 10e-2,
    "U4": np.array([-1.33, 1.18, 1.3, -1.23]) * 10e-2,
}

M_4 = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([4.3, 4.3, 4.3, 4.3]) * 10e-4,
    "U1": np.array([-3.09, -3.09, 3.09, 3.09]) * 10e-1,
    "U2": np.array([-3.25, -3.25, 3.25, 3.25]) * 10e-1,
    "U3": np.array([-1.59, 1.6, 1.59, -1.6]) * 10e-2,
    "U4": np.array([-1.76, 1.43, 1.76, -1.43]) * 10e-2,
}


def correction_function(f, r):
    return cosh((r - 1) / (r + 1) * log(2) / f) - 1 / 2 * exp(log(2) / f)



def f(r):
    correction_function_fixed = lambda f: correction_function(f, r)
    result = fsolve(func=correction_function_fixed, x0=0.6)[0]
    return result


def calculate_resistivities(measurement_dict):
    rhos = []
    d = 500e-6
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


print(calculate_resistivities(P_SI))
print(calculate_resistivities(M_2))
print(calculate_resistivities(M_3))
print(calculate_resistivities(M_4))
print("\n")

print(calculate_hall_coefficient(P_SI))
print(calculate_hall_coefficient(M_2))
print(calculate_hall_coefficient(M_3))
print(calculate_hall_coefficient(M_4))
