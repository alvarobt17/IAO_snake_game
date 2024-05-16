import pyxel
import random
from .constants import *

class Fruit ():
    """
    Class to create a fruit object

    Attributes
    ----------
    posX : int
        X position of the fruit in pixels
    posY : int
        Y position of the fruit in pixels
    type : int
        Type of the fruit

    Methods
    -------
    draw ()
        Draws the fruit on the screen
    """

    def __init__ (self, snakes: list):
        """
        Parameters
        ----------
        snakePositions : list
            List of tuples with the positions of the snake's body
        """
        collides = True
        while collides:
            self.placeAtRandomPosition()
            collides = False
            for snake in snakes:
                if self.collidesWith(snake):
                    collides = True
                    continue

        self.type = random.randint (0, 2)

    def placeAtRandomPosition (self):
        """
        Generates a random position for the fruit
        """
        self.posX = random.randint(0, 15)*16
        self.posY = random.randint(2, 17)*16

    def collidesWith (self, snake):
        part = snake.head
        while part:
            if part.posX//CELLSIZE == self.posX//CELLSIZE and part.posY//CELLSIZE == self.posY//CELLSIZE:
                return True
            part = part.next
        return False

    def draw (self):
        """
        Draws the fruit on the screen
        """
        pyxel.blt(self.posX, self.posY, 0, self.type*16, 0, 16, 16, 1)
