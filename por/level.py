"""
Stuff related to loading and rendering a level.
"""

# This code is so you can run the samples without installing the package
import sys
import os

import pyglet
from pyglet.window import key

pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.path.append('data')
pyglet.resource.path.append('../data')
pyglet.resource.reindex()

import cocos
from cocos import tiles, actions, layer

def main():
    from cocos.director import director
    director.init(width=640, height=320, do_not_scale=True, resizable=True)

    scroller = layer.ScrollingManager()
    tmx = tiles.load('data/underground-level1.tmx')
    import pdb;pdb.set_trace()
    bg = tmx['map']
    playa = tmx['player']
    scroller.add(bg)
    scroller.add(playa)

    main_scene = cocos.scene.Scene(scroller)

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