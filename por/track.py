#
# KATE - KVURD's Alternative Track Engine
#
import pymunk

TRACK_FRICTION = 0.05
SEGMENT_RADIUS = 2
SEGMENT_WIDTH = 50
SEGMENT_HEIGHT = 25

class TrackSegment(object):
    def __init__(self, type, start_point):
        super(TrackSegment, self).__init__()

        track_types = {"f" : self.flat,
                "u" : self.up,
                "d" : self.down,
                }
        
        self.track = []
        self.start_point = start_point
        self.body = pymunk.Body()
        track_types[type]()

        for line in self.track:
            line.friction = TRACK_FRICTION

    def flat(self):
        x, y = self.start_point
        self.end_point = x + SEGMENT_WIDTH, y
        self.track = [pymunk.Segment(self.body, self.start_point, self.end_point, SEGMENT_RADIUS)]
    
    def up(self):
        x, y = self.start_point
        self.end_point = x + SEGMENT_WIDTH, y + SEGMENT_HEIGHT
        self.track = [pymunk.Segment(self.body, self.start_point, self.end_point, SEGMENT_RADIUS)]

    def down(self):
        x, y = self.start_point
        self.end_point = x + SEGMENT_WIDTH, y - SEGMENT_HEIGHT
        self.track = [pymunk.Segment(self.body, self.start_point, self.end_point, SEGMENT_RADIUS)]

    # hard(er) ones:
    def flat_to_up(self):
        pass
        #x, y = self.start_point
        #self.end_point = x + SEGMENT_WIDTH / 2.0, y + SEGMENT_HEIGHT / 2.0
        #self.track = [pymunk.Segment(self.body, self.start_point, 

    def flat_to_down(self):
        pass

    def up_to_flat(self):
        pass

    def down_to_flat(self):
        pass

    # probably also need functions to represent gaps in the track...


class Track(object):
    def __init__(self, space, start_point):
        super(Track, self).__init__()
        
        self.space = space
        self.start_point = start_point
        self.track_segments = []

    def add_track_segment(self, type):
        if len(self.track_segments) == 0:
            start_point_new_segment = self.start_point
        else:
            start_point_new_segment = self.track_segments[-1].end_point

        new_track_segment = TrackSegment(type, start_point_new_segment)
        self.space.add(new_track_segment.track)
        self.track_segments.append(new_track_segment)

    def add_track_string(self, track_string):
        for c in track_string:
            # probably should do some checking, but fuck it
            self.add_track_segment(c)

