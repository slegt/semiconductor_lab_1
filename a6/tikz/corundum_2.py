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


vacancies = []
hole_labels = [0,3,6,10,13,17,20,23, 25]
for i in range(-15, 16):
    for j in range(-15, 16):
        point = ((i+2/3) * base_vector_1 + (j+2/3) * base_vector_2)
        if np.linalg.norm(point) < 2.8:
            vacancies.append(point)


tikz = TikzPicture()

# O Sublattice

for number, point in enumerate(o_layer_1):
    tikz.circle(center=tuple(point), radius=0.5, options="fill=green!30")
    #tikz.node(position=tuple(point), text=str(number), options="inner sep=0pt, font=\\tiny")
for number, point in enumerate(vacancies):
    if number in hole_labels:
        tikz.circle(center=tuple(point), radius=0.2, options="fill=white!80")
    else:
        tikz.circle(center=tuple(point), radius=0.2, options="fill=black")
    #tikz.node(position=tuple(point), text=str(number), options="inner sep=0pt, font=\\tiny")

# Lattice Vectors
line = tikz.line(tuple(o_layer_1[4]), tuple(o_layer_1[5]), options="->")
tikz.node(line.end, text="$\mathbf{a}_1$", options="above , inner sep=0pt")

line = tikz.line(tuple(o_layer_1[4]), tuple(o_layer_1[10]), options="->")
tikz.node(line.end, text="$\mathbf{a}_2$", options="above, inner sep=0pt")


# Hole Lattice Vectors
line = tikz.line(tuple(vacancies[17]), tuple(vacancies[13]), options="->")
tikz.node(line.end, text="$\mathbf{b}_1$", options="above right, inner sep=4pt")

line = tikz.line(tuple(vacancies[17]), tuple(vacancies[23]), options="->")
tikz.node(line.end, text="$\mathbf{b}_2$", options="above right, inner sep=4pt")



tikz.compile(pdf_destination= file_path.parent / "assets" /  "corundum_2.pdf")
