import pygame

BIRD_WIDTH = 34
BIRD_HEIGHT = 24

class Bird:

    def __init__(self, WIN_H):
        self.__Y_POS =  WIN_H / 2
        self.__X_POS = 100
        self.__GRAVITY = 0
        self.__ROTATE = 0

    def jump(self):
        self.__GRAVITY = 10

    def gravity(self):
        self.__GRAVITY -= 1
        if self.__GRAVITY <= -10:
            self.__GRAVITY = -10
        elif self.__GRAVITY >= 10:
            self.__GRAVITY = 10
        self.__Y_POS -= self.__GRAVITY

    def getBirdRect(self):
        return pygame.Rect(self.__X_POS, self.__Y_POS, BIRD_WIDTH, BIRD_HEIGHT)

    def __controllRotate(self):
        if self.__GRAVITY == 0:
            self.__ROTATE = 0
        elif self.__GRAVITY > 0:
            for number in range(10):
                if self.__GRAVITY == number:
                    self.__ROTATE = number * 5
                    break
        elif self.__GRAVITY < 0:
            for number in range(10):
                if self.__GRAVITY == (number) * -1:
                    self.__ROTATE = number * (-5)
                    break

    def getRotate(self):
        self.__controllRotate()
        return self.__ROTATE