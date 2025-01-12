from PIL import Image, ImageDraw
import pathlib
from numpy import cos, pi


x = 1426
y_min, y_max = 472, 566
conversion_factor = 5 / 451  # micrometer per pixel

current_path = pathlib.Path(__file__).parent.resolve()
import_prefix = current_path.parent / "data"
export_prefix = current_path.parent / "plots"

import_path = str(import_prefix / "tilted_sample.tiff")
export_path = str(export_prefix / "tilted.pdf")
image = Image.open(import_path).convert("RGB")

draw = ImageDraw.Draw(image)
draw.line([(x, y_min), (x, y_max)], fill="orange", width=10)
draw.line([(x - 30, y_min), (x + 30, y_min)], fill="orange", width=10)
draw.line([(x - 30, y_max), (x + 30, y_max)], fill="orange", width=10)

image.save(export_path)

distance = (y_max - y_min) * conversion_factor
alpha = 0.977
distance_calibrated = distance * alpha / cos(pi / 4)
print(f"The distance d* is {distance}")
print(f"The calibrated distance d is {distance_calibrated}")
