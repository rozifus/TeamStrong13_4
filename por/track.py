#
# KATE - KVURD's Alternative Track Engine
#
from __future__ import division
import math

from utils import Point, Vec2d, Rect
import utils

TRACK_FRICTION = 0.05
SEGMENT_RADIUS = 2
SEGMENT_WIDTH = 50
SEGMENT_HEIGHT = 25

class Track(object):
    def __init__(self):
        super(Track, self).__init__()
        
        self.track_segments = []
        self.visible_track_segments = []

    def add_tracks(self, tracks):
        self.track_segments.extend(tracks)

    def track_info_at_x(self, gpx):
        height = -1000.0 # default off the screen
        angle = 0.0
        for segment in self.track_segments:
            #y = mx + c, tnx eng degree
            (x1, y1, x2, y2) = segment
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            if gpx > x1 and gpx <= x2:
                height = m * gpx + c
                angle = math.degrees(math.atan2(m, 1.0))
                
        return (height, angle)

    def update_visible(self, viewport):
        self.visible_track_segments = []
        for segment in self.track_segments:
            if self.segment_in_rect(segment, viewport):
                self.visible_track_segments.append(segment)

    def segment_in_rect(self, segment, rect):
        (x1, y1, x2, y2) = segment
        point1 = (x1, y1)
        point2 = (x2, y2)
        
        if utils.point_in_rect(point1, rect) or utils.point_in_rect(point2, rect):
            result = True
        else:
            result = False

        return result
        

