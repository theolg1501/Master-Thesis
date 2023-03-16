import math

import numpy as np
from matplotlib import pyplot as plt


def dimension_of_image(altitude, HFOV=62.2, VFOV=46.8):
    d_horizontal = 2 * altitude * math.tan(math.radians(HFOV) / 2)
    d_vertical = 2 * altitude * math.tan(math.radians(VFOV) / 2)
    return d_horizontal, d_vertical


def distances_between_photos(horizontal_overlap, vertical_overlap, d_horizontal, d_vertical):
    d_length = (1 - horizontal_overlap) * d_horizontal
    d_width = (1 - vertical_overlap) * d_vertical
    return d_length, d_width


def calculate_distance_between_photos(altitude, horizontal_overlap=0.75, vertical_overlap=0.75, HFOV=62.2, VFOV=46.8):
    d_horizontal, d_vertical = dimension_of_image(altitude, HFOV, VFOV)
    return distances_between_photos(horizontal_overlap, vertical_overlap, d_horizontal, d_vertical)


if __name__ == "__main__":
    print(calculate_distance_between_photos(15))
    x = np.linspace(1, 50, 100)
    y_horizontal, y_vertical = calculate_distance_between_photos(x)

    plt.plot(x, y_horizontal, 'r')
    plt.plot(x, y_vertical, 'g')

    plt.show()



