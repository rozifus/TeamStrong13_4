# cutscene
import pyglet
import settings

class Cutscene(object):
    def __init__(self, game, title="", python="", ruby="", status=""):
        self.game = game
        self.main_batch = pyglet.graphics.Batch()
        
        lord_ruby_image = pyglet.resource.image("lord_ruby.png")
        cart_image = pyglet.resource.image("cart_large.png")
        self.lord_ruby = pyglet.sprite.Sprite(batch=self.main_batch,
                img=lord_ruby_image)
        self.cart = pyglet.sprite.Sprite(batch=self.main_batch,
                img=cart_image)
        
        self.title_label = pyglet.text.Label(batch=self.main_batch)
        self.title_label.text = title
        
        self.python_label = pyglet.text.Label(batch=self.main_batch)
        self.python_label.text = python

        self.ruby_label = pyglet.text.Label(batch=self.main_batch)
        self.ruby_label.text = ruby 

        self.status_label = pyglet.text.Label(batch=self.main_batch)
        self.status_label.text = status

        self.controls_label = pyglet.text.Label(batch=self.main_batch,
                text="[space] to continue")

        self.layout()

    def layout(self):
        # set font sizes
        
        self.title_label.font_size = self.game.window.height / 10.0
        self.status_label.font_size = self.game.window.height / 40.0
        self.python_label.font_size = self.game.window.height / 40.0
        self.ruby_label.font_size = self.game.window.height / 40.0
        self.controls_label.font_size = self.game.window.height / 40.0
        
        # center labels
        for label in [self.title_label, self.status_label, self.controls_label]:
            label.x = (self.game.window.width - label.content_width) / 2.0
        
        self.title_label.y = self.game.window.height * 0.85
        self.status_label.y = self.game.window.height * 0.75
        self.controls_label.y = 20
        
        self.python_label.x = 20
        self.python_label.y = self.game.window.height * 0.6
        
        self.ruby_label.x = self.game.window.width - self.ruby_label.content_width - 20
        self.ruby_label.y = self.game.window.height * 0.50
        
        self.lord_ruby.x = self.game.window.width - self.lord_ruby.width
        self.lord_ruby.y = 20.0

        self.cart.x = 20
        self.cart.y = 100
        self.cart.rotation = -20
        # set colours
        self.title_label.color = settings.MENU_COLOR_TITLE
        self.status_label.color = settings.MENU_COLOR_OPTION
        self.controls_label.color = settings.MENU_COLOR_OPTION
        #for label in self.option_labels:
        #    label.color = settings.MENU_COLOR_OPTION
        #self.controls_label.color = settings.MENU_COLOR_CONTROLS
        #self.by_label.color = settings.MENU_COLOR_BY

        

    def start(self):
        print "Cutscene starting"
    
    def stop(self):
        print "Cutscene stopping"

    def finish(self):
        self.game.scene_finished("cutscene_finished")

    def on_draw(self):
        self.game.window.clear()
        self.main_batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.finish()
