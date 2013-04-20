# settings for POR
import utils as pymunk
import os

MAIN_WINDOW_WIDTH = 1024
MAIN_WINDOW_HEIGHT = 768

RESOURCE_PATH = map(os.path.abspath, ['data', 'data/images', 'data/sounds',
                 'data/music', 'data/other'])

# master game FPS
MAIN_UPDATE_INTERVAL = 1.0/120.0

STARTING_LIVES = 5

ENTITY_DEFAULT_GAME_POSITION_X = 500.0
ENTITY_DEFAULT_GAME_POSITION_Y = 500.0

SPEED_LABEL_X = 120
SPEED_LABEL_Y = 5
LIVES_LABEL_X = 5
LIVES_LABEL_Y = 100
SCORE_LABEL_X = 5
SCORE_LABEL_Y = 80
QUIT_LABEL_X = 5
QUIT_LABEL_Y = 60

CART_NORMAL_VELOCITY = 900.0
CART_JUMP_VELOCITY = 1200.0
CART_JUMP_ROTATION = -15.0
CART_SPEED_UP = 150.0
CART_SLOW_DOWN = -150.0
CART_MAX_VELOCITY = CART_NORMAL_VELOCITY + 600.0
CART_MIN_VELOCITY = CART_NORMAL_VELOCITY - 300.0
CART_EARLY_JUMP_TIME = 0.5 # can press jump up to 0.3s before landing and will jump when landed


CART_IMAGE = "cart.png"
RUBY_IMAGE = "ruby.png"
ANVIL_IMAGE = "anvil.png"
POST_IMAGE = "post.png"
SPAWN_IMAGE = "flower.png"

def normalized_colour(*colours):
    return tuple(colour / 255. for colour in colours)

GRAVITY = -3000.0 # pixels/s**2
TRACK_FUZZ = 10.0 # fuzziness of track detection algorithm
TRACK_WIDTH = 30.0

#colors are for pairs of points. [r, g, b, r, g, b] 0.0 <= r,g,b <= 1.0
TRACK_COLOR_TOP = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
TRACK_COLOR_BOTTOM = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
SLEEPER_COLOR_TOP = [0.290, 0.133, 0.027]
SLEEPER_COLOR_BOTTOM = [0.577, 0.262, 0.051]
SLEEPER_LENGTH = 60.0
SLEEPER_WIDTH = 10.0
SLEEPER_SPACING = 30
SLEEPER_WIDTH_JITTER = 3
SLEEPER_LENGTH_JITTER = 10
SLEEPER_SKEW = 10


VIEWPORT_OFFSET_X = 200.0
VIEWPORT_OFFSET_Y = 384.0
VIEWPORT_LOOKAHEAD = 50.0
VIEWPORT_MAX_RATE = 10 # px/frame change.
VIEWPORT_DEADBAND = 20 # px wait this many pixels before moving.

DEAD_OFFSET_Y = 300.0

MENU_COLOR_TITLE = (209, 0, 92, 255)
MENU_COLOR_BY = (50, 50, 50, 255)
MENU_COLOR_CONTROLS = (100, 100, 100, 255)
MENU_COLOR_OPTION = (200, 200, 200, 200)
MENU_COLOR_OPTION_SELECTED = (255, 255, 255, 255)

BACKGROUND_COLOUR = normalized_colour(20, 20, 20, 255)

CUTSCENES = { "default" : ("Level 1", "Is anyone there?", "Prepare to die on my rails, Python!!", ""),
        "level2" : ("Level 2", "&nbsp;", "Whitespace, eh? That won't save you now!", ""),
        "level3" : ("Level 3", "from __future__ import braces", "You'll need semi-colons where you're going", ""),
        "level4" : ("Level 4", "I'm here to defend zope's honour", "Looks like you are the only one", ""),
        "level5" : ("Level 5", "This is getting tough. speed+=1", "Cute, but you'll never collect enough precious gems", ""),
        "level6" : ("Level 6", "We were brothers..", "Yes, once. Those days are long gone snake", ""),
        "level7" : ("Level 7", "I'm in your lair, watch out", "You are getting close to my heart. Back off", ""),
        "level8" : ("Level 8", "Zope powers a generation of internet", "Please, I'm the princess of the web", ""),
        "level9" : ("Level 9", "These last steps I collect your powers", "<captain>He's getting close sir</captain>", ""),
        "level10" : ("Level 10", "This is for Zope!", "Please be kind to my gems", ""),
        "victory" : ("Victory", "Rails == Fails, Ruby", "lol", "", "enter_hiscores"),
        "defeat" : ("Defeat", "Meow", "All your base are belong to us.", "", "enter_hiscores")
        }

