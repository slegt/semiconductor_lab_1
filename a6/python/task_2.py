import numpy as np
from matplotlib import pyplot as plt
from parser import XRDMLParser
from scipy.signal import find_peaks, peak_widths
from exporter import update_json_file

# serialize data
filepath006 = "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task2_006_rockingcurve1.xrdml"
session = XRDMLParser.parse_file(filepath006)
offset_2theta = 0.0088
delta_theta = 0.0001

# extract relevant data
data = session.measurement.scan.get_plot_data() 
theta = session.measurement.scan.get_position("2Theta")
wavelength = session.measurement.used_wavelength.k_alpha_1.value * 1e-10
omega = data["omega"]
intensity = data["intensity"]

# find peaks
peaks, _ = find_peaks(intensity, height=1e4)
results_half = peak_widths(intensity, peaks, rel_height=0.5)
widths, width_heights, left_ips, right_ips = results_half

delta_omega = omega[1] - omega[0]
omega_width = delta_omega * widths[0]

hw_omega = [left_ips[0] * delta_omega+ omega[0], right_ips[0] * delta_omega + omega[0]]
hw_intensity = [width_heights[0], width_heights[0]]

# calculate quantities
L = 0.9 * wavelength / (omega_width * np.sin(np.deg2rad(theta)))

sq_term1 = (delta_omega / omega_width)**2
sq_term2 = (delta_theta / np.tan(theta))**2
delta_L = L * np.sqrt(sq_term1 + sq_term2)

# export quantities
exportable_data = {
    "delta_omega": f"{delta_omega:.2}",
    "omega_width": f"{omega_width:.2f}",
    "coherence_length": f"{L:.2e}",
    "coherence_length_delta": f"{delta_L:.2e}"
}
update_json_file(data_dict=exportable_data, key="task_2")

# plot peak
plt.plot(omega, intensity)
plt.scatter(omega[peaks], intensity[peaks], color="orange", zorder=10)
plt.scatter(hw_omega, hw_intensity, color="red", zorder=10)
plt.hlines(y=width_heights[0], xmin=hw_omega[0], xmax=hw_omega[1], color="red")
plt.text(
    x=0.7,
    y=0.5,
    s=f"$\Delta\Omega={exportable_data['width']} \degree$",
    transform=plt.gca().transAxes,
    horizontalalignment="center",
    verticalalignment="center",
)

plt.xlim(20.7, 21.1)
plt.yscale("log")
plt.legend()
plt.show()
