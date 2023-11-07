import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes/Detectors.xlsx",
                   engine='openpyxl')

# Define color scheme
colors = {"SIFT": "tab:red", "ORB": "tab:orange", "AKAZE": "tab:blue"}

# Elapsed time plot
plt.figure(figsize=(10, 6))
for detector in ["SIFT", "ORB", "AKAZE"]:
    plt.plot(df["Resize Factor"], df[f"{detector}_time"], marker='o', color=colors[detector], label=detector)

plt.xlabel("Resize Factor")
plt.ylabel("Elapsed Time (s)")
plt.xlim(1.06, 0.16, 0.2)
plt.title("Elapsed Time for Different Feature Detectors")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\Detector_time.png")
plt.show()

# Keypoints plot
plt.figure(figsize=(10, 6))
for detector in ["SIFT", "ORB", "AKAZE"]:
    plt.plot(df["Resize Factor"], df[f"{detector}_keypoints"], marker='o', color=colors[detector], label=detector)
plt.xlabel("Resize Factor")
plt.ylabel("Keypoints Detected (units)")
plt.title("Number of Keypoints Detected for Different Feature Detectors")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("D:\Documents\GitHub\Master-Thesis\Image_processing\panorama\HighRes\Detector_kps.png")
plt.show()
