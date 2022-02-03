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

    figure_path = Path.cwd() / "outputs" / "2021-01-21"
    try:
        Path.mkdir(figure_path)
    except OSError:
        pass

    # in wavenumber
    spectra.plot_spectrum(
        bkgd_wavenumbers,
        bkgd_intensity,
        "Background measurement: -95 kPa, 4.0 resolution",
        "Wavenumber (cm$^{-1}$)",
        "Intensity (arbitrary units)",
        save_fig=False,
        path_save=figure_path / (str(data_files[0].name)[:-8] + "wavenumber.png"),
    )

    # in wavelength
    spectra.plot_spectrum(
        bkgd_wavenumbers,
        bkgd_intensity,
        "Background measurement: -95 kPa, 4.0 resolution",
        "Wavelength (nm)",
        "Intensity (arbitrary units)",
        wavelength_convert=True,
        save_fig=False,
        path_save=figure_path / (str(data_files[0].name)[:-8] + "wavelength.png"),
    )
