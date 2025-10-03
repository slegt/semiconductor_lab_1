from tikzpy import TikzPicture
import numpy as np
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()

base_vector_1 = np.array([0, 1], dtype=float)
base_vector_2 = np.array([np.cos(np.deg2rad(30)), np.sin(np.deg2rad(30))], dtype=float)
padding=0.2

o_layer_1 = []
for i in range(-15, 16):
    for j in range(-15, 16):
        point = (i * base_vector_1 + j * base_vector_2)
        if np.linalg.norm(point) < 3:
            o_layer_1.append(point)

o_layer_2 = []
for i in range(-15, 16):
    for j in range(-15, 16):
        point = ((i+1/3) * base_vector_1 + (j+1/3) * base_vector_2)
        if np.linalg.norm(point) < 2.8:
            o_layer_2.append(point)

vacancies = []
for i in range(-15, 16):
    for j in range(-15, 16):
        point = ((i+2/3) * base_vector_1 + (j+2/3) * base_vector_2)
        if np.linalg.norm(point) < 2.8:
            vacancies.append(point)


tikz = TikzPicture()

for point in o_layer_1:
    tikz.circle(center=tuple(point), radius=0.5, options="fill=green!30")

for point in vacancies:
    tikz.circle(center=tuple(point), radius=0.2, options="fill=gray!80")

for point in o_layer_2:
    tikz.circle(center=tuple(point), radius=0.5, options="fill=yellow!70, opacity=0.8")


tikz.compile(pdf_destination= file_path.parent / "assets" /  "corundum_1.pdf")
