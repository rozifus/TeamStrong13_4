import pyglet
import sys
import math
import settings

def main():
    """ your app starts here
    """
    pyglet.resource.path = settings.RESOURCE_PATH
    pyglet.resource.reindex()
    game = Game()
    pyglet.clock.schedule(game.update) # main loop
    pyglet.app.run()

    #cart_image = pyglet.resource.image("cart.png")
    #score_label = pyglet.text.Label(text = "Score: 0", x = 10, y = 10)
    #fps_label = pyglet.text.Label(text = "FPS: 1271", x = 10, y = 50)

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

        cart_image = pyglet.resource.image("cart.png")
        self.center_image(cart_image)
        self.cart_sprite = pyglet.sprite.Sprite(img = cart_image,
                                                x = settings.CART_X,
                                                y = settings.CART_Y,
                                                batch = self.main_batch)
        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self): #runs every frame
        self.clear()
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
        rotation = dt * 360.0
        if rotation > 360.0:
            rotation -= 360.0
        self.cart_sprite.rotation += dt * 180.0

    def center_image(self, image):
        """Sets an image's anchor point to its center"""
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2
        
