import numpy as np

from reverse_engineering_functions import calculate_resistivities, get_meta_df


P_SI = {
    "T": np.array([300, 300, 300, 300]),
    "I": np.array([0.01, 0.01, 0.01, 0.01]),
    "U1": np.array([-5.69, -5.63, 5.86, 5.87]) * 10**-4,
    "U2": np.array([-3.92, -3.92, 3.99, 4.02]) * 10**-4,
    "U3": np.array([1.84, -1.77, -1.72, 1.87]) * 10**-4,
    "U4": np.array([1.90, -1.72, -1.78, 1.81]) * 10**-4,
    "d": 500e-6,
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

thicknesses = {
    "p_si": 500e-6,  # m
    "zn_o": 1e-6,  # m
    "zto": 1.3e-6,  # m
    "cu_i": 330e-6,  # m
}

if __name__ == "__main__":
    # P_SI Data
    p_si_file_paths = [
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/1/P-Si - Jorrit.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/1/P-Si.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/2/p-Si_Gruppe4.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/3/p-Si_Christopher.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/Gruppe 5/p_si1.pra",
    ]

    print("p-Si")
    for file_path in p_si_file_paths:
        data = get_meta_df(file_path)
        for entry in data:
            rhos = calculate_resistivities(entry)
            print(rhos)

    print("My data")
    rhos = calculate_resistivities(P_SI)
    print(rhos)

    # ZnO Data
    zno_file_paths = [
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2022/E927.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/Gruppe 5/E927.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/3/E927_Christopher.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/2/ZnO_Gruppe4.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/1/ZnO-Jorrit.pra",
    ]

    print("zno")
    for file_path in zno_file_paths:
        data = get_meta_df(file_path)
        for entry in data:
            rhos = calculate_resistivities(entry)
            print(rhos)

    print("My data")
    for entry in [M_2, M_3, M_4]:
        entry["d"] = thicknesses["zn_o"]
        rhos = calculate_resistivities(entry)
        print(rhos)

    # ZTO Data
    zto_file_paths = [
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2022/E3266_ZTO.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/3/ZTO_Gruppe4.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2020/2/ZTO_Gruppe4.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2019/3/a-ZTO.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2019/2/a-ZTO.pra",
    ]

    print("zto")
    for file_path in zto_file_paths:
        data = get_meta_df(file_path)
        for entry in data:
            rhos = calculate_resistivities(entry)
            print(rhos)

    print("My data")
    for entry in [M_2, M_3, M_4]:
        entry["d"] = thicknesses["zto"]
        rhos = calculate_resistivities(entry)
        print(rhos)


    # CuI Data
    cui_file_paths = [
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2019/2/CuI.pra",
        "/run/media/simon/1C8A12CB8A12A0F6/A4/Prak/2019/3/CuI.pra",
    ]

    print("cu_i")
    for file_path in cui_file_paths:
        data = get_meta_df(file_path)
        for entry in data:
            rhos = calculate_resistivities(entry)
            print(rhos)

    print("My data")
    for entry in [M_2, M_3, M_4]:
        entry["d"] = thicknesses["cu_i"]
        rhos = calculate_resistivities(entry)
        print(rhos)


# print(calculate_resistivities(P_SI))
# print(calculate_resistivities(M_2))
# print(calculate_resistivities(M_3))
# print(calculate_resistivities(M_4))
# print("\n")

# print(calculate_hall_coefficient(P_SI))
# print(calculate_hall_coefficient(M_2))
# print(calculate_hall_coefficient(M_3))
# print(calculate_hall_coefficient(M_4))
