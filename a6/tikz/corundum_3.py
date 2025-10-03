import pathlib

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.proj3d import proj_transform

file_path = pathlib.Path(__file__).parent.resolve()


plt.rcParams.update(
    {
        "text.usetex": True,
        "font.size": 10,
        "font.family": "serif",
    }
)

latex_column_width = 221.48395  # pt
pt_to_inch = latex_column_width / 72  # 1 inch = 72 points
a = pt_to_inch * 0.98


class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)


def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    """Add an 3d arrow to an `Axes3D` instance."""

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(Axes3D, "arrow3D", _arrow3D)


# Fixing random state for reproducibility
base_vector_1 = np.array([0, 1, 0])
base_vector_2 = np.array([np.cos(np.deg2rad(30)), np.sin(np.deg2rad(30)), 0])

fig = plt.figure(figsize=(a, a), constrained_layout=True)
ax = fig.add_subplot(projection="3d", computed_zorder=False)

# Make data
points = []
for i in range(-15, 16):
    for j in range(-15, 16):
        point = i * base_vector_1 + j * base_vector_2
        if np.linalg.norm(point) < 2.5:
            points.append(point)

concat_points = []
for i in range(4):
    concat_points = concat_points + [point + np.array([0, 0, i * 2.5]) for point in points]
white_indexes = [1, 3, 6, 9, 12, 15, 17, 19, 24, 27, 30, 33, 35, 40, 42, 45, 48, 51, 56, 58, 60, 63, 66, 69, 72, 74]
border_indexes = [0, 1, 2, 6, 11, 15, 18, 17, 16, 12, 7, 0]

x, y, z = [], [], []
for index in border_indexes:
    x.append(concat_points[index][0])
    y.append(concat_points[index][1])
    z.append(concat_points[index][2])
for i in range(4):
    ax.plot(x, y, np.array(z) + i * 2.5, color="black", alpha=0.8, linewidth=2, zorder=1)

for label, point in enumerate(concat_points):
    print(point)
    print(len(point))
    if label in white_indexes:
        ax.scatter(xs=point[0], ys=point[1], zs=point[2], s=15, c="white", edgecolors="black", zorder=2)
    else:
        ax.scatter(xs=point[0], ys=point[1], zs=point[2], s=15, c="black", zorder=4)

for i1, p1 in enumerate(concat_points):
    for i2, p2 in enumerate(concat_points[i1 + 1 :]):
        dist = np.linalg.norm(p1 - p2)
        if dist < 1.5:
            if i1 not in white_indexes and (i2 + i1 + 1) not in white_indexes:
                ax.plot(
                    [p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], c="gray", alpha=0.5, linewidth=0.5, linestyle="--"
                )


ax.arrow3D(0, 0, 7.5, *concat_points[17], mutation_scale=13, arrowstyle="->", color="red")
ax.arrow3D(0, 0, 7.5, *concat_points[15], mutation_scale=13, arrowstyle="->", color="red")
ax.text(0, 0, 9, "$\mathbf{b}_2$", color="red", horizontalalignment="center", verticalalignment="center")
ax.text(
    *(concat_points[15] + (0, 0, 8)),
    "$\mathbf{b}_1$",
    color="red",
    horizontalalignment="center",
    verticalalignment="center",
)

ax.arrow3D(0, 0, 0, *(concat_points[28]), arrowstyle="->", mutation_scale=13, color="blue", zorder=3)
ax.arrow3D(0, 0, 0, *(concat_points[14]), arrowstyle="->", mutation_scale=13, color="blue", zorder=3)
ax.arrow3D(0, 0, 0, *(concat_points[13]), arrowstyle="->", mutation_scale=13, color="blue", zorder=3)
ax.text(
    *(concat_points[28] + (0, 0, 0.3)),
    "$\mathbf{a}_3$",
    color="blue",
    horizontalalignment="center",
    verticalalignment="center",
)
ax.text(
    *(concat_points[14] + (0, 0.4, 0.1)),
    "$\mathbf{a}_1$",
    color="blue",
    horizontalalignment="center",
    verticalalignment="center",
)
ax.text(
    *(concat_points[13] + (0, 0, 0.3)),
    "$\mathbf{a}_2$",
    color="blue",
    horizontalalignment="center",
    verticalalignment="center",
)

ax.arrow3D(
    *concat_points[2 * 19 + 13],
    *concat_points[14],
    arrowstyle="->",
    mutation_scale=10,
    color="orange",
    zorder=3,
    alpha=0.8,
)
ax.arrow3D(
    *concat_points[1 * 19 + 8],
    *concat_points[14],
    arrowstyle="->",
    mutation_scale=10,
    color="orange",
    zorder=3,
    alpha=0.8,
)
ax.arrow3D(
    *concat_points[3], *concat_points[14], arrowstyle="->", mutation_scale=10, color="orange", zorder=3, alpha=0.8
)
ax.arrow3D(
    *concat_points[8],
    *(0, 0, 2.5),
    arrowstyle="-",
    mutation_scale=10,
    color="orange",
    zorder=3,
    alpha=0.5,
    linestyle="--",
)
ax.arrow3D(
    *concat_points[32],
    *(0, 0, 2.5),
    arrowstyle="-",
    mutation_scale=10,
    color="orange",
    zorder=3,
    alpha=0.5,
    linestyle="--",
)


ax.text(*(concat_points[7] - (0.5, 0, 0)), "A")
ax.text(*(concat_points[26] - (0.5, 0, 0)), "B")
ax.text(*(concat_points[45] - (0.5, 0, 0)), "C")
ax.text(*(concat_points[64] - (0.5, 0, 0)), "A")


# Set an equal aspect ratio
ax.set_proj_type("ortho")
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)


plt.savefig(file_path.parent / "assets" / "corundum_3.pdf")
