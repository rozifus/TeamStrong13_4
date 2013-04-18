#
# KATE - KVURD's Alternative Track Engine
#
from __future__ import division
import math
import random
import settings
from utils import Point, Vec2d, Rect, Sleeper
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
            if utils.point_in_rect((sleeper.x, sleeper.y), viewport):
                self.visible_sleepers.append(sleeper)

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
            lowest_x = 10000
            highest_x = 0
            for segment in self.track_segments:
                (sx1, sy1, sx2, sy2) = segment
                if(sx1 < lowest_x):
                    lowest_x = sx1
                if(sx2 < lowest_x):
                    lowest_x = sx2
                if(sx1 > highest_x):
                    highest_x = sx1
                if(sx2 > highest_x):
                    highest_x = sx2

            start_x = math.floor(lowest_x / settings.SLEEPER_SPACING) * settings.SLEEPER_SPACING
            end_x = (math.floor(highest_x / settings.SLEEPER_SPACING) + 1.0) * settings.SLEEPER_SPACING
            
            for x in xrange(int(start_x), int(end_x), settings.SLEEPER_SPACING):
                w = (settings.SLEEPER_WIDTH + (random.random() * settings.SLEEPER_WIDTH_JITTER * 2.0 - settings.SLEEPER_WIDTH_JITTER)) / 2.0
                l = (settings.SLEEPER_LENGTH + (random.random() * settings.SLEEPER_LENGTH_JITTER * 2.0 - settings.SLEEPER_LENGTH_JITTER)) / 2.0
                skew = random.random() * settings.SLEEPER_SKEW * 2.0 - settings.SLEEPER_SKEW
                (y, r) = self.track_info_at_x(x)
                x1 = x - w + skew
                x2 = x + w + skew
                x3 = x + w - skew
                x4 = x - w - skew
                y1 = y + l
                y2 = y + l
                y3 = y - l
                y4 = y - l
                ctr, ctg, ctb = settings.SLEEPER_COLOR_TOP
                cbr, cbg, cbb = settings.SLEEPER_COLOR_BOTTOM
                self.sleepers.append(Sleeper(x, y, r, x1, y1, x2, y2, x3, y3, x4, y4, ctr, ctg, ctb, cbr, cbg, cbb))

