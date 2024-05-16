import pyxel
import time
from ..header import Header
from ..fruit import Fruit
from ..constants import *
from ..players.player import Player


class GameMode():
    def __init__(self, players, startCountdown=3):
        self.players: Player = players
        self.snakes = [player.snake for player in self.players]
        self.isAnyOneDead = False
        self._header = Header(self.players)
        self._fruit = Fruit(self.snakes)
        self._startCountdown = CountDown(startCountdown)

    def start(self):
        self._startCountdown.start()

    def reset(self):
        self._startCountdown.reset()
        self.isAnyOneDead = False
        for player in self.players:
            player.reset()
        self.snakes = [player.snake for player in self.players]
        self._header.update(self.players)
        self._fruit = Fruit(self.snakes)

        self.start()

    def update(self):
        self._startCountdown.update()
        if not self.isAnyOneDead and self._startCountdown.isFinished():
            for player in self.players:
                status = player.update(self._fruit, self.snakes)
                if status == PlayerStatus.DEAD:
                    self.isAnyOneDead = True
                if status == PlayerStatus.EATEN:
                    self._fruit = Fruit(self.snakes)                

        self._header.update(self.players)

    def draw(self):
        pyxel.bltm(0, 32, 0, 0, 0, 256, 256)
        self._startCountdown.draw()
        self._fruit.draw()
        self._header.draw()
        for player in self.players:
            player.draw()


class CountDown:
    def __init__(self, time):
        self.countdownTime = time
        self.__startTimestamp = None

    def start(self):
        if self.countdownTime is None:
            return
        self.__startTimestamp = time.time()

    def reset(self):
        self.__startTimestamp = None

    def update(self):
        if self.__startTimestamp is None or self.countdownTime is None:
            return
        if time.time() - self.__startTimestamp > self.countdownTime:
            self.__startTimestamp = None 
    
    def draw(self):
        if self.__startTimestamp is None or self.countdownTime is None:
            return
        pyxel.blt(GAME_WIDTH//2 - 16, 125, 0, 32*(self.countValue()), 128, 32, 32, 2)

    def isFinished(self):
        return self.__startTimestamp is None
    
    def countValue(self):
        return int(time.time() - self.__startTimestamp)




