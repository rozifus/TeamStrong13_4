# abstract class for physical objects in POR

import math
import pyglet
import settings
from collections import namedtuple
from utils import Point, Vec2d

class Entity(pyglet.sprite.Sprite):

    # just set this to the settings image value in the subclass.
    IMAGE = None

    def __init__(self, *args, **kwargs):
        if self.IMAGE:
            args = (pyglet.resource.image(self.IMAGE),) + args
        super(Entity, self).__init__(*args, **kwargs)

        # center the image anchors
        self.image.anchor_x = self.image.width / 2.0
        self.image.anchor_y = self.image.height / 2.0
        
        # create the sprite
        self.sprite = pyglet.sprite.Sprite(img = self.image)

        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
        self.gp = Point(settings.ENTITY_DEFAULT_GAME_POSITION_X,
                        settings.ENTITY_DEFAULT_GAME_POSITION_Y)

        self.init()

    def init(self):
        """
        Called post init. Pls override me.
        """
        pass

    def collides_with(self, other_entity):
        # circular collision detection
        collision_threshold = self.image.width / 2.0 + other_entity.image.width / 2.0
        distance = self.distance(other_entity)
        return distance < collision_threshold

    def distance(self, other_entity):
        #tnx pythagoras
        x1, y1 = self.gp
        x2, y2 = other_entity.gp
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def update(self, dt):
        self.gp = Point(self.gp.x + dt * self.velocity_x, self.gp.y + dt * self.velocity_y)

    def __repr__(self):
        classname = self.__class__.__name__
        x, y = self.gp
        return "{classname}({x}, {y})".format(**locals())