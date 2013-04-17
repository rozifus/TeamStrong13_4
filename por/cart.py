# everything to do with the cart

import pyglet
import settings
import entity
import sounds

from utils import Point, Vec2d

class Cart(entity.Entity):
    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(img = pyglet.resource.image(settings.CART_IMAGE), *args, **kwargs)
        self.velocity_x = settings.CART_NORMAL_VELOCITY
        self.on_track = False
        self.above_track = True
        self.track_height = 0.0
        self.track_angle = 0.0

    def jump(self):
        if self.on_track:
            print "Jumping cart"
            sounds.cart_jump.play()
            self.velocity_y = settings.CART_JUMP_VELOCITY
            self.rotation = settings.CART_JUMP_ROTATION

    def update(self, dt, track_height, track_angle):
        super(Cart, self).update(dt)

        self.track_height = track_height
        self.track_angle = track_angle

        #print "on track: " + str(self.on_track)
        if self.gp.y - self.image.height / 2.0 <= self.track_height + settings.TRACK_FUZZ and self.above_track and self.velocity_y <= 0: 
            self.gp = Point(self.gp.x, self.track_height + self.image.height / 2.0)
            self.velocity_y = 0.0
            self.rotation = -self.track_angle
            
            if self.on_track == False:
                sounds.cart_land.play()
            self.on_track = True
        
        else:
            # we are off the track
            self.velocity_y += dt * settings.GRAVITY
            self.on_track = False

        self.above_track = (self.gp.y >= self.track_height - settings.TRACK_FUZZ and self.track_height > 0)
