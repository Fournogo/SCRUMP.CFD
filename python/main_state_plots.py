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

# MAIN FUNCTION
# MAIN FUNCTION
# MAIN FUNCTION
# MAIN FUNCTION
if __name__ == '__main__':
    #IMPORTANT VARIABLES
    ###################
    forecast_hours = 48 #NUMBER OF FORECAST HOURS
    ###################
    path = '/home/scrump/containers/website/html/goes/hrrr_data/' #PATH TO SAVE IMAGES
    json_filename = 'state-model-images' #FILENAME FOR JSON CONTAINING IMAGE PATHS
    usa_cities = pd.read_csv("/home/scrump/containers/website/python/model_files/USA_Major_Cities.csv")

    #Define the offset from the current time in order to get a sufficiently old model run
    model_utc_time = datetime.utcnow() - timedelta(hours=4, minutes=0)

    #Set range of times for forecast hour definitions
    DATES = pd.date_range(
        start=model_utc_time.strftime('%Y-%m-%d %H:00'),
        periods=1,
        freq="1H", #Changes by forecast model
    )

    #Set start time of the main part of the program for timing execution
    start_time = time.time()
    print('Getting GRIB2 Data...')

    #Define Herbie object
    H = FastHerbie(
        DATES,
        model="hrrr",
        product="subh",
        fxx=range(0, forecast_hours),
    )
    print(H.objects)
    #Pull the model description out of the Herbie object directly
    description = H.objects[0].product_description

    #Download and parse out reflectivity
    print('Preparing reflectivity data...')
    reflectivity_1000m = H.xarray("REFD:1000 m above", max_threads=50)
    print('Preparing temperature data...')
    #Download and parse temperature
    temp_2m = H.xarray("TMP:2 m above", max_threads=50)

    #Set 0 and negative reflectivities to NaN, convert Kelvin to Fahrenheit
    reflectivity_1000m["refd"] = reflectivity_1000m.refd.where(reflectivity_1000m.refd > 0)
    temp_2m["t2m"] = (temp_2m.t2m - 273.15) * (9/5) + 32

    #Pull state parameters out of file and add in important bits for reflectivity
    reflectivity_state_params = copy.deepcopy(default_state_params)
    for refd_param in reflectivity_state_params:
        refd_param['ds'] = reflectivity_1000m
        refd_param['city_csv'] = usa_cities
        refd_param['path'] = path
        refd_param['description'] = description
        refd_param['product'] = 'refd'
        refd_param['sample_points'] = False
        refd_param['cmap'] = cm.gist_ncar
        refd_param['data_unit'] = 'dBZ'
        refd_param['data_min'] = -10
        refd_param['data_max'] = 75
        refd_param['data_label'] = 'Derived Radar Reflectivity, dBZ'

    #Pull state parameters out of file and add in important bits for reflectivity
    temperature_state_params = copy.deepcopy(default_state_params)
    for t2m_param in temperature_state_params:
        t2m_param['ds'] = temp_2m
        t2m_param['city_csv'] = usa_cities
        t2m_param['path'] = path
        t2m_param['description'] = description
        t2m_param['product'] = 't2m'
        t2m_param['sample_points'] = True
        t2m_param['cmap'] = cm.nipy_spectral
        t2m_param['data_unit'] = 'F'
        t2m_param['data_min'] = -50
        t2m_param['data_max'] = 130
        t2m_param['data_label'] = 'Surface Temperature, Degrees F'

    #Merge parameters into a single state_params list
    #Not memory efficient but works for now
    merged_state_params = temperature_state_params + reflectivity_state_params
    merged_state_params = merged_state_params
    #Start multiprocess pool and generate plots
    print('Generating Plots...')
    p = Pool(14) #Set to number of total different plots we need to make and let the computer do the rest
    process_results = p.map(generateLocalPlot, merged_state_params)

    #Add all the paths and related location names to a single dictionary to write to JSON
    state_dict = {}
    #Add all the states as keys to a dictionary
    for state in default_state_params:
        state_dict.update({state['state']: {}})
    #Go through the process results and add each product to the correct state
    for result in process_results:
        state_dict[result[0]].update({result[1]: result[2]})

    print(state_dict)
    print('Writing JSON File...')
    writeJson(state_dict, path, json_filename)
    print('Replacing operational files...')
    renameFiles(path)
    print('Removing temporary files...')
    removeFiles(path)
    print("--- %s seconds ---" % (time.time() - start_time))