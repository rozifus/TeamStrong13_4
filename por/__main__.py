import pyglet
import sys
import math
import random
import settings
import pymunk

def main():
    """ your app starts here
    """
    pyglet.resource.path = settings.RESOURCE_PATH
    pyglet.resource.reindex()
    game = Game()
    pyglet.clock.schedule(game.update) # main loop
    pyglet.clock.schedule_once(game.spawn_logo, .1)
    pyglet.clock.schedule_interval(game.spawn_logo, 10/6.)

    pyglet.app.run()

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game, self).__init__(1024, 768)
        self.main_batch = pyglet.graphics.Batch()
        
        self.score_label = pyglet.text.Label(text = "Score: 0", 
                                             x = settings.SCORE_LABEL_X, 
                                             y = settings.SCORE_LABEL_Y, 
                                             batch = self.main_batch)
        

        self.quit_label = pyglet.text.Label(text = "By NSTeamStrong: Press q to quit", 
                                             x = settings.QUIT_LABEL_X, 
                                             y = settings.QUIT_LABEL_Y, 
                                             batch = self.main_batch)

        self.fps_display = pyglet.clock.ClockDisplay()
        
        # set up pymunk
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0.0, settings.GRAVITY)
        
        static_body = pymunk.Body()
        self.static_lines = [pymunk.Segment(static_body, (11.0, 280.0), (407.0, 246.0), 0.0)
                            ,pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                            ]
        for l in self.static_lines:
            l.friction = 0.5
        
        self.space.add(self.static_lines)
        self.logos = []

    def on_draw(self): #runs every frame
        self.clear()
        for line in self.static_lines:
            body = line.body
             
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2f', (pv1.x,pv1.y,pv2.x,pv2.y)),
                ('c3f', (.8,.8,.8)*2)
                )

        
        #debug draw
        for logo_sprite in self.logos:
            ps = logo_sprite.shape.get_points()
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

    def on_key_release(self, symbol, modifiers):
        # called every time a key is released
        pass

    def update(self, dt):
        # main game loop
        # dt is time in seconds in between calls

        # pymunk update
        self.space.step(dt)

        for sprite in self.logos:
            # We need to rotate the image 180 degrees because we have y pointing 
            # up in pymunk coords.
            sprite.rotation = math.degrees(-sprite.body.angle) + 180
            sprite.set_position(sprite.body.position.x, sprite.body.position.y)

    def center_image(self, image):
        """Sets an image's anchor point to its center"""
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2

    def spawn_logo(self, dt):
        x = random.randint(20,400)
        y = 500
        angle = random.random() * math.pi
        vs = [(-23,26), (23,26), (0,-26)]
        mass = 10
        moment = pymunk.moment_for_poly(mass, vs)
        body = pymunk.Body(mass, moment)
        shape = pymunk.Poly(body, vs)
        shape.friction = 0.5
        body.position = x, y
        body.angle = angle
        
        self.space.add(body, shape)
        
        cart_image = pyglet.resource.image("cart.png")
        self.center_image(cart_image)
        sprite = pyglet.sprite.Sprite(img = cart_image,
                                                x = settings.CART_X,
                                                y = settings.CART_Y,
                                                batch = self.main_batch)
        sprite.shape = shape
        sprite.body = body
        self.logos.append(sprite) 
        
