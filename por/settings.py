# settings for POR
import utils as pymunk

MAIN_WINDOW_WIDTH = 1024
MAIN_WINDOW_HEIGHT = 768

RESOURCE_PATH = ['data', 'data/images', 'data/sounds',
                 'data/music', 'data/other']

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

CART_IMAGE = "cart.png"
CART_NORMAL_VELOCITY = 700.0
CART_JUMP_VELOCITY = 1000.0
CART_JUMP_ROTATION = -15.0
CART_SPEED_UP = 150.0
CART_SLOW_DOWN = -150.0
CART_MAX_VELOCITY = CART_NORMAL_VELOCITY + 300.0
CART_MIN_VELOCITY = CART_NORMAL_VELOCITY - 300.0
CART_EARLY_JUMP_TIME = 0.3 # can press jump up to 0.3s before landing and will jump when landed


RUBY_IMAGE = "ruby.png"
ANVIL_IMAGE = "anvil.png"
POST_IMAGE = "post.png"
SPAWN_IMAGE = "flower.png"

GRAVITY = -3000.0 # pixels/s**2
TRACK_FUZZ = 10.0 # fuzziness of track detection algorithm
TRACK_WIDTH = 30.0
TRACK_COLOR_TOP = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
TRACK_COLOR_BOTTOM = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]


VIEWPORT_OFFSET_X = 200.0
VIEWPORT_OFFSET_Y = 384.0
VIEWPORT_LOOKAHEAD = 100.0
VIEWPORT_MAX_RATE = 8 # px/frame change.
VIEWPORT_DEADBAND = 20 # px wait this many pixels before moving.

DEAD_OFFSET_Y = 300.0

MENU_COLOR_TITLE = (209, 0, 92, 255)
MENU_COLOR_BY = (50, 50, 50, 255)
MENU_COLOR_CONTROLS = (100, 100, 100, 255)
MENU_COLOR_OPTION = (200, 200, 200, 200)
MENU_COLOR_OPTION_SELECTED = (255, 255, 255, 255)
