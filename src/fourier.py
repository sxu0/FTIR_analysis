"""
fourier.py

Fourier transforms and inverse Fourier transforms of FTIR interferograms/spectra.
"""

from pathlib import Path

import spectra

if __name__ == "__main__":

    sample_ifgs_220125 = [
        "2022-01-25_run00_2.0res_evac_-93kPa_sample_ifg.CSV",
        "2022-01-25_run01_2.0res_air_-80kPa_sample_ifg_wavy.CSV",
        "2022-01-25_run02_2.0res_air_-80kPa_sample_ifg.CSV",
        "2022-01-25_run04_2.0res_air_-70kPa_sample_ifg.CSV",
        "2022-01-25_run05_2.0res_air_-59kPa_sample_ifg.CSV",
        "2022-01-25_run06_2.0res_air_-50kPa_sample_ifg.CSV",
        "2022-01-25_run07_2.0res_air_-40kPa_sample_ifg.CSV"
        ]

    output_path = Path.cwd() / "outputs" / "fourier_transform"
    try:
        Path.mkdir(output_path)
    except OSError:
        pass

    for i in range(len(sample_ifgs_220125)):
        ifg_path = (
            Path.cwd()
            / "data"
            / "2022-01-25"
            / sample_ifgs_220125[i]
        )
        data_points, voltage = spectra.read_data(ifg_path)
        fig_name = "_".join(sample_ifgs_220125[i].split("_")[:5]) + "_fft_spectrum.png"
        wavenumbers, intensity = spectra.fourier_transform(
            data_points,
            voltage,
            0.241,
            plot = True,
            save_fig = True,
            path_save = output_path / fig_name,
        )
