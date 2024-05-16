import pyxel

class TypeMenuOption():
    
    def __init__(self, type):
        self._type = type
        self.__xPos = 104
        self.__yPos = 120

        self.__values = [
            {
                "value": 0,
                "title": "NORMAL",
                "offset": 13,
            },
            {
                "value": 1,
                "title": "DESERT",
                "offset": 13,
            },
            {
                "value": 2,
                "title": "COBRA",
                "offset": 15,
            }
        ]

    def update(self):
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self._type < 2:
                self._type += 1
            else:
                self._type = 0

        if pyxel.btnp(pyxel.KEY_LEFT):
            if self._type > 0:
                self._type -= 1
            else:
                self._type = 2

    def draw(self):
        pyxel.text(self.__xPos + 2, self.__yPos,   "SELECT TYPE", 7)
        pyxel.text(self.__xPos - 4 , self.__yPos + 9, "(LEFT / RIGHT):", 7)
        for value in self.__values:
            if value["value"] == self._type:
                pyxel.text(self.__xPos+value["offset"], self.__yPos + 18, value["title"], 7)

        pyxel.bltm(self.__xPos, self.__yPos + 27, 0, 256, 0, 48, 80)
        pyxel.blt(self.__xPos+16, self.__yPos + 43, 1, 16, self._type*80, 16, 16, 2)
        pyxel.blt(self.__xPos+16, self.__yPos + 59, 1, 0, 64 + self._type*80, 16, 16, 2)
        pyxel.blt(self.__xPos+16, self.__yPos + 75, 1, 0, 64 + self._type*80, 16, 16, 2)
