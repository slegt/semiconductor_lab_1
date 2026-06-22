# --- Geometric and Font Constants ---
PT_TO_INCHES = 1.0 / 72.27
BASE_FONT_SIZE = 10

# --- Single Unified rcParams Configuration ---

SINGLE_COLUMN = {
    # Figure Geometry
    "figure.figsize": (221 * PT_TO_INCHES, 221 * PT_TO_INCHES),
    # Font Configuration
    "font.size": BASE_FONT_SIZE,
    "text.usetex": True,
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
    "font.family": "serif",
    "font.serif": [
        "Computer Modern Roman",
        "Times New Roman",
        "Times",
        "Liberation Serif",
    ],
}
