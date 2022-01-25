"""
spectra.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def wavelength_to_wavenumber(wavelengths):
    """Converts wavelengths (nm) to wavenumbers (cm^{-1}).

    Args:
        wavelengths (numpy.array): Array of wavelengths, in nm.

    Returns:
        wavenumbers (numpy.array): Array of wavenumbers, in cm^{-1}.
    """
    wavenumbers = 1e7 / wavelengths
    return wavenumbers


def wavenumber_to_wavelength(wavenumbers):
    wavelengths = 1e7 / wavenumbers
    return wavelengths


def plot_spectra(
    path_csv,
    title,
    x_label,
    y_label,
    wavelength_convert=False,
    save_fig=False,
    path_save=None,
):
    """Plots spectra.

    Args:
        path_csv (pathlib.Path): Path to CSV file containing data.
        title (str): Plot title.
        x_label (str): Horizontal axis label for plot.
        y_label (str): Vertical axis label for plot.
        save_fig (bool, optional): Whether to save output figure. Defaults to False.
        path_save (str, optional): Path to save output figure. Defaults to None.
    """
    data = pd.read_csv(path_csv, header=None)
    x_data = data.iloc[:, 0]
    y_data = data.iloc[:, 1]

    if wavelength_convert:
        x_data = wavenumber_to_wavelength(x_data)

    plt.figure()
    plt.plot(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    if save_fig:
        plt.savefig(path_save)
        plt.close()
    else:
        plt.show()
