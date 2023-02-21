import numpy as np
import cv2
import glob
import imutils

image_paths = glob.glob('D:\PycharmProject\Master-Thesis\Image_processing\panorama\images_1\*.jpg')
images = []


for image in image_paths:
    img = cv2.imread(image)
    images.append(img)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
