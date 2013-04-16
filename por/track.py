#
# KATE - KVURD's Alternative Track Engine
#
TRACK_FRICTION = 0.05
SEGMENT_RADIUS = 2
SEGMENT_WIDTH = 50
SEGMENT_HEIGHT = 25

class Track(object):
    def __init__(self):
        super(Track, self).__init__()
        
        self.track_segments = []

    def add_tracks(self, tracks):
        self.track_segments.extend(tracks)
