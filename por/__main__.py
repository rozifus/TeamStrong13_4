import pyglet
import sys
import math
import random
import settings
import pymunk

import entity
import cart
import ruby
import track

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
        

        self.quit_label = pyglet.text.Label(text = "By NSTeamStrong: Press q to quit, space to jump cart", 
                                             x = settings.QUIT_LABEL_X, 
                                             y = settings.QUIT_LABEL_Y, 
                                             batch = self.main_batch)

        self.fps_display = pyglet.clock.ClockDisplay()
        
        # set up pymunk
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0.0, settings.GRAVITY)
        self.space.add_collision_handler(settings.COLLISION_CART, 
                                         settings.COLLISION_RUBY, 
                                         begin=self.collision_cart_ruby_begin)
        
        # dish shaped ramp
        self.track = track.Track(self.space, (0, 200))
        self.track.add_track_string("ddffffffufufufddddffuu")

        
        self.entities = []
        self.rubies = []

    def on_draw(self): #runs every frame
        self.clear()
        for track_segment in self.track.track_segments:
            for line in track_segment.track:
                body = line.body
                pv1 = body.position + line.a.rotated(body.angle)
                pv2 = body.position + line.b.rotated(body.angle)
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                    ('v2f', (pv1.x,pv1.y,pv2.x,pv2.y)),
                    ('c3f', (.8,.8,.8)*2)
                    )

        
        #debug draw
        for entity in self.entities:
            ps = entity.shape.get_points()
            n = len(ps)
            ps = [c for p in ps for c in p]
            pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP,
                ('v2f', ps),
                ('c3f', (1,0,0)*n)
                )

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
        # pymunk update
        self.space.step(dt)

        # entity update
        entities_to_remove = []
        for entity in self.entities:
            entity.update(dt)
            x, y = entity.body.position
            if y < 0 or entity.deletion_flag:
                entities_to_remove.append(entity)

        for entity in entities_to_remove:
            self.delete_entity(entity)
            if entity in self.rubies:
                self.rubies.remove(entity)

    def collision_cart_ruby_begin(self, space, arbiter, *args, **kwargs):
        print "Detected collision between cart and ruby"
        print "shapes are " + str(arbiter.shapes)
        
        ruby_to_delete = None
        for ruby in self.rubies:
            if ruby.shape == arbiter.shapes[1]:
                ruby.deletion_flag = True
                ruby_to_delete = ruby
                self.score = self.score + 1
                break
        self.rubies.remove(ruby_to_delete)
        return False

    def delete_entity(self, entity):
        self.space.remove(entity.shape, entity.body)
        self.entities.remove(entity)
        

    def create_cart(self, dt):
        new_cart = cart.Cart()
        new_cart.sprite.batch = self.main_batch
        self.space.add(new_cart.body, new_cart.shape)
        self.entities.append(new_cart)

    def spawn_ruby(self, dt):
        if len(self.entities) < 50:
            new_ruby = ruby.Ruby()
            new_ruby.update_position(random.random() * 1024.0, 700)
            new_ruby.sprite.batch = self.main_batch
            self.space.add(new_ruby.body, new_ruby.shape)
            self.rubies.append(new_ruby)
            self.entities.append(new_ruby)
