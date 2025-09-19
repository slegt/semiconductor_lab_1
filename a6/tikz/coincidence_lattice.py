from tikzpy import TikzPicture
import numpy as np
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()

base_vector_1 = np.array([0, 1], dtype=float)
base_vector_2 = np.array([np.cos(np.deg2rad(30)), np.sin(np.deg2rad(30))], dtype=float)
padding=0.2

points = []
for i in range(-15, 16):
    for j in range(-15, 16):
        point = (i * base_vector_1 + j * base_vector_2)
        if np.linalg.norm(point) < 3:
            points.append(point)

tikz = TikzPicture()

# O Sublattice
for index, point in enumerate(points):
    for neibhbor in points[:index]:
        if np.linalg.norm((neibhbor - point)) < 1.1 and np.linalg.norm((neibhbor - point)) > 0.9:
            tikz.line(start=tuple(point), end=tuple(neibhbor), options="line width=0.2pt, gray, dashed")
for point in points:
    tikz.circle(center=tuple(point), radius=0.05, options="fill=black")

# Zn Lattice 
points = [1.1 * point for point in points]
for point in points:
    tikz.circle(center=tuple(point), radius=0.05, options="fill=gray!50")

length_1 = tikz.line(start=(padding,0), end=(padding, 1), options="|-|")
tikz.node(position=length_1.midpoint(), text="$a_\mathrm{O}$", options="right, inner sep=0.6pt")
length_2 = tikz.line(start=(-padding, 0), end=(-padding, 1.1), options="|-|, gray")
tikz.node(position=length_2.midpoint(), text="$a_\mathrm{Zn}$", options="left, inner sep=0pt, gray")



    


tikz.compile(pdf_destination= file_path.parent / "assets" /  "coincidence_lattice.pdf")
