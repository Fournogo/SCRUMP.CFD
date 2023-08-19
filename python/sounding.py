#!/usr/bash/python3
import requests
from bs4 import BeautifulSoup
import glob
import os
import json

path = '/home/scrump/containers/website/html/goes/sounding/'
url = 'https://www.spc.noaa.gov/exper/soundings/'
num_images = 1

city_file = '/home/scrump/containers/website/html/json/cities.json'

file = open(city_file)
json_data = json.loads(file.read())
three_letter_code = []
for city in json_data['cities']:
    code = city['sounding_code']
    three_letter_code.append(code)
    
json_filename = "sounding_link.json"

def getNewestLinks(num_links):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_list = []
    for link in soup.find_all('a'):
        link_list.append(link.get('href'))

    #count = -1
    #indicies = []

    links = {}
    for code in three_letter_code:
        count = -1
        indicies = []
        for link in link_list:
            count += 1
            if link[0:6] != '/exper' or len(link) < 26:
                indicies.append(count)
                continue
            if link[23:25] != '12' and link[23:25] != '00':
                indicies.append(count)

        for i in sorted(indicies, reverse=True):
            del link_list[i]
        link_dict = {}
        for link in link_list:
            link = link + code + '.gif'
            link_dict.update({link[17:25]: link})

        date_keys = list(link_dict.keys())
        date_keys.sort()
        sorted_dict = {i: link_dict[i] for i in date_keys}
        link = list(sorted_dict.values())[-num_links:]
        links.update({code: link[0]})

    return links

def removeFiles():
    json_files = glob.glob(os.path.join(path, "*.json"))
    if json_files:
        print("Removing existing .json files..")
        for file_path in json_files:
            os.remove(os.path.join(file_path))
    else:
        print("No .json files found... continuing.")

def writeJson(links):
    json_data = links
    #json_data = {}
    #for i in range(len(links)):
        #json_data[i] = links[i]
    try:
        os.chmod(path + json_filename, 0o777)
    except:
        print('No JSON file to change permissions on.')
    with open(path + json_filename, "w") as f:
        json.dump(json_data, f)
        print('JSON saved to ' + json_filename)

def maintain():
    links = getNewestLinks(num_images)
    writeJson(links)

def start():
    removeFiles()
    links = getNewestLinks(num_images)
    writeJson(links)

maintain()