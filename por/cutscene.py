# cutscene
import pyglet
import settings

class Cutscene(object):
    def __init__(self, game):
        self.game = game
        self.main_batch = pyglet.graphics.Batch()
        self._title = None
        self._python_quote = None
        self._ruby_quote = None
        self._status = None
        
        lord_ruby_image = pyglet.resource.image("lord_ruby.png")
        cart_image = pyglet.resource.image("cart_large.png")
        self.lord_ruby = pyglet.sprite.Sprite(batch=self.main_batch,
                img=lord_ruby_image)
        self.cart = pyglet.sprite.Sprite(batch=self.main_batch,
                img=cart_image)
        self.title_label = pyglet.text.Label(batch=self.main_batch)
        self.title_label.text = self.title
        
        self.python_label = pyglet.text.Label(batch=self.main_batch)
        self.python_label.text = self.python_quote
        self.ruby_label = pyglet.text.Label(batch=self.main_batch)
        self.ruby_label.text = self.ruby_quote
        self.status_label = pyglet.text.Label(batch=self.main_batch)
        self.status_label.text = self.status
        self.controls_label = pyglet.text.Label(batch=self.main_batch,
                text="[space] to continue")
        self.all_labels = [self.title_label, self.python_label,
                self.status_label, self.ruby_label]


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
    @property
    def python_quote(self):
        if not self._python_quote:
            self._python_quote = "Give up Ruby! You're not as cool as you think you are."
        return self._python_quote
    @python_quote.setter
    def python_quote(self, quote):
        self._python_quote = quote
        self.python_label.text = self._python_quote
        self.layout()

    @property
    def ruby_quote(self):
        if not self._ruby_quote:
            self._ruby_quote = "Never!"
        return self._ruby_quote
    @ruby_quote.setter
    def ruby_quote(self, quote):
        self._ruby_quote = quote
        self.ruby_label.text = self._ruby_quote
        self.layout()

    @property
    def title(self):
        if not self._title:
            self._title = "Cutscene"
        return self._title
    @title.setter
    def title(self, text):
        self._title = text
        self.title_label.text = self._title
        self.layout()

    @property
    def status(self):
        if not self._status:
            self._status = "Lives: Infinite"
        return self._status
    @status.setter
    def status(self, text):
        self._status = text
        self.status_label.text = self._status
        self.layout()
