"""
spectra.py

Functions for manipulating and analysing FTIR spectra.

Author: Shiqi Xu
"""

from pathlib import Path
from typing import Tuple, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate


def wavelength_to_wavenumber(wavelengths):
    """Converts wavelengths (nm) to wavenumbers (cm^{-1}).

    Args:
        wavelengths (np.ndarray[float]): Array of wavelengths, in nm.

    Returns:
        wavenumbers (np.ndarray[float]): Array of wavenumbers, in cm^{-1}.
    """
    wavenumbers = 1e7 / wavelengths
    return wavenumbers


def wavenumber_to_wavelength(wavenumbers):
    """Converts wavenumbers (cm^{-1}) to wavelengths (nm).

    Args:
        wavenumbers (np.ndarray[float]): Array of wavenumbers, in cm^{-1}.

    Returns:
        wavelengths (np.ndarray[float]): Array of wavelengths, in nm.
    """
    wavelengths = 1e7 / wavenumbers
    return wavelengths


def read_data(path_csv):
    """Reads CSV file containing data.

    Args:
        path_csv (pathlib.Path): Path to CSV file containing data.

    Returns:
        x_data (np.ndarray[float]): Array containing independent variable data.
        y_data (np.ndarray[float]): Array containing dependent variable data.
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
    x_inv=False,
    y_lim=None,
    wavelength_convert=False,
    save_fig=False,
    path_save=None,
    hold_on=False,
):
    """Plots the input spectrum.

    Args:
        wavenumber_data (np.ndarray[float]): Array containing wavenumber data.
        y_data (np.ndarray[float]): Array containing dependent variable data.
        title (str): Plot title.
        x_label (str): Plot horizontal axis label.
        y_label (str): Plot vertical axis label.
        x_inv (bool, optional): Whether to invert the x-axis such that x-values
            decrease towards the right.
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

    plt.plot(wavenumber_data, y_data, linewidth=0.75)

    if x_inv:
        plt.gca().invert_xaxis()

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
    x_inv=False,
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
        x_inv (bool, optional): Whether to invert the x-axis such that x-values
            decrease towards the right.
        y_lim (Tuple(float, float), optional): Tuple containing min and max of
            vertical axis in plot window. Defaults to None.
        wavelength_convert (bool, optional): Whether to convert wavenumber to
            wavelength units. Defaults to False.
        save_fig (bool, optional): Whether to save output figure. Defaults to False.
        path_save (str, optional): Path to save output figure. Defaults to None.
    """
    plt.figure()
    for i in range(len(list_wavenumber_data)):
        plot_spectrum(
            list_wavenumber_data[i],
            list_y_data[i],
            title,
            x_label,
            y_label,
            y_lim=y_lim,
            wavelength_convert=wavelength_convert,
            hold_on=True,
        )
    plt.legend(plot_labels, loc="upper right")

    if x_inv:
        plt.gca().invert_xaxis()

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
        wavenumbers (np.ndarray[float]): Array containing wavenumber data.
        transmission (np.ndarray[float]): Array containing % transmission data.
    """
    bkgd_data = pd.read_csv(bkgd_path_csv, header=None)
    bkgd_data.set_index(0, inplace=True)
    bkgd_data.columns = ["background"]

    sample_data = pd.read_csv(sample_path_csv, header=None)
    sample_data.set_index(0, inplace=True)
    sample_data.columns = ["sample"]

    joined_data = bkgd_data.join(sample_data, how="inner")
    joined_data["transmission"] = (
        joined_data.loc[:, "sample"] / joined_data.loc[:, "background"] * 100
    )

    wavenumbers = joined_data.index.to_numpy()
    transmission = joined_data.loc[:, "transmission"].to_numpy()

    return wavenumbers, transmission


def tot_transmission(
    wavenumber_data, transmission_data, min_wavenumber, max_wavenumber
):
    """Integrates to find total transmission over indicated spectral window.

    Args:
        wavenumber_data (np.ndarray[float]): Array containing wavenumber data.
        transmission_data (np.ndarray[float]): Array containing % transmission data.
        min_wavenumber (float): Lower wavenumber in spectral window.
        max_wavenumber (float): Upper wavenumber in spectral window.

    Returns:
        total_transmission (float): Total % transmission (normalized) over
            spectral window.
    """
    start = 0
    while wavenumber_data[start] < min_wavenumber:
        start += 1
    end = start
    while wavenumber_data[end] < max_wavenumber:
        end += 1
    wavenumber_cropped = wavenumber_data[start:end]
    transmission_cropped = transmission_data[start:end]
    total_transmission = integrate.trapz(transmission_cropped, wavenumber_cropped) / (
        max_wavenumber - min_wavenumber
    )

    return total_transmission


def fourier_transform(
    ifg_x: np.ndarray,
    ifg_y: np.ndarray,
    wavenumber_res: float,
    ref_spectrum_x: np.ndarray = None,
    ref_spectrum_y: np.ndarray = None,
    plot: bool = False,
    save_fig: bool = False,
    path_save: Union[str, Path] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
    """Performs the Fourier transform on an input interferogram to output a
    single-beam spectrum. Optionally generates a plot of the single-beam spectrum.

    Args:
        ifg_x (np.ndarray[float]): Interferogram independent variable data, in units of
            "data points" (i.e. time-domain spacing to be deduced).
        ifg_y (np.ndarray[float]): Interferogram intensity data, in units of Volts.
        ref_spectrum_x (np.ndarray[float]): Wavenumber data of reference single-beam
            spectrum, in cm^{-1}.
        ref_spectrum_y (np.ndarray[float]): Intensity data of reference single-beam
            spectrum, in arbitrary units.
        plot (bool, optional): Whether to generate a plot. Defaults to False.
        save_fig (bool, optional): Whether to save output figure. Defaults to False.
        path_save (str, optional): Path to save output figure. Defaults to None.

    Returns:
        Tuple[np.ndarray[float], np.ndarray[float]]: Arrays containing wavenumber data
            in cm^{-1}, and single-beam intensity data, in arbitrary units.
    """
    spectrum_y = np.fft.hfft(ifg_y)[:len(ifg_y)]
    spectrum_x = np.fft.fftfreq(len(ifg_x), 1/wavenumber_res/len(ifg_x))

    start = 0
    while spectrum_x[start] < 400:
        start += 1
    end = start
    while spectrum_x[end] < 4000:
        end += 1
    spectrum_x_cropped = spectrum_x[start:end]
    spectrum_y_cropped = spectrum_y[start:end]

    ## fold negative-intensity component over the x-axis
    spectrum_x_filtered = spectrum_x_cropped
    spectrum_y_filtered = np.abs(spectrum_y_cropped)

    ## take upper envelope
    spectrum_x_envelope, spectrum_y_envelope = [], []
    x_peaks, y_peaks = [], []
    x_troughs, y_troughs = [], []
    for i in range(1, len(spectrum_x_filtered)-1):
        if (spectrum_y_filtered[i] - spectrum_y_filtered[i-1] > 0) and (spectrum_y_filtered[i] - spectrum_y_filtered[i+1] < 0):
            x_peaks.append(spectrum_x_filtered[i])
            y_peaks.append(spectrum_y_filtered[i])
        if (spectrum_y_filtered[i] - spectrum_y_filtered[i-1] < 0) and (spectrum_y_filtered[i] - spectrum_y_filtered[i+1] > 0):
            x_troughs.append(spectrum_x_filtered[i])
            y_troughs.append(spectrum_y_filtered[i])
    y_troughs_interp = np.interp(x_peaks, x_troughs, y_troughs)
    for i in range(len(x_peaks)):
        spectrum_y_envelope.append(max(y_peaks[i], y_troughs_interp[i]))
    spectrum_y_envelope = np.array(spectrum_y_envelope)
    spectrum_x_envelope = np.array(x_peaks)

    if plot:
        if (ref_spectrum_x is not None) and (ref_spectrum_y is not None):
            overlay_spectra(
                [ref_spectrum_x, spectrum_x_envelope],
                [ref_spectrum_y, spectrum_y_envelope],
                "Single-Beam Spectrum, FFT'd from Interferogram",
                "Wavenumber (cm$^{-1}$)",
                "Single-Beam Intensity (arbitrary units)",
                ["reference", "from FFT"],
                x_inv=True,
                save_fig=save_fig,
                path_save=path_save,
            )
        else:
            plot_spectrum(
                spectrum_x_envelope,
                spectrum_y_envelope,
                "Single-Beam Spectrum, FFT'd from Interferogram",
                "Wavenumber (cm$^{-1}$)",
                "Single-Beam Intensity (arbitrary units)",
                x_inv=True,
                save_fig=save_fig,
                path_save=path_save,
            )

    return spectrum_x_filtered, spectrum_y_filtered
