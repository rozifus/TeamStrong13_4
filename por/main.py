import random

import pyglet

import cocos

from cocos.director import director
from cocos.menu import *
from cocos.actions import *

import game, help, backgrounds, settings

def main():
    director.init(width=1024, height=768)
    director.show_FPS = True

    pyglet.gl.glClearColor(1, 1, 1, 1)
    pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)

    menu = cocos.scene.Scene(MainMenu())
    menu.add(backgrounds.GradientLayer((200, 200, 100, 255),
        (200, 200, 200, 255)), z=-1)
    director.run(menu)

class MainMenu(Menu):
    def __init__( self ):
        super( MainMenu, self ).__init__("Python on Rails")

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        self.font_item['color'] = (0, 0, 0, 255)
        self.font_item_selected['color'] = (150, 150, 0, 255)
        self.font_title['color'] = (0, 0, 0, 255)

        items = []
        items.append( MenuItem('Play', self.on_play ) )
        items.append( MenuItem('Help', self.on_help ) )
        items.append( MenuItem('Quit', self.on_quit ) )

        self.create_menu(items)

    def on_play(self):
        director.push(game.GameScene())

    def on_help(self):
        director.push(help.HelpScene())

    def on_quit(self):
        pyglet.app.exit()

