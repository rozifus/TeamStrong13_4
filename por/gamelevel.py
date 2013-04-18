import pyglet
import sys
import math
import random
import settings
from itertools import chain

import entity
import sounds
import music
import cart
import ruby
import scene
import track
import level
import obstacle

from collections import namedtuple
from utils import Point, Vec2d, Rect

class GameLevel(object):
    def __init__(self, game):
        super(GameLevel, self).__init__()
        # in game coords. viewport is your window into game world
        self.game = game
        pyglet.gl.glClearColor(*settings.BACKGROUND_COLOUR)
        self.width = self.game.window.width
        self.height = self.game.window.height
        self.viewport = scene.ViewportManager(Rect(0.0, 0.0, self.width, self.height))
        

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
    
    # next 3 are needed to play nicely with scene manager
    def start(self):
        self.start2("default")

    def stop(self):
        pyglet.clock.unschedule(self.update)
        pass

    def finish(self):
        self.game.scene_finished("BLAH BLAH BLAH")

    def start2(self, levelname):
        sounds.load()
        self.score = 0
        self.lives = settings.STARTING_LIVES
        self.update_labels()
        print str(pyglet.resource.path)
        self.level = level.load(levelname)
        self.track = track.Track()
        self.track.add_tracks(self.level.tracks)
        self.ruby_list = entity.ObjectList({'default': ruby.Ruby})
        self.ruby_list.add(self.level.rubies)
        self.obstacle_list = entity.ObjectList({
                                        'default': obstacle.Obstacle,
                                        'exit': obstacle.EndLevel})
        self.obstacle_list.add(self.level.obstacles)
        self.spawn_points = entity.ObjectList({'default': obstacle.Spawn})
        self.spawn_points.add(self.level.spawn)
        self.entities.extend(self.spawn_points.objects)

        self.objects = [self.ruby_list, self.obstacle_list]

        self.create_cart()

        # now check the level contents.
        self.bg = scene.Background(self.level.layers, self.viewport)

        pyglet.clock.schedule(self.update) # main loop

    def on_draw(self): #runs every frame
        self.game.window.clear()
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

        # draw the background


         #for now, just assume everything needs to be rendered
        self.bg.draw()
        self.draw_track()
        self.update_labels()
        self.draw_entities()
        self.draw_objects()
        self.fps_display.draw()
        self.main_batch.draw()

    def draw_entities(self):
        # TODO: check if entities are visible before drawing
        (vpx, vpy, vpwidth, vpheight) = self.viewport
        for entity in self.entities:
            entity.position = (entity.gp.x - vpx, entity.gp.y - vpy)
            entity.draw()

    def draw_track(self):
        (vpx, vpy, vpwidth, vpheight) = self.viewport
        vertices = []
        colors = []
        #sleeper magick
        for sleeper in self.track.visible_sleepers:
            # 1 top left, 2 top right, 3 bottom right, 4 bottom left of sleeper
            jitter_length = (random.random() * 20.0 - 10.0)
            jitter_width = (random.random() * 10.0 - 5.0)
            sl = settings.SLEEPER_LENGTH / 2.0 + jitter_length
            sw = settings.SLEEPER_WIDTH / 2.0 + jitter_width
            (x, y, r) = sleeper
            x -= vpx
            y -= vpy 
            x1 = x - sw
            y1 = y + sl
            x2 = x + sw
            y2 = y + sl 
            x3 = x + sw
            y3 = y - sl
            x4 = x - sw
            y4 = y - sl
            vertices.extend([x1, y1, x2, y2, x3, y3, x4, y4])
            colors.extend(settings.SLEEPER_COLOR_TOP)
            colors.extend(settings.SLEEPER_COLOR_BOTTOM)

        vlist = pyglet.graphics.vertex_list(len(self.track.visible_sleepers) * 4,
                ('v2f/stream', vertices),
                ('c3f/stream', colors))
        vlist.draw(pyglet.gl.GL_QUADS)
        vlist.delete()
        
        vertices = []
        colors = []
        for line in self.track.visible_track_segments:
            vertices.extend([line.x1 - vpx, line.y1 - vpy + settings.TRACK_WIDTH/2.0, line.x2 - vpx, line.y2 - vpy + settings.TRACK_WIDTH/2.0])
            colors.extend(settings.TRACK_COLOR_TOP)
            vertices.extend([line.x2 - vpx, line.y2 - vpy - settings.TRACK_WIDTH/2.0, line.x1 - vpx, line.y1 - vpy - settings.TRACK_WIDTH/2.0])
            colors.extend(settings.TRACK_COLOR_BOTTOM)

        vlist = pyglet.graphics.vertex_list(len(self.track.visible_track_segments) * 4,
                ('v2f/stream', vertices),
                ('c3f/stream', colors))
        vlist.draw(pyglet.gl.GL_LINES)
        vlist.delete()
        

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

        elif symbol == pyglet.window.key.I:
            raw_input()
        elif symbol == pyglet.window.key.O:
            music.next()
        elif symbol == pyglet.window.key.P:
            music.stop()


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

        # rate limit movements by settings.VIEWPORT_MAX_RATE px per frame.
        self.viewport.update(self.cart.gp.x, track_height)

        self.track.update_visible(self.viewport.rect)
        self.ruby_list.update_visible(self.viewport.rect)
        self.obstacle_list.update_visible(self.viewport.rect)

        self.check_collisions()

        if self.cart.gp.y < self.viewport.y - settings.DEAD_OFFSET_Y:
            self.die()

    def check_collisions(self):

        # rubies.
        rubies_to_delete = self.cart.collided_objects(self.ruby_list.visible)
        for ruby in rubies_to_delete:
            self.score += 1
            self.ruby_list.objects.remove(ruby)

        if rubies_to_delete:
            sounds.cart_ruby.play()

        # obstacles.
        for obstacle in chain(self.obstacle_list.visible, self.spawn_points):
            if obstacle.collides_with(self.cart):
                obstacle.collided(self)

    def die(self):
        if self.lives > 1:
            self.lives -= 1
            sounds.cart_die.play()
            self.update_labels()
            self.reset_level()
        else:
            self.game_over()

    def reset_level(self):
        self.cart.gp = self.spawn_points[0].gp
        self.cart.reset()
        self.viewport.reset(Rect(100, self.viewport.y, self.width, self.height))

    def game_over(self):
        if self.lives <= 1:
            print "ALL YOUR LIFE ARE BELONG TO US"
        sys.exit(0)

    def update_labels(self):
        self.score_label.text = "Score: " + str(self.score)
        self.lives_label.text = "Lives: " + str(self.lives)
        if self.cart is not None:
            self.speed_label.text = "Cart speed: " + str(self.cart.velocity_x)

    def create_cart(self):
        self.cart = cart.Cart()
        self.cart.gp = self.spawn_points[0].gp
        self.cart.batch = self.main_batch
        self.entities.append(self.cart)

class Level2(GameLevel):
    def start(self):
        self.start2("level2")