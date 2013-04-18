# main game file for Python on Rails

import pyglet
import settings
import menu
import gamelevel
import sounds

# all scenes need to implement a start method and a stop method

class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pyglet.resource.path = settings.RESOURCE_PATH
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(width = 1024, height = 768)
        self.current_scene = menu.MainMenu(self)
        sounds.load()
    
    def start_scene(self):
        pyglet.resource.path = settings.RESOURCE_PATH
        pyglet.resource.reindex()
        self.current_scene.start()
        self.window.push_handlers(self.current_scene)

    def stop_scene(self):
        self.current_scene.stop()
        self.window.pop_handlers()
        self.window.clear()

    def scene_finished(self, result):
        print "Scene finished, result was " + str(result)
        self.stop_scene()

        if result == "play_game":
            self.current_scene = gamelevel.GameLevel(self)
            self.start_scene()

def run():
    game = Game()
    game.start_scene()
    pyglet.app.run()

if __name__ == "__main__":
    run()
