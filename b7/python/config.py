"""Shared plotting configuration and data helpers for the B7 notebooks.

The notebook kernels do not run with this directory on sys.path, so import it
package-qualified from the project root:

    from b7.python.config import DATA_DIR, DOUBLE_COLUMN, SINGLE_COLUMN, convert_to_nw
"""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd

# --- Directories ---
# Anchored on this file rather than the working directory, which differs between
# PyCharm and a plain jupyter server.
B7_DIR = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = B7_DIR / "data"
PLOTS_DIR = B7_DIR / "plots"

# --- Geometric and Font Constants ---
PT_TO_INCHES = 1.0 / 72.27
BASE_FONT_SIZE = 10

LATEX_PREAMBLE = r"\usepackage{siunitx}"

# The preamble is read when a figure is drawn, not when its artists are created, and the
# inline backend draws the figure after the rc_context in the notebook has already
# exited. Setting it globally on import is what makes \unit{} survive until draw time;
# every other rcParam below is baked into the artists inside the context.
plt.rcParams["text.latex.preamble"] = LATEX_PREAMBLE


# --- Single Unified rcParams Configuration ---

SINGLE_COLUMN = {
    # Figure Geometry
    "figure.figsize": (221 * PT_TO_INCHES, 221 * PT_TO_INCHES),
    # Font Configuration
    "font.size": BASE_FONT_SIZE,
    "text.usetex": True,
    "text.latex.preamble": LATEX_PREAMBLE,
    "font.family": "serif",
    "font.serif": [
        "Computer Modern Roman",
        "Times New Roman",
        "Times",
        "Liberation Serif",
    ],
}

DOUBLE_COLUMN = {
    # Figure Geometry
    "figure.figsize": (452 * PT_TO_INCHES, 250 * PT_TO_INCHES),
    # Font Configuration
    "font.size": BASE_FONT_SIZE,
    "text.usetex": True,
    "text.latex.preamble": LATEX_PREAMBLE,
    "font.family": "serif",
    "font.serif": [
        "Computer Modern Roman",
        "Times New Roman",
        "Times",
        "Liberation Serif",
    ],
}


# Define a function to standardize optical power units to nanowatts (nW)
def convert_to_nw(val):
    if pd.isna(val):
        return val
    val_str = str(val).strip()
    if "nW" in val_str:
        return float(val_str.replace("nW", "").strip())
    elif "uW" in val_str:
        return float(val_str.replace("uW", "").strip()) * 1000
    else:
        return float(val_str)
