import os
import json

path = '/home/scrump/containers/website/json/'

json_filename = "location_links.json"

json_data = {'location': 
        {'Fort-Worth': {
            'daily-forecast-link': 'https://api.weather.gov/gridpoints/FWD/70,103/forecast',
            'hourly-forecast-link': '"https://api.weather.gov/gridpoints/FWD/70,103/forecast/hourly"',
            'current-conditions-link': 'https://api.weather.gov/stations/KFWS/observations/latest?require_qc=false'
        },'Austin': {
            'daily-forecast-link': 'https://api.weather.gov/gridpoints/EWX/156,91/forecast',
            'hourly-forecast-link': 'https://api.weather.gov/gridpoints/EWX/156,91/forecast/hourly',
            'current-conditions-link': 'https://api.weather.gov/stations/KAUS/observations/latest?require_qc=false'
        }
             }
}

def writeJson(json_data):
    try:
        os.chmod(path + json_filename, 0o777)
    except:
        print('No JSON file to change permissions on.')
    with open(path + json_filename, "w") as f:
        json.dump(json_data, f)
        print('JSON saved to ' + json_filename)