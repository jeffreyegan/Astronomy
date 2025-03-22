

from skyfield.api import load, EarthSatellite
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import Stamen


ts = load.timescale(builtin=True)


TLE = """1 25544U 98067A   22277.67252396 -.00011725  00000-0 -19986-3 0  9994
2 25544  51.6412 154.1524 0003224 266.9628 188.3164 15.49705802362163"""

L1, L2 = TLE.splitlines()

sat = EarthSatellite(L1, L2)

minutes = np.arange(0, 200, 0.1) # about two orbits
times   = ts.utc(2022, 10, 0, 0, minutes)

geocentric = sat.at(times)
subsat = geocentric.subpoint()


if True:
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-150, -30, -20, 90], crs=ccrs.PlateCarree())

    ax.stock_img()

    plt.scatter(subsat.longitude.degrees, subsat.latitude.degrees, transform=ccrs.PlateCarree(), color='red')

    plt.scatter([-71], [42.5], transform=ccrs.PlateCarree(), color='green')


    plt.savefig("ground_track_0.png")
    plt.show()
    plt.close()


if True:
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.stock_img()

    plt.scatter(subsat.longitude.degrees, subsat.latitude.degrees, transform=ccrs.PlateCarree(), color='red')

    plt.scatter([-71], [42.5], transform=ccrs.PlateCarree(), color='green')


    plt.savefig("ground_track_1.png")
    plt.show()
    plt.close()


