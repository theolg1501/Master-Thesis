import cv2
import numpy as np
import glob
import argparse

# 构建参数解析器
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True, help="文件夹路径")
ap.add_argument("-o", "--output", required=True, help="输出全景图路径")
ap.add_argument("-s", "--scale", type=float, default=0.5, help="缩放比例")
ap.add_argument("-m", "--method", choices=["SIFT", "SURF", "ORB"], default="SIFT", help="特征点检测算法")
args = vars(ap.parse_args())

# 加载图像
image_files = sorted(glob.glob(args["folder"] + "/*.jpg") + glob.glob(args["folder"] + "/*.png"))
if len(image_files) < 2:
    print("需要至少两张图片才能拼接全景图")
    exit()
images = []
for image_file in image_files:
    image = cv2.imread(image_file)
    image = cv2.resize(image, None, fx=args["scale"], fy=args["scale"])
    images.append(image)

# 初始化特征点检测器
if args["method"] == "SIFT":
    detector = cv2.SIFT_create()
elif args["method"] == "SURF":
    detector = cv2.xfeatures2d.SURF_create()
else:
    detector = cv2.ORB_create()

# 提取特征点和计算描述符
keypoints = []
descriptors = []
for image in images:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kp, des = detector.detectAndCompute(gray, None)
    keypoints.append(kp)
    descriptors.append(des)

# 匹配特征点
matches = []
for i in range(len(images) - 1):
    matcher = cv2.BFMatcher()
    raw_matches = matcher.knnMatch(descriptors[i], descriptors[i+1], k=2)
    good_matches = []
    for m in raw_matches:
        if len(m) == 2 and m[0].distance < m[1].distance * 0.75:
            good_matches.append(m[0])
    matches.append((i, i+1, good_matches))

# 找到图像间的变换矩阵
homographies = []
for (i, j, matches_ij) in matches:
    keypoints_i = np.float32([keypoints[i][m.queryIdx].pt for m in matches_ij]).reshape(-1, 1, 2)
    keypoints_j = np.float32([keypoints[j][m.trainIdx].pt for m in matches_ij]).reshape(-1, 1, 2)
    H_ij, _ = cv2.findHomography(keypoints_i, keypoints_j, cv2.RANSAC, 5.0)
    homographies.append(H_ij)

# 计算全景图的大小
panorama_corners = np.zeros((4, 2), dtype=np.float32)
panorama_corners[1, 1] = images[0].shape[0]
panorama_corners[2] = images[0].shape[:2][::-1]
for H in homographies:
    corners = np.array([[0, 0, 1], [0, images[0].shape[0]-1, 1], [images[0].shape[1]-1, images[0].shape[0]-1, 1], [images[0].shape[1]-1, 0, 1]])
    transformed_corners = np.matmul(corners, np.transpose(H))
    transformed_corners = transformed_corners / transformed_corners[:, 2].reshape(-1, 1)
    panorama_corners = np.vstack((panorama_corners, transformed_corners[:, :2]))
panorama_corners -= panorama_corners.min(axis=0)
panorama_shape = np.ceil(panorama_corners.max(axis=0)).astype(int)

# 创建空的全景图
panorama = np.zeros(tuple(panorama_shape), dtype=np.uint8)

# 拼接图像
for i in range(len(images)):
    if i == 0:
        H = np.eye(3)
    else:
        H = homographies[i-1]
    image = images[i]
    h, w, _ = image.shape
    corners = np.array([[0, 0, 1], [0, h-1, 1], [w-1, h-1, 1], [w-1, 0, 1]])
    transformed_corners = np.matmul(corners, np.transpose(H))
    transformed_corners = transformed_corners / transformed_corners[:, 2].reshape(-1, 1)
    x_min = int(np.floor(transformed_corners[:, 0].min()))
    x_max = int(np.ceil(transformed_corners[:, 0].max()))
    y_min = int(np.floor(transformed_corners[:, 1].min()))
    y_max = int(np.ceil(transformed_corners[:, 1].max()))

    # 对变换矩阵进行平移，使图像的左上角在全景图的左边界
    T = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]])
    H = np.matmul(T, H)

    # 对图像进行透视变换，并将其加入全景图
    warped_image = cv2.warpPerspective(image, H, (x_max - x_min, y_max - y_min))
    panorama[-y_min:-y_min+h, -x_min:-x_min+w] = warped_image

# 将全景图保存到文件
cv2.imwrite(args["output"], panorama)
print("全景图已保存到", args["output"])
