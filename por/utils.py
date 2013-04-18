from itertools import izip, tee
from collections import namedtuple

Vec2d = namedtuple("Vec2d", "x y")
Point = namedtuple("Point", "x y")
Rect = namedtuple("Rect", "x y width height")
TMXMap = namedtuple("Map", "resources layers worldmap")
#sleeper gx gy = world pos, r rotation, x,y1-4 = vertices for openGL quad
Sleeper = namedtuple("Sleeper", "x y r x1 y1 x2 y2 x3 y3 x4 y4 ct1 ct2 ct3 cb1 cb2 cb3")

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

