import cv2
import numpy as np
from matplotlib import pyplot as plt


def plot_image(img, figsize=(5, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def plot_images(imgs, figsize=(5, 5)):
    fig, axs = plt.subplots(1, len(imgs), figsize=figsize)
    for col, img in enumerate(imgs):
        axs[col].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def get_dim(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    return dim


def resize(img, dim):
    return cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR_EXACT)


def get_features(img):
    sift = cv2.SIFT_create()
    features = cv2.detail.computeImageFeatures2(sift, img)
    keypoints = cv2.drawKeypoints(img, features.getKeypoints(), None)
    # plot_image(keypoints, (15, 10))
    return features


def match_features(features1, features2):
    matcher = cv2.detail_AffineBestOf2NearestMatcher()
    feature_matched = matcher.apply(features1, features2)
    matcher.collectGarbage()
    return feature_matched


def BF_mathcer(img1, img2):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return good


def draw_matches(img1, features1, img2, features2, match12):
    keypoints1 = features1.getKeypoints()
    keypoints2 = features2.getKeypoints()
    matches = match12.getMatches()
    return cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None)

def estimate_largest_interior_rectangle(mask):
    # largestinteriorrectangle is only imported if cropping
    # is explicitly desired (needs some time to compile at the first run!)
    import largestinteriorrectangle

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not hierarchy.shape == (1, 1, 4) or not np.all(hierarchy == -1):
        print("Invalid Contour. Try without cropping.")
    contour = contours[0][:, 0, :]

    lir = largestinteriorrectangle.lir(mask > 0, contour)
    lir = Rectangle(*lir)
    return lir


img1 = cv2.imread('/Users/chang/Documents/GitHub/Master-Thesis/Image_processing/panorama/images_2/1.JPG')
img2 = cv2.imread('/Users/chang/Documents/GitHub/Master-Thesis/Image_processing/panorama/images_2/2.JPG')
features1 = get_features(resize(img1, get_dim(img1, 0.2)))
features2 = get_features(resize(img2, get_dim(img2, 0.2)))

# plot_image(draw_matches(img1, features1, img2, features2, match_features(features1, features2)), (20, 10))

img3 = BF_mathcer(resize(img1, get_dim(img1, 0.2)), resize(img2, get_dim(img2, 0.2)))
plot_image(img3, (20,10))
