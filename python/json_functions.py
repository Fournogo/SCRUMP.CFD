import glob
import os
import json

# REMOVE ALL FILES IN THE WORKING PATH TO KEEP JUST THE FILES IN THE OPERATIONAL PATH
def removeFiles(path):
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

# RENAME FILES FUNCTION, MOVES WORKING DIR FILES TO OPERATIONAL FOLDER
def renameFiles(path):
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

# WRITE JSON DATA TO FILE
def writeJson(data, path, json_filename):
    json_data = data
    try:
        os.chmod(path + json_filename, 0o777)
    except:
        print('No JSON file to change permissions on.')
    with open(path + json_filename + '.json', "w") as f:
        json.dump(json_data, f)
        print('JSON saved to ' + json_filename)