import pyxel
from .menuOptions.typeMenuOption import TypeMenuOption
from .menuOptions.velocityMenuOption import VelocityMenuOption
from .menuOptions.playersMenuOption import PlayersMenuOption


class Menu ():
    def __init__(self):
        # Initialize the menu options
        self.__typeOption = TypeMenuOption(0)
        self.__velocityOption = VelocityMenuOption(1)
        self.__playersOption = PlayersMenuOption(1)

    # Getter to type value
    @property
    def type(self):
        return self.__typeOption._type

    # Getter to velocity value
    @property
    def velocity(self):
        return self.__velocityOption.velocity
    
    # Getter to players value
    @property
    def players(self):
        return self.__playersOption._players
        
    def update(self):
        # Update each setting
        self.__typeOption.update()
        self.__velocityOption.update()
        self.__playersOption.update()

    def draw(self):
        # Print the game title
        pyxel.blt(56, 30, 0, 0, 64, 144, 32, 2)
        
        # Print the options
        self.__typeOption.draw()
        self.__velocityOption.draw()
        self.__playersOption.draw()

        pyxel.text(75, 250, "Press 'M' to start the game", 7)


