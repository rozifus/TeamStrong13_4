# settings for POR
import pymunk

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
CART_MASS = 50.0
CART_FRICTION = 0.05
CART_STARTING_ANGLE = 0.0
CART_BOUNCE_IMPULSE = pymunk.Vec2d(0.0, CART_MASS * 500.0)

RUBY_IMAGE = "ruby.png"
RUBY_MASS = 1.0
RUBY_FRICTION = 0.80
RUBY_STARTING_ANGLE = 0.0

# collision types
COLLISION_CART = 1
COLLISION_RUBY = 2

GRAVITY = -980.0
TRACK_FRICTION = 0.00

ENTITY_DEFAULT_X = 500
ENTITY_DEFAULT_Y = 500
ENTITY_DEFAULT_MASS = 50
ENTITY_DEFAULT_FRICTION = 0.5
ENTITY_DEFAULT_ANGLE = 0

