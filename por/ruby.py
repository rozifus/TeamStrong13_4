# everything to do with the rubies

import pyglet
import pymunk
import settings
import entity

class Ruby(entity.Entity):
    def __init__(self, *args, **kwargs):
        super(Ruby, self).__init__(img = pyglet.resource.image(settings.RUBY_IMAGE), *args, **kwargs)

