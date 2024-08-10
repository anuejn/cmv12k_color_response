import numpy as np

def rescale(data, zero_before, full_before, zero_after, full_after):
    """Rescale data from one range to another."""
    return (data - zero_before) / (full_before - zero_before) * (full_after - zero_after) + zero_after

def read_and_rescale(filename, x_red_min, x_red_max, x_min, x_max, y_min, y_max):
    """Read and rescale data from a given file."""
    data = np.genfromtxt(f"{filename}.csv", delimiter=",")
    x, y, *rest = np.transpose(data)

    # Rescale x values to the common range
    x_rescaled = np.round(rescale(x, x_red_min, x_red_max, x_min, x_max))

    # Rescale y values
    y_rescaled = rescale(y, y_min, y_max, 0, 1)

    return x_rescaled, y_rescaled

# Define the common wavelength range
wavelength_range = np.arange(400, 1005, 5)

# Initialize arrays to store rescaled y values
y_red = np.zeros_like(wavelength_range, dtype=float)
y_green = np.zeros_like(wavelength_range, dtype=float)
y_blue = np.zeros_like(wavelength_range, dtype=float)

# Read and rescale data from each file
x_red, y_red_rescaled = read_and_rescale("Red", 400, 1000, 400, 1000, y_min=0, y_max=1)
x_green, y_green_rescaled = read_and_rescale("Green", 400, 1000, 400, 1000, y_min=0, y_max=1)
x_blue, y_blue_rescaled = read_and_rescale("Blue", 400, 1000, 400, 1000, y_min=0, y_max=1)

# Interpolate the rescaled y values to the common wavelength range
y_red = np.interp(wavelength_range, x_red, y_red_rescaled)
y_green = np.interp(wavelength_range, x_green, y_green_rescaled)
y_blue = np.interp(wavelength_range, x_blue, y_blue_rescaled)

# Save the combined data to a single CSV file
np.savetxt(
    "./combined.csv",
    np.transpose(np.array([wavelength_range, y_red, y_green, y_blue])),
    delimiter=",",
    fmt="%.8f",
    header="# wavelength [nm], r, g, b",
)
