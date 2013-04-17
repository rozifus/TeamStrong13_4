"""
Stuff related to loading and rendering a level.
"""

# This code is so you can run the samples without installing the package
from collections import namedtuple
import math
import os
import random
import sys

import pyglet

from pytmx import tmxloader

import ruby
import settings
from utils import pairwise

LineSegment = namedtuple('Vector', 'x1 y1 x2 y2')

class LevelLoader(object):
    """
    The tmx object should have these layers:

    1. 'map' for the background
    2. 'triggers' for the object world.
    """

    def __init__(self, tmx):
        self.tmx = tmx

    @property
    def tracks(self):
        _tracks = self.tmx['track']
        segments = []
        for track in _tracks:
            for (x1, y1), (x2, y2) in pairwise(track.points):
                segments.append(
                    LineSegment(
                        x1 + track.x, -y1 + track.y,
                        x2 + track.x, -y2 + track.y))
        print "number of segments in level is " + str(len(segments))
        return segments

    @property
    def rubies(self):
        _rubies = []
        for tiled_object in self.tmx['rubies']:
            _rubies.append((tiled_object.x, tiled_object.y))
        print "number of rubies in level is " + str(len(_rubies))
        return _rubies;

def load(level):
    """
    Load level number from tmx file.
    """
    levelfname = level + ".tmx"
    print "Loading level " + levelfname
    tmx = tmxloader.load_tmx(pyglet.resource.file(levelfname))

    return LevelLoader(tmx)

def main():

    pyglet.resource.path = settings.RESOURCE_PATH
    pyglet.resource.reindex()

    director.init(width=1024, height=768, do_not_scale=True, resizable=True)

    scroller = layer.ScrollingManager()

    tmx = tiles.load('underground-level1.tmx')
    tilemap = tmx['map']



    # physics,yo
    space = pymunk.Space()
    space.gravity = pymunk.Vec2d(0.0, settings.GRAVITY)

    # set up our hero cart.
    startcell, = triggers.find('player')
    cart_image = pyglet.resource.image("cart.png")
    pos = Vector(startcell.x + cart_image.width // 2, startcell.y + cart_image.height // 2)
    hero = make_sprite(image=cart_image, position=(pos.x, tilemap.px_height - pos.y))
    space.add(hero.body, hero.shape)
        

    # set up our blockers.
    blockers = triggers.find('blocker')
    walls = []
    static_body = pymunk.Body()
    for blocker in blockers:
        try:
            line_blocker(blocker, walls, tilemap.px_height, static_body)
        except AttributeError:
            # ok then treat as a rect blocker.
            rect_blocker(blocker, walls, tilemap.px_height, static_body)

    [setattr(wall, 'friction', 0.1) for wall in walls]
    space.add(walls)


    # set up our in-game collectables.
    rubies = triggers.find('Ruby')
    rubis = []
    for _ruby in rubies:
        new_ruby = ruby.Ruby()
        new_ruby.update_position(_ruby.x, tilemap.px_height - _ruby.y)
        rubis.append(new_ruby.sprite)

    scroller.add(tilemap, z=-1)
    scroller.add(CollisionLayer(walls))

    class FocusOnHero(actions.Action):
        def done(self): return False
        def step(self, dt):
            x, y = self.target.hero.position
            self.target.manager.set_focus(x, y)

    main_scene = cocos.scene.Scene(scroller)
    main_scene.manager = scroller
    main_scene.add(hero)
    main_scene.hero = hero
    main_scene.do(FocusOnHero())
    map(main_scene.add, rubis)

    def update(dt):
        space.step(dt)
        hero.set_position(*hero.body.position)

    pyglet.clock.schedule(update)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def on_key_press(key, modifier):
        """K left J right"""
        try:
            impulse = impulses[key]
        except KeyError:
            return

        hero.body.apply_impulse(impulse)

    director.window.push_handlers(on_key_press)

    director.run(main_scene)


def line_blocker(blocker, walls, map_height, static_body):
    """
    Turn a series of "points" on a poly-line into a rigid wall.
    """
    for (c1x, c1y), (c2x, c2y) in pairwise(blocker.points):
        c1 = Vector(c1x + blocker.x, map_height-(c1y + blocker.y))
        c2 = Vector(c2x + blocker.x, map_height-(c2y + blocker.y))
        walls.append(pymunk.Segment(static_body, c1, c2, 0))

def rect_blocker(blocker, walls, map_height, static_body):
    """turn the four corners of the 'blocker objects'
       defined in tilemap into rigid walls."""
    c1 = Vector(blocker.x, map_height - blocker.y)
    c2 = Vector(blocker.x + blocker.width, map_height - blocker.y)
    c3 = Vector(blocker.x + blocker.width, (map_height - blocker.y - blocker.height))
    c4 = Vector(blocker.x, (map_height - blocker.y - blocker.height))

    # a wall is a block made from four lines joining the four corners.
    walls.extend([pymunk.Segment(static_body, c1, c2, 0),
                  pymunk.Segment(static_body, c2, c3, 0),
                  pymunk.Segment(static_body, c3, c4, 0),
                  pymunk.Segment(static_body, c4, c1, 0)])


def make_sprite(**kwargs):
    # taken from Karl's __main__ code.
    _sprite = sprite.Sprite(**kwargs)
    angle = random.random() * math.pi
    vs = [(-75,-39), (-75,39), (75,39), (75, -39)]
    mass = 20
    moment = pymunk.moment_for_poly(mass, vs)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Poly(body, vs)
    shape.friction = 0.5
    body.position = _sprite.position
    body.angle = angle
        
    _sprite.shape = shape
    _sprite.body = body 
    return _sprite
