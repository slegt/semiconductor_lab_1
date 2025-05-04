import numpy as np
from numpy import cosh, exp, log
from scipy.constants import pi
from scipy.optimize import fsolve

B= 0.43

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

ZTO= {
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
    "U2": np.array([-3.26, -3.25, 3.25, 3.25]) * 10e-1,
    "U3": np.array([-1.59, 1.6, 1.59, -1.6]) * 10e-2,
    "U4": np.array([-1.76, 1.43, 1.76, -1.43]) * 10e-2,
    "d": 1e-6
}

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
def calculate_hall_coefficient(measurement_dict):
    halls = []
    d = measurement_dict["d"]
    for index in range(0, 4):
        i_1 = measurement_dict["I"][index]
        u_1 = measurement_dict["U3"][index]
        u_2 = measurement_dict["U4"][index]
        hall = d * (u_1 - u_2) / (B * i_1)
        halls.append(hall)

    rhos = [a *  b for a, b in zip(halls, hall_correction)]
    return rhos


if __name__ == "__main__":
    p_si = np.array(calculate_hall_coefficient(P_SI))
    zno = np.array(calculate_hall_coefficient(ZnO))
    zto = np.array(calculate_hall_coefficient(ZTO))
    cui = np.array(calculate_hall_coefficient(CuI))

    print(f"P-Si: {np.round(p_si*1000, 3)}")
    print(f"ZnO: {np.eound(zno*1000, 3)}")
    print(f"ZTO: {(zto}")
    print(f"CuI: {cui}")

    print(f"P-Si: {np.mean(p_si)}+-{np.std(p_si)}")
    print(f"ZnO: {np.mean(zno)}+-{np.std(zno)}")
    print(f"ZTO: {np.mean(zto)}+-{np.std(zto)}")
    print(f"CuI: {np.mean(cui)}+-{np.std(cui)}")

