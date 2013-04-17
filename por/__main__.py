import pyglet
import sys
import math
import random
import settings

import entity
import sounds
import cart
import ruby
import track
import level
import obstacle

from collections import namedtuple
from utils import Point, Vec2d, Rect

def main(levelname):
    """ your app starts here
    """
    pyglet.resource.path = settings.RESOURCE_PATH
    pyglet.resource.reindex()
    sounds.load()
    game = Game()
    game.start(levelname)

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1024, 768)
        
        # in game coords. viewport is your window into game world
        self.viewport = Rect(0.0, 0.0, self.width, self.height)

        self.main_batch = pyglet.graphics.Batch()
        self.score_label = pyglet.text.Label(text = "",
                                             x = settings.SCORE_LABEL_X,
                                             y = settings.SCORE_LABEL_Y,
                                             batch = self.main_batch)
        
        self.lives_label = pyglet.text.Label(text = "", 
                                             x = settings.LIVES_LABEL_X, 
                                             y = settings.LIVES_LABEL_Y, 
                                             batch = self.main_batch)
        
        self.quit_label = pyglet.text.Label(text = "By NSTeamStrong: q [quit] space [jump]", 
                                             x = settings.QUIT_LABEL_X, 
                                             y = settings.QUIT_LABEL_Y, 
                                             batch = self.main_batch)

        self.speed_label = pyglet.text.Label(text = "", 
                                             x = settings.SPEED_LABEL_X,
                                             y = settings.SPEED_LABEL_Y, 
                                             batch = self.main_batch)

        self.fps_display = pyglet.clock.ClockDisplay()
        self.cart = None
        self.entities = []

    def start(self, levelname):
        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.update_labels()
        self.level = level.load(levelname)
        self.track = track.Track()
        self.track.add_tracks(self.level.tracks)
        self.ruby_list = entity.ObjectList(ruby.Ruby)
        self.ruby_list.add(self.level.rubies)
        self.obstacle_list = entity.ObjectList(obstacle.Obstacle)
        self.obstacle_list.add(self.level.obstacles)

        self.objects = [self.ruby_list, self.obstacle_list]

        self.create_cart()
        pyglet.clock.schedule(self.update) # main loop
        pyglet.app.run()


    def on_draw(self): #runs every frame
        self.clear()
        #
        # the basic idea behind scrolling is as follows:
        # - the level is large, say from (0, 0) to (10000, 2000)
        #   game coordinates are the coordinates in this space
        # - we look at a small section of it: (vpx, vpy) to (window_width, window_height)
        #   (vpx, vpy) is the viewport_origin, screen coordinates are the coordinates in this space
        # - we need to render things that are within a certain buffer of the viewport
        #   this is the renderzone (x - rz_size, y - rz_size) to (x + window_width + rz_size, y + window_width + rz_size)
        #
        # thus our code needs to:
        # - remove objects that are no longer within the render zone
        # - add objects that move into the render zone
        # - update the relative positions of objects on screen
        #

        #for line in self.track:
        #    (x1, y1), (x2, y2) = line
        #    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #            ('v2f', (x1 - vpx, y1 - vpy, x2 - vpx, y2 - vpy)),
        #            ('c3f', (0.8, 0.8, 0.8) * 2))

         #for now, just assume everything needs to be rendered
        self.update_labels()
        self.draw_entities()
        self.draw_track()
        self.draw_objects()
        self.fps_display.draw()
        self.main_batch.draw()

    def draw_entities(self):
        # TODO: check if entities are visible before drawing
        (vpx, vpy, vpwidth, vpheight) = self.viewport
        for entity in self.entities:
            entity.position = (entity.gp.x - vpx, entity.gp.y - vpy)

    def draw_track(self):
        (vpx, vpy, vpwidth, vpheight) = self.viewport
        for line in self.track.visible_track_segments:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                    ('v2f', (line.x1 - vpx, line.y1 - vpy, line.x2 - vpx,line.y2 - vpy)),
                    ('c3f', (.8,.8,.8)*2))
    
    def draw_objects(self):
        (vpx, vpy, vpwidth, vpheight) = self.viewport
        for objects in self.objects:
            for ruby in objects.visible:
                ruby.position = (ruby.gp.x - vpx, ruby.gp.y - vpy)
                ruby.draw()

    def on_key_press(self, symbol, modifiers):
        # called every time a key is pressed

        # quit if q is pressed
        if symbol == pyglet.window.key.Q:
            print "Our system has been shocked!! But remember to Salt the Fries"
            sys.exit(0)

        elif symbol == pyglet.window.key.SPACE:
            self.cart.jump()

        elif symbol == pyglet.window.key.R:
            print "Resetting cart position"
            self.cart.gp = (100, 650)

        #debug sfx
        elif symbol == pyglet.window.key.I:
            sounds.cart_jump.play()
        elif symbol == pyglet.window.key.O:
            sounds.cart_land.play()
        elif symbol == pyglet.window.key.P:
            sounds.cart_ruby.play()


    def on_key_release(self, symbol, modifiers):
        # called every time a key is released
        pass

    def update(self, dt):
        # main game loop
        # dt is time in seconds in between calls
        
        # update cart with track info for current x coord
        (track_height, track_angle) = self.track.track_info_at_x(self.cart.gp.x)
        self.cart.update(dt, track_height, track_angle)

        # update viewport and visible track/entities
        (track_height, track_angle) = self.track.track_info_at_x(self.cart.gp.x + settings.VIEWPORT_LOOKAHEAD)
        #TODO: ugly hack, keep viewport level for breaks in track (for breaks in track track_level < 0)
        if track_height > 0:
            self.viewport = Rect(self.cart.gp.x - settings.VIEWPORT_OFFSET_X, track_height - settings.VIEWPORT_OFFSET_Y, self.width, self.height)
        else:
            self.viewport = Rect(self.cart.gp.x - settings.VIEWPORT_OFFSET_X, self.viewport.y, self.width, self.height)
        
        self.track.update_visible(self.viewport)
        self.ruby_list.update_visible(self.viewport)
        self.obstacle_list.update_visible(self.viewport)

        self.check_collisions()

        if self.cart.gp.y < self.viewport.y - settings.DEAD_OFFSET_Y:
            self.die()

    def check_collisions(self):
        rubies_to_delete = []
        for ruby in self.ruby_list.visible:
            if self.cart.collides_with(ruby):
                print "collected ruby " + str(ruby)
                sounds.cart_ruby.play()
                self.score += 1
                rubies_to_delete.append(ruby)
        
        for ruby in rubies_to_delete:
            self.ruby_list.objects.remove(ruby)

    def die(self):
        if self.lives > 1:
            self.lives -= 1
            sounds.cart_die.play()
            self.update_labels()
            self.reset_level()
        else:
            self.game_over()

    def reset_level(self):
        self.cart.gp = Point(100.0, 650.0)
        self.cart.reset()
        pass

    def game_over(self):
        print "ALL YOUR LIFE ARE BELONG TO US"
        sys.exit(0)

    def update_labels(self):
        self.score_label.text = "Score: " + str(self.score)
        self.lives_label.text = "Lives: " + str(self.lives)
        if self.cart is not None:
            self.speed_label.text = "Cart speed: " + str(self.cart.velocity_x)

    def create_cart(self):
        self.cart = cart.Cart()
        self.cart.gp = Point(100.0, 650.0)
        self.cart.batch = self.main_batch
        self.entities.append(self.cart)
