import pyxel
from ..fruit import Fruit
from .gameMode import GameMode
from ..players.AIPlayer import AIPlayer
from ..constants import *
import random
import numpy as np
from ..neuralNet import NeuralNet
import time
from ..SaveData import SaveData
import json
import multiprocessing
from typing import *

class TrainingAIGameMode(GameMode):
    def __init__(self, gameWidth, gameHeight, velocity, checkpoint=0, num_threads=1, manager=None):
        self.__trainingTime = time.time()
        self.__num_threads = num_threads
        self.__player_threads = [0] * self.__num_threads

        self._gameWidth = gameWidth
        self._gameHeight = gameHeight
        self._velocity = velocity

        with open("parameters.json") as f:
            data = json.load(f)
            self.__generations_per_checkpoint = data["GA"]["SaveCheckpointRate"]
            self.__generations = data["GA"]["Generations"]
            self.__num_parents = data["GA"]["CrossoverAbsolute"]
            self.__mutation_rate = data["GA"]["MutationRate"]
            self.__populationSize = data["GA"]["PopulationSize"]
            self.__stepsPerGen = data["GA"]["StepsPerGeneration"]*(CELLSIZE/velocity)

        self.__currentStep = 0,
        self.__weights = SaveData.loadCheckpoint(checkpoint, self.__populationSize)
        players = [AIPlayer(gameWidth, gameHeight, random.randint(1, 14)*16, random.randint(3, 16)*16,
                               velocity, self.__weights[i], 0, Moves.randomDir()) for i in range(self.__populationSize)]

        if (manager is not None):
            self.player_stats = manager.list([manager.dict({'deaths': 0, 'score_record': 0, 'penalties': 0, "mean_score": 0, "steps":0}) for _ in range(self.__populationSize)])
        else:
            self.player_stats = [{'deaths': 0, 'score_record': 0, 'penalties': 0, "mean_score": 0, "steps": 0} for _ in range(self.__populationSize)]

        self.__currentGeneration = checkpoint + 1
        # self._fruits = [Fruit([player.snake]) for player in players]

        super().__init__(players, startCountdown=None)

    def FitnessFunction(self, statistic):
        return statistic['steps'] * 150 + statistic['score_record'] * 5000 - statistic['penalties'] * 10000 + statistic["deaths"] * 10000
    
    def update(self):
        if self.__currentGeneration > self.__generations:
            # Stop the game
            print("Training finished")
            exit()
        else:
            self.threadUpdate()

    def threadUpdate(self):
        num_players = self.__populationSize // self.__num_threads
        remaining_players = self.__populationSize % self.__num_threads
        for i in range(self.__num_threads):
            startIdx = i * num_players
            endIdx = startIdx + num_players
            if i == self.__num_threads - 1:
                endIdx += remaining_players
            self.__player_threads[i] = multiprocessing.Process(target=PlayerThread, args=(self.players[startIdx:endIdx], self.__stepsPerGen, self.player_stats, startIdx))
            self.__player_threads[i].start()
        
        for thread in self.__player_threads:
            thread.join()
        # Evaluate the generation            
        print("---------------------------------")
        print("Generation: " + str(self.__currentGeneration))
        print("Gen time:", time.time() - self.__trainingTime)   
        print("---------------------------------")
        self.__nextGeneration(self.__evaluateGeneration())
        print("---------------------------------")
        print("Generation: " + str(self.__currentGeneration) + " ended")
        print("Gen time:", time.time() - self.__trainingTime)
        print("---------------------------------")
        self.__trainingTime = time.time()
        # Create new generation
        self.__currentGeneration += 1

    def __evaluateGeneration(self):
        fitnessSet = []
        for i in range(self.__populationSize):
            # Calculate the fitness value
            fitness_value = self.FitnessFunction(self.player_stats[i])
            fitnessSet.append(fitness_value)
        if self.__currentGeneration % self.__generations_per_checkpoint == 0:
            # Save the weights of the current generation
            SaveData.saveCheckpoint(self.__currentGeneration, self.__weights, fitnessSet)
        # Save generation statistics and fitness values in a file
        SaveData.saveStatistics(self.__currentGeneration, self.player_stats, fitnessSet)
        return fitnessSet

    def __nextGeneration(self, fitnessSet):
        bestParents = []
        fitnessOrder = np.argsort(fitnessSet)[::-1]
        # Get the best parents
        for i in fitnessOrder:
            bestParents.append(self.__weights[i])
            print(self.player_stats[i])
            print(fitnessSet[i])
            print("=======================================================================")
            if len(bestParents) == self.__num_parents:
                break
        
        # Create the new generation
        newGeneration = bestParents.copy()
        while len(newGeneration) < self.__populationSize:
            # Select two parents index randomly
            parent1Index = random.randint(0, self.__num_parents-1)
            parent2Index = random.randint(0, self.__num_parents-1)
            while parent1Index == parent2Index:
                parent2Index = random.randint(0, self.__num_parents-1)
            # Get the parents
            parent1 = bestParents[parent1Index].copy()
            parent2 = bestParents[parent2Index].copy()
            # Create the child
            child = self.__crossover(parent1, parent2)
            # Mutate the child
            self.__mutate(child)
            # Transform the child to a numpy array
            child = np.array(child)
            # Add the child to the new generation
            newGeneration.append(child)

        # Update the weights
        self.__weights = newGeneration.copy()

        # Create the new players
        for i in range(self.__populationSize):
            self.players[i] = AIPlayer(self._gameWidth, self._gameHeight, random.randint(1, 14)*16, random.randint(3, 16)*16,
                               self._velocity, newGeneration[i], 0, Moves.randomDir())

    def __crossover(self, parent1, parent2):
        """Method to take the half of the weight of each layer of the parents for the child"""
        # Create the child
        child = []
        for i in range(len(NeuralNet.layers) - 1):
            # Select the crossover point to the half of the layer
            crossoverPoint = NeuralNet.layers[i] * NeuralNet.layers[i+1] // 2
            endLayer = NeuralNet.layers[i] * NeuralNet.layers[i+1]
            # Add the weights of the parent1
            child.extend(parent1[:crossoverPoint])
            # Add the weights of the parent2
            child.extend(parent2[crossoverPoint:endLayer])
            # Remove the used weights
            parent1 = parent1[endLayer:]
            parent2 = parent2[endLayer:]

        # Return the child
        return child

        
    def __mutate(self, child):
        mutations = int(self.__mutation_rate * NeuralNet.weights_size())
        for _ in range(mutations):
            # Select a random weight
            randomWeight = random.randint(0, NeuralNet.weights_size()-1)
            # Mutate the weight
            child[randomWeight] = random.uniform(-1, 1)

    def __resetPlayer(self, player):
        player._startPosX = 128
        player._startPosY = 144
        player._startMove = Moves.RIGHT
        player.reset()

    def draw(self):
        pyxel.bltm(0, 32, 0, 0, 0, 256, 256)
        self._startCountdown.draw()

        # for fruit in self._fruits:
        #     fruit.draw()
        self._fruits[0].draw()

        # for player in self.players:
        #     player.draw()
        self.players[0].draw()

class PlayerThread:
    def __init__(self, players:List[AIPlayer], maxSteps, stats, startIdx=0):
        self.players = players
        self.fruits = [Fruit([player.snake]) for player in players]
        self.steps = 0
        while True:
            status = self.update()
            if status == PlayerStatus.DEAD or self.steps > maxSteps:
                for i in range(len(self.players)):
                    stats[i + startIdx]['deaths'] = self.players[i].deaths
                    stats[i + startIdx]['score_record'] = self.players[i].totalFruits
                    stats[i + startIdx]['penalties'] = self.players[i].penalties
                    stats[i + startIdx]['mean_score'] =  maxSteps / (self.players[i].totalFruits + 1)
                    stats[i + startIdx]['steps'] = self.players[i].pasos # Add the steps count to the stats
                break
            self.steps += 1

    def __resetPlayer(self, player):
        player._startPosX = random.randint(1, 14)*16
        player._startPosY = random.randint(3, 16)*16
        player._startMove = Moves.randomDir()
        player.reset()

    def update(self):
        status_all = PlayerStatus.DEAD
        for i in range(len(self.players)):
            status = self.players[i].update(self.fruits[i], [self.players[i].snake])
            if (status == PlayerStatus.ALIVE):
                status_all = PlayerStatus.ALIVE
            #if status == PlayerStatus.DEAD:
                #self.__resetPlayer(self.players[i])

            if status == PlayerStatus.EATEN:
                self.fruits[i] = Fruit([self.players[i].snake])
        return status_all
    