
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import json

class NeuralNet ():
    with open("parameters.json") as f:
        data = json.load(f)
        layers = data["NeuralNetLayers"]

    def __init__(self, weights):
        self.model = Sequential()
        self.createModel(weights)

    @staticmethod
    def weights_size():
        """Function to get the size of the weights"""
        size = 0
        for i in range(len(NeuralNet.layers) - 1):
            size += NeuralNet.layers[i] * NeuralNet.layers[i+1]
        return size

    @staticmethod
    def randomWeights():
        """Function to get random weights"""
        return np.random.uniform(-1, 1, NeuralNet.weights_size())
    
    def formatWeights(self, weights):
        """Function to format the weights to use it in set_weights"""
        formatted_weights = []
        for i in range(len(NeuralNet.layers) - 1):
            formatted_weights.append(weights[:NeuralNet.layers[i] * NeuralNet.layers[i+1]].reshape((NeuralNet.layers[i], NeuralNet.layers[i+1])))
            # Add the bias with value 0
            formatted_weights.append(np.zeros(NeuralNet.layers[i+1]))
            weights = weights[NeuralNet.layers[i] * NeuralNet.layers[i+1]:]
        return formatted_weights

    def createModel(self, weights):
        """Method to create the model"""
        formatedWeights = self.formatWeights(weights)
        for i in range(1, len(NeuralNet.layers) - 1):
            self.model.add(Dense(NeuralNet.layers[i], activation='relu'))
        self.model.add(Dense(NeuralNet.layers[-1], activation='softmax'))
        self.model.build(input_shape=(None, NeuralNet.layers[0]))
        self.model.set_weights(formatedWeights)
        # self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def show(self):    
        """Method to show the model summary"""
        self.model.summary()
