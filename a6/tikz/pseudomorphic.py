from tikzpy import TikzPicture
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()



substrate_width = 0.8
film_width = 0.6
padding = 0.2

tikz = TikzPicture()
for x in range(4):
    for y in range(3):
        tikz.rectangle(
            left_corner=(x * substrate_width, y * substrate_width),
            width=substrate_width,
            height=substrate_width,
        )

for x in range(4):
    for y in range(2):
        tikz.rectangle(
            left_corner=(x * substrate_width, 3 * substrate_width + y * film_width),
            width=substrate_width,
            height=film_width,
            options="fill=gray!50",
        )

width = tikz.line(start=(0, -padding), end=(substrate_width, -padding), options="|-|")
tikz.node(position=width.midpoint(), text="$a_\mathrm{sub}$", options="below")

height = tikz.line(
    start=(4 * substrate_width + padding, 0),
    end=(4 * substrate_width + padding, substrate_width),
    options="|-|",
)
tikz.node(position=height.midpoint(), text="$c_\mathrm{sub}$", options="right")

thin_film_height = tikz.line(
    start=(4 * substrate_width + padding, 3 * substrate_width),
    end=(4 * substrate_width + padding, 3 * substrate_width + film_width),
    options="|-|",
)
tikz.node(position=thin_film_height.midpoint(), text="$c_\mathrm{film}$", options="right")

thin_film_width = tikz.line(
    start=(0, 3 * substrate_width + 2 * film_width + padding),
    end=(substrate_width, 3 * substrate_width + 2 * film_width + padding),
    options="|-|",
)
tikz.node(position=thin_film_width.midpoint() - (2.5 * padding, 0), text="$a_\mathrm{film}=a_\mathrm{sub}$", options="above, anchor= south west")

tikz.compile(pdf_destination= file_path.parent / "assets" /  "pseudomorphic.pdf")
