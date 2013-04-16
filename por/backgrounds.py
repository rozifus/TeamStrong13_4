import random
from pyglet.gl import *
import cocos
from cocos import tiles

from cocos.director import director

class GradientLayer(tiles.ScrollableLayer):
    def __init__(self, bottom, top):
        self.bottom = bottom
        self.top = top
        super(GradientLayer, self).__init__()

    def draw(self, x=0, y=0):
        w, h = director.window.width, director.window.height
        glBegin(GL_QUADS)
        glColor4ub(*self.bottom)
        glVertex2f(x, y)
        glVertex2f(x+w, y)
        glColor4ub(*self.top)
        glVertex2f(x+w, y+h)
        glVertex2f(x, y+h)
        glEnd()

