import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.image as image
from cartopy import crs as ccrs, feature as cfeature
import time

#  Suppress warnings issued by Cartopy when downloading data files
warnings.filterwarnings('ignore')

from herbie import FastHerbie
import pandas as pd
import pytz
from datetime import datetime, timedelta

from adjustText import adjust_text
import glob
import os
import json

from multiprocessing import Pool

def generateRadarPlot(state_params):
    projPC = ccrs.PlateCarree()
    res = '10m'
    link_list = []
    state = state_params['state']
    tz = state_params['tz']
    lonW = state_params['lonW']
    lonE = state_params['lonE']
    latS = state_params['latS']
    latN = state_params['latN']
    ds = state_params['ds']
    path = state_params['path']
    USA_cities = state_params['city_csv']
    description = state_params['description']
    for step in range(ds.step.size):
        #print(state + ' step number: ' + str(step))
        time = ds['valid_time'].to_index()

        time_utc = time.tz_localize(pytz.UTC)
        local_tz = pytz.timezone(tz)
        time_local = time_utc.tz_convert(local_tz)

        fig = plt.figure(figsize=(11, 8.5))
        ax = plt.subplot(1, 1, 1, projection=projPC)
        gl = ax.gridlines(
            draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--'
        )

        im = image.imread('/home/scrump/containers/website/python/model_files/scrump-logo.png')
        ax.imshow(im, aspect='equal', extent=(lonW + 0.1, lonE - 18.1, latS + 0.1, latN - 11.1), zorder=300)

        gl.ylocator = mticker.FixedLocator([25, 30, 35, 40, 45, 50])
        gl.xlocator = mticker.FixedLocator([-65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125])
        gl.xlabels_bottom = False
        ax.set_extent([lonW, lonE, latS, latN], crs=projPC)
        ax.coastlines(resolution=res, color='black')
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown')
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.LAKES)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='blue');
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
            transform=projPC,
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
            f"{ds.isel(step=step).model.upper()}: {description}\nLocal Time: {time_local[step].strftime('%Y-%m-%d %H:%M:%S')}",
            loc="left",
        )
        ax.set_title(ds.isel(step=step).refd.GRIB_name, loc="right")
        final_path = path + state + '_' + str(step) + '.png'
        #print('Saving ' + final_path)
        fig.savefig(final_path, edgecolor='black',bbox_inches='tight', dpi=126, transparent=True)
        link_list.append('../goes/hrrr_radar/operational/' + state + '_' + str(step) + '.png')
        plt.clf()
    return [state, link_list]

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

if __name__ == '__main__':
    forecast_hours = 19
    path = '/home/scrump/containers/website/html/goes/hrrr_radar/'
    json_filename = 'radar-images'

    model_utc_time = datetime.utcnow() - timedelta(hours=2, minutes=00)

    DATES = pd.date_range(
        start=model_utc_time.strftime('%Y-%m-%d %H:00'),
        periods=1,
        freq="1H",
    )

    start_time = time.time()
    print('Getting GRIB2 Data...')

    H = FastHerbie(
        DATES,
        model="hrrr",
        product="subh",
        fxx=range(0, forecast_hours),
    )

    print(H.objects)

    print('Parsing Model Data...')
    ds = H.xarray("REFD:1000 m above", max_threads=50)
    print(ds)
    ds["refd"] = ds.refd.where(ds.refd > 0)

    USA_cities = pd.read_csv("/home/scrump/containers/website/python/model_files/USA_Major_Cities.csv")

    description = H.objects[0].product_description

    states = [
        {
            'state': 'tx',
            'lonW': -110,
            'lonE': -90,
            'latS': 25,
            'latN': 38,
            'tz': 'America/Chicago',
            'ds': ds,
            'city_csv': USA_cities,
            'path': path,
            'description': description
        },
        {
            'state': 'nm',
            'lonW': -120,
            'lonE': -100,
            'latS': 28,
            'latN': 41,
            'tz': 'America/Denver',
            'ds': ds,
            'city_csv': USA_cities,
            'path': path,
            'description': description
        },
        {
            'state': 'ny',
            'lonW': -85,
            'lonE': -65,
            'latS': 34,
            'latN': 47,
            'tz': 'America/New_York',
            'ds': ds,
            'city_csv': USA_cities,
            'path': path,
            'description': description
        },
        {
            'state': 'il',
            'lonW': -100,
            'lonE': -80,
            'latS': 36,
            'latN': 49,
            'tz': 'America/Chicago',
            'ds': ds,
            'city_csv': USA_cities,
            'path': path,
            'description': description
        },
        {
            'state': 'mn',
            'lonW': -105,
            'lonE': -85,
            'latS': 37,
            'latN': 50,
            'tz': 'America/Chicago',
            'ds': ds,
            'city_csv': USA_cities,
            'path': path,
            'description': description
        },
        {
            'state': 'wa',
            'lonW': -130,
            'lonE': -110,
            'latS': 41,
            'latN': 54,
            'tz': 'America/Los_Angeles',
            'ds': ds,
            'city_csv': USA_cities,
            'path': path,
            'description': description
        }
    ]

    print('Generating Plots...')
    p = Pool(6)
    state_file_paths = p.map(generateRadarPlot, states)
    link_dict = {}
    for file in state_file_paths:
        link_dict.update({file[0]: file[1]})
    print('Writing JSON File...')
    writeJson(link_dict)
    print('Replacing operational files...')
    renameFiles()
    print('Removing temporary files...')
    removeFiles()
    print("--- %s seconds ---" % (time.time() - start_time))