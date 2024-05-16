import pyxel
from .gameMode import GameMode
from ..players.AIPlayer import AIPlayer
from ..constants import *
import random
from ..SaveData import SaveData

class TestAIGameMode(GameMode):
    def __init__(self, gameWidth, gameHeight, velocity):
        self._gameWidth = gameWidth
        self._gameHeight = gameHeight
        self._velocity = velocity
    
        self.mode = ModeStatus.SELECTING_CHECKPOINT
        self.__checkpoint_input = ""
        self.__num_players_input = ""
        self.__num_keys = [pyxel.KEY_0, pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4, pyxel.KEY_5, pyxel.KEY_6, pyxel.KEY_7, pyxel.KEY_8, pyxel.KEY_9]

    def start_test(self):
        self.mode = ModeStatus.TESTING
        self.__weights = SaveData.loadCheckpoint(self.__checkpoint, 1)[0]
        players = [AIPlayer(self._gameWidth, self._gameHeight, random.randint(1, 14)*16, random.randint(3, 16)*16,
                               self._velocity, self.__weights, 0, Moves.randomDir()) for _ in range(self.__num_players)]

        super().__init__(players, startCountdown=None)

    def start(self):
        pass

    def reset(self):
        for player in self.players:
            self.__resetPlayer(player)
        super().reset()


    def __resetPlayer(self, player):
        player._startPosX = random.randint(1, 14)*16
        player._startPosY = random.randint(3, 16)*16
        player._startMove = Moves.randomDir()

    def update(self):
        if self.mode == ModeStatus.TESTING:
            super().update()
            if (self.isAnyOneDead):
                self.reset()
        else:
            self.selection_input()

    def draw(self):
        pyxel.bltm(0, 32, 0, 0, 0, 256, 256)

        if self.mode == ModeStatus.TESTING:
            for player in self.players:
                player.draw()
            self._fruit.draw()
        else:
            pyxel.cls(0)
            if self.mode == ModeStatus.SELECTING_CHECKPOINT:
                pyxel.text(10, 10, "Select the checkpoint to test:", 7)
                pyxel.text(10, 20, self.__checkpoint_input, 7)
            elif self.mode == ModeStatus.SELECTING_NUM_PLAYERS:
                pyxel.text(10, 10, "Select the number of players:", 7)
                pyxel.text(10, 20, self.__num_players_input, 7)
            pyxel.text(10, 30, "Press T to confirm", 7)

    def selection_input(self):
        for button in self.__num_keys:
            if pyxel.btnp(button):
                self.__checkpoint_input += str(self.__num_keys.index(button))
                self.__num_players_input += str(self.__num_keys.index(button))
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.__checkpoint_input = self.__checkpoint_input[:-1]
            self.__num_players_input = self.__num_players_input[:-1]
        if pyxel.btnp(pyxel.KEY_T):
            if self.mode == ModeStatus.SELECTING_CHECKPOINT:
                self.mode = ModeStatus.SELECTING_NUM_PLAYERS
                self.__checkpoint = int(self.__checkpoint_input)
                self.__num_players_input = ""
            elif self.mode == ModeStatus.SELECTING_NUM_PLAYERS:
                self.__num_players = int(self.__num_players_input)
                self.start_test()

class ModeStatus:
    SELECTING_CHECKPOINT = 0
    SELECTING_NUM_PLAYERS = 1
    TESTING = 2
