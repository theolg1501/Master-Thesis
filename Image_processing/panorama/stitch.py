import glob
import operator

import cv2
import numpy as np
import two_stitching_util


def stitch_loop(images, images_tmp, pos):  # max & pos are (row, column)
    panorama1 = images[0]+images[1]
    images_tmp.append(panorama1)
    for index, image in enumerate(images):
        if 1 < index:
            panorama2 = images_tmp[pos]+image
            images_tmp[pos] = panorama2
            print(images_tmp[pos])
        else:
            print(images_tmp[pos])
            continue
    return images_tmp


row = 4
column = 2
imgs_tmp = []
imgs = [0, 1, 2, 3, 4, 5, 6, 7]


def main():
    for i in range(0, column):
        stitch_loop(imgs[row * i:row * (i + 1)], imgs_tmp, i)

main()