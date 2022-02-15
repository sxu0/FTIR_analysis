"""
fourier.py

Fourier transforms and inverse Fourier transforms of FTIR interferograms/spectra.
"""

from pathlib import Path

import spectra

if __name__ == "__main__":

    ifg_path = (
        Path.cwd()
        / "data"
        / "2022-01-25"
        / "2022-01-25_run00_2.0res_evac_-93kPa_sample_ifg.CSV"
    )
    data_points, voltage = spectra.read_data(ifg_path)
    spectra.fourier_transform(data_points, voltage)
