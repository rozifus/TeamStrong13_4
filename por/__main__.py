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

        self.viewport_origin = (0.0, 0.0)
        self.viewport_size = (self.width, self.height)
        self.renderzone_buffer_size = (500.0, 500.0)

        self.main_batch = pyglet.graphics.Batch()
        self.score_label = pyglet.text.Label(text = "",
                                             x = settings.SCORE_LABEL_X,
                                             y = settings.SCORE_LABEL_Y,
                                             batch = self.main_batch)
        self.score = 0


        self.quit_label = pyglet.text.Label(text = "By NSTeamStrong: q [quit] space [jump] r [reset] i,o,p [sfx]",
                                             x = settings.QUIT_LABEL_X,
                                             y = settings.QUIT_LABEL_Y,
                                             batch = self.main_batch)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.cart = None

        self.entities = []
        self.rubies = []
        self.powerups = []
        self.obstacles = []
        #self.track = [((0.0, 300.0), (300.0, 100.0)),
        #              ((300.0, 100.0), (700.0, 100.0)),
        #              ((700.0, 100.0), (900.0, 500.0))]

    def start(self, levelname):
        self.level = level.load(levelname)
        self.track = track.Track()
        self.track.add_tracks(self.level.tracks)

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

        (vpx, vpy) = self.viewport_origin

        #for line in self.track:
        #    (x1, y1), (x2, y2) = line
        #    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #            ('v2f', (x1 - vpx, y1 - vpy, x2 - vpx, y2 - vpy)),
        #            ('c3f', (0.8, 0.8, 0.8) * 2))

         #for now, just assume everything needs to be rendered
        for line in self.track.track_segments:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                    ('v2f', (line.x1 - vpx, line.y1 - vpy, line.x2 - vpx,line.y2 - vpy)),
                    ('c3f', (.8,.8,.8)*2))

        for entity in self.entities:
           (vpx, vpy) = self.viewport_origin
           (gpx, gpy) = entity.gp
           entity.position = (gpx - vpx, gpy - vpy)


        self.fps_display.draw()
        self.main_batch.draw()

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

        elif symbol == pyglet.window.key.RIGHT:
            (x, y) = self.viewport_origin
            self.viewport_origin = (x + 100.0, y)

        elif symbol == pyglet.window.key.LEFT:
            (x, y) = self.viewport_origin
            self.viewport_origin = (x - 100.0, y)

        elif symbol == pyglet.window.key.DOWN:
            (x, y) = self.viewport_origin
            self.viewport_origin = (x, y - 100.0)

        elif symbol == pyglet.window.key.UP:
            (x, y) = self.viewport_origin
            self.viewport_origin = (x, y + 100.0)

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

        self.score_label.text = "Score: " + str(self.score)

        # TODO: this should query the track module for the
        # track_height and track_angle for the cart's x coord
        # here i have jsut written a method to do it
        (gpx, gpy) = self.cart.gp
        (track_height, track_angle) = self.track.track_info_at_x(gpx)
        print "track height: " + str(track_height) + " angle " + str(track_angle)
        self.cart.update(dt, track_height, track_angle)
        self.viewport_origin = (gpx - settings.VIEWPORT_OFFSET_X, track_height - settings.VIEWPORT_OFFSET_Y)

    def scroll(self, dt):
        pass

    def create_cart(self):
        self.cart = cart.Cart()
        self.cart.gp = (100, 650)
        self.cart.batch = self.main_batch
        self.entities.append(self.cart)
