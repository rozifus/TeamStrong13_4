# everything to do with the cart

import pyglet
import pymunk
import settings
import entity

class Cart(entity.Entity):
    def __init__(self):
        super(Cart, self).__init__("cart.png",
                                   settings.CART_MASS,
                                   settings.CART_FRICTION,
                                   settings.CART_STARTING_ANGLE)
        self.shape.collision_type = settings.COLLISION_CART

    def bounce(self):
        self.body.apply_impulse(settings.CART_BOUNCE_IMPULSE, (0, 0))

