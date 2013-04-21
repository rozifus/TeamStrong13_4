# cutscene
import pyglet
import settings
import math
import random

class Cutscene(object):
    def __init__(self, game, title="", python="", ruby="", status="", label=None):
        self.game = game
        self.main_batch = pyglet.graphics.Batch()
        if not label:
            label = "cutscene_finished"
        self.finish_label = label

        self.pep20 = [
                "Beautiful is better than ugly.",
                "Explicit is better than implicit.",
                "Simple is better than complex.",
                "Complex is better than complicated.",
                "Flat is better than nested.",
                "Sparse is better than dense.",
                "Readability counts.",
                "Special cases aren't special enough to break the rules. Although practicality beats purity.",
                "Errors should never pass silently.",
                "Unless explicitly silenced.",
                "In the face of ambiguity, refuse the temptation to guess.",
                "There should be one-- and preferably only one --obvious way to do it. Although that way may not be obvious at first unless you're Dutch.",
                "Now is better than never. Although never is often better than *right* now.",
                "If the implementation is hard to explain, it's a bad idea.",
                "If the implementation is easy to explain, it may be a good idea.",
                "Namespaces are one honking great idea -- let's do more of those!",
                ]
        
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
        self.status_label.text = status or "{0} rubies".format(self.game.scores['rubies'])

        self.controls_label = pyglet.text.Label(batch=self.main_batch,
                text="[space] to continue")

        self.pep20_label = pyglet.text.Label(batch=self.main_batch)
        self.pep20_label.text = self.pep20[random.randint(0, len(self.pep20) - 1)]

        #self.fps_display = pyglet.clock.ClockDisplay()
        self.layout()

    def layout(self):
        # set font sizes
        
        self.title_label.font_size = self.game.window.height / 10.0
        self.status_label.font_size = self.game.window.height / 40.0
        self.python_label.font_size = self.game.window.height / 40.0
        self.ruby_label.font_size = self.game.window.height / 40.0
        self.controls_label.font_size = self.game.window.height / 40.0
        self.pep20_label.font_size = self.game.window.height / 60.0
        
        # center labels
        for label in [self.title_label, self.status_label, self.controls_label, self.pep20_label]:
            label.x = (self.game.window.width - label.content_width) / 2.0
        
        self.title_label.y = self.game.window.height * 0.85
        self.status_label.y = self.game.window.height * 0.75
        self.pep20_label.y = self.game.window.height * 0.80
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
        self.pep20_label.color = settings.MENU_COLOR_CONTROLS
        #for label in self.option_labels:
        #    label.color = settings.MENU_COLOR_OPTION
        #self.controls_label.color = settings.MENU_COLOR_CONTROLS
        #self.by_label.color = settings.MENU_COLOR_BY

        

    def start(self):
        pass
    
    def stop(self):
        self.main_batch = None

    def finish(self):
        self.game.scene_finished(self.finish_label)

    def on_draw(self):
        self.game.window.clear()
        #self.fps_display.draw()
        self.main_batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.finish()
