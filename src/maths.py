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


def parabola(x0, y0, x1, y1, peakX=None):
    if peakX is None:
        peakX = x0
    c = (y0 - y1) / (2 * x1 * peakX - x1 ** 2 - 2 * x0 * peakX + x0 ** 2)
    a = 2 * c * x1 * peakX - c * x1 ** 2 + y1
    b = -2 * c * peakX
    return a, b, c


def get_parabola(x0, y0, x1, y1, x, peakX=None):
    a, b, c = parabola(x0, y0, x1, y1, peakX)
    y = a + b * x + c * x ** 2
    return y
