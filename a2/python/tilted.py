from PIL import Image, ImageDraw
import pathlib
from numpy import cos, pi, tan


def t(d_star, alpha, theta):
    return d_star * alpha / cos(theta)


def delta_t(d_star, alpha, theta, delta_d_star, delta_alpha, delta_theta):
    s1 = d_star * delta_alpha / cos(theta)
    s2 = alpha * delta_d_star / cos(theta)
    s3 = d_star * alpha * delta_theta * tan(theta) / cos(theta)
    return s1 + s2 + s3


x = 1426
y_min, y_max = 472, 566
conversion_factor = 5 / 451  # micrometer per pixel
delta_d_star = conversion_factor / 2

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

d_star = (y_max - y_min) * conversion_factor

alpha = 0.98
delta_alpha = 0.01

theta = 45 * 2 * pi / 360
delta_theta = 5 * 2 * pi / 360

t_param = t(d_star, alpha, theta)
delta_t_param = delta_t(d_star, alpha, theta, delta_d_star, delta_alpha, delta_theta)


print(f"The distance d* is {d_star} +- {delta_d_star} micrometer")
print(f"The calibrated distance d is {t_param} +- {delta_t_param}")
