import numpy as np
import matplotlib.pyplot as plt
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()

plt.rcParams['text.usetex'] = True
font = {
    "size": 10,
    "family": "serif",
}
plt.rc("font", **font)
width = 300 # pt
height = 80 # pt


time = np.linspace(0, 100, 1000)
offset = np.array(1000 * [9])
data = 0.5 * np.sin(time)


fig, ax = plt.subplots(figsize=(width/72, height/72))
ax.plot(time, data, label=r"$v_{\mathrm{gs}}$", lw=1)
ax.plot(time, data + offset, label=r"$v_{\mathrm{GS}}$", lw=1)
ax.plot(time, offset, label=r"$V_{\mathrm{GS}}$", lw=1)
ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
ax.set_xlim(0, 100)
ax.set_ylim(-1, 11)
ax.spines['top'].set_visible(False)   
ax.spines['right'].set_visible(False) 
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_linewidth(1)
ax.spines['bottom'].set_linewidth(1)
ax.tick_params(axis='both', which='major', width=1, length=3)
ax.set_yticks([0, 2, 4, 6, 8, 10])
ax.set_xticks([])
ax.set_xlabel("time", labelpad=10)
ax.set_ylabel("voltage") 
plt.subplots_adjust(right=0.6, left=0.2, top=1, bottom=0.18)
fig.savefig( file_path / "../plots/notational_convention.pdf")