# abstract class for physical objects in POR

import math
import pyglet
import settings
from collections import namedtuple
from utils import Point, Vec2d, point_in_rect

class Entity(pyglet.sprite.Sprite):

    # just set this to the settings image value in the subclass.
    IMAGE = None
    name = None

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

    def collided_objects(self, objects):
        # returns a list of objects that were collided.
        return filter(self.collides_with, objects)

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

class ObjectList(object):
    def __init__(self, klass_dict):
        self.objects = []
        self.visible = []
        self.klass_dict = klass_dict

    def add(self, points):
        for point in points:
            # points can be named (in Tiled) so you can have multiple object types
            # in the one level. handy for grouping all collideable objects together.
            Klass = self.klass_dict.get(point.name, self.klass_dict['default'])
            new = Klass()
            new.name = point.name
            new.gp = Point(point.x, point.y)
            self.objects.append(new)

    def update_visible(self, viewport):
        self.visible = [
            obj for obj in self.objects
            if point_in_rect(obj.gp, viewport)]

    def __getitem__(self, item):
        return self.objects[item]

    def pop(self, idx=None):
        return self.objects.pop(idx)
