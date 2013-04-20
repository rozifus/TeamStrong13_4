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

glevels = []

class GameLevel(object):
    name = "default"
    music = 'strike-force'
    VIEWPORT_MAX_RATE = settings.VIEWPORT_MAX_RATE

    def __init__(self, game):
        super(GameLevel, self).__init__()

        glevels.append(self)
        if self.music:
            music.play(self.music)

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
        self.catchup = True
        self.setup(self.name)
    
    # next 3 are needed to play nicely with scene manager
    def start(self):
        pyglet.clock.schedule(self.update) # main loop

    def stop(self):
        pyglet.clock.unschedule(self.update)
        self.fps_display.unschedule()
        pass

    def finish(self, skip=None):
        label = getattr(self, 'finish_label', 'level_finished')
        self.game.scene_finished(label, skip=skip)

    def setup(self, levelname):
        sounds.load()
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
        self.viewport.reset(
            Rect(self.cart.gp.x, 
                self.cart.gp.y - self.height / 2,
                self.width, self.height))

        # now check the level contents.
        self.bg = scene.Background(self.level.layers, self.viewport)

    def on_draw(self): #runs every frame
        self.game.window.clear()
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
            (x, y, r, x1, y1, x2, y2, x3, y3, x4, y4, ctr, ctg, ctb, cbr, cbg, cbb) = sleeper
            vertices.extend([x1 - vpx, y1 - vpy, x2 - vpx, y2 - vpy, x3 - vpx, y3 - vpy, x4 - vpx, y4 - vpy])
            colors.extend([ctr, ctg, ctb, ctr, ctg, ctb])
            colors.extend([cbr, cbg, cbb, cbr, cbg, cbb])
        
        if len(colors) > 0 and len(vertices) > 0:
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

        if len(colors) > 0 and len(vertices) > 0:
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
            self.cart.gp = self.spawn_points[0].gp

        elif symbol == pyglet.window.key.I:
            raw_input()
        elif symbol == pyglet.window.key.O:
            music.next()
        elif symbol == pyglet.window.key.P:
            music.stop()
        else:
            # ok check for level skipping.
            level = skip.get(symbol)
            if level:
                self.finish(skip=level)



    def on_key_release(self, symbol, modifiers):
        # called every time a key is released
        pass

    def update(self, dt):
        # main game loop
        # dt is time in seconds in between calls

        # update cart with track info for current x coord
        (track_height, track_angle) = self.track.track_info_at_x(self.cart.gp)
        self.cart.update(dt, track_height, track_angle)

        # update viewport and visible track/entities
        viewpos = Point(self.cart.gp.x + settings.VIEWPORT_LOOKAHEAD, self.cart.gp.y)
        (track_height, track_angle) = self.track.track_info_at_x(viewpos)
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
            self.game.scores['rubies'] += 1
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
        self.cart.gp = gp = self.spawn_points[0].gp
        self.cart.reset()
        self.viewport.reset(Rect(gp.x, gp.y - self.height / 2, self.width, self.height))

    def game_over(self):
        if self.lives <= 1:
            print "ALL YOUR LIFE ARE BELONG TO US"
        self.game.scene_finished("defeat")

    def update_labels(self):
        self.score_label.text = "Score: " + str(self.game.scores['rubies'])
        self.lives_label.text = "Lives: " + str(self.lives)
        if self.cart is not None:
            self.speed_label.text = "Cart speed: " + str(self.cart.velocity_x)

    def create_cart(self):
        self.cart = cart.Cart()
        self.cart.gp = self.spawn_points[0].gp
        self.cart.batch = self.main_batch
        self.entities.append(self.cart)

class Level2(GameLevel): name = "level2"
class Level3(GameLevel): name = "level3"
class Level4(GameLevel): name = "level4"
class Level5(GameLevel): name = "level5"
class Level6(GameLevel):
    name = "level6"
    VIEWPORT_MAX_RATE = 20
class Level7(GameLevel): name = "level7"
class Level8(GameLevel): name = "level8"
class Level9(GameLevel): 
    name = "level9"
    finish_label = "victory"

glevels.extend([GameLevel, Level2, Level3, Level4, Level5, Level6, Level7,
                Level8, Level9])

# for now allow skipping.
skip = {
    pyglet.window.key._1: 1
    , pyglet.window.key._2: 2
    , pyglet.window.key._3: 3
    , pyglet.window.key._4: 4
    , pyglet.window.key._5: 5
    , pyglet.window.key._6: 6
    , pyglet.window.key._7: 7
    , pyglet.window.key._8: 8
    , pyglet.window.key._9: 9
}

