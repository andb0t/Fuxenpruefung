import math


def get_angle(x0, y0, x1, y1):
    mag0 = math.sqrt(x0**2 + y0**2)
    mag1 = math.sqrt(x1**2 + y1**2)
    if not mag0 or not mag1:
        return 0
    dot = x0 * x1 + y0 * y1
    det = x0 * y1 - x1 * y0
    angle = math.degrees(math.atan2(det, dot))
    return angle
