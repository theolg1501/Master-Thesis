import argparse
import glob
import sys

import cv2
import numpy as np


def draw_matches(img1, img2, pts1, pts2):
    # Put images side-by-side into 'image'
    (h1, w1) = img1.shape[:2]
    (h2, w2) = img2.shape[:2]
    matches_image = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    matches_image[:h1, :w1] = img1
    matches_image[:h2, w1:w1 + w2] = img2

    # Draw yellow lines connecting corresponding features.
    for (x1, y1), (x2, y2) in zip(np.int32(pts1), np.int32(pts2)):
        cv2.line(matches_image, (x1, y1), (x2 + w1, y2), (0, 255, 255))

    return matches_image


def main(image1, image2):
    ### MAIN PROGRAM

    ### 1. FEATURE DETECTION AND DESCRIPTION

    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    ### 1.1 Extract keypoints and descriptors of gray1

    # detect and extract SIFT features from the image
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)

    # Print, display and save the result
    print('{0} features detected in image1'.format(len(keypoints1)))
    features1 = cv2.drawKeypoints(gray1, keypoints1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imwrite('Features1.jpg', features1)
    cv2.imshow('Features 1', features1)
    cv2.waitKey(0)

    ### 1.2 Extract keypoints and descriptors of gray2

    # detect and extract SIFT features from the image
    sift = cv2.SIFT_create()
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Print, display and save the result
    print('{0} features detected in image2'.format(len(keypoints2)))
    features2 = cv2.drawKeypoints(gray2, keypoints2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imwrite('Features2.jpg', features2)
    cv2.imshow('Features 2', features2)
    cv2.waitKey(0)

    ### 2. MATCH DESCRIPTORS

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    # Match descriptors
    matches = bf.match(descriptors1, descriptors2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # convert first 10 matches from KeyPoint objects to NumPy arrays
    points1 = np.float32([keypoints1[m.queryIdx].pt for m in matches[0:10]])
    points2 = np.float32([keypoints2[m.trainIdx].pt for m in matches[0:10]])

    # Print, display and save the result
    print('{0} features matched'.format(len(points1)))
    match = draw_matches(image1, image2, points1, points2)
    cv2.imshow('Matching', match)
    cv2.waitKey(0)

    ### 3. ESTIMATE A HOMOGRAPHY MATRIX

    # Convert the keypoints from KeyPoint objects to NumPy arrays
    src_pts = points2.reshape(-1, 1, 2)
    dst_pts = points1.reshape(-1, 1, 2)

    # Compute the homography

    # find homography
    homography, m = cv2.findHomography(src_pts, dst_pts)

    ### 4. WARPING AND BLENDING

    ### 4.1 Calculate the size and offset of the stitched panorama

    # Compute de coordinates of image2 corners in image1
    height2 = image2.shape[0]
    width2 = image2.shape[1]
    corners2 = np.float32([[[0, 0], [0, height2 - 1], [width2 - 1, height2 - 1], [width2 - 1, 0]]])
    transformedCorners2 = cv2.perspectiveTransform(corners2, homography)
    print("TransformedCorners2:")
    print(transformedCorners2)

    # Calculate the size and offset of the stitched panorama.
    # offset is the position of image 1 relative to the top-left corner of the stitched panorama

    # compute de coordinates of image2 corners in image1
    h2 = image2.shape[0]
    w2 = image2.shape[1]
    corners2 = np.float32([[[0, 0], [0, h2 - 1], [w2 - 1, h2 - 1], [w2 - 1, 0]]])
    transformedCorners2 = cv2.perspectiveTransform(corners2, homography)

    offset = (0, 0)
    size = (1500, 1500)

    print('Size of the stitched panorama: {0}'.format(size))
    print('Offset of the stitched panorama: {0}'.format(offset))

    # Update the homography to shift by the offset
    homography[0:2, 2] += offset
    print("Homography:")
    print(homography)

    ## 4.2 Combine images into a panorama

    # Transform image 2
    panorama = cv2.warpPerspective(image2, homography, size)
    cv2.imshow('Warped image 2', panorama)
    cv2.waitKey(0)

    # Copy image 1 to panorama
    (height1, width1) = image1.shape[0:2]
    panorama[offset[1]: offset[1] + height1, offset[0]: offset[0] + width1] = image1
    cv2.imshow('Panorama', panorama)
    cv2.waitKey(0)

    # Save panorama
    # cv2.imwrite('D:\PycharmProject\Master-Thesis\Image_processing\panorama\images_temp\Panoramatemp_%d.jpg'%d, panorama)
    # Close all windows
    # cv2.destroyAllWindows()
    print('------------')
    return panorama


scale_percent = 10  # percent of original size
width = int(1920 * scale_percent / 100)
height = int(1080 * scale_percent / 100)
dim = (width, height)
main(cv2.resize(cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama/test_0606/2/5.jpg'), dim,
                interpolation=cv2.INTER_AREA),
     cv2.resize(cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama/test_0606/2/6.jpg'), dim,
                interpolation=cv2.INTER_AREA))
