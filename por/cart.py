# everything to do with the cart

import pyglet
import settings
import entity

class Cart(entity.Entity):
    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(img = pyglet.resource.image(settings.CART_IMAGE), *args, **kwargs)
        self.velocity_x = settings.CART_NORMAL_VELOCITY
        self.on_track = False
        self.track_height = 0.0
        self.track_angle = 0.0

    def jump(self):
        if self.on_track:
            print "Jumping cart"
            self.velocity_y = settings.CART_JUMP_VELOCITY
            self.rotation = settings.CART_JUMP_ROTATION
    
    def update(self, dt, track_height, track_angle):
        super(Cart, self).update(dt)

        self.track_height = track_height
        self.track_angle = track_angle
        
        #print "on track: " + str(self.on_track)
        (gpx, gpy) = self.gp
        if gpy - self.image.height / 2.0 <= self.track_height + settings.TRACK_FUZZ:
            self.gp = (gpx, self.track_height + self.image.height / 2.0)
            self.velocity_y = 0.0
            self.rotation = -self.track_angle
            self.on_track = True 

        else:
            # we are off the track
            self.velocity_y += dt * settings.GRAVITY
            self.on_track = False
