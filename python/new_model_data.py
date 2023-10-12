import time

import matplotlib.cm as cm

from herbie import FastHerbie
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

from multiprocessing import Pool

from state_plots import generateLocalPlot
from json_functions import writeJson,removeFiles,renameFiles
from state_parameters import state_params as default_state_params
from region_parameters import region_params as default_region_params

import copy
import re

#danger ! warning~ brain damage to ye who enter here

#IMPORTANT VARIABLES
###################
path = '/home/scrump/containers/website/html/goes/model_data/' #PATH TO SAVE IMAGES
json_path = '/home/scrump/containers/website/html/goes/json/'
usa_cities = pd.read_csv('/home/scrump/containers/website/python/model_files/USA_Major_Cities.csv')
json_name = 'model_data'

def convertRefdNan(ds, forecast_name):
    ds[forecast_name] = ds[forecast_name].where(ds[forecast_name] > 0)
    return ds

def convertRefdZero(ds, forecast_name):
    ds[forecast_name] = ds[forecast_name].where(ds[forecast_name] > 0)
    ds[forecast_name].values = np.nan_to_num(ds[forecast_name].values)
    return ds

def convertT2m(ds, forecast_name):
    ds[forecast_name] = (ds[forecast_name] - 273.15) * (9/5) + 32
    return ds

def convertGH(ds, forecast_name):
    ds[forecast_name] = ds[forecast_name] / 10
    return ds

def convertWind(ds, forecast_name):
    #Convert from m/s to mph
    ds[forecast_name] = ds[forecast_name] * 2.23694
    return ds

models = {
        'hrrr': {
            'product': {
                'subh': {
                    'run_freq': 1,
                    'fxx': [18],
                    'freq': ['1H'],
                    # 'fxx': [1],
                    # 'freq': ['1H'],
                    'forecast': [
                         {  'name':['refd'],
                            'search': ['REFD:1000 m above'],
                            'conversion': convertRefdNan,
                            'sample_points': False,
                            'colormap': cm.gist_ncar,
                            'data_unit': 'dBz',
                            'data_min': -10,
                            'data_max': 75,
                            'data_label': 'Derived Radar Reflectivity, dBZ',
                            'lat_index': 'y',
                            'lon_index': 'x',
                            'gaussian': False,
                            'algorithm': 'pcolormesh',
                            'prune': True,
                            'level_increment': 1,
                            'model_res': 3,
                            'data_var_names': ['refd'],
                            'height': '1000m'
                        },
                        {   'name': ['t2m'],
                            'search': ['TMP:2 m above'],
                            'conversion': convertT2m,
                            'sample_points': True,
                            'colormap': cm.nipy_spectral,
                            'data_unit': 'F',
                            'data_min': -50,
                            'data_max': 130,
                            'data_label': 'Surface Temperature, Degrees F',
                            'lat_index': 'y',
                            'lon_index': 'x',
                            'gaussian': False,
                            'algorithm': 'pcolormesh',
                            'prune': False,
                            'level_increment': 1,
                            'model_res': 3,
                            'data_var_names': ['t2m'],
                            'height': '2m'
                        }
                    ]
            }, 
                'sfc': {
                    'run_freq': 6,
                    'fxx': [48],
                    'freq': ['1H'],
                    # 'fxx': [1],
                    # 'freq': ['1H'],
                    'forecast': [
                        {   'name': ['refd'],
                            'search': ['REFD:1000 m above'],
                            'conversion': convertRefdNan,
                            'sample_points': False,
                            'colormap': cm.gist_ncar,
                            'data_unit': 'dBz',
                            'data_min': -10,
                            'data_max': 75,
                            'data_label': 'Derived Radar Reflectivity, dBZ',
                            'lat_index': 'y',
                            'lon_index': 'x',
                            'gaussian': False,
                            'algorithm': 'pcolormesh',
                            'prune': True,
                            'level_increment': 1,
                            'model_res': 3,
                            'data_var_names': ['refd'],
                            'height': '1000m'
                        },
                        {   'name': ['t2m'],
                            'search': ['TMP:2 m above'],
                            'conversion': convertT2m,
                            'sample_points': True,
                            'colormap': cm.nipy_spectral,
                            'data_unit': 'F',
                            'data_min': -50,
                            'data_max': 130,
                            'data_label': 'Surface Temperature, Degrees F',
                            'lat_index': 'y',
                            'lon_index': 'x',
                            'gaussian': False,
                            'algorithm': 'pcolormesh',
                            'prune': False,
                            'level_increment': 1,
                            'model_res': 3,
                            'data_var_names': ['t2m'],
                            'height': '2m'
                        },
                        {   'name': ['d2m'],
                            'search': ['DPT:2 m above'],
                            'conversion': convertT2m,
                            'sample_points': True,
                            'colormap': cm.nipy_spectral,
                            'data_unit': 'F',
                            'data_min': -50,
                            'data_max': 130,
                            'data_label': 'Dew Point Temperature, Degrees F',
                            'lat_index': 'y',
                            'lon_index': 'x',
                            'gaussian': False,
                            'algorithm': 'pcolormesh',
                            'prune': False,
                            'level_increment': 1,
                            'model_res': 3,
                            'data_var_names': ['d2m'],
                            'height': '2m'
                        },
                        {   'name': ['gh'],
                            'search': ['HGT:500 mb'],
                            'conversion': convertGH,
                            'sample_points': False,
                            'colormap': None,
                            'data_unit': None,
                            'data_min': None,
                            'data_max': None,
                            'data_label': '500 mb Geopotential Height',
                            'lat_index': 'y',
                            'lon_index': 'x',
                            'gaussian': True,
                            'algorithm': 'contour',
                            'prune': False,
                            'level_increment': 3,
                            'model_res': 3,
                            'data_var_names': ['gh'],
                            'height': '500mb'
                        }
                    ]
                }
            }    
        },
        'gfs': {
            'product': {
                    'pgrb2.0p25': {
                        'run_freq': 6,
                        'fxx': [120, 240, 384],
                        'freq': ['1H', '3H', '6H'],
                        # 'fxx': [3],
                        # 'freq': ['1H'],
                        'forecast': [
                            {   'name': ['refd'],
                                'search': ['REFD:1000 m above'],
                                'conversion': convertRefdZero,
                                'sample_points': False,
                                'colormap': cm.gist_ncar,
                                'data_unit': 'dBz',
                                'data_min': -10,
                                'data_max': 75,
                                'data_label': 'Derived Radar Reflectivity, dBZ',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                                'gaussian': True,
                                'algorithm': 'contourf',
                                'prune': True,
                                'level_increment': 1,
                                'model_res': 18,
                                'data_var_names': ['refd'],
                                'height': '1000m'
                            },
                            {   'name': ['t2m'],
                                'search': ['TMP:2 m above'],
                                'conversion': convertT2m,
                                'sample_points': True,
                                'colormap': cm.nipy_spectral,
                                'data_unit': 'F',
                                'data_min': -50,
                                'data_max': 130,
                                'data_label': 'Surface Temperature, Degrees F',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                                'gaussian': False,
                                'algorithm': 'contourf',
                                'prune': False,
                                'level_increment': 1,
                                'model_res': 18,
                                'data_var_names': ['t2m'],
                                'height': '2m'
                            },
                            {   'name': ['d2m'],
                                'search': ['DPT:2 m above'],
                                'conversion': convertT2m,
                                'sample_points': True,
                                'colormap': cm.nipy_spectral,
                                'data_unit': 'F',
                                'data_min': -50,
                                'data_max': 130,
                                'data_label': 'Dew Point Temperature, Degrees F',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                                'gaussian': False,
                                'algorithm': 'contourf',
                                'prune': False,
                                'level_increment': 1,
                                'model_res': 18,
                                'data_var_names': ['d2m'],
                                'height': '2m'
                            },
                            {   'name': ['gh'],
                                'search': ['HGT:500 mb'],
                                'conversion': convertGH,
                                'sample_points': False,
                                'colormap': None,
                                'data_unit': None,
                                'data_min': None,
                                'data_max': None,
                                'data_label': '500 mb Geopotential Height',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                                'gaussian': True,
                                'algorithm': 'contour',
                                'prune': False,
                                'level_increment': 3,
                                'model_res': 18,
                                'data_var_names': ['gh'],
                                'height': '500mb'
                            },
                            {   'name': ['u','v'],
                                'search': ['UGRD:20 m above','VGRD:20 m above'], #Must put in U, V order
                                'conversion': convertWind,
                                'sample_points': False,
                                'colormap': cm.gist_ncar,
                                'data_unit': None,
                                'data_min': 0,
                                'data_max': 100,
                                'data_label': 'Wind 20m Above Surface, MPH',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                                'gaussian': False,
                                'algorithm': 'barbs',
                                'prune': False,
                                'level_increment': 3,
                                'model_res': 18,
                                'data_var_names': ['u','v'],
                                'height': '20m'
                            },
                            {   'name': ['u','v'],
                                'search': ['UGRD:500 mb','VGRD:500 mb'], #Must put in U, V order
                                'conversion': convertWind,
                                'sample_points': False,
                                'colormap': cm.gist_ncar,
                                'data_unit': None,
                                'data_min': 0,
                                'data_max': 100,
                                'data_label': 'Wind at 500mb level, MPH',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                                'gaussian': False,
                                'algorithm': 'barbs',
                                'prune': False,
                                'level_increment': 3,
                                'model_res': 18,
                                'data_var_names': ['u','v'],
                                'height': '500mb'
                            },
                        ]
                    }
                }    
            }
}

#Regex pattern for getting frequency integer from string
pattern = r'(\d+)H'

#Set start time of the main part of the program for timing execution
start_time = time.time()

start_utc_time = datetime.utcnow()

if __name__ == '__main__':

    final_links = {}

    for model_name in models:
        model = models[model_name]
        final_links.update({model_name: {}})

        for region_list in default_region_params:

            #Skip the international regions for HRRR
            if region_list == default_region_params[1] and model_name == 'hrrr':
                continue

            for product_name in model['product']:
                product = model['product'][product_name]
                
                time_offset = product['run_freq'] + 1
                #Define the offset from the current time in order to get a sufficiently old model run
                model_run_time = start_utc_time - timedelta(hours=time_offset, minutes=0)

                #Not all of these models run every hour. Make sure the requested hour will work.
                if model_run_time.hour % product['run_freq'] != 0:
                    continue

                if region_list == default_region_params[0]:
                    final_links[model_name].update({product_name: {}})

                fxx_list = product['fxx']
                freq_list = product['freq']
                for i in range(len(fxx_list)):
                    fxx_upper = fxx_list[i]
                    freq = freq_list[i]

                    match = re.search(pattern, freq)
                    if match:
                        interval = int(match.group(1))
                    else:
                        interval = 1

                    fxx_lower = 0
                    if i > 0:
                        fxx_lower = fxx_list[i - 1] + interval

                    #Set range of times for forecast hour definitions
                    DATES = pd.date_range(
                        start=model_run_time.strftime('%Y-%m-%d %H:00'),
                        periods=1,
                        freq=freq, #Changes by forecast model
                    )

                    forecast_range = range(fxx_lower, fxx_upper + 1, interval)

                    print('Getting GRIB2 Data For: ' + model_name + ' ' + product_name)

                    #Define Herbie object
                    H = FastHerbie(
                        DATES,
                        model=model_name,
                        product=product_name,
                        fxx=forecast_range
                    )

                    print('Data Sources Found For: ' + model_name + ' ' + product_name)
                    print(H.objects)

                    description = H.objects[0].product_description

                    #Finally iterate through each different "forecast". Forecasts are stored in a list to make them easily iterable by index
                    #By manipulating the index and using a "params2" copy of the state parameters you can do multiple forecasts at once which will better use multiple cores
                    #I can live with this arrangement tbh
                    for pos in range(len(product['forecast'])):

                        if pos % 2 == 0:

                            params1 = copy.deepcopy(region_list)
                            params2 = copy.deepcopy(region_list)

                            forecast1 = product['forecast'][pos]
                            forecast2 = product['forecast'][pos + 1]

                            height1 = forecast1['height']
                            height2 = forecast2['height']

                            forecast_name1 = forecast1['name']
                            forecast_name2 = forecast2['name']

                            ds1 = []
                            ds2 = []

                            if i == 0:
                                if region_list == default_region_params[0]:
                                    final_links[model_name][product_name].update({forecast_name1[0] + height1: {}})
                                    final_links[model_name][product_name].update({forecast_name2[0] + height2: {}})
                                for region in region_list:
                                    final_links[model_name][product_name][forecast_name1[0] + height1].update({region['state']: []})
                                    final_links[model_name][product_name][forecast_name2[0] + height2].update({region['state']: []})

                            print('Downloading GRIB Files and Parsing: ' + forecast_name1[0])
                            ds1.append(H.xarray(forecast1['search'][0], max_threads=50))
                            ds1[0] = forecast1['conversion'](ds1[0], forecast_name1[0])

                            if len(forecast1['search']) > 1:
                                print('Downloading GRIB Files and Parsing: ' + forecast_name1[1])
                                ds1.append(H.xarray(forecast1['search'][1], max_threads=50))
                                ds1[1] = forecast1['conversion'](ds1[1], forecast_name1[1])

                            print('Downloading GRIB Files and Parsing: ' + forecast_name2[0])
                            ds2.append(H.xarray(forecast2['search'][0], max_threads=50))
                            ds2[0] = forecast2['conversion'](ds2[0], forecast_name2[0])

                            if len(forecast2['search']) > 1:
                                print('Downloading GRIB Files and Parsing: ' + forecast_name2[1])
                                ds2.append(H.xarray(forecast2['search'][1], max_threads=50))
                                ds2[1] = forecast2['conversion'](ds2[1], forecast_name2[1])

                            forecast_hour_list = list(forecast_range)
                            
                            for param1 in params1:
                                param1.update({'ds': ds1})
                                param1.update({'city_csv': usa_cities})
                                param1.update({'path': path})
                                param1.update({'description': description})
                                param1.update({'model_name': model_name})
                                param1.update({'product_name': product_name})
                                param1.update({'forecast': forecast_name1})
                                param1.update({'sample_points': forecast1['sample_points']})
                                param1.update({'cmap': forecast1['colormap']})
                                param1.update({'data_unit': forecast1['data_unit']})
                                param1.update({'data_min': forecast1['data_min']})
                                param1.update({'data_max': forecast1['data_max']})
                                param1.update({'data_label': forecast1['data_label']})
                                param1.update({'lat_index': forecast1['lat_index']})
                                param1.update({'lon_index': forecast1['lon_index']})
                                param1.update({'forecast_range': forecast_hour_list})
                                param1.update({'gaussian': forecast1['gaussian']})
                                param1.update({'algorithm': forecast1['algorithm']})
                                param1.update({'prune': forecast1['prune']})
                                param1.update({'level_increment': forecast1['level_increment']})
                                param1.update({'model_res': forecast1['model_res']})
                                param1.update({'data_var_names': forecast1['data_var_names']})
                                param1.update({'height': forecast1['height']})

                            for param2 in params2:
                                param2.update({'ds': ds2})
                                param2.update({'city_csv': usa_cities})
                                param2.update({'path': path})
                                param2.update({'description': description})
                                param2.update({'model_name': model_name})
                                param2.update({'product_name': product_name})
                                param2.update({'forecast': forecast_name2})
                                param2.update({'sample_points': forecast2['sample_points']})
                                param2.update({'cmap': forecast2['colormap']})
                                param2.update({'data_unit': forecast2['data_unit']})
                                param2.update({'data_min': forecast2['data_min']})
                                param2.update({'data_max': forecast2['data_max']})
                                param2.update({'data_label': forecast2['data_label']})
                                param2.update({'lat_index': forecast2['lat_index']})
                                param2.update({'lon_index': forecast2['lon_index']})
                                param2.update({'forecast_range': forecast_hour_list})
                                param2.update({'gaussian': forecast2['gaussian']})
                                param2.update({'algorithm': forecast2['algorithm']})
                                param2.update({'prune': forecast2['prune']})
                                param2.update({'level_increment': forecast2['level_increment']})
                                param2.update({'model_res': forecast2['model_res']})
                                param2.update({'data_var_names': forecast2['data_var_names']})
                                param2.update({'height': forecast2['height']})

                            params = params1 + params2

                            print('Generating Plots...')
                            p = Pool(14) #2 forecasts at a time multiplied by 7 regions gives 14 processes we can run simultaneously
                            process_results = p.map(generateLocalPlot, params)
                            #Go through the process results and add each product to the correct state
                            for result in process_results:
                                final_links[result[0]][result[1]][result[2]][result[3]] += result[4]
                            
                            del params
                            del params1
                            del params2

    #Each model's json
    print('Writing JSON File...')
    writeJson(final_links, json_path, json_name)

    print('Replacing Operational Files...')
    renameFiles(path)
    print('Removing Temporary Files...')
    removeFiles(path)
    print("--- %s Seconds ---" % (time.time() - start_time))