import pygame as pg

# define colors (R, G, B)
WHITE = (255, 255, 255)
WALL_COLOR = (210, 210, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SETTING_COLOR = (100, 100, 100)

# grid
TILESIZE = 32
GRIDWIDTH = 14 * TILESIZE  # 288 #640# 928
GRIDHEIGHT = 14 * TILESIZE  # 288 #448# 608

# game settings
HEIGHT = GRIDHEIGHT + 1
FPS = 60
TITLE = "HCI roguelike Demo"
BGCOLOR = DARKGREY
SETTING_WIDTH = 200
SETTING_HEIGHT = HEIGHT
WIDTH = GRIDWIDTH + SETTING_WIDTH
# gameplay settings
#   player
MIN_START_DISTANCE_PLAYER_ENEMY = 2
MIN_START_DISTANCE_PLAYER_EXIT = 2  # 8
#   map generation
NUM_EXITS = 0
MIN_NUM_POWERUP = 2
MAX_NUM_POWERUP = 3
MIN_NUM_OBSTACLE = 2
MAX_NUM_OBSTACLE = 3  # 9#7
MIN_LENGHT_LINE = 1
MAX_LENGHT_LINE = 2  # 5
MIN_LINES_FOR_OBSTACLES = 1
MAX_LINES_FOR_OBSTACLES = 2  # 4

# custom events
ENEMY_TURN_EVENT = pg.event.custom_type()
PLAYER_SHOOT_EVENT = pg.event.custom_type()
PLAYER_GAME_OVER = pg.event.custom_type()

# settings
SIMULTAING_ENVIROMENT = False
ON_SIMULATING_ENV_MANUAL_INPUT_AGENT = False
ON_SIMULATING_ENV_MANUAL_INPUT_PLAYER = False

# ON_GAME_MANUAL_INPUT_AGENT = True
ON_GAME_PRINT_MAP_DURING_STEPS = False
ON_GAME_PRINT_INFO_DURING_STEPS = False
