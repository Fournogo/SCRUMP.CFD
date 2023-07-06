import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.image as image
#import numpy as np
from cartopy import crs as ccrs, feature as cfeature

#  Suppress warnings issued by Cartopy when downloading data files
warnings.filterwarnings('ignore')

from herbie import FastHerbie
from toolbox import pc
import pandas as pd
import pytz
from datetime import datetime, timedelta

from adjustText import adjust_text
import glob
import os
import json

# IMPORTANT VARIABLES
forecast_hours = 19
path = ''
json_filename = 'radar-images'

# REGION DICTIONARY

states = {
    'tx': {
        'lonW': -110,
        'lonE': -90,
        'latS': 25,
        'latN': 38,
        'tz': 'America/Chicago'
    },
    'nm': {
        'lonW': -120,
        'lonE': -100,
        'latS': 28,
        'latN': 41,
        'tz': 'America/Denver'
    },
    'ny': {
        'lonW': -85,
        'lonE': -65,
        'latS': 34,
        'latN': 47,
        'tz': 'America/New_York'
    },
    'mn': {
        'lonW': -105,
        'lonE': -85,
        'latS': 37,
        'latN': 50,
        'tz': 'America/Chicago'
    },
    'wa': {
        'lonW': -130,
        'lonE': -110,
        'latS': 41,
        'latN': 54,
        'tz': 'America/Los_Angeles'
    },
    'nv': {
        'lonW': -130,
        'lonE': -110,
        'latS': 31,
        'latN': 44,
        'tz': 'America/Los_Angeles'
    },
    'co': {
        'lonW': -120,
        'lonE': -100,
        'latS': 38,
        'latN': 51,
        'tz': 'America/Denver'
    }
}

tz = 'America/Chicago'
link_dict = {}
link_list = []

model_utc_time = datetime.utcnow() - timedelta(hours=2, minutes=10)

DATES = pd.date_range(
    start=model_utc_time.strftime('%Y-%m-%d %H:00'),
    periods=1,
    freq="1H",
)

print('Getting GRIB2 Data...')

H = FastHerbie(
    DATES,
    model="hrrr",
    product="subh",
    fxx=range(0,forecast_hours),
)

print(H.objects)

print('Parsing Model Data...')
ds = H.xarray("REFD:1000 m above")
print(ds)
ds["refd"] = ds.refd.where(ds.refd > 0)

projPC = ccrs.PlateCarree()
res = '10m'

USA_cities = pd.read_csv("/USA_Major_Cities.csv")

def generateRadarPlot(step):
    print('Step number: ' + str(step))
    time = ds['valid_time'].to_index()

    time_utc = time.tz_localize(pytz.UTC)
    local_tz = pytz.timezone(tz)
    time_local = time_utc.tz_convert(local_tz)

    fig = plt.figure(figsize=(11, 8.5))
    ax = plt.subplot(1, 1, 1, projection=projPC)
    gl = ax.gridlines(
        draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--'
    )

    im = image.imread('/scrump-logo.png')
    ax.imshow(im, aspect='equal', extent=(lonW + 0.1, lonE - 18.1, latS + 0.1, latN - 11.1), zorder=300)

    gl.ylocator = mticker.FixedLocator([25, 30, 35, 40, 45, 50])
    gl.xlocator = mticker.FixedLocator([-65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125])
    gl.xlabels_bottom = False
    ax.set_extent([lonW, lonE, latS, latN], crs=projPC)
    ax.coastlines(resolution=res, color='black')
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.LAKES)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='blue')
    plt.scatter(x=USA_cities.X, y=USA_cities.Y,
                color="dodgerblue",
                s=1,
                alpha=0.5,
                transform=projPC)

    texts=[]
    #csfont = {'fontname': 'Comic Sans MS'}
    for index in range(len(USA_cities.index)):
        x=USA_cities.iloc[index].X
        y=USA_cities.iloc[index].Y
        if lonW+1 < x < lonE-1 and latS+1 < y < latN-1:
            texts.append(plt.text(x=USA_cities.iloc[index].X, y=USA_cities.iloc[index].Y,
                        s=USA_cities.iloc[index].NAME,
                        color="red",
                        fontsize=8,
                        #**csfont,
                        transform=projPC)) ## Important
    adjust_text(texts,autoalign='y', only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle="-", color='r', lw=0.5))

    p = ax.pcolormesh(
        ds.isel(step=step).longitude,
        ds.isel(step=step).latitude,
        ds.isel(step=step).refd,
        vmin=-10,
        vmax=75,
        transform=pc,
        cmap="gist_ncar",
    )
    p.set_zorder(200)
    bounds = list(range(-30,80,5))
    cmap = cm.gist_ncar
    norm = colors.BoundaryNorm(bounds, cmap.N, extend='both')

    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                 ax=ax,
                 orientation='horizontal',
                 pad=0.01,
                 shrink=0.5,
                 label='Derived Radar Reflectivity: dBZ')

    ax.set_title(
        f"{ds.isel(step=step).model.upper()}: {H.objects[0].product_description}\nLocal Time: {time_local[step].strftime('%Y-%m-%d %H:%M:%S')}",
        loc="left",
    )
    ax.set_title(ds.isel(step=step).refd.GRIB_name, loc="right")
    final_path = path + state + '_' + str(step) + '.png'
    print('Saving ' + final_path)
    fig.savefig(final_path, edgecolor='black',bbox_inches='tight', dpi=126, transparent=True)
    link_list.append('../goes/hrrr_radar/operational/' + state + '_' + str(step) + '.png')
    plt.cla()
    plt.clf()
    return

def removeFiles():
    json_files = glob.glob(os.path.join(path, "*.json"))
    if json_files:
        print("Removing existing .json files..")
        for file_path in json_files:
            os.remove(os.path.join(file_path))
    else:
        print("No .json files found... continuing.")

    png_files = glob.glob(os.path.join(path, "*.png"))
    if png_files:
        print("Removing existing .png files..")
        for file_path in png_files:
            os.remove(os.path.join(file_path))
    else:
        print("No .png files found... continuing.")

def renameFiles():
    json_files = glob.glob(os.path.join(path, "*.json"))
    if json_files:
        print("Renaming temp .json files..")
        for file_path in json_files:
            os.rename(file_path, os.path.join(os.path.dirname(file_path) + '/operational/' + os.path.basename(file_path)))
    else:
        print("No .json files found... continuing.")

    png_files = glob.glob(os.path.join(path, "*.png"))
    if png_files:
        print("Renaming temp .png files..")
        for file_path in png_files:
            os.rename(file_path, os.path.join(os.path.dirname(file_path) + '/operational/' + os.path.basename(file_path)))
    else:
        print("No .png files found... continuing.")

def writeJson(data):
    json_data = data
    try:
        os.chmod(path + json_filename, 0o777)
    except:
        print('No JSON file to change permissions on.')
    with open(path + json_filename + '.json', "w") as f:
        json.dump(json_data, f)
        print('JSON saved to ' + json_filename)

print('Generating Plots...')
for state in states:
    tz = states[state]['tz']
    lonW = states[state]['lonW']
    lonE = states[state]['lonE']
    latS = states[state]['latS']
    latN = states[state]['latN']
    for step in range(ds.step.size):
        generateRadarPlot(step)
    link_dict.update({state: link_list})
    link_list = []
print('Writing JSON File...')
writeJson(link_dict)
print('Replacing operational files...')
renameFiles()
print('Removing temporary files...')
removeFiles()