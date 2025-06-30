import cv2
from app_setup import *
from generic_helpers import *
from helpers import *


# ---------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------

_EXTENSIONS_ = ["jpg", "png", "jpeg", "JPG", "PNG", "JPEG"]

# ---------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------

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
        return True
    pprint (f'File is not a valid image: {file}, only {", ".join(_EXTENSIONS_)} files are allowed.')
    return False

def get_image_dimensions(image):
    dimensions = cv2.imread(image).shape
    pprint(f'Image dimensions: {dimensions}')
    return dimensions


def make_processing_image_name(file, sub_dir = '', suffix = '_processed', fileType = 'jpg'):
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
        file_name = file.split("/")[-1]
        return (
            PATH_TO_IMAGES
            + ending_slash(sub_dir)
            + file_name.split(".")[0]
            + suffix
            + '.'
            + fileType
        )
    return file.split(".")[0] + suffix + '.' + fileType

def prepare_image(file, subDir = '', suffix = '', fileType = 'jpg'):
    if subDir != '' and not check_directory(ending_slash(subDir)):
        check_or_create_directory(ending_slash(subDir))
    if check_valid_image(file):
        return make_processing_image_name(file, subDir, suffix, fileType)
