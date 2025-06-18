import cv2
import os
from helpers import pprint

def processContour(pathToImage, imageName, folder):
    pprint('pathToImage', pathToImage)
    pprint('folder', folder)
    newName = 'contour_' + imageName.split(".")[0] + '.jpg'
    contouredImage = os.path.join(folder, newName)
    # Load the pathToImage
    img = cv2.imread(pathToImage)

    # convert to grayscale
    cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edged = cv2.Canny(img, 120, 890)
    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(edged, 255, 1, 1, 11, 2)
    cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
    thresh = cv2.dilate(thresh, None, iterations=50)
    thresh = cv2.erode(thresh, None, iterations=50)

    # Find the contours
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # For each contour, find the bounding rectangle and draw it
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 20000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    pprint('contouredImage', contouredImage)
    cv2.imwrite(contouredImage, img)

    return contouredImage