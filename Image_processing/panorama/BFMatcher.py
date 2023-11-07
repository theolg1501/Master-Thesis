import os
import time
import numpy
import cv2

def resize(img, scale_factor):
    # Assume img3 is the output from cv2.drawMatchesKnn
    height, width = img.shape[:2]

    # Resize the image
    img_resized = cv2.resize(img, (int(width * scale_factor), int(height * scale_factor)))

    return img_resized

# read images (option: resize)
img1 = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\2023-06-02-12-50-08.jpg', 0)
img1 = resize(img1, 1)

img2 = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\2023-06-02-12-50-17.jpg', 0)
img2 = resize(img2, 1)

# Initiate SIFT detector
sift = cv2.SIFT_create()

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# BFMatcher with default params
bf = cv2.BFMatcher()
start = time.time()
matches = bf.knnMatch(des1, des2, k=2)
end = time.time()

# Apply ratio test
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])

print("BFMatcher Time:", end - start)
print("BFMatcher Good Matches:", len(good))
print("BFMatcher Matches:", len(matches))

# Draw matches
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

img3_resized = resize(img3, 1)

# Display the resized image
cv2.imwrite('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\0817_bfmatcher_full.jpg', img3_resized)
cv2.imshow("Matches", img3_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()


if __name__ == '__main__':
    print('BFMatcher ends')
