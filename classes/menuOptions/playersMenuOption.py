import pyxel

class PlayersMenuOption():
    def __init__(self, players):
        self._players = players
        self.__xPos = 170
        self.__yPos = 120

        self.__values = [
            {
                "value": 1,
                "title": "1 - 1 PLAYER",
                "offset": 8,
            },
            {
                "value": 2,
                "title": "2 - 2 PLAYERS",
                "offset": 6,
            },
            {
                "value": 3,
                "title": "3 - Training View",
                "offset": 0,
            },
            {
                "value": 4,
                "title": "4 - AI VS. Player",
                "offset": 0,
            }
        ]

    def update(self):
        if pyxel.btnp(pyxel.KEY_1):
            self._players = 1

        elif pyxel.btnp(pyxel.KEY_2):
            self._players = 2

        elif pyxel.btnp(pyxel.KEY_3):
            self._players = 3

        elif pyxel.btnp(pyxel.KEY_4):
            self._players = 4

    def draw(self):
        pyxel.text(self.__xPos + 8, self.__yPos, "SELECT MODE:", 7)
        for value in self.__values:
            if value["value"] == self._players:
                pyxel.text(self.__xPos + value["offset"], self.__yPos + (value["value"])*9, value["title"], 7)
            else:
                pyxel.text(self.__xPos + value["offset"], self.__yPos + (value["value"])*9, value["title"], 13)
