"""
analysis.py

Analysis of FTIR spectra collected using Nicolet iS50.

Author: Shiqi Xu
"""

from pathlib import Path

import numpy as np

import spectra

if __name__ == "__main__":

    data_path = Path.cwd() / "data" / "2022-01-25"
    data_files = []
    for csv_file in data_path.iterdir():
        data_files.append(csv_file)
    data_path = Path.cwd() / "data" / "2022-01-28"
    for csv_file in data_path.iterdir():
        data_files.append(csv_file)
    data_files.sort()
    # for i in range(len(data_files)):
    #     print(data_files[i])

    single_beam_bkgd_files = []
    single_beam_sample_files = [[], []]
    for i in range(len(data_files)):
        if str(data_files[i])[-12:-4] == "spectrum":
            if "evac" in str(data_files[i]):
                single_beam_bkgd_files.append(data_files[i])
            elif "air" in str(data_files[i]):
                single_beam_sample_files[0].append(data_files[i])
            elif "argon" in str(data_files[i]):
                single_beam_sample_files[1].append(data_files[i])
            else:
                print("warning: file missed:", str(data_files[i]))
    # print("\n\nbackground spectra:\n")
    # for file in single_beam_bkgd_files:
    #     print(file)
    # print("\n\nsample spectra:\n")
    # for sample in single_beam_sample_files:
    #     for file in sample:
    #         print(file)

    figure_path = Path.cwd() / "outputs" / "bkgd_ratio"
    try:
        Path.mkdir(figure_path)
    except OSError:
        pass

    overlay_plot_titles = ["air", "argon"]
    for i in range(len(single_beam_bkgd_files)):
        bkgd = single_beam_bkgd_files[i]
        list_wavenumbers, list_transmission = [], []
        overlay_plot_labels = []
        for j in range(len(single_beam_sample_files[i])):
            sample = single_beam_sample_files[i][j]
            wavenumbers, transmission = spectra.background_ratio(bkgd, sample)
            list_wavenumbers.append(wavenumbers)
            list_transmission.append(transmission)
            overlay_plot_labels.append(str(sample).split("_")[5])
            spectra.plot_spectrum(
                wavenumbers,
                transmission,
                str(sample.name)[17:-13],
                "Wavenumber (cm$^{-1}$)",
                "% Transmission",
                y_lim=(0, 1),
                save_fig=True,
                path_save=figure_path / (str(sample.name)[17:-12] + ".png"),
            )
        spectra.overlay_spectra(
            list_wavenumbers,
            list_transmission,
            overlay_plot_titles[i],
            "Wavenumber (cm$^{-1}$)",
            "% Transmission",
            overlay_plot_labels,
            y_lim=(0, 1),
            save_fig=True,
            path_save=figure_path / (overlay_plot_titles[i] + "_by_pressure.png"),
        )