import numpy as np
import colour

all = []

for file in ["Hayda", "Hoya", "UQG"]:
    read = sorted(np.genfromtxt(f"{file}.csv", delimiter=','), key=lambda row: row[0])
    transmissivity = [[x, 1 / 10**max(0, y)] for x, y in read]
    deduplicated = list(dict(((x, y) for x, y in transmissivity)).items())
    x, data = np.transpose(deduplicated)
    sd = colour.SpectralDistribution(data, x).align(colour.SpectralShape(300, 1100, 1)).align(colour.SpectralShape(300, 1100, 5))
    
    all.append(sd)
    np.savetxt(
        f"../{file}.csv",
        np.transpose(np.array([sd.wavelengths, sd.values])),
        delimiter=",",
        fmt='%.8f',
        header="wavelength [nm], Transmissivity",
    )

np.savetxt(
    f"../all.csv", 
    np.transpose(np.array([all[0].wavelengths, *[sd.values for sd in all]])),
    delimiter=",",
    fmt='%.8f',
    header="wavelength [nm], Hayda Transmissivity, Hoya Transmissivity, UQG Transmissivity",
)