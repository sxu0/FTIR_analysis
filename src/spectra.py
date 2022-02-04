"""
spectra.py

Functions for manipulating and analysing FTIR spectra.

Author: Shiqi Xu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def wavelength_to_wavenumber(wavelengths):
    """Converts wavelengths (nm) to wavenumbers (cm^{-1}).

    Args:
        wavelengths (numpy.array[float]): Array of wavelengths, in nm.

    Returns:
        wavenumbers (numpy.array[float]): Array of wavenumbers, in cm^{-1}.
    """
    wavenumbers = 1e7 / wavelengths
    return wavenumbers


def wavenumber_to_wavelength(wavenumbers):
    """Converts wavenumbers (cm^{-1}) to wavelengths (nm).

    Args:
        wavenumbers (numpy.array[float]): Array of wavenumbers, in cm^{-1}.

    Returns:
        wavelengths (numpy.array[float]): Array of wavelengths, in nm.
    """
    wavelengths = 1e7 / wavenumbers
    return wavelengths


def read_data(path_csv):
    """Reads CSV file containing data.

    Args:
        path_csv (pathlib.Path): Path to CSV file containing data.

    Returns:
        x_data (numpy.array[float]): Array containing independent variable data.
        y_data (numpy.array[float]): Array containing dependent variable data.
    """
    data = pd.read_csv(path_csv, header=None)
    x_data = data.iloc[:, 0].to_numpy()
    y_data = data.iloc[:, 1].to_numpy()

    return x_data, y_data


def plot_spectrum(
    wavenumber_data,
    y_data,
    title,
    x_label,
    y_label,
    y_lim=None,
    wavelength_convert=False,
    save_fig=False,
    path_save=None,
    hold_on=False,
):
    """Plots the input spectrum.

    Args:
        wavenumber_data (numpy.array[float]): Array containing wavenumber data.
        y_data (numpy.array[float]): Array containing dependent variable data.
        title (str): Plot title.
        x_label (str): Plot horizontal axis label.
        y_label (str): Plot vertical axis label.
        y_lim (Tuple(float, float), optional): Tuple containing min and max of
            vertical axis in plot window. Defaults to None.
        wavelength_convert (bool, optional): Whether to convert wavenumber to
            wavelength units. Defaults to False.
        save_fig (bool, optional): Whether to save output figure. Defaults to
            False.
        path_save (str, optional): Path to save output figure. Defaults to None.
    """
    if wavelength_convert:
        wavenumber_data = wavenumber_to_wavelength(wavenumber_data)

    # plt.figure()
    plt.plot(wavenumber_data, y_data)
    if y_lim is not None:
        plt.ylim(y_lim)

    if not hold_on:
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

        if save_fig:
            plt.savefig(path_save)
            plt.close()
        else:
            plt.show()


def overlay_spectra(
    list_wavenumber_data,
    list_y_data,
    title,
    x_label,
    y_label,
    plot_labels,
    y_lim=None,
    wavelength_convert=False,
    save_fig=False,
    path_save=None,
):
    """Plots multiple spectra on the same axes.

    Args:
        list_wavenumber_data (List[List[float]]): List of wavenumber arrays.
        list_y_data (List[List[float]]): List of arrays of dependent variable data.
            Same length as list_wavenumber_data.
        title (str): Plot title.
        x_label (str): Plot horizontal axis label.
        y_label (str): Plot vertical axis label.
        plot_labels (List[str]): Legend for plot. Array-like object containing
            descriptor of each spectrum.
        y_lim (Tuple(float, float), optional): Tuple containing min and max of
            vertical axis in plot window. Defaults to None.
        wavelength_convert (bool, optional): Whether to convert wavenumber to
            wavelength units. Defaults to False.
        save_fig (bool, optional): Whether to save output figure. Defaults to False.
        path_save (str, optional): Path to save output figure. Defaults to None.
    """
    plt.figure()
    for i in range(len(list_wavenumber_data)):
        if wavelength_convert:
            plot_spectrum(
                list_wavenumber_data[i],
                list_y_data[i],
                title,
                x_label,
                y_label,
                y_lim=y_lim,
                wavelength_convert=True,
                hold_on=True,
            )
        else:
            plot_spectrum(
                list_wavenumber_data[i],
                list_y_data[i],
                title,
                x_label,
                y_label,
                y_lim=y_lim,
                hold_on=True,
            )
    plt.legend(plot_labels)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    if save_fig:
        plt.savefig(path_save)
        plt.close()
    else:
        plt.show()


def background_ratio(
    bkgd_path_csv,
    sample_path_csv,
):
    """Ratios single-beam sample data against background to calculate % transmission.

    Args:
        bkgd_path_csv (pathlib.Path): Path to CSV file containing background data.
        sample_path_csv (pathlib.Path): Path to CSV file containing sample data.

    Returns:
        wavenumbers (numpy.array[float]): Array containing wavenumber data.
        transmission (numpy.array[float]): Array containing % transmission data.
    """
    bkgd_data = pd.read_csv(bkgd_path_csv, header=None)
    bkgd_data.set_index(0, inplace=True)
    bkgd_data.columns = ["background"]

    sample_data = pd.read_csv(sample_path_csv, header=None)
    sample_data.set_index(0, inplace=True)
    sample_data.columns = ["sample"]

    joined_data = bkgd_data.join(sample_data, how="inner")
    joined_data["transmission"] = (
        joined_data.loc[:, "sample"] / joined_data.loc[:, "background"]
    )

    wavenumbers = joined_data.index.to_numpy()
    transmission = joined_data.loc[:, "transmission"].to_numpy()

    return wavenumbers, transmission


# def fourier_transform(ifg_x, ifg_y):
#     spectrum_y = np.fft.fft(ifg_y)


#     plt.figure()
#     plt.plot()

#     plt.figure()
