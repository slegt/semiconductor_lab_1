
from PIL import Image
import pathlib
import os

python_path = pathlib.Path(__file__).parent.resolve()
folder_path = python_path.parent / "data"
output_folder = python_path.parent / "plots"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(folder_path):
    if file_name.endswith('.bmp'):
        file_path = os.path.join(folder_path, file_name)
        img = Image.open(file_path)
        new_img = img.resize((512, 512))
        output_file_name = os.path.splitext(file_name)[0] + '.pdf'
        output_file_path = os.path.join(output_folder, output_file_name)
        new_img.save(output_file_path, 'pdf')