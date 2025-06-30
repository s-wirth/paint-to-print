import os
import cv2
from app_setup import *
from generic_helpers import *



#######################################################################
# Image Processing Helper Functions                                 
#######################################################################



# ---------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------

def get_file_name(file):
    return file.split(".")[0]

def get_file_upload_url(file):
    return f'/uploads/{file}'


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
