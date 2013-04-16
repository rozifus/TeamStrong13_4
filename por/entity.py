# abstract class for physical objects in POR

import math
import pyglet
import settings

class Entity(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)

        # center the image anchors
        self.image.anchor_x = self.image.width / 2.0
        self.image.anchor_y = self.image.height / 2.0
        
        # create the sprite
        self.sprite = pyglet.sprite.Sprite(img = self.image)

        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def collides_with(self, other_entity):
        # circular collision detection
        collision_threshold = self.image.width / 2.0 + other_entity.image.width / 2.0
        distance = self.distance(self, other_entity)
        return distance < collision_threshold

    def distance(self, other_entity):
        #tnx pythagoras
        x1, y1 = self.position
        x2, y2 = other_entity.position
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def update(self, dt):
        # We need to rotate the image 180 degrees because we have y pointing 
        self.x += dt * self.velocity_x
        self.y += dt * self.velocity_y
