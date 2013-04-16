import pyglet

import cocos
from cocos.director import director

from pytmx import tmxloader

import settings, backgrounds

class GameScene(cocos.scene.Scene):

    def __init__(self):
        super(GameScene, self).__init__()
        self.manager = cocos.layer.ScrollingManager(director.window)

        pyglet.resource.path = settings.RESOURCE_PATH
        pyglet.resource.reindex()

        tmx = cocos.tiles.load('underground-level1.tmx')
        bg = tmx['map']

        self.add(bg, z=-1)
        self.manager.add(bg)
 
    
        # tmx = tmxloader.load_tmx(pyglet.resource.file('underground-level1.tmx'))
        # triggers = tmx['triggers']

        # self.manager.add(self.bg)
        # self.add(self.bg, z=-1)


    def focus(self):
        self.do(FocusOnHero())

    def init():
        
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
        static_body = pymunk.Body()
        self.track = [pymunk.Segment(static_body, (0.0, 300.0), (150.0, 150.0), 0.0),
                             pymunk.Segment(static_body, (150.0, 150.0), (300.0, 75.0), 0.0),
                             pymunk.Segment(static_body, (300.0, 75.0), (450.0, 75.0), 0.0),
                             pymunk.Segment(static_body, (450.0, 75.0), (600.0, 150.0), 0.0),
                             pymunk.Segment(static_body, (600.0, 150.0), (750.0, 300.0), 0.0)]
        
        for l in self.track:
            l.friction = settings.TRACK_FRICTION 
        
        self.space.add(self.track)
        self.entities = []
        self.rubies = []