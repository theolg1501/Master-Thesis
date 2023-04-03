import math
import numpy as np

# From camera hardware specification
HFOV = 62.2  # degrees
VFOV = 48.8  # degrees

res_x = 1920  # pixels
res_y = 1080  # pixels

f = 3.04  # mm

# Different altitude variable
ALT = 6  # meters
SPEED = 1.8  # m/s
INTERVAL = 2  # second(s)
AREA_X = 35  # meters
AREA_Y = 80  # meters


def area_covered(vfov, hfov, alt):
    m = 2 * np.tan(np.deg2rad(vfov / 2)) * alt
    n = 2 * np.tan(np.deg2rad(hfov / 2)) * alt
    return m, n


def overlapping(x, y, speed, interval):
    front = (speed * interval) / 2 * y
    side = (speed * interval) / 2 * x
    return math.ceil(front), math.ceil(side)


def row_col(front, side, area_x, area_y, x, y):
    row = area_y + (front * y) // ((1 - front) * y)
    col = area_x + (side * x) // ((1 - side) * x)


# Ground area covered
y, x = area_covered(VFOV, HFOV, ALT)

GSD = x / 1920 * 100  # cm/pixel

front, side = overlapping(x, y, SPEED, INTERVAL)

print('GSD:'+str(GSD))
print('Area_x: '+str(x))
print('Area_y: '+str(y))



