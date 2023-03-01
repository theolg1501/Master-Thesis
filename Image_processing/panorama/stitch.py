import glob

import cv2
import numpy as np
import two_stitching_util


def get_dim(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    return dim


def resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR_EXACT)


input_imgs = [cv2.imread(file) for file in
              glob.glob('D:\PycharmProject\Master-Thesis\Image_processing\panorama\images_2\*.jpg')]

tmp = two_stitching_util.main(resize(input_imgs[5], get_dim(input_imgs[5], 0.1)),
                                         resize(input_imgs[6], get_dim(input_imgs[6], 0.1)))

cv2.imshow('12',tmp)
cv2.waitKey(0)