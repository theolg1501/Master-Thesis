import os
import time
import numpy as np
import cv2


def resize(img, scale_factor):
    # Assume img3 is the output from cv2.drawMatchesKnn
    height, width = img.shape[:2]

    # Resize the image
    img_resized = cv2.resize(img, (int(width * scale_factor), int(height * scale_factor)))

    return img_resized


# read images (option: resize)
img1 = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\2023-06-02-12-50-08.jpg', 0)
img1 = resize(img1, 0.5)
print(img1.shape)
img2 = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\2023-06-02-12-50-17.jpg', 0)
img2 = resize(img2, 0.5)

# Initiate SIFT detector
sift = cv2.SIFT_create()

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN k-d tree parameters
FLANN_INDEX_KDTREE = 2
index_params = dict(algorithm=FLANN_INDEX_KDTREE)
search_params = dict(checks=50)

# FLANN k-means parameters


flann = cv2.FlannBasedMatcher(index_params, {})
start = time.time()
matches = flann.knnMatch(des1, des2, k=2)
end = time.time()

# Apply ratio test
good = []
good_without_list = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])
        good_without_list.append(m)

print("FLANN Time:", end - start)
print("FLANN Good Matches:", len(good))
print("FLANN Matches:", len(matches))

# Draw matches
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

img3_resized = resize(img3, 1)

# Display the resized image
# cv2.imwrite('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\0817_flann_full.jpg', img3_resized)
# cv2.imshow("Matches", img3_resized)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Prepare the lists of points
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_without_list]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_without_list]).reshape(-1, 1, 2)

# Step 2: Find homography using RANSAC and measure the elapsed time
start = time.time()
H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
elapsed_time = time.time() - start

print('Elapsed time using FLANN: ', elapsed_time)
print('Homography matrix: ')
print(H)

# Assuming you have the two images loaded as img1 and img2
# Step 3: Apply the homography to change the perspective of the second image
h1, w1 = img1.shape
h2, w2 = img2.shape

corners = np.array([
    [0, 0],
    [0, h2 - 1],
    [w2 - 1, h2 - 1],
    [w2 - 1, 0]
], dtype=np.float32)

# Apply the homography to the 4 corners of the second image
corners_transformed = cv2.perspectiveTransform(corners.reshape(-1, 1, 2), H)

# Get the bounds of the transformed corners
x_min, y_min = np.int0(corners_transformed.min(axis=0)[0])
x_max, y_max = np.int0(corners_transformed.max(axis=0)[0])

# Compute the size of the new resulting image , which it's the largest external rectangle
width_new, height_new = x_max - x_min, y_max - y_min

# Adjust the homography to shift to (0, 0). Move the image to right and down. OpenCV的默认坐标系为第四象限
H_shift = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])
H_transform = np.dot(H_shift, H)

# Warp the second image with the computed homography
warped_img = cv2.warpPerspective(img2, H_transform, (width_new, height_new))

# Step 4: Show the result
cv2.imwrite('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\warped_img_2.jpg', warped_img)
cv2.imshow('Warped Image', warped_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

if __name__ == '__main__':
    print('FLANN ends')
