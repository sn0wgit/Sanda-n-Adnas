__author__ = 'justinarmstrong'

SCREEN_HEIGHT = 672
SCREEN_WIDTH = 897

SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

ORIGINAL_CAPTION = "Sanda & Adnas"

## COLORS ##

#                 R    G    B
GRAY         = (100, 100, 100)
NAVYBLUE     = ( 60,  60, 100)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
FOREST_GREEN = ( 31, 162,  35)
BLUE         = (  0,   0, 255)
SKY_BLUE     = ( 39, 145, 251)
YELLOW       = (255, 255,   0)
ORANGE       = (255, 128,   0)
PURPLE       = (255,   0, 255)
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK   = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)

BGCOLOR = WHITE

MULTIPLIER = 3
SIZE_MULTIPLIER = 3
BRICK_SIZE_MULTIPLIER = 3
BACKGROUND_MULTIPLER = 3
GROUND_HEIGHT = SCREEN_HEIGHT - 72

#MARIO FORCES
WALK_ACCEL = .15
RUN_ACCEL = 10
SMALL_TURNAROUND = .35

GRAVITY = 1.5
JUMP_GRAVITY = .25
JUMP_VEL = -9.75
FAST_JUMP_VEL = -12.5
MAX_Y_VEL = 12

MAX_RUN_SPEED = 10
MAX_WALK_SPEED = 6


#States

STAND = 'standing'
WALK = 'walk'
JUMP = 'jump'
FALL = 'fall'
SMALL_TO_BIG = 'small to big'
BIG_TO_FIRE = 'big to fire'
BIG_TO_SMALL = 'big to small'
FLAGPOLE = 'flag pole'
WALKING_TO_CASTLE = 'walking to castle'
END_OF_LEVEL_FALL = 'end of level fall'


#GOOMBA Stuff

LEFT = 'left'
RIGHT = 'right'
JUMPED_ON = 'jumped on'
DEATH_JUMP = 'death jump'

#KOOPA STUFF

SHELL_SLIDE = 'shell slide'

#BRICK STATES

RESTING = 'resting'
BUMPED = 'bumped'

#COIN STATES
OPENED = 'opened'

#MUSHROOM STATES

REVEAL = 'reveal'
SLIDE = 'slide'

#COIN STATES

SPIN = 'spin'

#STAR STATES

BOUNCE = 'bounce'

#FIRE STATES

FLYING = 'flying'
BOUNCING = 'bouncing'
EXPLODING = 'exploding'

#Brick and coin box contents

MUSHROOM = 'mushroom'
SCARAB = 'Scarab'
SIXCOINS = '6coins'
COIN = 'coin'
LIFE_MUSHROOM = '1up_mushroom'

#LIST of ENEMIES

GOOMBA = 'goomba'
KOOPA = 'koopa'

#LEVEL STATES

FROZEN = 'frozen'
NOT_FROZEN = 'not frozen'
IN_CASTLE = 'in castle'
FLAG_AND_FIREWORKS = 'flag and fireworks'

#FLAG STATE
TOP_OF_POLE = 'top of pole'
SLIDE_DOWN = 'slide down'
BOTTOM_OF_POLE = 'bottom of pole'

#1UP score
ONEUP = '360'

#MAIN MENU CURSOR STATES
PLAYER1 = '1 player'
PLAYER2 = '2 player'
IsSingleGame = 'is single game'

#OVERHEAD INFO STATES
MAIN_MENU = 'main menu'
LOAD_SCREEN = 'loading screen'
LEVEL = 'level'
GAME_OVER = 'game over'
FAST_COUNT_DOWN = 'fast count down'
END_OF_LEVEL = 'end of level'

#GAME INFO DICTIONARY KEYS
COIN_TOTAL = 'coin total'
SCORE = 'score'
TOP_SCORE = 'top score'
SANDA_LIVES = 'sanda lives'
ADNAS_LIVES = 'adnas lives'
CURRENT_TIME = 'current time'
LEVEL_STATE = 'level state'
CAMERA_START_X = 'camera start x'
SANDA_DEAD = 'sanda dead'
ADNAS_DEAD = 'adnas dead'

#STATES FOR ENTIRE GAME
MAIN_MENU = 'main menu'
LOAD_SCREEN = 'load screen'
TIME_OUT = 'time out'
GAME_OVER = 'game over'
LEVEL1 = 'level1'

#SOUND STATES
NORMAL = 'normal'
STAGE_CLEAR = 'stage clear'
WORLD_CLEAR = 'world clear'
TIME_WARNING = 'time warning'
SPED_UP_NORMAL = 'sped up normal'
SANDA_INVINCIBLE = 'mario invincible'
ADNAS_INVINCIBLE = 'mario invincible'
