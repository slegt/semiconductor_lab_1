import numpy as np
from PIL import Image, ImageDraw
import pathlib

def alpha(d_grid, d_sem):
    return d_grid / d_sem

def delta_alpha(d_grid, d_sem, delta_d_grid, delta_d_sem):
    return delta_d_grid / d_sem + d_grid * delta_d_sem / d_sem**2

current_path = pathlib.Path(__file__).parent.resolve()

# manually choose points rectangle edges
dots_x = np.array(
    [
        [183, 430, 676, 922, 1169, 1415, 1663],
        [183, 430, 676, 922, 1168, 1416, 1662],
        [183, 430, 676, 921, 1168, 1414, 1661],
        [182, 429, 676, 922, 1168, 1414, 1661],
    ]
)
dots_y = np.array(
    [
        [126, 126, 125, 126, 126, 126, 127],
        [371, 371, 372, 371, 371, 372, 371],
        [619, 619, 619, 619, 619, 619, 619],
        [866, 866, 866, 867, 867, 867, 867],
    ]
)

# save image with dots for plotting
image_path = current_path / ".." / "data" / "calibration.tiff"
image = Image.open(image_path).convert("RGB")
draw = ImageDraw.Draw(image)
for x, y in zip(dots_x.flatten(), dots_y.flatten()):
    draw.circle((x, y), 10, fill="orange", outline=None, width=1)

export_path = current_path / ".." / "plots" / "calibration.pdf"
image.save(export_path)

# calculate distances and convert in micrometer
conversion_factor = 20 / 488 # micro meter per pixel
delta_mess = conversion_factor / 2


distances = []

# horizontal distances
for y in range(4):
    for x in range(6):
        distance_squared = (dots_x[y][x + 1] - dots_x[y][x]) ** 2 + (
            dots_y[y][x + 1] - dots_y[y][x]
        ) ** 2
        distance = distance_squared ** (1 / 2)
        distance = distance * conversion_factor
        distances.append(distance)


# vertical distance
for x in range(7):
    for y in range(3):
        distance_squared = (dots_x[y + 1][x] - dots_x[y][x]) ** 2 + (
            dots_y[y + 1][x] - dots_y[y][x]
        ) ** 2
        distance = distance_squared ** (1 / 2)
        distance = distance * conversion_factor
        distances.append(distance)

d_sem, std_sem = np.average(distances), np.std(distances, ddof=1)
delta_stat = 1 / len(distances) * std_sem
delta_d_sem = delta_stat + delta_mess
print(f"The average distance is {d_sem}+-{delta_d_sem} micrometer")

d_grid = 9.87
delta_d_grid = 0.05
print(f"The grid distance is {d_grid}+-{delta_d_grid} micrometer")

alpha_param = alpha(d_grid, d_sem)
delta_alpha_param = delta_alpha(d_grid, d_sem, delta_d_grid, delta_d_sem)
print(f"The alpha parameter is {alpha_param}+-{delta_alpha_param}")
