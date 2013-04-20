from collections import namedtuple
from operator import itemgetter

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
            self.scores = [line.split(',') for line in scorefile.readlines() if line]

        labels = [
            Label('h1', "HiScores", 10, 0.3, 0.85, settings.MENU_COLOR_TITLE),
        ]

        for i, (name, score) in enumerate(self.scores):
            labels.append(
                Label('h2', '{i}\t{name}\t{score}'.format(**locals()), 40, 0.3, 0.65 - i * 0.05, settings.MENU_COLOR_OPTION))

        map(self.make_label, labels)

        self.init()

    def init(self):
        lbl = Label('h3', "[space] to continue", 20, 0.3, 0.2, settings.MENU_COLOR_OPTION)
        self.make_label(lbl)

    def start(self):
        pass
    
    def stop(self):
        pass

    def finish(self, name=None):
        self.game.scene_finished(name or "show_menu")

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
        lbl.x = int(self.game.window.width * label.x)
        lbl.y = int(self.game.window.height * label.y)
        lbl.color = label.color
        self.labels[label.key] = lbl
        return lbl

class EditHiScores(HiScores):

    def init(self):
        your_name = Label('h3', "Enter Your Name", 40, 0.3, 0.75, settings.MENU_COLOR_OPTION_SELECTED)
        self.make_label(your_name)
        lbl = self.labels['h2']
        self.text_input = TextWidget('| ', 
                    int(lbl.x), int(.70*self.game.window.height)
                    , 50, self.main_batch) 

    def save(self, text):
        def to_score((name, score)):
            try:
                score = int(score)
            except ValueError:
                score = float(score)
            return name, score

        original_scores = map(to_score, self.scores)
        original_scores.append((text, self.game.scores['rubies']*1000))
        sorted_scores = sorted(original_scores, key=itemgetter(1))

        # now put gvr on top where he should be.
        if sorted_scores[0][0] == "GVR":
            gvr = sorted_scores.pop(0)
            sorted_scores.append((gvr[0], str(gvr[1]).replace("n", "N")))

        # now write to disk. Was thinking of requiring postgres 9.2 for this...
        with open('data/scores.txt', 'wb') as scores_file:
            for score in list(reversed(sorted_scores))[:8]:
                scores_file.write("{0},{1}\n".format(*score))

        self.finish("show_hiscores")

    def on_text(self, text):
        if not text.isalnum():
            return

        self.text_input.caret.on_text(text)
        if len(self.text) == 3:
            self.save(self.text)

    @property
    def text(self):
        return self.text_input.document.text.replace("| ", "").upper()

    def on_key_press(self, symbol, *args):
        if symbol == pyglet.window.key.ENTER:
            self.save(self.text)

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [40, 40, 40, 255] * 4)
        )

class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), 
            dict(color=(255, 255, 255, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)        
