import pyxel
from .player import Player
from ..constants import *

class Player2 (Player):
    def __init__(self, gameWidth, gameHeight, posX, posY, velocity, type=1, startMove=Moves.RIGHT):
        super().__init__(gameWidth, gameHeight, posX, posY, velocity, type, startMove)
        self._playerKeys = {
            Moves.LEFT: pyxel.KEY_A,
            Moves.RIGHT: pyxel.KEY_D,
            Moves.UP: pyxel.KEY_W,
            Moves.DOWN: pyxel.KEY_S
        }