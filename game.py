import pygame
import os
import random
import birdy
import wally
import time

pygame.init()

# WINDOW_OPTION
WINDOW_HEIGHT = 512
WINDOW_WIDTH = 288
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("FlappyBird")

FPS = 60

#Import Assets
BACKGROUND = pygame.image.load(os.path.join("assets", "bg.png"))
BIRD_ASSETS = pygame.image.load(os.path.join("assets", "bird2.png"))
BOTTOM_WALL_ASSET = pygame.image.load(os.path.join("assets", "pipe.png"))
TOP_WALL_ASSET = pygame.image.load(os.path.join("assets", "pipe_down.png"))

#Bird Constants
BIRD_WIDTH = 34
BIRD_HEIGHT = 24

#Wall Constants
WALL_FREE_SPACE = 120

BIRD_COLIDE_WALL = pygame.USEREVENT + 1


RED = (186, 43, 43)

def game():
    clock = pygame.time.Clock()
    run = True
    bird = birdy.Bird(WINDOW_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT)
    walls = [wally.Wall(random.randint(50,280), WALL_FREE_SPACE, 170), wally.Wall(random.randint(50,280) , WALL_FREE_SPACE, 340),]
    #  time.sleep(3)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
        birdImage = pygame.transform.rotate(BIRD_ASSETS, bird.getRotate())
        bird.gravity()
        wallsMove(walls)
        controlBird(bird)
        for event in pygame.event.get():
            if event.type == BIRD_COLIDE_WALL:
                run = False
        draw(bird, birdImage, walls)


def draw(bird, birdImage, walls):
    birdRect = bird.getBirdRect()
    #wallTopRect, wallBottRect = wall.getWallRects()
    WINDOW.blit(BACKGROUND, (0, 0))
   # WINDOW.blit(TOP_WALL_ASSET, (wallTopRect.x, wallTopRect.y))
    #pygame.draw.rect(WINDOW, RED, wallTopRect)
    #WINDOW.blit(BOTTOM_WALL_ASSET, (wallBottRect.x, wallBottRect.y))
    drawWalls(walls)
    WINDOW.blit(birdImage, (birdRect.x,birdRect.y))
    pygame.display.update()

def drawWalls(walls):
    for wall in walls:
        wallTopRect, wallBottRect = wall.getWallRects()
        pygame.draw.rect(WINDOW, RED, wallTopRect)
        WINDOW.blit(BOTTOM_WALL_ASSET, (wallBottRect.x, wallBottRect.y))


def controlBird(bird):
    birdRect = bird.getBirdRect()
    if (birdRect.y + BIRD_HEIGHT) >= WINDOW_HEIGHT:
        pygame.event.post(pygame.event.Event(BIRD_COLIDE_WALL))
    elif birdRect.y <= 0:
        pygame.event.post(pygame.event.Event(BIRD_COLIDE_WALL))

def wallsMove(walls):
    for wall in walls:
        wall.movingWalls()