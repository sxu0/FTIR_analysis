"""
analysis.py

Analysis of FTIR spectra collected using Nicolet iS50.

Author: Shiqi Xu
"""

from pathlib import Path
import re

import numpy as np
import matplotlib.pyplot as plt

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

    figure_path = Path.cwd() / "outputs"
    try:
        Path.mkdir(figure_path / "bkgd_ratio")
    except OSError:
        pass
    try:
        Path.mkdir(figure_path / "co2_absorption")
    except OSError:
        pass

    sample_types = ["air", "argon"]
    for i in range(len(single_beam_bkgd_files)):
        bkgd = single_beam_bkgd_files[i]
        list_wavenumbers, list_transmission = [], []
        pressure_labels = []
        for j in range(len(single_beam_sample_files[i])):
            sample = single_beam_sample_files[i][j]
            wavenumbers, transmission = spectra.background_ratio(bkgd, sample)
            list_wavenumbers.append(wavenumbers)
            list_transmission.append(transmission)
            pressure_labels.append(str(sample).split("_")[5])
            spectra.plot_spectrum(
                wavenumbers,
                transmission,
                str(sample.name)[17:-13],
                "Wavenumber (cm$^{-1}$)",
                "% Transmission",
                y_lim=(0, 100),
                save_fig=True,
                path_save=figure_path
                / "bkgd_ratio"
                / (str(sample.name)[17:-13] + ".png"),
            )
        spectra.overlay_spectra(
            list_wavenumbers,
            list_transmission,
            sample_types[i],
            "Wavenumber (cm$^{-1}$)",
            "% Transmission",
            pressure_labels,
            y_lim=(0, 100),
            save_fig=True,
            path_save=figure_path
            / "bkgd_ratio"
            / (sample_types[i] + "_by_pressure.png"),
        )

        ## CO2 absorption peak: 2200-2500 cm^{-1}
        list_cropped_wavenumbers, list_cropped_transmission = [], []
        for j in range(len(list_wavenumbers)):
            start = 0
            while list_wavenumbers[j][start] < 2200:
                start += 1
            end = start
            while list_wavenumbers[j][end] < 2500:
                end += 1
            list_cropped_wavenumbers.append(list_wavenumbers[j][start:end])
            list_cropped_transmission.append(list_transmission[j][start:end])
        spectra.overlay_spectra(
            list_cropped_wavenumbers,
            list_cropped_transmission,
            "CO$_2$ peak observed in " + sample_types[i] + " sample",
            "Wavenumber (cm$^{-1}$)",
            "% Transmission",
            pressure_labels,
            y_lim=(0, 100),
            save_fig=True,
            path_save=figure_path
            / "co2_absorption"
            / ("co2_peak_" + sample_types[i] + "_by_pressure.png"),
        )

        ## integrating to get total transmission over 2280-2390 cm^{-1}
        list_pressures, list_co2_transmission = [], []
        for j in range(len(list_cropped_wavenumbers)):
            co2_transmission = spectra.tot_transmission(
                list_cropped_wavenumbers[j], list_cropped_transmission[j], 2280, 2390
            )
            list_co2_transmission.append(co2_transmission)
            list_pressures.append(int(pressure_labels[j][:-3]))
        plt.figure()
        plt.plot(list_pressures, list_co2_transmission, "x")
        plt.title(
            "% transmission over CO$_2$ peak in " + sample_types[i] + ", by pressure"
        )
        plt.xlabel("Pressure (kPa)")
        plt.ylabel("% Transmission")
        plt.savefig(
            figure_path
            / "co2_absorption"
            / ("transmission_co2_peak_" + sample_types[i] + "_by_pressure.png")
        )
        plt.close()

    ## exploring difference resolutions
    res_filenames = [
        "2022-01-21_run05_1.0res_argon_0kPa_sample.CSV",
        "2022-01-21_run03_4.0res_argon_0kPa_sample.CSV",
        "2022-01-21_run04_16.0res_argon_0kPa_sample.CSV",
    ]
    res_data_paths = [
        Path.cwd() / "data" / "2022-01-21" / res_filenames[i]
        for i in range(len(res_filenames))
    ]
    list_argon_wavenumbers, list_argon_intensities = [], []
    for i in range(len(res_data_paths)):
        argon_wavenumbers, argon_intensities = spectra.read_data(res_data_paths[i])
        list_argon_wavenumbers.append(argon_wavenumbers)
        list_argon_intensities.append(argon_intensities)
    try:
        Path.mkdir(figure_path / "resolution")
    except OSError:
        pass
    # spectra.overlay_spectra(
    #     list_argon_wavenumbers,
    #     list_argon_intensities,
    #     "Argon at 0 kPa, at different resolutions",
    #     "Wavenumber (cm$^{-1}$)",
    #     "Single-Beam Intensity (arbitrary units)",
    #     ["1.0 resolution", "4.0 resolution", "16.0 resolution"],
    #     save_fig=True,
    #     path_save=figure_path / "resolution" / "argon_0kPa_by_resolution.png",
    # )
