#
# KATE - KVURD's Alternative Track Engine
#
from __future__ import division
import math
import settings
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
        self.sleepers = []
        self.visible_sleepers = []

    def add_tracks(self, tracks):
        self.track_segments.extend(tracks)
        self.generate_sleepers()
        print "track segments: " + str(len(self.track_segments)) + ", sleepers: " + str(len(self.sleepers))

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
        
        self.visible_sleepers = []
        for sleeper in self.sleepers:
            (x, y, r) = sleeper
            if utils.point_in_rect((x, y), viewport):
                self.visible_sleepers.append(sleeper)
        print str(len(self.visible_sleepers))

    def segment_in_rect(self, segment, rect):
        (x1, y1, x2, y2) = segment
        point1 = (x1, y1)
        point2 = (x2, y2)
        
        if utils.point_in_rect(point1, rect) or utils.point_in_rect(point2, rect):
            result = True
        else:
            result = False
        return result
        

    def generate_sleepers(self):
        if len(self.track_segments):
            (sx1, sy1, sx2, sy2) = self.track_segments[0]
            (ex1, ey1, ex2, ey2) = self.track_segments[-1]
            #print str(self.track_segments)

            start_x = math.floor(sx1 / settings.SLEEPER_SPACING) * settings.SLEEPER_SPACING
            end_x = (math.floor(ex2 / settings.SLEEPER_SPACING) + 1.0) * settings.SLEEPER_SPACING
            print "sleeper startx is " + str(start_x) + " end x is " + str(end_x)
            for x in xrange(int(start_x), int(end_x), settings.SLEEPER_SPACING):
                (th, ta) = self.track_info_at_x(x)
                self.sleepers.append((x, th, ta))

            print str(self.sleepers)

