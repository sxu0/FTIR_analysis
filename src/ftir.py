"""
ftir.py

Analyzes spectra and interferograms.

Author: Shiqi Xu
"""

from pathlib import Path

import numpy as np

import spectra


if __name__ == "__main__":

    data_path = Path.cwd() / "data"
    data_files = []
    for csv_file in data_path.iterdir():
        data_files.append(csv_file)
    data_files.sort()
    # for i in range(len(data_files)):
    #     print(data_files[i])

    # in wavenumber
    figure_path = (
        Path.cwd() / "outputs" / (str(data_files[0].name)[11:-8] + "wavenumber.png")
    )
    spectra.plot_spectra(
        data_files[0],
        "Background measurement: -95 kPa, 4.0 resolution",
        "Wavenumber (cm$^{-1}$)",
        "TO CHECK",
        save_fig=True,
        path_save=figure_path,
    )  # TODO
    # in wavelength
    figure_path = (
        Path.cwd() / "outputs" / (str(data_files[0].name)[11:-8] + "wavelength.png")
    )
    spectra.plot_spectra(
        data_files[0],
        "Background measurement: -95 kPa, 4.0 resolution",
        "Wavelength (nm)",
        "TO CHECK",
        wavelength_convert=True,
        save_fig=True,
        path_save=figure_path,
    )  # TODO
