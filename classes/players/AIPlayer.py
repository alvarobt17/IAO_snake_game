from classes.constants import PlayerStatus
from .player import Player
from ..neuralNet import NeuralNet
import numpy as np
from ..constants import *
import json

class AIPlayer (Player):
    def __init__(self, gameWidth, gameHeight, posX, posY, velocity, weights, type=1, startMove=Moves.RIGHT):
        super().__init__(gameWidth, gameHeight, posX, posY, velocity, type, startMove)

        # Modelo
        self._model = NeuralNet(weights)
        with open("parameters.json") as f:
            data = json.load(f)
            self.__maxStepsPerFruit = data["AIPlayer"]["PenaltySteps"]*(CELLSIZE/velocity)
            
        self.possibleMoves = [Moves.LEFT, Moves.RIGHT, Moves.UP, Moves.DOWN]
        self.__currentStep = 0
        self.penalties = 0
        self.totalFruits = 0
        self.maxScore = 0

        self.__input = [0] * 16
        self.pasos = 0
        self.status = PlayerStatus.ALIVE

    def update(self, fruit, gameSnakes: list) -> PlayerStatus:
        if (self.status == PlayerStatus.DEAD):
            return PlayerStatus.DEAD
        self.status = super().update(fruit, gameSnakes)
        if self.status == PlayerStatus.EATEN:
            self.totalFruits += 1
            self.__currentStep = 0
        elif self.status == PlayerStatus.DEAD:
            self.maxScore = max(self.maxScore, self.snake.length)
            self.__currentStep = 0

        # Add a penalty if the snake is stuck
        if self.__currentStep > self.__maxStepsPerFruit:
            self.penalties += 1
            self.__currentStep = 0
        else:
            self.__currentStep += 1
            
        return self.status

    def _getMove(self, fruit, gameSnakes):
        # Get the distances to each direction        
        # if not self.snake.head.isInCell():
        #     return None
        
        i = 0
        axisDistances = self.snake.getAxisDistances(gameSnakes)
        for key in axisDistances:
            self.__input[i] = axisDistances[key]
            i+=1

        spaceRegions = self.snake.getSpaceRegions(gameSnakes)
        for region in spaceRegions:
            self.__input[i] = spaceRegions[region]
            i+=1

        distanceToFruits = self.snake.getDistanceToFruits([fruit])
        for key in distanceToFruits:
            self.__input[i] = distanceToFruits[key]
            i+=1

        for move in self.possibleMoves:
            self.__input[i] = (self._currentMove == move)
            i+=1

        # Transform the input to a numpy array with the correct shape
        input = np.array(self.__input).reshape(1, len(self.__input))
        #Normalize the input
        # input = input / np.linalg.norm(input)
        # Get the prediction
        prediction = self._model.model(input)
        moveIndex = np.argmax(prediction)
        # Select the move by the index
        move = self.possibleMoves[moveIndex]

        self.pasos += 1
        return move
    
    def reset(self):
        super().reset()
        self.penalties = 0
        self.totalFruits = 0
        self.maxScore = 0
        self.pasos = 0
        self.__currentStep = 0
        self.status = PlayerStatus.ALIVE
