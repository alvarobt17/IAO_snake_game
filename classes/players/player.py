import pyxel
import random
from ..snake import Snake
from ..constants import *

class Player ():
    def __init__(self, gameWidth, gameHeight, posX, posY, velocity, type, startMove=Moves.RIGHT):
        self._playerKeys = {
            Moves.UP: None,
            Moves.DOWN: None,
            Moves.RIGHT: None,
            Moves.LEFT: None
        }

        self.__restrictedMoves = {
            Moves.UP: Moves.DOWN,
            Moves.DOWN: Moves.UP,
            Moves.RIGHT: Moves.LEFT,
            Moves.LEFT: Moves.RIGHT
        }
        self._startMove = startMove # Start movement of the snake
        self._currentMove = startMove # Actual movement of the snake
        self.__nextMove = None # Next posible move to the snake when it will be in a cell

        self._type = type
        self.__gameWidth = gameWidth
        self.__gameHeight = gameHeight
        self.__velocity = velocity
        self._startPosX = posX
        self._startPosY = posY

        self.deaths = 0
        self.snake = Snake(self.__gameWidth, self.__gameHeight, self._startPosX,
                           self._startPosY, self.__velocity, self._type, self._startMove)

    def reset(self):
        self._currentMove = self._startMove
        self.__nextMove = None
        self.snake = Snake(self.__gameWidth, self.__gameHeight, self._startPosX,
                           self._startPosY, self.__velocity, self._type, self._startMove)

    def _getMove(self, fruit, gameSnakes):
        if pyxel.btnp(self._playerKeys[Moves.LEFT]):
            return Moves.LEFT
        elif pyxel.btnp(self._playerKeys[Moves.RIGHT]):
            return Moves.RIGHT
        elif pyxel.btnp(self._playerKeys[Moves.UP]):
            return Moves.UP
        elif pyxel.btnp(self._playerKeys[Moves.DOWN]):
            return Moves.DOWN
        else:
            return None
        

    def updateMove(self, fruit, gameSnakes:list):
        # Este método detecta la tecla pulsada correspondiente a un movimiento
        # y devuelve el valor del correspondiente siguiente movimiento. Teniendo en
        # cuenta los posibles valores no válidos
        # Get the move by the user or the IA logic
        move = self._getMove(fruit, gameSnakes)

        if move is not None and self.__restrictedMoves[move] != self._currentMove:
            self.__nextMove = move
    
        if self.snake.head.posX % 16 == 0 and self.snake.head.posY % 16 == 0:
            if self.__nextMove != None:
                self._currentMove = self.__nextMove


    def update(self, fruit, gameSnakes: list) -> PlayerStatus:
        self.updateMove(fruit, gameSnakes)
        self.snake.update(self._currentMove, gameSnakes)

        if (self.snake.dead):
            self.deaths += 1
            return PlayerStatus.DEAD

        if (self.checkFruit(fruit)):
            return PlayerStatus.EATEN
        return PlayerStatus.ALIVE

    def checkFruit(self, fruit):
        """ Check if the snake
        """
        if (self.snake.head.posX == fruit.posX and self.snake.head.posY == fruit.posY):
            self.snake.growSnake()
            return True
        return False

    def draw(self):
        self.snake.draw()

