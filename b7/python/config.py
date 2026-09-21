"""
Shared plotting configuration and data helpers for the B7 notebooks.
import as:
from b7.python.config import DATA_DIR, DOUBLE_COLUMN, SINGLE_COLUMN, convert_to_nw
"""

import pathlib

import matplotlib.pyplot as plt
from matplotlib.typing import RcKeyType

# --- Directories ---
B7_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR: pathlib.Path = B7_DIR / "data"
PLOTS_DIR: pathlib.Path = B7_DIR / "plots"

# --- Geometric and Font Constants ---
PT_TO_INCHES: float = 1.0 / 72.27
BASE_FONT_SIZE = 10

LATEX_PREAMBLE = r"\usepackage{siunitx}"

# The preamble is read when a figure is drawn, not when its artists are created, and the
# inline backend draws the figure after the rc_context in the notebook has already
# exited.
plt.rcParams["text.latex.preamble"] = LATEX_PREAMBLE


# --- Single Unified rcParams Configuration ---

SINGLE_COLUMN: dict[RcKeyType, tuple[float, float] | int | str | list[str]] = {
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

DOUBLE_COLUMN: dict[RcKeyType, tuple[float, float] | int | str | list[str]] = {
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
