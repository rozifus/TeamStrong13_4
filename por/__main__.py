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
    pyglet.clock.schedule(game.update) # main loop
    pyglet.clock.schedule_once(game.create_cart, .2)
    pyglet.clock.schedule_interval(game.spawn_ruby, .2)
    pyglet.app.run()

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1024, 768)
        self.main_batch = pyglet.graphics.Batch()
        
        self.score_label = pyglet.text.Label(text = "Score: 0", 
                                             x = settings.SCORE_LABEL_X, 
                                             y = settings.SCORE_LABEL_Y, 
                                             batch = self.main_batch)
        self.score = 0
        self.level = level.load(1)
        

        self.quit_label = pyglet.text.Label(text = "By NSTeamStrong: Press q to quit, space to jump cart", 
                                             x = settings.QUIT_LABEL_X, 
                                             y = settings.QUIT_LABEL_Y, 
                                             batch = self.main_batch)

        self.fps_display = pyglet.clock.ClockDisplay()

        self.track = track.Track()
        self.track.add_tracks(self.level.tracks)
        
        self.entities = []
        self.rubies = []

    def on_draw(self): #runs every frame
        self.clear()
        for line in self.track.track_segments:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                    ('v2f', (line.x1,line.y1,line.x2,line.y2)),
                    ('c3f', (.8,.8,.8)*2))

        
        self.fps_display.draw()
        self.main_batch.draw()

    def on_key_press(self, symbol, modifiers):
        # called every time a key is pressed

        # quit if q is pressed
        if symbol == pyglet.window.key.Q:
            sys.exit(0)

        elif symbol == pyglet.window.key.SPACE:
            print "Bouncing carts"
            for entity in self.entities:
                entity.bounce()

    def on_key_release(self, symbol, modifiers):
        # called every time a key is released
        pass

    def update(self, dt):
        # main game loop
        # dt is time in seconds in between calls
        
        self.score_label.text = "Score: " + str(self.score)

        # entity update
        entities_to_remove = []
        for entity in self.entities:
            entity.update(dt)

        for entity in entities_to_remove:
            self.delete_entity(entity)
            if entity in self.rubies:
                self.rubies.remove(entity)

    def delete_entity(self, entity):
        self.entities.remove(entity)
        

    def create_cart(self, dt):
        new_cart = cart.Cart()
        new_cart.sprite.batch = self.main_batch
        self.entities.append(new_cart)

    def spawn_ruby(self, dt):
        if len(self.entities) < 50:
            new_ruby = ruby.Ruby()
            new_ruby.update_position(random.random() * 1024.0, 700)
            new_ruby.sprite.batch = self.main_batch
            self.rubies.append(new_ruby)
            self.entities.append(new_ruby)
