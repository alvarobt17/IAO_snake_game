from .gameMode import GameMode
from ..players.player1 import Player1
from ..players.player2 import Player2
from ..constants import Moves

class MultiplayerGameMode(GameMode):
    def __init__(self, gameWidth, gameHeight, velocity):
        players = [Player1(gameWidth, gameHeight, 160, 144, velocity, 0, Moves.LEFT),
                   Player2(gameWidth, gameHeight,  80, 144, velocity, 1, Moves.RIGHT)]
        super().__init__(players)

