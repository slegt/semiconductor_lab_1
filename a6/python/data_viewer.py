from pathlib import Path

from config import SINGLE_COLUMN
from matplotlib import pyplot as plt
from parser import XRDMLParser

plt.rcParams.update(SINGLE_COLUMN)

file_path = Path(__file__).resolve()
destination = file_path.parent.parent / "plots"

# import files
filepath = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/task3_036_2theta_omega.xrdml"
session = XRDMLParser.parse_file(filepath)

data = session.measurement.scan.get_plot_data()
two_theta = data["2theta"] - 0.0088
omega = data["omega"] - session.measurement.sample_offset[1].value
intensity = data["intensity"]

plt.scatter(two_theta, intensity)
plt.yscale("log")
plt.show()