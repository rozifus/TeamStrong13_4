import math

import pyglet
from pyglet.gl import glPushMatrix, glPopMatrix

from utils import Rect
import settings

class ViewportManager(object):
    """
    The viewport has a deadband so it doesn't jitter on uneven track.
    It also has rate limiting to avoid it moving really jerkily.
    """

    def __init__(self, rect):
        self.rect = rect
        self.highpoint = None

    @property
    def y(self):
        return self.rect.y

    def __iter__(self):
        return iter(self.rect)

    def update(self, x, track_height):
        y = self.rect.y

        xnew = x - settings.VIEWPORT_OFFSET_X
        if track_height > 0:
            ynew = track_height - settings.VIEWPORT_OFFSET_Y
        else:
            ynew = y

        ychange_o = ychange = ynew - y

        if not abs(ychange) > settings.VIEWPORT_DEADBAND:
            ychange = 0
        else:
            self.highpoint = True
            if ychange > 0:
                ychange = min(max(ychange - settings.VIEWPORT_DEADBAND, 0), settings.VIEWPORT_MAX_RATE)
            else:
                ychange = max(min(ychange + settings.VIEWPORT_DEADBAND, 0), -settings.VIEWPORT_MAX_RATE)

        # clip the y delta to the MAX_RATE and add to the original y.
        if self.highpoint and ychange == 0:
            boost = ychange_o * 0.25
            if abs(ychange_o) < 5:
                boost = 0
            else:
                self.highpoint = False
        else:
            boost = 0

        yactual = y + (ychange + boost) 
        print "{y} + {ychange:.2f} = {yactual:.2f} ({ychange_o:.2f}: {boost:.2f})".format(**locals())

        self.rect = Rect(xnew, yactual, self.rect.width, self.rect.height)

    def reset(self, rect):
        self.rect = rect

class Background(object):

    def __init__(self, image):
        tiles = image.parent.getTileImages((0, 0, 1023, 767), 'map')
        #import pdb;pdb.set_trace()
        self.batch = pyglet.graphics.Batch()

    def draw(self):
        glPushMatrix()
        self.transform()
        self.batch.draw()
        glPopMatrix()

    def transform(self):
        pass

