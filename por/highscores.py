from collections import namedtuple

import pyglet

import settings

# size, smaller is bigger - x and y are in fractions of height and width
Label = namedtuple("Label", "key text size x y color")

class HiScores(object):
    def __init__(self, game):
        self.game = game
        self.main_batch = pyglet.graphics.Batch()

        self.labels = {}

        with open('data/scores.txt', 'r') as scorefile:
            scores = [line.split(',') for line in scorefile.readlines() if line]

        labels = [
            Label('h1', "HiScores", 10, 0.3, 0.85, settings.MENU_COLOR_TITLE),
        ]

        for i, (name, score) in enumerate(scores):
            labels.append(
                Label('h2', '{i}\t{name}\t{score}'.format(**locals()), 40, 0.3, 0.65 - i * 0.05, settings.MENU_COLOR_OPTION))

        map(self.make_label, labels)

    def start(self):
        print "Cutscene starting"
    
    def stop(self):
        print "Cutscene stopping"

    def finish(self):
        self.game.scene_finished("show_menu")

    def on_draw(self):
        self.game.window.clear()
        self.main_batch.draw()


    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.finish()

    def make_label(self, label):
        lbl = pyglet.text.Label(batch=self.main_batch)
        lbl.text = label.text.expandtabs(8).strip()
        lbl.font_size = self.game.window.height / label.size
        lbl.x = self.game.window.width * label.x
        lbl.y = self.game.window.height * label.y
        lbl.color = label.color
        self.labels[label.key] = lbl
        return lbl
