# main game file for Python on Rails

import copy

import pyglet
import settings
import menu
import gamelevel
import sounds
import music
import cutscene
import highscores

# all scenes need to implement a start method and a stop method

class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pyglet.resource.path = settings.RESOURCE_PATH
        pyglet.resource.reindex()
        self.window = pyglet.window.Window(width = 1024, height = 768, vsync = False)
        self.current_scene = menu.MainMenu(self)
        sounds.load()
        music.load()

        self.unfinished_levels = copy.copy(gamelevel.glevels)
        self.loaded_level = -1

    def start_scene(self):
        pyglet.resource.path = settings.RESOURCE_PATH
        pyglet.resource.reindex()
        self.current_scene.start()
        self.window.push_handlers(self.current_scene)

    def stop_scene(self):
        print "Main is stopping scene " + str(self.current_scene)
        self.current_scene.stop()
        self.window.pop_handlers()
        print "on_draw popped, on draw exists? " + str(hasattr(self.window, "on_draw"))
        self.window.clear()

    def scene_finished(self, result, skip=None):
        print "Scene finished, result was " + str(result)
        print "Scene was " + str(self.current_scene)
        
        self.stop_scene()

        if result == "play_game" or result == "level_finished":
            if skip:
                self.index = skip - 1 
            else:
                self.index = self.loaded_level + 1

            Level = self.unfinished_levels[self.index]
            cutscene_params = settings.CUTSCENES[Level.name]
            self.current_scene = cutscene.Cutscene(self,
                    title=cutscene_params[0],
                    python=cutscene_params[1],
                    ruby=cutscene_params[2],
                    status=cutscene_params[3])
            self.start_scene()
        
        elif result == "cutscene_finished":
            Level = self.unfinished_levels[self.index]
            self.current_scene = Level(self)
            self.loaded_level = self.index
            self.start_scene()
        elif result == "show_hiscores":
            self.current_scene = highscores.HiScores(self)
            self.start_scene()
        elif result == "show_menu":
            self.current_scene = menu.MainMenu(self)
            self.start_scene()


def run():
    game = Game()
    game.start_scene()
    pyglet.app.run()

if __name__ == "__main__":
    run()
