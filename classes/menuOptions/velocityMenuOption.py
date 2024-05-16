import pyxel

class VelocityMenuOption():
    def __init__(self, velocity):
        self.__velocity = velocity
        self.__xPos = 20
        self.__yPos = 120

        self.__values = [
            {
                "value": 0,
                "velocity": 1,
                "title": "SLOW",
                "offset": 22,
            },
            {
                "value": 1,
                "velocity": 2,
                "title": "NORMAL",
                "offset": 19,
            },
            {
                "value": 2,
                "velocity": 4,
                "title": "FAST",
                "offset": 22,
            }
        ]

    @property
    def velocity(self):
        return self.__values[self.__velocity]["velocity"]

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.__velocity > 0:
            self.__velocity -= 1

        if pyxel.btnp(pyxel.KEY_DOWN) and self.__velocity < 2:
            self.__velocity += 1

    def draw(self):
        pyxel.text(self.__xPos, self.__yPos, "SELECT VELOCITY", 7)
        pyxel.text(self.__xPos + 6 , self.__yPos + 9, "(UP / DOWN):", 7)

        for value in self.__values:
            if value["value"] == self.__velocity:
                pyxel.text(
                    self.__xPos+value["offset"], self.__yPos+(value["value"]+2)*9, value["title"], 7)
            else:
                pyxel.text(
                    self.__xPos+value["offset"], self.__yPos+(value["value"]+2)*9, value["title"], 13)
