import matplotlib.pyplot as plt
from .measurement import X


plt.plot(data["x"], data["data"])
omega_scan: XRDMeasurements = XRDMLParser.parse_file(
    "/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task1_omega_scan_024_al2o3peak_1deg_.005ss_phi=0.xrdml"
)
print(omega_scan)