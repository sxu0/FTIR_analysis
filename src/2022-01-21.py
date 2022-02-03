"""
2022-01-21.py

Pokes around at prelim spectra collected on 2022-01-21.

Author: Shiqi Xu
"""

from pathlib import Path

import numpy as np

import spectra


if __name__ == "__main__":

    data_path = Path.cwd() / "data" / "2022-01-21"
    data_files = []
    for csv_file in data_path.iterdir():
        data_files.append(csv_file)
    data_files.sort()
    # for i in range(len(data_files)):
    #     print(data_files[i])

    bkgd_wavenumbers, bkgd_intensity = spectra.read_data(data_files[0])

    # in wavenumber
    figure_path = (
        Path.cwd() / "outputs" / (str(data_files[0].name)[:-8] + "wavenumber.png")
    )
    spectra.plot_spectrum(
        bkgd_wavenumbers,
        bkgd_intensity,
        "Background measurement: -95 kPa, 4.0 resolution",
        "Wavenumber (cm$^{-1}$)",
        "TO CHECK",
        save_fig=False,
        path_save=figure_path,
    )  # TODO

    # in wavelength
    figure_path = (
        Path.cwd() / "outputs" / (str(data_files[0].name)[:-8] + "wavelength.png")
    )
    spectra.plot_spectrum(
        bkgd_wavenumbers,
        bkgd_intensity,
        "Background measurement: -95 kPa, 4.0 resolution",
        "Wavelength (nm)",
        "TO CHECK",
        wavelength_convert=True,
        save_fig=False,
        path_save=figure_path,
    )  # TODO
