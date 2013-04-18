# everything to do with the cart

import pyglet
import settings
import entity
import sounds

from utils import Point, Vec2d

class Cart(entity.Entity):
    IMAGE = settings.CART_IMAGE

    def init(self):
        self.reset()

    def jump(self):
        if self.on_track:
            sounds.cart_jump.play()
            self.velocity_y = settings.CART_JUMP_VELOCITY
            self.rotation = settings.CART_JUMP_ROTATION
        else:
            if (self.gp.x - self.track_height) / self.velocity_x < settings.CART_EARLY_JUMP_TIME:
                self.should_jump_on_landing = True
            

    def reset(self):
        self.velocity_x = settings.CART_NORMAL_VELOCITY
        self.on_track = False
        self.above_track = True
        self.track_height = 0.0
        self.track_angle = 0.0
        self.should_jump_on_landing = False

    def update(self, dt, track_height, track_angle):
        super(Cart, self).update(dt)

        self.track_height = track_height
        self.track_angle = track_angle

        if track_angle < 0:
            self.speed_up(dt)
        elif track_angle > 0:
            self.slow_down(dt)

        #print "on track: " + str(self.on_track)
        if self.gp.y - self.image.height / 2.0 <= self.track_height + settings.TRACK_FUZZ and self.above_track and self.velocity_y <= 0: 
            self.gp = Point(self.gp.x, self.track_height + self.image.height / 2.0)
            self.velocity_y = 0.0
            self.rotation = -self.track_angle
            
            if self.on_track == False:
                # just landed
                sounds.cart_land.play()
                if self.should_jump_on_landing:
                    self.on_track = True
                    self.jump()

            self.should_jump_on_landing = False
            self.on_track = True
        
        else:
            # we are off the track
            self.velocity_y += dt * settings.GRAVITY
            self.on_track = False

        self.above_track = (self.gp.y >= self.track_height - settings.TRACK_FUZZ and self.track_height > 0)

    def speed_up(self, dt):
        self.velocity_x += settings.CART_SPEED_UP * dt
        if self.velocity_x > settings.CART_MAX_VELOCITY:
            self.velocity_x = settings.CART_MAX_VELOCITY
    
    def slow_down(self, dt):
        self.velocity_x += settings.CART_SLOW_DOWN * dt
        if self.velocity_x < settings.CART_MIN_VELOCITY:
            self.velocity_x = settings.CART_MIN_VELOCITY
