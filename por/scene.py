import math

import pyglet
from pyglet.gl import glPushMatrix, glPopMatrix, glLoadIdentity \
                     , glTranslatef

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

        self.rect = Rect(xnew, yactual, self.rect.width, self.rect.height)

    def reset(self, rect):
        self.rect = rect
        self.highpoint = None

class Background(object):

    def __init__(self, tmxmap, viewport):
        resources, layers, worldmap = tmxmap
        self.batch = batch = pyglet.graphics.Batch()
        self.sprites = []
        self.viewport = viewport

        for num, layer in enumerate(layers):
            group = pyglet.graphics.OrderedGroup(num)

            for ytile in range(layer.height):
                for xtile in range(layer.width):
                    image_id = layer.content2D[xtile][ytile]
                    if not image_id: continue

                    image_file = resources.indexed_tiles[image_id][2]
                    x, y = (worldmap.tilewidth * xtile,
                            worldmap.tileheight * (layer.height - ytile))


                    sprite = pyglet.sprite.Sprite(
                        image_file, x, y, batch=batch, group=group)

                    self.sprites.append(sprite)

    @property
    def coords(self):
        return self.viewport.rect[:2]

    def draw(self):
        glPushMatrix()
        self.transform()
        self.batch.draw()
        glPopMatrix()

    def transform(self):
        glLoadIdentity()
        x, y = self.coords
        glTranslatef(-x, -y, 0.0)

