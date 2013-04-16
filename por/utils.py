from itertools import izip, tee
from collections import namedtuple

Vec2d = namedtuple("Vec2d", "x y")

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)