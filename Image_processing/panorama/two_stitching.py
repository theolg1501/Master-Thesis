import argparse
import glob
import sys
import cv2
import numpy as np
import two_stitching_util

parser = argparse.ArgumentParser(prog='two_stitching.py', description='Two_stitching sample.')

parser.add_argument('img', nargs='+', help='input images')

args = parser.parse_args()
imgs = []
i = 0
max_imgs = len(imgs)

for img_name in args.img:
    imgs = [cv2.imread(file) for file in sorted(glob.glob(args.img[0]))]


def stitch_loop(imgs):
    for index, image in enumerate(imgs):
        scale_percent = 10  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        if index != num_imags-1:
            imgs.append(two_stitching_util.main(cv2.resize(imgs[index], dim, interpolation=cv2.INTER_AREA),
                                            cv2.resize(imgs[index+1], dim, interpolation=cv2.INTER_AREA), index))
            print(len(imgs))
        else:
            del (imgs[0:num_imags])
            print(len(imgs))
            break

num_imags = len(imgs)
while i != max_imgs-1:
    stitch_loop(imgs)
    i+=1
if i == max_imgs-1:
    for image in imgs:
        cv2.imshow('panorama', image)


