import argparse
import glob
import sys
import cv2
import numpy as np
import two_stitching_util
from matplotlib import pyplot as plt
import largestinteriorrectangle as lir


parser = argparse.ArgumentParser(prog='two_stitching.py', description='Stitching images two by two.')
parser.add_argument('img', nargs='+', help='input images')

args = parser.parse_args()
imgs = []
imgs_tmp = []
row = 20
column = 1

input_imgs = [cv2.imread(file) for file in glob.glob(args.img[0])]
print(len(input_imgs))


def get_dim(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    return dim


def resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR_EXACT)

def remove_the_blackborder(image):
    # img = cv2.medianBlur(image, 5)  # 中值滤波，去除黑色边际中可能含有的噪声干扰
    b = cv2.threshold(image, 3, 255, cv2.THRESH_BINARY)  # 调整裁剪效果
    binary_image = b[1]  # 二值图--具有三通道
    binary_image = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)
    # print(binary_image.shape)     #改为单通道

    contours, _ = \
        cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    polygon = np.array([contours[0][:, 0, :]])
    rect = lir.lir(polygon)
    print(rect)
    x, y, w, h = rect
    res_image = image[y:y + h, x:x + w]
    return res_image

def stitch_loop(images, images_tmp, pos):  # max & pos are (row, column)
    panorama1 = two_stitching_util.main(images[0], images[1])
    images_tmp.append(remove_the_blackborder(panorama1))
    for index, image in enumerate(images):
        if 1 < index:
            panorama2 = two_stitching_util.main(images_tmp[pos], image)
            images_tmp[pos] = remove_the_blackborder(panorama2)
            cv2.imshow('image_tmp', images_tmp[pos])
            cv2.waitKey(0)
        else:
            continue
    return images_tmp


def main():
    for image in input_imgs:
        imgs.append(resize(image, get_dim(image, 0.1)))
    for i in range(1, column):
        stitch_loop(imgs[row * i:row * (i + 1)], imgs_tmp, i)

    cv2.imshow('panorama', imgs_tmp[0])
    cv2.waitKey(0)


main()
