# main menu for python on railz
import settings
import sys
import pyglet

import music
from gamelevel import skip

class MainMenu(object):
    def __init__(self, game):

        # create a window and grab fullscreen with exclusive mouse
        #super(MainMenu, self).__init__(width = 1024, height = 768)
        #self.set_exclusive_mouse()
        super(MainMenu, self).__init__()
        music.load()
        music.play('pink')

        self.game = game
        
        self.num_options = 4 #number of menu items to choose from
        self.main_batch = pyglet.graphics.Batch()

        self.game_label = pyglet.text.Label(batch = self.main_batch)
        self.game_label.text = "Python on Rails"

        self.start_label = pyglet.text.Label(batch = self.main_batch)
        self.start_label.text = "Start Game"
        self.instructions_label = pyglet.text.Label(batch = self.main_batch)
        self.instructions_label.text = "Instructions"
        self.highscores_label = pyglet.text.Label(batch = self.main_batch)
        self.highscores_label.text = "Highscores"
        self.quit_label = pyglet.text.Label(batch = self.main_batch)
        self.quit_label.text = "Quit"
        
        self.controls_label = pyglet.text.Label(batch = self.main_batch)
        self.controls_label.text = "[UP], [DOWN] to select an option, [SPACE] to select"

        self.by_label = pyglet.text.Label(batch = self.main_batch)
        self.by_label.text = "By NSTeamStrong - jtrain, kburd, danaran and rozifus. Piece."
        
        self.option_labels = [self.start_label, self.instructions_label,
                self.highscores_label, self.quit_label]
        self.all_labels = [self.game_label, self.controls_label, self.by_label]
        self.all_labels.extend(self.option_labels)
        
        self.layout_items()
        self.selected_option = 1

    @property
    def selected_option(self):
        return self._selected_option
    @selected_option.setter
    def selected_option(self, value):
        self._selected_option = value
        i = 1 
        for label in self.option_labels:
            if self._selected_option == i:
                label.color = settings.MENU_COLOR_OPTION_SELECTED
            else:
                label.color = settings.MENU_COLOR_OPTION
            i += 1

    def start(self):
        pass

    def stop(self):
        pass

    def finish(self, skip=None):
        self.game.scene_finished(None, skip=skip)


    def layout_items(self):
        # set font sizes
        self.game_label.font_size = self.game.window.height / 10.0
        self.controls_label.font_size = self.game.window.height / 30.0
        self.by_label.font_size = self.game.window.height / 30.0
        for label in self.option_labels:
            label.font_size = self.game.window.height / 20.0
        
        # center all labels
        for label in self.all_labels:
            label.x = (self.game.window.width - label.content_width) / 2.0
        
        # set label positions
        self.game_label.y = 0.85 * self.game.window.height
        menu_top_y = self.game.window.height * 0.65
        menu_spacing_y = self.game.window.height * 0.1
        i = 0
        for label in self.option_labels:
            label.y = menu_top_y - menu_spacing_y * i
            i += 1
        self.by_label.y = self.game.window.height * 0.05
        self.controls_label.y = self.game.window.height * 0.15

        # set colours
        self.game_label.color = settings.MENU_COLOR_TITLE
        for label in self.option_labels:
            label.color = settings.MENU_COLOR_OPTION
        self.controls_label.color = settings.MENU_COLOR_CONTROLS
        self.by_label.color = settings.MENU_COLOR_BY

    
    def quit(self):
        sys.exit(0)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            self.quit()

        elif symbol == pyglet.window.key.UP:
            if self.selected_option == 1:
                self.selected_option = self.num_options
            else:
                self.selected_option -= 1

        elif symbol == pyglet.window.key.DOWN:
            if self.selected_option == self.num_options:
                self.selected_option = 1
            else:
                self.selected_option += 1

        elif symbol == pyglet.window.key.SPACE:

            if self.selected_option == 1:
                self.game.scores['rubies'] = 0
                self.game.scene_finished("play_game")
            elif self.selected_option == 2:
                self.game.scene_finished("instructions")
            elif self.selected_option == 3:
                self.game.scene_finished("show_hiscores")
            else:
                self.quit()

        try:
            levelno = skip[symbol]
            self.game.scene_finished("play_game", skip=levelno)
        except KeyError:
            pass

    def update(self, dt):
        # main loop
        pass

    def on_draw(self):
        self.game.window.clear()
        self.game_label.draw()
        self.main_batch.draw()
