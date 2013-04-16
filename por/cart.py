# everything to do with the cart

import pyglet
import settings
import entity

class Cart(entity.Entity):
    def __init__(self):
        super(Cart, self).__init__("cart.png",
                                   settings.CART_MASS,
                                   settings.CART_FRICTION,
                                   settings.CART_STARTING_ANGLE)
