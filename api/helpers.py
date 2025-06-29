import sys
import os
import math
import json
import cv2


#######################################################################
# General Helper Functions                                 
#######################################################################

# ---------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------

def pprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


#######################################################################
# Image Processing Helper Functions                                 
#######################################################################

# ---------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------

_EXTENSIONS_ = ["jpg", "png", "jpeg", "JPG", "PNG", "JPEG"]


# ---------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------

def ending_slash(path):
    """
    Adds a trailing slash to a given path if it does not already exist.

    Parameters
    ----------
    path : str
        The path to add the trailing slash to.

    Returns
    -------
    str
        The path with a trailing slash.
    """
    if path[-1] != '/':
        path += '/'
    return path

def check_directory(dirName):
    """
    Checks if a given directory path exists.

    Parameters
    ----------
    dirName : str
        The directory path to check.

    Returns
    -------
    bool
        True if the directory exists, False otherwise.
    """
    return os.path.exists(ending_slash(dirName))

def check_or_create_directory(dirName):
    """
    Creates a sub-directory if it does not already exist.

    Parameters
    ----------
    dirName : str
        The name of the sub-directory to create.

    """
    if not check_directory(dirName):
        os.makedirs(dirName)
        pprint(f'Created sub directory: {dirName}')
    else:
        pprint(f'Sub directory exists: {dirName}')


def find_file(file):
    """
    Checks if a given file exists.

    Parameters
    ----------
    file : str
        The file path to check.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    pprint(f'Searching for file: {file}')
    if os.path.exists(file):
        pprint(f'File found: {file}')
        return True
    else:
        pprint(f'File not found: {file}')
        return False

def check_valid_image(file):
    """
    Checks if a given file exists and is a valid image.

    Parameters
    ----------
    file : str
        The file path to check.

    Returns
    -------
    bool
        True if the file exists and is a valid image, False otherwise.
    """
    if file.split(".")[1] in _EXTENSIONS_:
        pprint (f'File is a valid image: {file}')
        return True
    else:
        pprint (f'File is not a valid image: {file}, only {", ".join(_EXTENSIONS_)} files are allowed.')
        return False

def get_image_dimensions(image):
    dimensions = cv2.imread(image).shape
    pprint(f'Image dimensions: {dimensions}')
    return dimensions

def get_file_name(file):
    return file.split(".")[0]

def get_file_upload_url(file):
    return f'/uploads/{file}'

def make_image_processing_meta(image, jsonFile):
    processing_meta = {}
    image_meta = json.loads(image)
    if os.path.getsize(jsonFile) == 0:
        with open(jsonFile, "w") as file:
            processing_meta[image_meta["id"]] = image_meta
            file.write(json.dumps(processing_meta, indent=4))
    else: 
        with open(jsonFile, "r") as file:
            processing_meta = json.load(file)
        if str(image_meta["id"]) not in processing_meta:
            processing_meta[image_meta["id"]] = image_meta
            with open(jsonFile, "w") as file:
                file.write(json.dumps(processing_meta, indent=4))
    return True

def update_processing_meta(image, newValues, jsonFile):
    newValues = json.loads(newValues)
    image_meta = json.loads(image)
    pprint('##################################################')
    pprint(newValues)
    pprint(image_meta)
    with open(jsonFile, "r") as file:
        processing_meta = json.load(file)
    if image_meta["id"] not in processing_meta:
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
            

def make_processing_file_name(file, sub_dir = '', suffix = '_processed', fileType = 'jpg'):
    """
    Generates a new file name with a specified suffix and file type, optionally
    including a sub-directory.

    Parameters
    ----------
    file : str
        The original file name.
    sub_dir : str, optional
        The sub-directory to include in the new file name, default is an empty string.
    suffix : str, optional
        The suffix to append to the file name, default is '_processed'.
    fileType : str, optional
        The file extension for the new file name, default is 'jpg'.

    Returns
    -------
    str
        The newly generated file name with the specified suffix, file type, and
        optionally a sub-directory.
    """
    if sub_dir != '':
        return ending_slash(sub_dir) + file.split(".")[0] + suffix + '.' + fileType
    return file.split(".")[0] + suffix + '.' + fileType

def prepare_image(file, subDir = '', suffix = '', fileType = 'jpg'):
    if subDir != '' and not check_directory(ending_slash(subDir)):
        check_or_create_directory(ending_slash(subDir))
    if check_valid_image(file):
        return make_processing_file_name(file, subDir, suffix, fileType)
