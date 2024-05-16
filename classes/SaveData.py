import os
import numpy as np
from .neuralNet import NeuralNet
import shutil
import pickle

class SaveData:
    CHECKPOINT_FOLDER="checkpoints"
    LOGS_FOLDER="generationLogs"

    @staticmethod
    def saveCheckpoint(generation, weightsSet, fitnessSet):
        """Method to save the weights of a generation"""
        # Save data ordered by fitness
        ordered_data = np.argsort(fitnessSet)[::-1]
        ordered_weights = []
        for i in ordered_data:
            ordered_weights.append(weightsSet[i])
        # Save the weights
        pickle.dump(ordered_weights, open(SaveData.CHECKPOINT_FOLDER + "/gen" + str(generation) + ".p", "wb"))

    @staticmethod
    def loadCheckpoint(generation, numPlayers):
        """Method to load the weights of a player"""
        try:
            # Load the weights
            weights = pickle.load(open(SaveData.CHECKPOINT_FOLDER + "/gen" + str(generation) + ".p", "rb"))
            while len(weights) < numPlayers:
                weights.append(NeuralNet.randomWeights())
            # Return the weights of the player
            return weights
        except:
            print("No checkpoint found")
            # If there is no checkpoint, return random weights
            return [NeuralNet.randomWeights() for _ in range(numPlayers)]

    @staticmethod
    def loadFinalModel(modelName):
        """Method to load the weights of a final model"""
        try:
            # Load the weights
            weights = pickle.load(open("finalModel/" + modelName + ".p", "rb"))
            # Return the weights of the model
            return weights
        except:
            # If there is no model, return random weights
            return NeuralNet.randomWeights()

    @staticmethod
    def saveStatistics(generation, statistics, fitnessSet):
        """Method to save the statistics of a player"""
        # Save data ordered by fitness
        with open(SaveData.LOGS_FOLDER + "/gen" + str(generation) + ".txt", "w") as f:
            fitnessOrder = np.argsort(fitnessSet)[::-1]
            for i in fitnessOrder:
                f.write("Player " + str(i) + ": " + str(fitnessSet[i]) + "\n")
                f.write("Deaths: " + str(statistics[i]['deaths']) + "\n")
                f.write("Penalties: " + str(statistics[i]['penalties']) + "\n")
                f.write("Max score: " + str(statistics[i]['score_record']) + "\n")
                f.write("Mean score: " + str(statistics[i]['mean_score']) + "\n")
                f.write("Steps: " + str(statistics[i]['steps']) + "\n")
                f.write("\n")
    
    @staticmethod
    def clearData(generation):
        """Method to clear all the data after generation"""
        # Remove all folders after this generation
        genaration_folders = os.listdir(SaveData.CHECKPOINT_FOLDER)
        for folder in genaration_folders:
            if (os.path.isdir(SaveData.CHECKPOINT_FOLDER + "/" + folder) and int(folder[3:]) > generation):
                shutil.rmtree(SaveData.CHECKPOINT_FOLDER + "/" + folder)
        # Remove files after this generation
        generation_files = os.listdir(SaveData.LOGS_FOLDER)
        for file in generation_files:
            if (os.path.isfile(SaveData.LOGS_FOLDER + "/" + file) and int(file[3:-4]) > generation):
                os.remove(SaveData.LOGS_FOLDER + "/" + file)
