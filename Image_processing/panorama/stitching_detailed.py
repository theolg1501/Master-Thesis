import cv2
import numpy as np
import os


def stitch_images(images, ratio=0.75, reproj_thresh=4.0, use_sift=True, resize_factor=None):
    if use_sift:
        feature_extractor = cv2.SIFT_create()
    else:
        feature_extractor = cv2.ORB_create()

    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

    # result = cv2.resize(images[0], (int(images[0].shape[1] * resize_factor), int(images[0].shape[0] * resize_factor)))
    result = images[0]
    for i in range(1, len(images)):
        result, _, _ = stitch(result, images[i], feature_extractor, matcher, ratio, reproj_thresh, resize_factor)

    return result


def stitch(imageA, imageB, feature_extractor, matcher, ratio, reproj_thresh, resize_factor):
    if resize_factor:
        imageB = cv2.resize(imageB, (int(imageB.shape[1] * resize_factor), int(imageB.shape[0] * resize_factor)))

    kpsA, featuresA = feature_extractor.detectAndCompute(imageA, None)
    kpsB, featuresB = feature_extractor.detectAndCompute(imageB, None)

    raw_matches = matcher.knnMatch(featuresA, featuresB, 2)
    matches = []

    for m, n in raw_matches:
        if m.distance < ratio * n.distance:
            matches.append((m.trainIdx, m.queryIdx))

    if len(matches) > 4:
        ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
        ptsB = np.float32([kpsB[i].pt for (i, _) in matches])

        H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reproj_thresh)

        stitched = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

        # imageB = cv2.resize(imageB, (stitched.shape[1], stitched.shape[0]))

        stitched[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        return stitched, kpsA, kpsB
    else:
        return None


def main():
    input_folder = 'D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\images_2'
    output_file = 'D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\\test_0606\panorama.jpg'

    images = [cv2.imread(os.path.join(input_folder, file)) for file in os.listdir(input_folder) if
              file.endswith(('.jpg', '.jpeg', '.png', '.JPG'))]

    rotated_images = []
    # for image in images:
    #     rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #     rotated_images.append(rotated)

    panorama = stitch_images(images, resize_factor=0.5)

    if panorama is None:
        print("Failed to stitch images")
        return

    cv2.imshow("Panorama", panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite(output_file, panorama)


if __name__ == '__main__':
    main()
