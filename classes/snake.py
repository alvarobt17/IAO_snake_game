import pyxel
from .constants import *

class SnakeBodyPart:
    def __init__ (self, posX: int, posY: int, velocity: int, type: int, isHead = False, startMove = None):
        self.posX = posX
        self.posY = posY
        self.next = None
        self.isHead = isHead
        self.currentDir: Moves = startMove
        self.__velocity = velocity
        self.__type = type

        if self.isHead:
            self.tongue = 0
        
    def update(self):
        if self.currentDir == Moves.LEFT:
            self.posX -= self.__velocity
        elif self.currentDir == Moves.RIGHT:
            self.posX += self.__velocity
        elif self.currentDir == Moves.UP:
            self.posY -= self.__velocity
        elif self.currentDir == Moves.DOWN:
            self.posY += self.__velocity
        
        return (self.posX, self.posY)

    def draw(self, dead):
        if self.isHead:
            # Tongue animation
            self.tongue = (self.tongue + 1) % 36 if not dead else 0
            # Dead sprite if dead
            color = 0 if dead else 1
            if self.currentDir == Moves.LEFT:
                offset = CELLSIZE
            elif self.currentDir == Moves.RIGHT:
                offset = 48
            elif self.currentDir == Moves.UP:
                offset = 0
            elif self.currentDir == Moves.DOWN:
                offset = 32
            pyxel.blt (self.posX, self.posY, 1, color*CELLSIZE + CELLSIZE*(self.tongue//6), offset+self.__type*80, CELLSIZE, CELLSIZE, 2) 
        else:
            pyxel.blt (self.posX, self.posY, 1, 0, 64+self.__type*80, CELLSIZE, CELLSIZE,2)

    def isInCell(self):
        return self.posX%CELLSIZE == 0 and self.posY%CELLSIZE == 0 

class Snake:
    def __init__(self, widht: int, height: int, x: int, y: int, velocity: int, type: int, startMove = Moves.RIGHT):
        self.__WIDHT = widht
        self.__HEIGHT = height
        self.__velocity = velocity
        self.__type = type
        self.head = SnakeBodyPart (x, y, self.__velocity, self.__type, True, startMove)
        self.__tail = self.head
        self.length = 1
        
        #Atributos para detectar el movimiento
        self.newTail = None
        self.dead = False


    def moveSnake (self, part: SnakeBodyPart, move):
        """Método que se encarga de enviar a cada parte de la
        serpiente que se mueva"""
        moveNextPart=move
        while part is not None:
            if part.isInCell():
                moveNextPart, part.currentDir = part.currentDir, moveNextPart
            part.update()
            part = part.next
            
    
    def checkDead (self, snakes: list):
        head = self.head
        if (head.posX + 15 > self.__WIDHT or head.posX < 0 
            or head.posY < 32 or head.posY + 15 > self.__HEIGHT):
            return True

        for snake in snakes:
            bodyPart = snake.head
            # Ignore the head of this snake
            if self.head is bodyPart:
                bodyPart = bodyPart.next
            while bodyPart:
                if head.currentDir == Moves.RIGHT and (bodyPart.posX < head.posX+15 < bodyPart.posX+CELLSIZE     
                                                    and bodyPart.posY <= head.posY < bodyPart.posY+CELLSIZE):
                        return True
                elif head.currentDir == Moves.LEFT and (bodyPart.posX < head.posX < bodyPart.posX+CELLSIZE 
                                                        and bodyPart.posY <= head.posY < bodyPart.posY+CELLSIZE):
                        return True
                elif head.currentDir == Moves.UP and (bodyPart.posY < head.posY < bodyPart.posY+CELLSIZE 
                                                    and bodyPart.posX <= head.posX < bodyPart.posX+CELLSIZE):
                        return True
                elif head.currentDir == Moves.DOWN and (bodyPart.posY < head.posY+15 < bodyPart.posY+CELLSIZE 
                                                and bodyPart.posX <= head.posX < bodyPart.posX+CELLSIZE):
                        return True
                bodyPart = bodyPart.next
        
        return False
            
    def getAxisDistances(self, snakes: list = []):
        """Function that calculate in the 4 axis starting by the snake head,
        the distance to the next bodyPart or map border"""
        distances = {
            "left": self.head.posX//CELLSIZE,
            "right": (self.__WIDHT-self.head.posX-1)//CELLSIZE,
            "up": (self.head.posY-32)//CELLSIZE,
            "down": (self.__HEIGHT-self.head.posY-1)//CELLSIZE
        }

        snakes = snakes.copy()
        snakes.append(self)

        for snake in snakes:
            part = snake.head
            while part:
                if part is self.head:
                    part = part.next
                    continue
                if part.posX//CELLSIZE == self.head.posX//CELLSIZE:
                    if part.posY > self.head.posY:
                        distances["down"] = min(distances["down"], (part.posY - self.head.posY-1)//CELLSIZE)
                    else:
                        distances["up"] = min(distances["up"], (self.head.posY - part.posY)//CELLSIZE)
                elif part.posY//CELLSIZE == self.head.posY//CELLSIZE:
                    if part.posX > self.head.posX:
                        distances["right"] = min(distances["right"], (part.posX - self.head.posX-1)//CELLSIZE)
                    else:
                        distances["left"] = min(distances["left"], (self.head.posX - part.posX)//CELLSIZE)
                part = part.next

        # Normalice each distance
        for key in distances:
            distances[key] = distances[key]/(max(self.__HEIGHT//CELLSIZE, self.__WIDHT//CELLSIZE) - 1)
            
        return distances

    def getSpaceRegions(self, snakes: list):
        # Function htat execute a amplitud algorithm starting in the snake head to 
        #  Get the accesible region without coliding with other body part or the 
        # map border

        snakes = snakes.copy()
        snakes.append(self)
         
        quadrants = {
            "left-up":      self.__getQuadrantRegion(snakes, self.head.posX//CELLSIZE-1, self.head.posY//CELLSIZE-1, -1, -1),
            "right-up":     self.__getQuadrantRegion(snakes, self.head.posX//CELLSIZE+1, self.head.posY//CELLSIZE-1, +1, -1),
            "left-down":    self.__getQuadrantRegion(snakes, self.head.posX//CELLSIZE-1, self.head.posY//CELLSIZE+1, -1, +1),
            "right-down":   self.__getQuadrantRegion(snakes, self.head.posX//CELLSIZE+1, self.head.posY//CELLSIZE+1, +1, +1),
        }


        # Normalize each quadrant
        totalSpace = 0
        for value in quadrants.values():
            totalSpace += value

        if totalSpace != 0:
            for key in quadrants:
                quadrants[key] = quadrants[key]/totalSpace
        
        return quadrants
        

    def __getQuadrantRegion(self, snakes: list, posX, posY, xDir, yDir, posVisited=None):
        if posVisited == None:
            posVisited = set()

        if (posX, posY) in posVisited:
            return 
        
        # Check if the position is a body part
        for snake in snakes:
            part = snake.head
            while part:
                if part.posX//CELLSIZE == posX and part.posY//CELLSIZE == posY:
                    return 0
                part = part.next
        
        # Check if the position is a border
        if  posX < 0 or posX >= self.__WIDHT//CELLSIZE or posY < 2 or posY >= (self.__HEIGHT)//CELLSIZE:
            return 0
        
        posVisited.add((posX, posY))
        # Recursive call on each direction
        self.__getQuadrantRegion(snakes, posX+xDir, posY, xDir, yDir, posVisited)
        self.__getQuadrantRegion(snakes, posX, posY+yDir, xDir, yDir, posVisited)
        return len(posVisited)
    
    def getDistanceToFruits(self, fruits):
        """Function that calculate the distance between the snake head and the fruit"""
        height_distance = (self.__HEIGHT-33)//CELLSIZE
        width_distance = (self.__WIDHT-1)//CELLSIZE
        distances = {
            "left": width_distance,
            "right": width_distance,
            "up": height_distance,
            "down": height_distance
        }

        # Calculate the distance to each fruit, and save the minimun one
        for fruit in fruits:
            if fruit.posY//CELLSIZE == self.head.posY//CELLSIZE:
                distances["down"] = min(distances["down"], height_distance)
                distances["up"] = min(distances["up"], height_distance)
            elif fruit.posY > self.head.posY:
                distances["down"] = min(distances["down"], (fruit.posY - self.head.posY-1)//CELLSIZE)
            else:
                distances["up"] = min(distances["up"], (self.head.posY - fruit.posY)//CELLSIZE)
                
            if fruit.posX//CELLSIZE == self.head.posX//CELLSIZE:
                distances["right"] = min(distances["right"], width_distance)
                distances["left"] = min(distances["left"], width_distance)
            elif fruit.posX > self.head.posX:
                distances["right"] = min(distances["right"], (fruit.posX - self.head.posX-1)//CELLSIZE)
            else:
                distances["left"] = min(distances["left"], (self.head.posX - fruit.posX)//CELLSIZE)

        # Normalize and invert the values
        for key in distances:
            distances[key] = 1 - distances[key]/max(height_distance, width_distance)

        return distances

    def growSnake(self):
        self.newTail = SnakeBodyPart (self.__tail.posX, self.__tail.posY, self.__velocity, self.__type)

    def __growSnake(self):
        """Function that add a new body part to the snake"""
        self.length += 1
        self.__tail.next = self.newTail
        self.__tail = self.__tail.next
        self.newTail = None

    def update(self, move, gameSnakes: list):
        if not self.dead:
            self.currentDir = move
            if self.currentDir:
                self.moveSnake (self.head, self.currentDir)

            self.dead = self.checkDead(gameSnakes)
            
            if self.newTail is not None and self.head.isInCell():
                self.__growSnake()

    def draw(self):
        part = self.head
        while part:
            part.draw(self.dead)
            part = part.next
