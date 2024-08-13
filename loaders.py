import numpy as np
import colour
from pathlib import Path

def load_spectral_data(filename):
    x, data = np.transpose(np.genfromtxt(filename, delimiter=",", skip_header=1))
    sd = colour.SpectralDistribution(data, x, name=Path(filename).stem)
    wavelengths = np.round(sd.wavelengths / 10) * 10
    wavelength_range = np.min(wavelengths), np.max(wavelengths)

    sd = sd.align(colour.SpectralShape(*wavelength_range, 1)).align(
        colour.SpectralShape(*wavelength_range, 5)
    )

    print(
        f"loaded spectral data named '{sd.name}' from {sd.wavelengths[0]}nm to {sd.wavelengths[-1]}nm"
    )
    return sd

def normalize_msd(msd):
    return msd / np.max(msd.values)

def load_image_sensor_response(filename):
    array = np.genfromtxt(filename, delimiter=",", skip_header=1)
    data = {row[0]: row[1:] for row in array}
    msd = colour.MultiSpectralDistributions(
        data, labels=["red", "green", "blue"], name=Path(filename).stem
    )
    print(
        f"loaded spectral data named '{msd.name}' from {msd.wavelengths[0]}nm to {msd.wavelengths[-1]}nm"
    )
    return normalize_msd(msd)
