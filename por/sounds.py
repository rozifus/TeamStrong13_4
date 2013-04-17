
import pyglet

class DummySound(object):
    @classmethod
    def play(*args): print('dummy sound - sound not played')
cart_jump = cart_land = cart_ruby = DummySound()

def load():
    global cart_jump, cart_land, cart_ruby, cart_die
    try:
        cart_jump = pyglet.resource.media('cart_jump.wav', streaming=False)
        cart_land = pyglet.resource.media('cart_land.wav', streaming=False)
        cart_ruby = pyglet.resource.media('cart_ruby.wav', streaming=False)
        cart_die = pyglet.resource.media('cart_die.wav', streaming=False)
    except pyglet.media.MediaException:
        print 'You should install AVBin so you can hear the sounds'
        print '   http://code.google.com/p/avbin/'
        print "(install a binary, don't try to compile)"

