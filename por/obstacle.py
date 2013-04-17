# everything to do with the rubies

import pyglet
import settings
import entity
import utils

from utils import Vec2d, Point, Rect

class Obstacle(entity.Entity):
    """
    In case we want more than one type?
    """
    IMAGE = settings.ANVIL_IMAGE
