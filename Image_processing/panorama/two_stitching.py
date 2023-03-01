import argparse
import glob
import sys
import cv2
import numpy as np
import two_stitching_util

parser = argparse.ArgumentParser(prog='two_stitching.py', description='Stitching images two by two.')
parser.add_argument('img', nargs='+', help='input images')

args = parser.parse_args()
imgs = []
imgs_tmp = []
row = 4
column = 2

input_imgs = [cv2.imread(file) for file in glob.glob(args.img[0])]
print(len(input_imgs))


def get_dim(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    return dim


def resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR_EXACT)


def stitch_loop(images, images_tmp, pos):  # max & pos are (row, column)
    panorama1 = two_stitching_util.main(images[0], images[1])
    images_tmp.append(panorama1)
    for index, image in enumerate(images):
        if 1 < index:
            panorama2 = two_stitching_util.main(images_tmp[pos], image)
            images_tmp[pos] = panorama2
        else:
            continue
    return images_tmp


def main():
    for image in input_imgs:
        imgs.append(resize(image, get_dim(image, 0.1)))
    for i in range(0, column):
        stitch_loop(imgs[row * i:row * (i + 1)], imgs_tmp, i)

    cv2.imshow('panorama', two_stitching_util.main(imgs_tmp[0], imgs_tmp[1]))
    cv2.waitKey(0)
    # print(len(imgs_tmp))
    # stitch_loop(imgs_tmp, imgs_tmp, column)
    #
    #
    # for i in imgs_tmp:
    #     cv2.imshow('panorama', i)
    #     cv2.waitKey(0)


if __name__ == '__main__':
    main()
