import time

import matplotlib.cm as cm

from herbie import FastHerbie
import pandas as pd
from datetime import datetime, timedelta

from multiprocessing import Pool

from state_plots import generateLocalPlot
from json_functions import writeJson,removeFiles,renameFiles
from state_parameters import state_params as default_state_params

import copy
import re

#IMPORTANT VARIABLES
###################
path = '/home/scrump/containers/website/html/goes/model_data/' #PATH TO SAVE IMAGES
json_path = '/home/scrump/containers/website/html/goes/json/'
usa_cities = pd.read_csv('/home/scrump/containers/website/python/model_files/USA_Major_Cities.csv')
json_name = 'model_data'

#Define the offset from the current time in order to get a sufficiently old model run
start_utc_time = datetime.utcnow() - timedelta(hours=2, minutes=0)

def convertRefd(ds, forecast_name):
    ds[forecast_name] = ds.refd.where(ds.refd > 0)
    return ds

def convertT2m(ds, forecast_name):
    ds[forecast_name] = (ds.t2m - 273.15) * (9/5) + 32
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
                         {  'name':'refd',
                            'search': 'REFD:1000 m above',
                            'conversion': convertRefd,
                            'sample_points': False,
                            'colormap': cm.gist_ncar,
                            'data_unit': 'dBz',
                            'data_min': -10,
                            'data_max': 75,
                            'data_label': 'Derived Radar Reflectivity, dBZ',
                            'lat_index': 'y',
                            'lon_index': 'x',
                        },
                        {   'name': 't2m',
                            'search': 'TMP:2 m above',
                            'conversion': convertT2m,
                            'sample_points': True,
                            'colormap': cm.nipy_spectral,
                            'data_unit': 'F',
                            'data_min': -50,
                            'data_max': 130,
                            'data_label': 'Surface Temperature, Degrees F',
                            'lat_index': 'y',
                            'lon_index': 'x',
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
                        {   'name': 'refd',
                            'search': 'REFD:1000 m above',
                            'conversion': convertRefd,
                            'sample_points': False,
                            'colormap': cm.gist_ncar,
                            'data_unit': 'dBz',
                            'data_min': -10,
                            'data_max': 75,
                            'data_label': 'Derived Radar Reflectivity, dBZ',
                            'lat_index': 'y',
                            'lon_index': 'x',
                        },
                        {   'name': 't2m',
                            'search': 'TMP:2 m above',
                            'conversion': convertT2m,
                            'sample_points': True,
                            'colormap': cm.nipy_spectral,
                            'data_unit': 'F',
                            'data_min': -50,
                            'data_max': 130,
                            'data_label': 'Surface Temperature, Degrees F',
                            'lat_index': 'y',
                            'lon_index': 'x',
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
                            {   'name': 'refd',
                                'search': 'REFD:1000 m above',
                                'conversion': convertRefd,
                                'sample_points': False,
                                'colormap': cm.gist_ncar,
                                'data_unit': 'dBz',
                                'data_min': -10,
                                'data_max': 75,
                                'data_label': 'Derived Radar Reflectivity, dBZ',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                            },
                            {   'name': 't2m',
                                'search': 'TMP:2 m above',
                                'conversion': convertT2m,
                                'sample_points': True,
                                'colormap': cm.nipy_spectral,
                                'data_unit': 'F',
                                'data_min': -50,
                                'data_max': 130,
                                'data_label': 'Surface Temperature, Degrees F',
                                'lat_index': 'latitude',
                                'lon_index': 'longitude',
                            }
                        ]
                    }
                }    
            }
}

#Regex pattern for getting frequency integer from string
pattern = r'(\d+)H'

#Set start time of the main part of the program for timing execution
start_time = time.time()

if __name__ == '__main__':

    final_links = {}

    for model_name in models:
        model = models[model_name]
        final_links.update({model_name: {}})

        for product_name in model['product']:
            product = model['product'][product_name]

            #Not all of these models run every hour. Make sure the requested hour will work.
            if start_utc_time.hour % product['run_freq'] != 0:
                continue

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
                    start=start_utc_time.strftime('%Y-%m-%d %H:00'),
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

                        params1 = copy.deepcopy(default_state_params)
                        params2 = copy.deepcopy(default_state_params)

                        forecast1 = product['forecast'][pos]
                        forecast2 = product['forecast'][pos + 1]

                        forecast_name1 = forecast1['name']
                        forecast_name2 = forecast2['name']

                        if i == 0:
                            final_links[model_name][product_name].update({forecast_name1: {}})
                            final_links[model_name][product_name].update({forecast_name2: {}})
                            for state in default_state_params:
                                final_links[model_name][product_name][forecast_name1].update({state['state']: []})
                                final_links[model_name][product_name][forecast_name2].update({state['state']: []})

                        print('Downloading GRIB Files and Parsing: ' + forecast_name1)
                        ds1 = H.xarray(forecast1['search'], max_threads=50)
                        ds1 = forecast1['conversion'](ds1, forecast_name1)

                        print('Downloading GRIB Files and Parsing: ' + forecast_name2)
                        ds2 = H.xarray(forecast2['search'], max_threads=50)
                        ds2 = forecast2['conversion'](ds2, forecast_name2)

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