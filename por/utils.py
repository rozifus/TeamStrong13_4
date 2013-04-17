from itertools import izip, tee
from collections import namedtuple

Vec2d = namedtuple("Vec2d", "x y")
Point = namedtuple("Point", "x y")
Rect = namedtuple("Rect", "x y width height")
TMXMap = namedtuple("Map", "resources layers worldmap")

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def point_in_rect(point, rect):
    (px, py) = point
    (x, y, width, height) = rect
    if px > x and px < x + width and py > y and py < y + width:
        result = True
    else:
        result = False

    return result

