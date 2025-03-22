
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.img_tiles import Stamen

from skyfield.api import load, EarthSatellite


def compute_radius(ortho, lat, lon, radius_degrees):
    phi1 = lat + radius_degrees if lat <= 0 else lat - radius_degrees
    _, y1 = ortho.transform_point(lon, phi1, ccrs.PlateCarree())
    return abs(y1)


def plot_coverage(TLE, cvg_rad, plot_scale=35):
    ts = load.timescale(builtin=True)

    L1, L2 = TLE.splitlines()

    sat = EarthSatellite(L1, L2)

    minutes = np.arange(0, 200, 0.1) # about two orbits
    times   = ts.utc(2022, 10, 0, 0, minutes)

    geocentric = sat.at(times)
    subsat = geocentric.subpoint()

    # Receiver Location and Coverage Radius at Desired Altitude
    lat = 42.5  # rcvr location - latitude in decimal degrees
    lon = -71.7  # rcvr location - longitude in decimal degrees
    r = cvg_rad # rcvr range at tracked object altitude
    theta_1 = -70  # adjustments for coverage azimuths when rcvr FOV is not 360, degrees
    theta_2 = theta_1 + 50

    # Define the projection used to display the circle:
    proj = ccrs.Orthographic(central_longitude=lon, central_latitude=lat)



    # Compute the required radius in projection native coordinates:
    r_ortho = compute_radius(proj, lat, lon, r)

    # We can now compute the correct plot extents to have padding in degrees:
    pad_radius = compute_radius(proj, lat, lon, r + plot_scale)

    # define image properties
    width = 800
    height = 800
    dpi = 96
    resolution = '50m'  # "110m", "50m", and "10m" supported

    # create figure
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    # Deliberately avoiding set_extent because it has some odd behaviour that causes
    # errors for this case. However, since we already know our extents in native
    # coordinates we can just use the lower-level set_xlim/set_ylim safely.
    ax.set_xlim([-pad_radius, pad_radius])
    ax.set_ylim([-pad_radius, pad_radius])
    
    #ax.imshow(np.tile(np.array([[cfeature.COLORS['water'] * 255]], dtype=np.uint8), [2, 2, 1]), origin='upper', transform=ccrs.PlateCarree(), extent=[-180, 180, -180, 180])
    #ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', resolution, edgecolor='black', facecolor=cfeature.COLORS['land']))
    ax.add_feature(cfeature.NaturalEarthFeature('cultural', 'admin_0_countries', resolution, edgecolor='black', facecolor='none'))
    #ax.add_feature(cfeature.NaturalEarthFeature('physical', 'lakes', resolution, edgecolor='none', facecolor=cfeature.COLORS['water']), alpha=0.5)
    #ax.add_feature(cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', resolution, edgecolor=cfeature.COLORS['water'], facecolor='none'))
    ax.add_feature(cfeature.NaturalEarthFeature('cultural', 'admin_1_states_provinces_lines', resolution, edgecolor='gray', facecolor='none'))

    plt.scatter(subsat.longitude.degrees, subsat.latitude.degrees, transform=ccrs.PlateCarree(), color='red', marker='.')
    plt.scatter([lon], [lat], transform=ccrs.PlateCarree(), color='green', marker="o")
    ax.add_patch(mpatches.Circle(xy=[lon, lat], radius=r_ortho, color='green', alpha=0.1, transform=proj, zorder=30))  # Full 360 coverage
    ax.add_patch(mpatches.Wedge(center=(lon, lat), r=r_ortho, theta1=theta_1, theta2=theta_2, color='green', alpha=0.2, transform=proj, zorder=30))  # Narrower Receiver Field of View
    
    fig.tight_layout()
    plt.savefig('ReceiverCoverage_'+str(plot_scale)+'.png', dpi=dpi)
    plt.show()


TLE = """1 25544U 98067A   22277.67252396 -.00011725  00000-0 -19986-3 0  9994
2 25544  51.6412 154.1524 0003224 266.9628 188.3164 15.49705802362163"""

plot_coverage(TLE, cvg_rad=5, plot_scale=50)
plot_coverage(TLE, cvg_rad=5, plot_scale=35)
plot_coverage(TLE, cvg_rad=5, plot_scale=0)