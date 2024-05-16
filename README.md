# Snake_AI_Game

## Requirements
The currents libraries of the project are:
- ### Pyxel
    The Pyxel library is a retro game engine for Python that is designed for making 2D games. It provides a simple interface for creating games with a limited color palette and pixelated graphics, similar to the games of the 80s and 90s. Pyxel includes features such as sprite and tilemap support, sound effects, music, and keyboard input handling. It is a lightweight library that is easy to use and can be a great choice for creating small games or prototypes.
- ### Tensorflow
    TensorFlow is an open-source machine learning framework developed by the Google Brain team. It is widely used for building and training various machine learning models, especially deep learning models. TensorFlow provides a comprehensive set of tools, libraries, and community resources to facilitate the development and deployment of machine learning applications.

## Installation
```bash
pip install -r requirements.txt
```
## Execution
```bash
python3 Game.py
```

# Training
To train the model, enter option 2 and select the number of threads, you can adjust the ANN, and the GA parameters in the parameters.json file.

# Play the Game
To play the Main Game, enter option 1, then you can select a variaty of modes, pressing the corresponding num key:
1. Singleplayer
2. Two players mode
3. See the result of your trained model
4. Player vs AI

[press M to select the mode]

# Test your model
In option 3, you can select the checkpoint of the training you want to execute to see it's behavior.

Once you have the trained your model, introduce it in the finalModel folder, and name it finalModel.p

Then you can play against it in the <b>Player vs AI mode
