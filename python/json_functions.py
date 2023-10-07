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
def writeJson(json_data, path, json_filename):
    json_file = path + json_filename + '.json'
    if not os.path.exists(json_file):
        try:
            os.chmod(json_file, 0o777)
        except:
            print('No JSON file to change permissions on.')
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
            print('JSON saved to ' + json_filename)
    else:
        print('JSON File Exists... Updating it')
        with open(json_file, 'r') as f:
            data = json.load(f)

        for model in json_data:
            for product in json_data[model]:
                data[model][product] = json_data[model][product]

        with open(json_file, 'w') as f:
            json.dump(data, f)