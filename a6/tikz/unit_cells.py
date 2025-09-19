from tikzpy import TikzPicture
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()


substrate_width = 0.8
film_width = 0.6
padding = 0.2

tikz = TikzPicture()
substrate = tikz.rectangle(
    left_corner=(0, 0),
    width = substrate_width,
    height = substrate_width,
)
tikz.node(position=substrate.right_corner + (padding, -substrate_width), 
          text="Substrate", 
          options="anchor=south west",)

thin_film = tikz.rectangle(
    left_corner=(0, substrate_width + padding),
    width=film_width,
    height=film_width,
    options="fill=gray!50",
)
tikz.node(position=thin_film.right_corner + (padding, -film_width), 
          text="Thin Film", 
          options="anchor=south west",)


width_sub = tikz.line(start=(0, -padding), end=(substrate_width, -padding), options="|-|")
tikz.node(position=width_sub.midpoint(), text="$a_\mathrm{sub}$", options="below")
height_sub = tikz.line(start=(-padding, 0), end=(-padding, substrate_width), options="|-|")
tikz.node(position=height_sub.midpoint(), text="$c_\mathrm{sub}$", options="left")

width_film = tikz.line(start = (0, substrate_width + padding + film_width + padding), 
                      end = (film_width, substrate_width + padding + film_width + padding), 
                      options="|-|")
tikz.node(position=width_film.midpoint(), text="$a_\mathrm{film}^\mathrm{relax}$", options="above")
height_film = tikz.line(start=(-padding, substrate_width + padding), 
                       end=(-padding, substrate_width + padding + film_width), 
                       options="|-|")
tikz.node(position=height_film.midpoint(), text="$c_\mathrm{film}^\mathrm{relax}$", options="left")



tikz.compile(pdf_destination= file_path.parent / "assets" / "unit_cell.pdf")