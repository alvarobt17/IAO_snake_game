# Para ejecutar: python '.\Game V2.py'
import pyxel

from classes.constants import GAME_HEIGHT, GAME_WIDTH, CELLSIZE
from classes.menu import Menu
from classes.gameModes.singleplayerGameMode import SingleGameMode
from classes.gameModes.multiplayerGameMode import MultiplayerGameMode
from classes.gameModes.multiplayerAIGameMode import MultiplayerAIGameMode
from classes.gameModes.trainingAIGameMode import TrainingAIGameMode
from classes.gameModes.testAIGameMode import TestAIGameMode
from classes.colors import bcolors
from classes.SaveData import SaveData
from multiprocessing import Manager


GAME_VELOCITY = 60

class Game ():

    def __init__(self):
        # Atributos que definen el tamaño de la pantalla
        self.pause = False
        self.menuMode = True

        print("=====================================")
        print(f"{bcolors.OKGREEN}Wellcome{bcolors.ENDC} to {bcolors.OKGREEN}Snake AI{bcolors.ENDC}, select and option:")
        print(f"1. {bcolors.OKCYAN}Play Game{bcolors.ENDC} & {bcolors.OKCYAN}Visual{bcolors.ENDC} Training Mode")
        print(f"2. {bcolors.HEADER}Boosted{bcolors.ENDC} Training Mode")
        print(f"3. {bcolors.FAIL}Exit{bcolors.ENDC}")
        option = input("Option: ")
        if option == "1":

            # Menú que controla la configuración del juego
            self.menu = Menu()

            # Se ejecuta el método init para iniciar la pantalla
            pyxel.init(GAME_WIDTH, GAME_HEIGHT, title="SnakeGame",
                    fps=GAME_VELOCITY, quit_key=pyxel.KEY_Q, capture_scale=3)

            pyxel.load("assets/my_resource.pyxres")
            pyxel.colors[8] = 0xFF0000
            pyxel.colors[14] = 0x800303
            pyxel.clip()
            pyxel.mouse(True)

            pyxel.run(self.update, self.draw)
        elif option == "2":
            checkpoint = 0
            option = input("Do you want to load a checkpoint? ([checkpoint number]/No): ")
            if option.isnumeric():
                checkpoint = int(option)
                print(f"Loading checkpoint {checkpoint}...")
            print("=====================================")
            print(f"Executing {bcolors.HEADER}Boosted{bcolors.ENDC} Training Mode...")
            num_threads = int(input("Number of threads: "))
            with Manager() as manager:
                training = TrainingAIGameMode(GAME_WIDTH, GAME_HEIGHT, CELLSIZE, checkpoint=checkpoint, num_threads=num_threads, manager=manager)
                print("=====================================")
                while (True):
                    training.update()
        else:
            print("Exiting...")


    def check_mode_keys(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_M):
            if self.menuMode == True:
                self.start_new_game()

            self.menuMode = not self.menuMode

        if not self.menuMode:
            if pyxel.btnp(pyxel.KEY_P):
                self.pause = not self.pause

            if pyxel.btnp(pyxel.KEY_R):
                self.game.reset()

    def start_new_game(self):
        self.pause = False
        if self.menu.players == 1:
            self.game = SingleGameMode(GAME_WIDTH, GAME_HEIGHT, self.menu.velocity, self.menu.type)
        elif self.menu.players == 2:
            self.game = MultiplayerGameMode(GAME_WIDTH, GAME_HEIGHT, self.menu.velocity)
        elif self.menu.players == 3:
            self.game = TestAIGameMode(GAME_WIDTH, GAME_HEIGHT, self.menu.velocity)
        elif self.menu.players == 4:
            self.game= MultiplayerAIGameMode(GAME_WIDTH, GAME_HEIGHT, self.menu.velocity)


        self.game.start()

    def update(self):
        self.check_mode_keys()

        if self.menuMode:
            self.menu.update()
        elif not self.pause:
            self.game.update()

    def draw(self):
        # Se pinta el fondo
        pyxel.cls(5)

        if not self.menuMode:
            self.game.draw()
        else:
            self.menu.draw()


if __name__ == "__main__":
    Game()
