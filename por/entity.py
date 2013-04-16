# abstract class for physical objects in POR

import math
import pyglet

import settings


class Entity(object):
    def __init__(self, image_name, mass, friction, angle):
        super(Entity, self).__init__()
        self.deletion_flag = False

        # create the image 
        self.image = pyglet.resource.image(image_name, rotate = 180.0)

        # center the image anchors
        self.image.anchor_x = self.image.width / 2.0
        self.image.anchor_y = self.image.height / 2.0
        
        # create the sprite
        self.sprite = pyglet.sprite.Sprite(img=self.image)

        # physics setup - mass, vertices, friction, position, angle
        self.mass = mass
        self.friction = friction
        self.angle = angle
        self.vertices = self.rectangular_vertices()
        
        # update position
        self.update_position(settings.ENTITY_DEFAULT_X, settings.ENTITY_DEFAULT_Y)

    def update_position(self, x, y):
        self._position = x, y
        self.sprite.x = x
        self.sprite.y = y
        
    def rectangular_vertices(self):
        """Sets the vertices for the entity to the size of its image"""
        x = self.image.width / 2.0
        y = self.image.height / 2.0
        return [(-x, -y), (-x, y), (x, y), (x, -y)]

    def update(self, dt):
        # We need to rotate the image 180 degrees because we have y pointing 
        # up in pymunk coords.
        pass

    def bounce(self):
        pass

