import pygame
import random

class Wall:

    def __init__(self, topWallHeight, freeSpace, xPos):
        self.__topWallHeight = topWallHeight
        self.__freeSpace = freeSpace
        self.__X_POS = xPos
        self.__Y_POS = 0
        self.__Y_POS_TOP = self.__topWallHeight - 320
        self.__WIDTH = 52
        self.__Y_BOTT_POS = self.__topWallHeight + self.__freeSpace
        self.__BOTT_HEIGHT = 512 - self.__Y_BOTT_POS

    def getWallRects(self):
        return pygame.Rect(self.__X_POS, self.__Y_POS_TOP, self.__WIDTH, 320), pygame.Rect(self.__X_POS, self.__Y_BOTT_POS, self.__WIDTH, self.__BOTT_HEIGHT)

    def movingWalls(self):
        self.__controlWall()
        self.__X_POS -= 5

    def __regenWall(self):
        self.__topWallHeight = random.randint(50,280)
        self.__WallHeight = self.__topWallHeight + 320
        self.__X_POS = 300
        self.__Y_POS_TOP = self.__topWallHeight - 320
        self.__Y_BOTT_POS = self.__topWallHeight + self.__freeSpace
        self.__BOTT_HEIGHT = 512 - self.__Y_BOTT_POS

    def __controlWall(self):
        if self.__X_POS < 0 - self.__WIDTH:
            self.__regenWall()

    def getPassWall(self):
        return pygame.Rect(self.__X_POS + (self.__WIDTH/2), self.__Y_POS + self.__topWallHeight, 1, self.__freeSpace)