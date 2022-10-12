import numpy as np

def rescale(data, zero_before, full_before, zero_after, full_after):
    return (data - zero_before) / (full_before - zero_before) * (full_after - zero_after) + zero_after

red = np.genfromtxt("red.csv", delimiter=",")
x_red, y_red, *rest = np.transpose(red)

y_all = []
x_main = np.round(rescale(x_red, x_red[0], x_red[-1], 300, 1100))

def rescale_by_red_measured(filename):
    red = np.genfromtxt(f"{filename}.csv", delimiter=",")
    x, y, *rest = np.transpose(red)

    x = np.round(rescale(x, x_red[0], x_red[-1], 300, 1100))
    y = rescale(y, y_red[0], y_red[1], 306.065, 305.488)
    y = rescale(y, 0, 321.702, 0.3, 0)
    assert (x == x_main).all(), (x, x_main)
    y_all.append(y)

    np.savetxt(
        f"../{filename}.csv", 
        np.transpose(np.array([x, y])), 
        delimiter=",", 
        fmt="%.8f",
        header="wavelength [nm], spectral response [A / W]",
    )

for f in ["red", "green_red", "green_blue", "blue", "mono", "nir"]:
    rescale_by_red_measured(f)

np.savetxt(
    f"../all.csv",
    np.transpose(np.array([x_main, *y_all])),
    delimiter=",",
    fmt="%.8f",
    header="wavelength [nm], red [A / W], green_red [A / W], green_blue [A / W], blue [A / W], mono [A / W], nir [A / W]",
)

