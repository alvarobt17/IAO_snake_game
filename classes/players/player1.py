import pyxel
from .player import Player
from ..constants import *

class Player1 (Player):
    def __init__(self, gameWidth, gameHeight, posX, posY, velocity, type=0, startMove=Moves.LEFT):
        super().__init__(gameWidth, gameHeight, posX, posY, velocity, type, startMove)
        self._playerKeys = {
            Moves.LEFT: pyxel.KEY_LEFT,
            Moves.RIGHT: pyxel.KEY_RIGHT,
            Moves.UP: pyxel.KEY_UP,
            Moves.DOWN: pyxel.KEY_DOWN
        }