import two_stitching_util
import largestinteriorrectangle as lir
import cv2
from matplotlib import pyplot as plt
import numpy as np


def get_dim(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    return dim


def resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR_EXACT)


def remove_the_blackborder(image):
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

    # cv2.imshow('lir', crop)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # edges_y, edges_x = np.where(binary_image == 255)  ##h, w
    # bottom = min(edges_y)
    # top = max(edges_y)
    # height = top - bottom
    #
    # left = min(edges_x)
    # right = max(edges_x)
    # height = top - bottom
    # width = right - left
    #
    # res_image = image[bottom:bottom + height, left:left + width]
    #
    # plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.imshow(image)
    # plt.subplot(1, 2, 2)
    # plt.imshow(res_image)
    # # plt.savefig(os.path.join("res_combine.jpg"))
    # plt.show()
    return res_image


img1 = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\images_2\IMG_5.JPG')
img2 = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\images_2\IMG_6.JPG')

img1_resize = resize(img1, get_dim(img1, 0.2))
img2_resize = resize(img2, get_dim(img2, 0.2))

img1_cropped = remove_the_blackborder(img1_resize)
img2_cropped = remove_the_blackborder(img2_resize)

cv2.imshow('img1', img1_cropped)
cv2.imshow('img2', img2_cropped)

cv2.imwrite('pano56.jpg', two_stitching_util.main(img1_resize, img2_cropped))
cv2.waitKey(0)
