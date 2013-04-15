# everything to do with the rubies

import pyglet
import pymunk
import settings
import entity

class Ruby(entity.Entity):
    def __init__(self):
        super(Ruby, self).__init__(settings.RUBY_IMAGE,
                                   settings.RUBY_MASS,
                                   settings.RUBY_FRICTION,
                                   settings.RUBY_STARTING_ANGLE)
        self.shape.collision_type = settings.COLLISION_RUBY

