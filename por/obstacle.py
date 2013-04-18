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

    def collided(self, game):
        game.die()

class EndLevel(Obstacle):
    """
    Hit this, and it's all over.
    """
    IMAGE = settings.POST_IMAGE

    def collided(self, game):
        game.finish()