import cv2
import os
import helpers

def convertToGrayscale(pathToImage, imageName, folder):
    helpers.prepare_image(imageName, folder)
    image = cv2.imread(pathToImage)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'{folder}/{imageName}', grayImage)