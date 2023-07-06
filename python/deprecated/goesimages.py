#!/usr/bash/python3
import requests
from bs4 import BeautifulSoup
import glob
import os
import json
import stat

path = ''
url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/sp/GEOCOLOR/'
image_size = '600x600'
num_images = 36

json_filename = "last_link.json"

def getNewestLinks(num_links):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_list = []
    for link in soup.find_all('a'):
        link_list.append(link.get('href'))

    count = -1
    indicies = []

    for link in link_list:
        count += 1
        if image_size not in link:
            indicies.append(count)
        elif len(link) < 31:
            indicies.append(count)
    for i in sorted(indicies, reverse=True):
        del link_list[i]

    link_dict = {}
    for link in link_list:
        link_dict.update({link[:11]: link})
    date_keys = list(link_dict.keys())
    date_keys.sort()
    sorted_dict = {i: link_dict[i] for i in date_keys}
    links = list(sorted_dict.values())[-num_links:]
    print(links)
    return links

def saveImages(link_list):
    count = len(link_list)
    for link in link_list:
        get_url = url + link

        if len(link_list) == 1:
            if checkJSON(link) == True:
                print('Latest image is already in sync! Cancelling...')
                return False

        if count == 1:
            writeJSON(link)
        image_response = requests.get(get_url)

        if image_response.status_code == 200:
            print("Request successful")

            # Assumes you want to append an image instead of overwrite if you're only requesting 1 image
            if len(link_list) == 1:
                with open(str(path + '0.jpg'), 'wb') as f:
                    f.write(image_response.content)
                    print('Image saved to ' + '0.jpg')
            else:
                with open(str(path + str(count) + '.jpg'), 'wb') as f:
                    f.write(image_response.content)
                    print('Image saved to ' + str(count) + '.jpg')
                count -= 1
        else:
            print("Request failure")
    return True

def removeFiles():
    jpg_files = glob.glob(os.path.join(path, "*.jpg"))
    if jpg_files:
        print("Removing existing .jpg files..")
        for file_path in jpg_files:
            os.remove(os.path.join(file_path))
    else:
        print("No .jpg files found... continuing.")
    json_files = glob.glob(os.path.join(path, "*.json"))
    if json_files:
        print("Removing existing .json files..")
        for file_path in json_files:
            os.remove(os.path.join(file_path))
    else:
        print("No .json files found... continuing.")

def addOneToFileNames():
    jpg_files = glob.glob(os.path.join(path, "*.jpg"))
    if not jpg_files:
        print("No .jpg files found in the folder.")
        return False
    else:
        file_names = []
        for file_path in jpg_files:
            file_names.append(int(os.path.basename(file_path)[:-4]))
        file_names.sort(reverse=True)
        for file_name in file_names:
            os.rename(os.path.join(path, (str(file_name) + ".jpg")),os.path.join(path, (str(file_name+1) + ".jpg")))
            print("Renamed " + str(file_name) + ".jpg to " + str(file_name+1) + ".jpg")

def removeBiggestFileName():
    file_names = []
    jpg_files = glob.glob(os.path.join(path, "*.jpg"))
    for file_path in jpg_files:
        file_names.append(int(os.path.basename(file_path)[:-4]))
    file_names.sort()
    os.remove(os.path.join(path, (str(file_names[-1]) + ".jpg")))
    print("Deleted " + (str(file_names[-1]) + ".jpg"))

def writeJSON(link):
    json_data = {
        'Newest': link,
    }
    with open(path + json_filename, "w") as f:
        json.dump(json_data, f)
        print('JSON saved to ' + json_filename)
    os.chmod((path + json_filename), stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
def checkJSON(link):
    with open(path + json_filename, 'r') as f:
        json_data = json.load(f)
        newest_link = json_data['Newest']
    if link == newest_link:
        # Return True for match - means the link is the same as the most recent one
        print("LINK MATCH")
        return True
    else:
        # Return False for no match - means the link is new
        return False

def getjpgNumber():
    jpg_files = glob.glob(os.path.join(path, "*.jpg"))
    return len(jpg_files)

def maintain():
    links = getNewestLinks(1)
    success = saveImages(links)
    if success != False:
        addOneToFileNames()
        removeBiggestFileName()

def start():
    removeFiles()
    links = getNewestLinks(num_images)
    saveImages(links)