from .gameMode import GameMode
from ..players.player1 import Player1
from ..players.AIPlayer import AIPlayer
from ..constants import Moves
from ..SaveData import SaveData

class MultiplayerAIGameMode(GameMode):
    def __init__(self, gameWidth, gameHeight, velocity):

        players = [Player1(gameWidth, gameHeight, 160, 144, velocity, 0, Moves.RIGHT),
                   AIPlayer(gameWidth, gameHeight, 80, 144,
                               velocity, SaveData.loadFinalModel("finalModel")[0], 2, Moves.LEFT)]
        super().__init__(players)