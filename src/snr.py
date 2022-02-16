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

## data
no_scans = np.array([1, 2, 4, 8, 16, 32, 64])
no_scans_log2 = np.log2(no_scans)
no_scans_sqrt = np.sqrt(no_scans)
p2p_noise = np.array([0.07548, 0.06194, 0.06584, 0.06507, 0.06308, 0.06230, 0.06341])
rms_noise = np.array([0.01866, 0.01782, 0.01841, 0.01832, 0.01825, 0.01821, 0.01821])

df_noise = pd.DataFrame({"no_scans": no_scans, "peak_to_peak": p2p_noise, "rms": rms_noise})
df_noise.set_index("no_scans", inplace=True)
# print(df_noise)

## output directory
path_save = Path.cwd() / "outputs" / "snr"
try:
    Path.mkdir(path_save)
except OSError:
    pass

def plot_p2p(save_fig=False):

    plt.figure()
    plt.plot(no_scans, p2p_noise, ".", label="peak to peak")
    plt.title("Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("No. of Averaged Scans")
    plt.ylabel("Peak-to-Peak Noise (arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "p2p_noise_vs_scan_count.png")
        plt.close()

    plt.figure()
    plt.plot(no_scans_log2, p2p_noise, ".", label="peak to peak")
    plt.title("Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("log$_2$(No. of Averaged Scans)")
    plt.ylabel("Peak-to-Peak Noise (arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "p2p_noise_vs_log_scan_count.png")
        plt.close()

    ## recall that SNR goes up as sqrt(N), N being scan count
    plt.figure()
    plt.plot(no_scans_sqrt, p2p_noise, ".", label="peak to peak")
    plt.title("Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("sqrt(No. of Averaged Scans)")
    plt.ylabel("Peak-to-Peak Noise (arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "p2p_noise_vs_sqrt_scan_count.png")
        plt.close()

    if not save_fig:
        plt.show()

    return

def plot_rms(save_fig=False):

    plt.figure()
    plt.plot(no_scans, rms_noise, ".", label="RMS")
    plt.title("RMS Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("No. of Averaged Scans")
    plt.ylabel("RMS Noise (arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "rms_noise_vs_scan_count.png")
        plt.close()

    plt.figure()
    plt.plot(no_scans_log2, rms_noise, ".", label="RMS")
    plt.title("RMS Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("log$_2$(No. of Averaged Scans)")
    plt.ylabel("RMS Noise (arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "rms_noise_vs_log_scan_count.png")
        plt.close()

    ## recall that SNR goes up as sqrt(N), N being scan count
    plt.figure()
    plt.plot(no_scans_sqrt, rms_noise, ".", label="RMS")
    plt.title("RMS Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("sqrt(No. of Averaged Scans)")
    plt.ylabel("RMS Noise (arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "rms_noise_vs_sqrt_scan_count.png")
        plt.close()

    if not save_fig:
        plt.show()

    return

def plot_inv_p2p(save_fig=False):

    plt.figure()
    plt.plot(no_scans, 1/p2p_noise, ".", label="peak to peak")
    plt.title("1/Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("No. of Averaged Scans")
    plt.ylabel("1/Peak-to-Peak Noise (1/arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "inv_p2p_noise_vs_scan_count.png")
        plt.close()

    plt.figure()
    plt.plot(no_scans_log2, 1/p2p_noise, ".", label="peak to peak")
    plt.title("1/Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("log$_2$(No. of Averaged Scans)")
    plt.ylabel("1/Peak-to-Peak Noise (1/arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "inv_p2p_noise_vs_log_scan_count.png")
        plt.close()

    ## recall that SNR goes up as sqrt(N), N being scan count
    plt.figure()
    plt.plot(no_scans_sqrt, 1/p2p_noise, ".", label="peak to peak")
    plt.title("1/Peak-to-Peak Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("sqrt(No. of Averaged Scans)")
    plt.ylabel("1/Peak-to-Peak Noise (1/arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "inv_p2p_noise_vs_sqrt_scan_count.png")
        plt.close()

    if not save_fig:
        plt.show()

    return

def plot_inv_rms(save_fig=False):

    plt.figure()
    plt.plot(no_scans, 1/rms_noise, ".", label="RMS")
    plt.title("1/RMS Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("No. of Averaged Scans")
    plt.ylabel("1/RMS Noise (1/arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "inv_rms_noise_vs_scan_count.png")
        plt.close()

    plt.figure()
    plt.plot(no_scans_log2, 1/rms_noise, ".", label="RMS")
    plt.title("1/RMS Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("log$_2$(No. of Averaged Scans)")
    plt.ylabel("1/RMS Noise (1/arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "inv_rms_noise_vs_log_scan_count.png")
        plt.close()

    ## recall that SNR goes up as sqrt(N), N being scan count
    plt.figure()
    plt.plot(no_scans_sqrt, 1/rms_noise, ".", label="RMS")
    plt.title("1/RMS Noise in 2603-2398 cm$^{-1}$ Region")
    plt.xlabel("sqrt(No. of Averaged Scans)")
    plt.ylabel("1/RMS Noise (1/arbitrary single beam units)")
    if save_fig:
        plt.savefig(path_save / "inv_rms_noise_vs_sqrt_scan_count.png")
        plt.close()

    if not save_fig:
        plt.show()

    return

if __name__ == "__main__":

    plot_inv_p2p(save_fig=True)

    plot_inv_rms(save_fig=True)
