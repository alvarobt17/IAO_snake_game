import pyxel


class Header():
    """
    A class representing the header of the Snake IA game.

    Attributes:
    - longitud (int): the length of the snake.
    - longitud2 (int): the lenght of the second snake in multiplayer mode.
    - dead (int): the number of times player 1 has died.
    - dead2 (int): the number of times player 2 has died.
    """

    def __init__(self, players):
        """
        Initializes a new instance of the Header class.

        Parameters:
        - longitud (int): the initial length of the snake.
        - longitud2 (int): the lenght of the second snake in multiplayer mode.
        - dead (int): the initial number of times player 1 has died.
        - dead2 (int): the initial number of times player 2 has died.
        """
        self.__players = players
        self.__xPosOptions = 202
        self.__yPosOptions = 3
        self.__xPosPlayers = 15
        self.__yPosPlayers = 3
        self.__xOffsetBetweenPlayers = 60

    @staticmethod
    def __get_players_dict(players):
        playersDict = []
        for player in players:
            playersDict.append({
                'length': player.snake.length,
                'deaths': player.deaths
            })
        return playersDict

    def update(self, players):
        """
        Updates the header with new values.

        Parameters:
        - longitud (int): the new length of the snake.
        - longitud2 (bool): the new lenght of the second snake in multiplayer mode.
        - dead (int): the new number of times player 1 has died.
        - dead2 (int): the new number of times player 2 has died.
        """
        self.__players = self.__get_players_dict(players)

    def draw(self):
        """
        Draws the header on the screen.
        """
        playerCounter = 1
        for player in self.__players:
            xPos = self.__xPosPlayers + \
                (playerCounter-1)//2 * self.__xOffsetBetweenPlayers
            yPos = self.__yPosPlayers + (playerCounter-1) % 2*14
            
            if player['length'] >= 100:
                lengthSpaces = " "
            elif player['length'] >= 10:
                lengthSpaces = "  "
            else:
                lengthSpaces = "   "
            pyxel.text(xPos, yPos, f"Length {playerCounter}:{lengthSpaces}{player['length']}", 7)

            if player['deaths'] >= 100:
                deathsSpaces = " "
            elif player['deaths'] >= 10:
                deathsSpaces = "  "
            else:
                deathsSpaces = "   "
            pyxel.text(xPos, yPos + 7, f"deaths {playerCounter}:{deathsSpaces}{player['deaths']}", 7)

            playerCounter += 1

        pyxel.text(self.__xPosOptions, self.__yPosOptions, "Menu -> M", 7)
        pyxel.text(self.__xPosOptions, self.__yPosOptions + 7, "Pause -> P", 7)
        pyxel.text(self.__xPosOptions, self.__yPosOptions +
                   14, "Restart -> R", 7)
        pyxel.text(self.__xPosOptions, self.__yPosOptions + 21, "Quit -> Q", 7)
