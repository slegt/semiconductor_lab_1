import pandas as pd

from task_1 import P_SI, ZTO, CuI, ZnO, calculate_resistivities


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
    rhos = calculate_resistivities(ZnO)
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
    rhos = calculate_resistivities(ZTO)
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
    rhos = calculate_resistivities(CuI)
    print(rhos)
    
# calculate hall coefficients
def calculate_hall_coefficient(measurement_dict):
    hall_coefficients = []
    d = 500e-6
    for index in range(0, 4):
        i = measurement_dict["I"][index]
        u_3 = measurement_dict["U3"][index]
        u_4 = measurement_dict["U4"][index]

        hall_coefficient = d / (i * B) * (u_3 - u_4)
        hall_coefficients.append(float(hall_coefficient))
    return hall_coefficients