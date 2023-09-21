import requests
from bs4 import BeautifulSoup
import json
import os

url = 'https://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=32.7529204&lon=-97.3342545&product=time-series&sky=sky'

json_filename = "sky_cover_data.json"
path = '/home/scrump/containers/website/html/json/'
city_file = '/home/scrump/containers/website/html/json/cities.json'

final_data = {}

def getLatestValues(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    sky_values = []
    for value in soup.find_all('value'):
        sky_values.append(value.contents[0])

    time_codes = []
    for time_code in soup.find_all('start-valid-time'):
        time_codes.append(time_code.contents[0])

    data_array = []
    if len(sky_values) == len(time_codes):
        for i in range(len(sky_values)):
            sky_cover_array = [time_codes[i], sky_values[i]]
            data_array.append(sky_cover_array)
    else:
        print('TIME AND CLOUD COVER DATA DO NOT MATCH')

    return data_array

def writeJson(values):
    try:
        os.chmod(path + json_filename, 0o777)
    except:
        print('No JSON file to change permissions on.')
    with open(path + json_filename, "w") as f:
        json.dump(values, f)
        print('JSON saved to ' + json_filename)

def main():
    file = open(city_file)
    json_data = json.loads(file.read())

    for city in json_data['cities']:
        coordinates = city['coordinates']
        city_name = city['city']
        url = 'https://digital.mdl.nws.noaa.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=' + str(coordinates[0]) + '&lon=' + str(coordinates[1]) +'&product=time-series&sky=sky'
        data_values = getLatestValues(url)
        final_data.update({city_name: data_values})

    writeJson(final_data)

main()