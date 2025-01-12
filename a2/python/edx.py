from PIL import Image, ImageSequence
import pathlib
import os


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


current_path = pathlib.Path(__file__).parent.resolve()
import_prefix = current_path.parent / "data"
export_prefix = current_path.parent / "plots"

import_path = str(import_prefix / "edx_10kV.tiff")
export_path = str(export_prefix / "edx_10kV.pdf")
tiff_to_pdf(import_path, export_path)

for i in [1, 2]:
    for j in [1, 2, 3]:
        import_path = import_prefix / f"edx_{i}0kV_{j}_spectrum.tiff"
        export_path = export_prefix / f"edx_{i}0kV_{j}_spectrum.pdf"
        tiff_to_pdf(str(import_path), str(export_path))

for i in ["", "_As", "_Ga", "_Si"]:
    import_path = import_prefix / f"map{i}.tiff"
    export_path = export_prefix / f"map{i}.pdf"
    tiff_to_pdf(str(import_path), str(export_path))
