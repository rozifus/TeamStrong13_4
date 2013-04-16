# settings for POR
import utils as pymunk

MAIN_WINDOW_WIDTH = 1024
MAIN_WINDOW_HEIGHT = 768

RESOURCE_PATH = ['data', 'data/images', 'data/sounds', 'data/other']

# master game FPS
MAIN_UPDATE_INTERVAL = 1.0/120.0

SCORE_LABEL_X = 5
SCORE_LABEL_Y = 80
QUIT_LABEL_X = 5
QUIT_LABEL_Y = 60

CART_IMAGE = "cart.png"
CART_NORMAL_VELOCITY = 300.0
CART_JUMP_VELOCITY = 1000.0
CART_JUMP_ROTATION = -15.0

RUBY_IMAGE = "ruby.png"

GRAVITY = -3000.0 # pixels/s**2
TRACK_FUZZ = 10.0 # fuzziness of track detection algorithm
