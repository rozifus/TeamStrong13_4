import glob
import os

import pyglet

import settings


pyglet.resource.path = settings.RESOURCE_PATH
pyglet.resource.reindex()

sound = pyglet.resource.media('pink-turrican_gbc6.mp3')
sound.play()

while 1:
    import time
    time.sleep(10)

