import sys
import csv
from collections import defaultdict

import numpy as np
import colour

colors = defaultdict(list)

with open(sys.argv[1], newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    first, _, second, _, third, _ = next(reader)
    xy = next(reader)
    for row in reader:
        for color in [first, second, third]:
            x, y, *row = row
            if x and y:
                colors[color].append((float(x), float(y)))

wavelengths = np.round(np.array(colors["r"])[:, 0] / 10) * 10
wavelength_range = np.min(wavelengths), np.max(wavelengths)
print("range:", wavelength_range)


all = []
for color in "rgb":
    data = np.array(colors[color])
    data = list(dict(((x, y) for x, y in data)).items())
    data = np.array(data)
    sd = (
        colour.SpectralDistribution(data[:,1], data[:,0])
        .align(colour.SpectralShape(*wavelength_range, 1))
        .align(colour.SpectralShape(*wavelength_range, 5))
    )
    all.append(sd)

np.savetxt(
    f"../{sys.argv[1]}", 
    np.transpose(np.array([all[0].wavelengths, *[sd.values for sd in all]])),
    delimiter=",",
    fmt='%.8f',
    header="wavelength [nm], r, g, b",
)