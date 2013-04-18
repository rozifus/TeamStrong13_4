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

class InfiniteHeightObstacle(Obstacle):
    _collided = False

    def collides_with(self, other):
        """
        Make our own height infinite. We only need to check if
        the other entity straddles us.
        """

        if self.name == 'start' or self._collided:
            # don't collide with the first spawn point. It screws up the numbering.
            return False

        #        ~ 
        #       `
        #       o
        #       |
        #       |
        #       |
        #   x[     ]+width

        self._collided = collided = self.gp.x < other.gp.x
        return collided

class EndLevel(InfiniteHeightObstacle):
    """
    Hit this, and it's all over.
    """
    IMAGE = settings.POST_IMAGE

    def collided(self, game):
        game.finish()

class Spawn(InfiniteHeightObstacle):
    """
    Hit this and postgres is saved.
    """
    IMAGE = settings.SPAWN_IMAGE

    def collided(self, game):
        # remove the just passed spawn point.
        print "popping n locking!!"
        game.spawn_points.pop(0)

