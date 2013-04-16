import pyglet
import sys
import math
import random
import settings

import entity
import cart
import ruby
import track
import level

def main():
    """ your app starts here
    """
    pyglet.resource.path = settings.RESOURCE_PATH
    pyglet.resource.reindex()
    game = Game()
    game.start()

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1024, 768)
        self.main_batch = pyglet.graphics.Batch()
        self.score_label = pyglet.text.Label(text = "", 
                                             x = settings.SCORE_LABEL_X, 
                                             y = settings.SCORE_LABEL_Y, 
                                             batch = self.main_batch)
        self.score = 0
        self.level = level.load(1)
        

        self.quit_label = pyglet.text.Label(text = "By NSTeamStrong: q [quit] space [jump] r [reset]", 
                                             x = settings.QUIT_LABEL_X, 
                                             y = settings.QUIT_LABEL_Y, 
                                             batch = self.main_batch)
        self.fps_display = pyglet.clock.ClockDisplay()
        
        self.cart = None

        self.jtrack = track.Track()
        self.jtrack.add_tracks(self.level.tracks)
        
        self.rubies = []
        self.powerups = []
        self.obstacles = []
        self.track = [((0.0, 300.0), (300.0, 100.0)),
                      ((300.0, 100.0), (700.0, 100.0)),
                      ((700.0, 100.0), (900.0, 500.0))]

    def track_info_at_x(self, x):
        #TODO: this should be in the track module
        height = -1000.0 # default off the screen
        angle = 0.0
        for segment in self.track:
            #y = mx + c, tnx eng degree
            (x1, y1), (x2, y2) = segment
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            if x > x1 and x <= x2:
                height = m * x + c
                angle = math.degrees(math.atan2(m, 1.0))
    
        return (height, angle)

    def start(self):
        self.create_cart()
        pyglet.clock.schedule(self.update) # main loop
        pyglet.app.run()


    def on_draw(self): #runs every frame
        self.clear()

        # draw the track
        for line in self.track:
            (x1, y1), (x2, y2) = line
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                    ('v2f', (x1, y1, x2, y2)),
                    ('c3f', (0.8, 0.8, 0.8) * 2))
        
        # uncomment this to show the jtrack
        #for line in self.jtrack.track_segments:
        #    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #            ('v2f', (line.x1,line.y1,line.x2,line.y2)),
        #            ('c3f', (.8,.8,.8)*2))

        
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
            self.cart.position = (100, 650)

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
        (track_height, track_angle) = self.track_info_at_x(self.cart.x)
        self.cart.update(dt, track_height, track_angle)

    def create_cart(self):
        self.cart = cart.Cart()
        self.cart.position = (100, 650)
        self.cart.batch = self.main_batch
