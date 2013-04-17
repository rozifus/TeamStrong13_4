"""
Stuff related to loading and rendering a level.
"""

# This code is so you can run the samples without installing the package
from collections import namedtuple
import math
import os
import random
import sys

import pyglet

from pytmx import tmxloader

import ruby
import settings
from utils import pairwise

LineSegment = namedtuple('Vector', 'x1 y1 x2 y2')

class LevelLoader(object):
    """
    The tmx object should have these layers:

    1. 'map' for the background
    2. 'triggers' for the object world.
    """

    def __init__(self, tmx):
        self.tmx = tmx

    @property
    def tracks(self):
        _tracks = self.tmx['track']
        segments = []
        for track in _tracks:
            for (x1, y1), (x2, y2) in pairwise(track.points):
                segments.append(
                    LineSegment(
                        x1 + track.x, -y1 + track.y,
                        x2 + track.x, -y2 + track.y))
        print "number of segments in level is " + str(len(segments))
        return segments

    def __getattr__(self, attr):
        """
        Turns a call for level._name_ into 
        level.point_objects(name)
        """
        return self.point_objects(attr)

    def point_objects(self, name):
        objects = []
        for tile in self.tmx[name]:
            objects.append((tile.x, tile.y))
        number = len(objects)
        print "number of {name} in level is {number}".format(**locals())
        return objects


def load(level):
    """
    Load level number from tmx file.
    """
    levelfname = level + ".tmx"
    print "Loading level " + levelfname
    tmx = tmxloader.load_tmx(pyglet.resource.file(levelfname))

    return LevelLoader(tmx)
