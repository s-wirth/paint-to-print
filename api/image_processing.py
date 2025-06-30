import cv2
import numpy as np
import json
from helpers import *
from app_setup import *

def convertToGrayscale(pathToImage, imageName, folder):
    prepare_image(imageName, folder)
    image = cv2.imread(pathToImage)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'{folder}/{imageName}', grayImage)

def IP_create_contour_from_points(image):
    image_meta = json.loads(image)
    file = image_meta["fullPath"]
    cv_image = cv2.imread(file)
    pprint('##################################################')
    pprint(cv_image.shape)
    bounding_box_image = prepare_image(file, "opencv_store", "_bb")
    jsonFile = PATH_TO_IMAGE_PROCESSING_META
    with open(jsonFile, "r") as file:
        processing_meta = json.load(file)
    
    pprint('##################################################')
    pprint(processing_meta[str(image_meta["id"])])
    pprint('##################################################')
    tl = [processing_meta[str(image_meta["id"])]["topLeft"]["x"], processing_meta[str(image_meta["id"])]["topLeft"]["y"]]
    tr = [processing_meta[str(image_meta["id"])]["topRight"]["x"], processing_meta[str(image_meta["id"])]["topRight"]["y"]]
    br = [processing_meta[str(image_meta["id"])]["bottomRight"]["x"], processing_meta[str(image_meta["id"])]["bottomRight"]["y"]]
    bl = [processing_meta[str(image_meta["id"])]["bottomLeft"]["x"], processing_meta[str(image_meta["id"])]["bottomLeft"]["y"]]
    
    pprint('#############_______________________############')
    contour = [np.array([tl, tr, br, bl])]
    pprint(contour)
    pprint(bounding_box_image)
    pprint('#############_______________________############')
    cv2.drawContours(cv_image, contour, 0, (0, 255, 0), 2)
    cv2.imwrite(bounding_box_image, cv_image)
    