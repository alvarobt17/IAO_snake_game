from .gameMode import GameMode
from ..players.player1 import Player1

class SingleGameMode(GameMode):
    def __init__(self, gameWidth, gameHeight, velocity, type):
        players = [Player1(gameWidth, gameHeight,
                                128, 144, velocity, type)]
        super().__init__(players)
