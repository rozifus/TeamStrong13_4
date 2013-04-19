
import pyglet

__tracks = {}
__player = pyglet.media.Player()
__player.eos_action = __player.EOS_LOOP
__currentIndex = None
__loaded = False

def addTrack(name, location):
    global __tracks
    try:
        track = pyglet.resource.media(location, streaming=False)
    except pyglet.media.MediaException:
        print 'You should install AVBin so you can hear the sounds'
        print '   http://code.google.com/p/avbin/'
        print "(install a binary, don't try to compile)"
        return
    except:
        return
    __tracks[name] = track

def load():
    global __loaded
    if not __loaded:
        addTrack('strike-force', 'skuter-strike_force.mp3')
        addTrack('pink', 'pink-turrican_gbc6.mp3')
    __loaded = True

def play(index):
    global __currentIndex, __player, __tracks
    if not len(__tracks):
        print("Can't play: No tracks.")
        return

    if index == __currentIndex:
        # nothing to-do, we are already playing.
        return 

    # ok stop the jukebox and put the next song on.
    stop()

    try:
       track =__tracks[index]
    except KeyError:
        return

    print "playing {0}".format(index)
    __currentIndex = index
    __player.queue(__tracks[index])
    __player.play()

def restart():
    global __currentIndex
    stop()
    play(__currentIndex)

def pause():
    global __player, __tracks
    if not len(__tracks): return
    __player.pause()

def stop():
    global __player, __tracks, __currentIndex
    if not len(__tracks): return

    __currentIndex = None
    __player.pause()
    __player = pyglet.media.Player()
    __player.eos_action = __player.EOS_LOOP


