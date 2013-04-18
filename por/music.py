
import pyglet

__tracks = []
__trackNames = {}
__player = pyglet.media.Player()
__player.eos_action = __player.EOS_LOOP
__currentIndex = 0

def addTrack(name, location):
    global __tracks, __trackNames
    try:
        track = pyglet.resource.media(location, streaming=False)
    except pyglet.media.MediaException:
        print 'You should install AVBin so you can hear the sounds'
        print '   http://code.google.com/p/avbin/'
        print "(install a binary, don't try to compile)"
        return
    __tracks.append(track)
    __trackNames[name] = len(__tracks) - 1

def load():
    addTrack('industry', 'The_Pyramid_-_Industry.mp3')

def play(index=None):
    global __currentIndex, __player, __tracks, __trackNames
    if not len(__tracks):
        print("Can't play: No tracks.")
        return

    if index == None: index = __currentIndex

    if isinstance(index, "".__class__):
        index = __trackNames.get(index, None)
    if index == None: return

    index = index % len(__tracks)
    print("playing,", index)
    __currentIndex = index
    __player.queue(__tracks[index])
    __player.play()

def restart():
    global __currentIndex, __player, __tracks, __trackIndex
    stop()
    play()

def next():
    global __currentIndex,  __tracks
    if not len(__tracks): return
    stop()
    __currentIndex = (__currentIndex + 1) % len(__tracks)
    play(__currentIndex)

def prev():
    global __currentIndex, __tracks
    if not len(__tracks): return
    stop()
    __currentIndex = (__currentIndex - 1) % len(__tracks)
    play(__currentIndex)

def pause():
    global __player, __tracks
    if not len(__tracks): return
    __player.pause()

def stop():
    global __player, __tracks
    if not len(__tracks): return
    __player.pause()
    __player = pyglet.media.Player()
    __player.eos_action = __player.EOS_LOOP


