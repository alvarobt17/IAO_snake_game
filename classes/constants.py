from enum import Enum
import random

GAME_WIDTH = 256
GAME_HEIGHT = 288

CELLSIZE = 16

MOVEMENTS: {
    'UP': 'up',
    'DOWN': 'down',
    'LEFT': 'left',
    'RIGHT': 'right'
}

class Moves(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    def randomDir():
        return random.choice([Moves.LEFT, Moves.RIGHT, Moves.UP, Moves.DOWN])

class PlayerStatus(Enum):
    ALIVE = 0
    DEAD = 1
    EATEN = 2

