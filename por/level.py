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

from pytmx import tmxloader, tmxreader
from pytmx.helperspyglet import ResourceLoaderPyglet

import ruby
import settings
from utils import pairwise, TMXMap

LineSegment = namedtuple('Vector', 'x1 y1 x2 y2')

class LevelLoader(object):
    """
    The tmx object should have these layers:

    1. 'map' for the background
    2. 'triggers' for the object world.
    """

    def __init__(self, tmx, maps):
        self.tmx = tmx
        self._maps = maps

    @property
    def layers(self):
        """
        returns the maps, but not object groups.
        """
        maplayers = filter(lambda l: not l.is_object_group, self._maps.layers)
        resources = ResourceLoaderPyglet()
        resources.load(self._maps)

        return TMXMap(resources, maplayers, self._maps)

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
        objects = list(self.tmx[name])
        number = len(objects)
        print "number of {name} in level is {number}".format(**locals())
        return objects


def load(level):
    """
    Load level number from tmx file.
    """
    levelfname = level + ".tmx"
    print "Loading level " + levelfname

    # first one is good for images.
    tmx = tmxloader.load_tmx(
        pyglet.resource.file(levelfname))

    # this second one is good for scrolling background.
    maps = tmxreader.TileMapParser().parse_decode(
                    pyglet.resource.file(levelfname))

    return LevelLoader(tmx, maps)
