# Define a function to standardize optical power units to nanowatts (nW)
import io
import math
import pathlib

import pandas as pd
from scipy import constants


def convert_to_nw(val: str | float | None) -> float | None:
    if pd.isna(val):
        return val

    val_str: str = str(val).strip()
    if "nW" in val_str:
        return float(val_str.replace("nW", "").strip())
    elif "uW" in val_str:
        return float(val_str.replace("uW", "").strip()) * 1000
    else:
        return float(val_str)


# --- Platinum resistance thermometer (IEC 60751) ---
PT_A = 3.9083e-3  # 1/degC
PT_B = -5.775e-7  # 1/degC^2


def pt_temperature(resistance: float, r_0: float = 100.0) -> float:
    """Convert a platinum RTD resistance in Ohm into a temperature in degrees Celsius.

    Inverts the Callendar-Van Dusen equation R(T) = r_0 (1 + A T + B T^2) of IEC 60751,
    with r_0 = 100 for a Pt100 and r_0 = 1000 for a Pt1000. Below 0 degC the standard
    adds a cubic term that this closed-form inversion does not cover, so the function is
    restricted to resistances at or above r_0.
    """
    if resistance < r_0:
        raise ValueError(f"only defined for T >= 0 degC, i.e. resistance >= {r_0} Ohm")

    # Of the two roots of B T^2 + A T + (1 - R/r_0) = 0 only this one is physical; the
    # other lies several thousand degrees above the range the sensor is specified for.
    root = math.sqrt(PT_A**2 - 4 * PT_B * (1 - resistance / r_0))
    return (-PT_A + root) / (2 * PT_B)


def enrich_data_frame(df: pd.DataFrame) -> pd.DataFrame:
    df: pd.DataFrame = df.rename(
        columns={
            "Diodenstrom I_D (mA)": "I_mA",
            "Diodenspannung V_D (mV)": "V_mV",
        }
    )

    # Convert Columns
    df["P_opt_nW"] = df["Optische Leistung P"].apply(convert_to_nw)

    # Add SI Base Units
    df["I"] = df["I_mA"] / 1e3
    df["V"] = df["V_mV"] / 1e3
    df["P_opt"] = df["P_opt_nW"] / 1e9
    df["P_opt_mW"] = df["P_opt_nW"] / 1e6

    df["P_el"] = df["V"] * df["I"]
    df["eta_total"] = df["P_opt"] / df["P_el"]
    df["eta_total_percent"] = df["eta_total"] * 100

    return df[["I", "V", "P_opt", "P_el", "I_mA", "V_mV", "P_opt_nW", "P_opt_mW", "eta_total", "eta_total_percent"]]


# --- Spectra (tasks 3 to 5) ---

# Photon energy of light with a vacuum wavelength of 1 nm, h c / e in eV nm.
HC_EV_NM: float = constants.h * constants.c / constants.e * 1e9

# The metadata block ends at a rule of dashes; the line above it holds the column names.
_RULE_CHARS = {"-"}


def read_spectrum(path: pathlib.Path | str) -> pd.DataFrame:
    """Read one monochromator scan from data/task_3_4_5 into a DataFrame.

    The instrument writes a CRLF file in a single-byte German code page: a block of
    metadata lines, a blank line, a tab separated column header, a rule of dashes, and
    then the scan in order of decreasing wavelength.

    Returns the scan sorted by increasing wavelength, with

        lambda_nm    detection wavelength in nm, as measured
        lambda_m     the same in m
        E_eV         photon energy h c / lambda in eV
        E_J          the same in J
        signal       lock-in signal in arbitrary units
        detection_V  the file's "Detection intensity (V)" column

    The lock-in output is written into the file's "Excitation intensity" column, which
    is what `signal` holds; "Detection intensity (V)" is identically zero in all three
    files of this run and is carried along only so that can be checked. The fourth
    column, "Excitation wavelength (nm)", is a constant 400 nm left over from the
    photoluminescence setup - the diode is driven electrically here - and is dropped.

    The metadata block is parsed into `df.attrs` under its own keys ("timestamp",
    "Sample name", "Comment", ...). `attrs` survives slicing but not every pandas
    operation, so read it off the frame this function returns.
    """
    lines: list[str] = pathlib.Path(path).read_text(encoding="cp1252").splitlines()

    # Locating the rule rather than counting header lines keeps the reader working if
    # the instrument software writes another metadata field.
    rule: int = next(i for i, line in enumerate(lines) if set(line.strip()) == _RULE_CHARS)

    # The first line is the bare acquisition timestamp; the rest of the block is
    # "Key: value", with the value empty for settings that were not recorded.
    attrs: dict[str, str] = {"timestamp": lines[0].strip()}
    for line in lines[1 : rule - 1]:
        key, separator, value = line.partition(":")
        if separator:
            attrs[key.strip()] = value.strip()

    columns: list[str] = [name.strip() for name in lines[rule - 1].split("\t")]
    df: pd.DataFrame = pd.read_csv(
        io.StringIO("\n".join(lines[rule + 1 :])),
        sep="\t",
        names=columns,
    )

    df = df.rename(
        columns={
            "Detection wavelength (nm)": "lambda_nm",
            "Excitation intensity": "signal",
            "Detection intensity (V)": "detection_V",
        }
    )

    df["lambda_m"] = df["lambda_nm"] / 1e9
    df["E_eV"] = HC_EV_NM / df["lambda_nm"]
    df["E_J"] = df["E_eV"] * constants.e

    # Stored from long to short wavelength, i.e. from low to high photon energy; sorting
    # by wavelength puts both axes in a monotonic order for plotting and fitting.
    df = df.sort_values("lambda_nm", ignore_index=True)

    df = df[["lambda_nm", "lambda_m", "E_eV", "E_J", "signal", "detection_V"]]
    df.attrs.update(attrs)
    return df
