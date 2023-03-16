import numpy as np

# From camera hardware specification
HFOV = 62.2  # degrees
VFOV = 48.8  # degrees

res_x = 3280  # pixels
res_y = 2464  # pixels

f = 3.04  # mm

# Different altitude variable
ALT = 8  # meters
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
    return front, side


# Ground area covered
y, x = area_covered(VFOV, HFOV, ALT)

GSD = x / 3280 * 100  # cm/pixel

print(GSD)
