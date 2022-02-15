"""
snr.py

Plots the noise from spectra containing varying numbers of scan counts, averaged.
Signal is omitted as it remains constant throughout this dataset.

Standalone script.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

no_scans = [1, 2, 4, 8, 16, 32, 64]
no_scans_log2 = [0, 1, 2, 3, 4, 5, 6]
peak_to_peak_noise = [0.07548, 0.06194, 0.06584, 0.06507, 0.06308, 0.06230, 0.06341]
rms_noise = [0.01866, 0.01782, 0.01841, 0.01832, 0.01825, 0.01821, 0.01821]

df_noise = pd.DataFrame({"no_scans": no_scans, "peak_to_peak": peak_to_peak_noise, "rms": rms_noise})
df_noise.set_index("no_scans", inplace=True)
# print(df_noise)

path_save = Path.cwd() / "outputs" / "snr"
try:
    Path.mkdir(path_save)
except OSError:
    pass

plt.figure()
plt.plot(no_scans, peak_to_peak_noise, ".", label="peak to peak")
plt.title("Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
plt.xlabel("No. of Averaged Scans")
plt.ylabel("Peak-to-Peak Noise (arbitrary single beam units)")
fig_name = "p2p_noise_vs_scan_count.png"
plt.savefig(path_save / fig_name)

plt.figure()
plt.plot(no_scans, rms_noise, ".", label="RMS")
plt.title("RMS Noise in 2603-2398 cm$^{-1}$ Region")
plt.xlabel("No. of Averaged Scans")
plt.ylabel("RMS Noise (arbitrary single beam units)")
fig_name = "rms_noise_vs_scan_count.png"
plt.savefig(path_save / fig_name)

plt.figure()
plt.plot(no_scans_log2, peak_to_peak_noise, ".", label="peak to peak")
plt.title("Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
plt.xlabel("log$_2$(No. of Averaged Scans)")
plt.ylabel("Peak-to-Peak Noise (arbitrary single beam units)")
fig_name = "log_p2p_noise_vs_scan_count.png"
plt.savefig(path_save / fig_name)

plt.figure()
plt.plot(no_scans_log2, rms_noise, ".", label="RMS")
plt.title("RMS Noise in 2603-2398 cm$^{-1}$ Region")
plt.xlabel("log$_2$(No. of Averaged Scans)")
plt.ylabel("RMS Noise (arbitrary single beam units)")
fig_name = "log_rms_noise_vs_scan_count.png"
plt.savefig(path_save / fig_name)
