import os
import json
from app_setup import *
from helpers.generic_helpers import *
from helpers.image_processing_helpers import *
from helpers.fs_helpers import *

def json_file_to_dict(file):
    pprint('json_file_to_dict',file)
    if os.path.getsize(file) == 0:
        with open(file, "w") as file:
            file.write(json.dumps({}, indent=4))
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data

def make_image_processing_meta(image, jsonFile):
    processing_meta = {}
    image_meta = json.loads(image)
    processing_meta = json_file_to_dict(jsonFile)
    if str(image_meta["id"]) not in processing_meta:
        processing_meta[image_meta["id"]] = image_meta
        with open(jsonFile, "w") as file:
            file.write(json.dumps(processing_meta, indent=4))
    return True

def update_processing_meta(image, newValues, jsonFile):
    newValues = json.loads(newValues)
    image_meta = json.loads(image)
    pprint('update_processing_meta')
    pprint(jsonFile)
    processing_meta = json_file_to_dict(jsonFile)
    if str(image_meta["id"]) not in processing_meta:
        make_image_processing_meta(image, jsonFile)
    processing_meta[str(image_meta["id"])].update(newValues)
    with open(jsonFile, "w") as file:
        file.write(json.dumps(processing_meta, indent=4))
    return True

def makeImageMetaData(files, jsonFile):
    imageMetaData = {}
    displayHeight = 500
    for id, file in enumerate(files, start=1):
        fileUploadURL = get_file_upload_url(file)
        fullPath = f'{os.getcwd()}/public{get_file_upload_url(file)}'
        imageHeight, imageWidth, _ = get_image_dimensions(fullPath)
        imageMetaData[id] = {
            "fileName": get_file_name(file),
            "customName": get_file_name(file),
            "fullPath": fullPath,
            "uploadURL": fileUploadURL,
            "id": id,
            "width": imageWidth,
            "height": imageHeight,
            "displayWidth": round((imageWidth / imageHeight) * displayHeight),
            "displayHeight": displayHeight,

        }
    with open(jsonFile, "w") as file:
        file.write(json.dumps(imageMetaData, indent=4))
    return True