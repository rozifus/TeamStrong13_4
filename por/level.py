"""
Stuff related to loading and rendering a level.
"""

# This code is so you can run the samples without installing the package
import sys
import os

import pyglet
from pyglet.window import key

from pytmx import tmxloader

import cocos
from cocos import tiles, actions, layer, sprite
from cocos.director import director

import settings

from collections import namedtuple

Vector = namedtuple('Vector', 'x y')

def main():

    pyglet.resource.path = settings.RESOURCE_PATH
    pyglet.resource.reindex()

    director.init(width=640, height=320, do_not_scale=True, resizable=True)

    scroller = layer.ScrollingManager()
    tmx = tiles.load('underground-level1.tmx')
    tilemap = tmx['map']

    tmx = tmxloader.load_tmx(pyglet.resource.file('underground-level1.tmx'))
    triggers = tmx['triggers']

    startcell, = triggers.find('player')
    pos = Vector(startcell.x + startcell.width // 2, startcell.y + startcell.height // 2)
    cart_image = pyglet.resource.image("cart.png")
    hero = sprite.Sprite(image=cart_image, position=(pos.x, 320 - pos.y), scale=0.09697)

    scroller.add(tilemap)

    main_scene = cocos.scene.Scene(scroller)
    main_scene.add(hero)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def on_key_press(key, modifier):
        if key == pyglet.window.key.Z:
            if scroller.scale == .75:
                scroller.do(actions.ScaleTo(1, 2))
            else:
                scroller.do(actions.ScaleTo(.75, 2))
        elif key == pyglet.window.key.D:
            bg.set_debug(True)
    director.window.push_handlers(on_key_press)

    director.run(main_scene)

if __name__ == '__main__':
    main()