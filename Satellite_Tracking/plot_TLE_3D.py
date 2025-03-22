import os

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import numpy as np

from skyfield.api import Loader, EarthSatellite
from skyfield.timelib import Time


degs, rads = 180/np.pi, np.pi/180

def make_cube_limits(axis, centers=None, hw=None):

    lims = axis.get_xlim(), axis.get_ylim(), axis.get_zlim()

    if centers is None:
        centers = [0.5 * sum(pair) for pair in lims]

    if hw is None:
        widths = [pair[1] - pair[0] for pair in lims]
        hw = 0.5 * max(widths)  # half-widths
        axis.set_xlim(centers[0]-hw, centers[0]+hw)
        axis.set_ylim(centers[1]-hw, centers[1]+hw)
        axis.set_zlim(centers[2]-hw, centers[2]+hw)
    else:
        try:
            hwx = 0 #TODO
        except:
            hwx = 0 #TODO


    return centers, hw


def plot_TLE_orbit(TLE):

    L1, L2 = TLE.splitlines()
    sat = EarthSatellite(L1, L2)

    load = Loader(os.path.join("SkyData"))
    data = load('de421.bsp')
    ts = load.timescale()

    planets = load('de421.bsp')
    earth = planets['earth']

    Roadster = EarthSatellite(L1, L2)
    print(Roadster.epoch.tt)

    minutes = np.arange(0, 200, 0.1) # about two orbits
    times   = ts.utc(2022, 10, 0, 0, minutes)

    Rpos = Roadster.at(times).position.km
    Rposec1 = Roadster.at(times).ecliptic_position().km
    print(Rpos.shape)

    re = 6378.

    theta = np.linspace(0, 2*np.pi, 201)

    cth, sth, zth = [f(theta) for f in [np.cos, np.sin, np.zeros_like]]
    lon0 = re * np.vstack((cth, zth, sth))
    lons = []

    for phi in rads * np.arange(-75, 90, 15):
        cph, sph = [f(phi) for f in [np.cos, np.sin]]
        lon = np.vstack((lon0[0]*cph - lon0[1]*sph,  lon0[1]*cph + lon0[0]*sph,  lon0[2]))
        lons.append(lon)

    lat0 = re * np.vstack((cth, sth, zth))
    lats = []

    for phi in rads * np.arange(-75, 90, 15):
        cph, sph = [f(phi) for f in [np.cos, np.sin]]
        lat = re * np.vstack((cth*cph, sth*cph, zth+sph))
        lats.append(lat)


    if True:  # plotting boolean
        fig = plt.figure(figsize=[12, 8])
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        x, y, z = Rpos
        ax.plot(x, y, z, color='red')
        for x, y, z in lons:
            ax.plot(x, y, z, '-k')
        for x, y, z in lats:
            ax.plot(x, y, z, '-k')

        centers, hw = make_cube_limits(ax)

        print("Centers are: "+str(centers))
        print("Half-Widths are: "+str(hw))
        plt.savefig("3D_Perspective.png")
        plt.show()


TLE = """1 25544U 98067A   22277.67252396 -.00011725  00000-0 -19986-3 0  9994
2 25544  51.6412 154.1524 0003224 266.9628 188.3164 15.49705802362163"""
plot_TLE_orbit(TLE)
