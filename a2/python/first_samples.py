import os
import pathlib
from PIL import Image, ImageDraw, ImageSequence


current_path = pathlib.Path(__file__).parent.resolve()


def tiff_to_pdf(tiff_path: str, pdf_path) -> str:
    if not os.path.exists(tiff_path):
        raise Exception(f"{tiff_path} does not find.")
    image = Image.open(tiff_path)

    images = []
    for _, page in enumerate(ImageSequence.Iterator(image)):
        page = page.convert("RGB")
        images.append(page)
    if len(images) == 1:
        images[0].save(pdf_path)
    else:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
    return pdf_path


import_prefix = current_path / ".." / "data"
export_prefix = current_path / ".." / "plots"
images = ["sample_1_BSD_full", "sample_1_BSD_45"]
for image in images:
    tiff_to_pdf(
        str(import_prefix / (image + ".tiff")), str(export_prefix / (image + ".pdf"))
    )

conversion_factor = 20 / 487  # pixel per micrometer

x1 = [744, 817]
x2 = [817, 933]

y1 = 120
y2 = 220

x3 = 510
y3 = [370, 444]

x4 = 610
y4 = [444, 507]

import_path = import_prefix / "sample_1_SED.tiff"
export_path = export_prefix / "sample_1_SED.pdf"
image = Image.open(import_path).convert("RGB")

draw = ImageDraw.Draw(image)
draw.line([(x1[0], y1), (x1[1], y1)], width=10, fill="orange")
draw.line([(x1[0], y1 - 25), (x1[0], y1 + 25)], width=10, fill="orange")
draw.line([(x1[1], y1 - 25), (x1[1], y1 + 25)], width=10, fill="orange")
draw.text((x1[0] - 40, y1), "1", anchor="mm", font_size=70, fill="orange")

draw.line([(x2[0], y2), (x2[1], y2)], width=10, fill="orange")
draw.line([(x2[0], y2 - 25), (x2[0], y2 + 25)], width=10, fill="orange")
draw.line([(x2[1], y2 - 25), (x2[1], y2 + 25)], width=10, fill="orange")
draw.text((x2[0] - 40, y2), "2", anchor="mm", font_size=70, fill="orange")

draw.line([(x3, y3[0]), (x3, y3[1])], width=10, fill="orange")
draw.line([(x3 - 25, y3[0]), (x3 + 25, y3[0])], width=10, fill="orange")
draw.line([(x3 - 25, y3[1]), (x3 + 25, y3[1])], width=10, fill="orange")
draw.text((x3, y3[0] - 50), "3", anchor="mm", font_size=70, fill="orange")

draw.line([(x4, y4[0]), (x4, y4[1])], width=10, fill="orange")
draw.line([(x4 - 25, y4[0]), (x4 + 25, y4[0])], width=10, fill="orange")
draw.line([(x4 - 25, y4[1]), (x4 + 25, y4[1])], width=10, fill="orange")
draw.text((x4, y4[0] - 50), "4", anchor="mm", font_size=70, fill="orange")

image.save(export_path)


distance_1 = (x1[1] - x1[0]) * conversion_factor
distance_2 = (x2[1] - x2[0]) * conversion_factor
distance_3 = (y3[1] - y3[0]) * conversion_factor
distance_4 = (y4[1] - y4[0]) * conversion_factor

c = 0.977
print(f"measured distance 1: {distance_1} \t converted distance 1: {distance_1 * c}")
print(f"measured distance 2: {distance_2} \t converted distance 2: {distance_2 * c}")
print(f"measured distance 3: {distance_3} \t converted distance 3: {distance_3 * c}")
print(f"measured distance 4: {distance_4} \t converted distance 4: {distance_4 * c}")
