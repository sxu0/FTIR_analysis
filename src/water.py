"""
water.py

Functions for analysing H2O absorption in FTIR spectra.

Author: Shiqi Xu
"""

from pathlib import Path
from typing import Tuple, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.optimize import curve_fit

import spectra


def crop_spectrum(x_lower_bound, x_upper_bound, x_data, y_data):
    start = 0
    while x_data[start] < x_lower_bound:
        start += 1
    end = start
    while x_data[end] < x_upper_bound:
        end += 1
    x_data_cropped = x_data[start:end]
    y_data_cropped = y_data[start:end]

    return x_data_cropped, y_data_cropped


def take_peaks(x_data, y_data):
    """Takes peaks in data (defined by change in slope from positive to negative).

    Args:
        x_data (np.ndarray[float]): Independent variable data.
        y_data (np.ndarray[float]): Dependent variable data.

    Returns:
        Tuple[np.ndarray[float], np.ndarray[float]]: Arrays containing x and y peaks.
    """
    ref_slope = (y_data[-1] - y_data[0]) / (x_data[-1] - x_data[0])
    x_peaks, y_peaks = [], []
    for i in range(1, len(x_data)):
        if np.abs((y_data[i] - y_data[i-1]) / (x_data[i] - x_data[i-1])) < 5 * np.abs(ref_slope):
            x_peaks.append(x_data[i])
            y_peaks.append(y_data[i])

    return x_peaks, y_peaks


def fit_bkgd(x_data, y_data, func, guess):
    fitted, err_cov = curve_fit(func, x_data, y_data, p0=guess)

    return fitted, err_cov


def absorption(x_data, y_data, fitted_params):
    y_fitted = parabola(x_data, fitted_params[0], fitted_params[1], fitted_params[2])
    y_diff = y_fitted - y_data
    x_int, y_int = [], []
    for i in range(len(x_data)):
        if y_diff[i] > 0:
            x_int.append(x_data[i])
            y_int.append(y_diff[i])
    # plt.figure()
    # plt.plot(x_int, y_int)
    # plt.show()
    absorbed_radiation = integrate.trapezoid(y_int, x_int)
    tot_radiation = integrate.trapezoid(y_fitted, x_data)
    absorp = absorbed_radiation / tot_radiation * 100

    return absorp


if __name__ == "__main__":

    data_path = Path.cwd() / "data" / "2022-02-15"
    data_files = []
    for csv_file in data_path.iterdir():
        if str(csv_file.name).split("_")[1] == "run02":
            data_files.append(csv_file)
    data_files.sort()

    def exponential(x, x0, y0, a, b):
        return a * np.exp((x - x0) / b) + y0

    def parabola(x, x0, y0, a):
        return a * (x - x0) ** 2 + y0

    output_path = Path.cwd() / "outputs" / "water"
    try:
        Path.mkdir(output_path)
    except:
        pass

    for i in range(len(data_files)):
    # for i in range(1):
        x_data, y_data = spectra.read_data(data_files[i])
        x_range = [1970, 2140]
        x_cropped, y_cropped = crop_spectrum(x_range[0], x_range[1], x_data, y_data)
        x_top, y_top = take_peaks(x_cropped, y_cropped)

        # exp_guess = [x_top[0], y_top[0] - 1, 1.33e-100, -1]
        # bkgd_params, fit_cov = fit_bkgd(x_top, y_top, exponential, exp_guess)
        para_guess = [2090, 8.57, 6.4e-7]
        bkgd_params, fit_cov = fit_bkgd(x_top, y_top, parabola, para_guess)

        xx_fit = np.linspace(x_range[0], x_range[1], (x_range[1] - x_range[0]) * 2)
        # yy_fit = exponential(
        #     xx_fit, bkgd_params[0], bkgd_params[1], bkgd_params[2], bkgd_params[3]
        # )
        yy_fit = parabola(xx_fit, bkgd_params[0], bkgd_params[1], bkgd_params[2])

        absorp = absorption(x_top, y_top, bkgd_params)
        # print("absorption: " + str(absorp) + "%")

        fig = plt.figure()
        plt.plot(x_cropped, y_cropped, 'x', label="data")
        plt.plot(x_top, y_top, '.', label="peaks")
        plt.plot(xx_fit, yy_fit, label="fit")
        plt.gca().invert_xaxis()
        plt.legend(loc="center left")
        plt.title("Background Fit for 2022-02-15_run02_" + str(data_files[i].name).split("_")[-1][:-4])
        plt.xlabel("Wavenumber (cm$^{-1}$)")
        plt.ylabel("Intensity (arbitrary units)")
        plt.text(200, 100, "absorption: " + str(round(absorp, 4)) + "%", ha='center', va='center', transform=None)

        # plt.show()
        fig_name_list = str(data_files[i].name).split("_")
        fig_name = fig_name_list[0] + "_" + fig_name_list[1] + "_" + fig_name_list[-1][:-4] + ".png"
        plt.savefig(output_path / fig_name)
