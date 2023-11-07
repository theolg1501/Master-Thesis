import cv2
import time
import matplotlib.pyplot as plt


def detect_and_describe(image, method):
    """
    Compute key points and feature descriptors using a specific method
    """

    assert method in ['SIFT', 'ORB', 'AKAZE'], \
        'Method not recognized. It must be one of "SIFT", "ORB" or "AKAZE"'

    # initialize the keypoint detector and local invariant descriptor
    if method == 'SIFT':
        descriptor = cv2.SIFT_create()
    elif method == 'ORB':
        descriptor = cv2.ORB_create()
    elif method == 'AKAZE':
        descriptor = cv2.AKAZE_create()

    # get keypoints and descriptors
    start = time.time()
    (kps, features) = descriptor.detectAndCompute(image, None)
    end = time.time()

    return (kps, features, end - start)

def resize(img, scale_factor):
    # Assume img3 is the output from cv2.drawMatchesKnn
    height, width = img.shape[:2]

    # Resize the image
    img_resized = cv2.resize(img, (int(width * scale_factor), int(height * scale_factor)))

    return img_resized


# read images (option: resize)
img = cv2.imread('D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\2023-06-02-12-50-08.jpg', 0)
img = resize(img, 0.05)
# load the image and convert it to grayscale


methods = ['SIFT', 'ORB', 'AKAZE']
info = {}

# detect and describe features for each method
for method in methods:
    (kps, features, time_taken) = detect_and_describe(img, method)
    info[method] = (kps, features, time_taken)
    print(f"Method: {method}, Keypoints detected: {len(kps)}, Time taken: {time_taken} seconds")

    # plot the keypoints
    img_kps = cv2.drawKeypoints(img, kps, None)
    plt.imshow(cv2.cvtColor(img_kps, cv2.COLOR_BGR2RGB))
    plt.title(f'Keypoints detected using {method}')
    # plt.savefig(f'D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\\{method}.png')
    plt.show()
