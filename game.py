import pygame
import pygame.freetype
import os
import random
import birdy
import wally

#INIT a PyGame
pygame.init()
pygame.freetype.init()

# WINDOW_OPTION
WINDOW_HEIGHT = 512
WINDOW_WIDTH = 288
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("FlappyBird")

#MAX FPS
FPS = 30

#Import Assets
BACKGROUND = pygame.image.load(os.path.join("assets", "bg.png"))
BIRD_ASSETS = pygame.image.load(os.path.join("assets", "bird2.png"))
BOTTOM_WALL_ASSET = pygame.image.load(os.path.join("assets", "pipe.png"))
TOP_WALL_ASSET = pygame.image.load(os.path.join("assets", "pipe_down.png"))
BASSE_ASSET = pygame.image.load(os.path.join("assets", "base.png"))

#Bird Constants
BIRD_WIDTH = 34
BIRD_HEIGHT = 24

#Wall Constants
WALL_FREE_SPACE = 120

#Register USEREVENTS
BIRD_COLIDE_GROUND = pygame.USEREVENT + 1
BIRD_COLIDE_WALL = pygame.USEREVENT + 2
BIRD_PASS_WALL = pygame.USEREVENT + 3

#IMPORT FONTS
ARCADE_FONT = pygame.freetype.Font(os.path.join("fonts", "8-bit Arcade In.ttf"), 50)

#DEFINE COLORO
WHITE = (255, 255, 255)

def game():     #Main game fuction
    clock = pygame.time.Clock()
    run = True
    life = False
    bird = birdy.Bird(WINDOW_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT)
    walls = [wally.Wall(random.randint(50,280), WALL_FREE_SPACE, 340),
             wally.Wall(random.randint(50,280) , WALL_FREE_SPACE, 510),]
    base = pygame.Rect(0, 480, WINDOW_WIDTH, 32)
    gameRun = False
    points = 0
    maxPoints = 0
    control = 0
    while run:
        if life:
            gameRun = True
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
            controlBird(bird, walls)
            for event in pygame.event.get():
                if event.type == BIRD_COLIDE_GROUND:
                    life = False
                elif event.type == BIRD_COLIDE_WALL:
                    life = False
                elif event.type == BIRD_PASS_WALL:
                    points += 1
            draw(bird, birdImage, walls, base, f"MAX SCORE {maxPoints}")
        else:
            clock.tick(FPS)
            textToRender = ""
            lose = False
            if gameRun:
                bird = birdy.Bird(WINDOW_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT)
                walls = [wally.Wall(random.randint(50, 280), WALL_FREE_SPACE, 340),
                         wally.Wall(random.randint(50, 280), WALL_FREE_SPACE, 510), ]
                if control == 0:
                    points = int(points / 7)
                    control = 1
                if points > maxPoints:
                    maxPoints = points
                textToRender = "GAME OVER"
                lose = True
            else:
                textToRender = "PRESS SPACE"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    run = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    bird.jump()
                    points = 0
                    control = 0
                    life = True
            drawOutsideGame(bird, base, textToRender, lose, points)
    pygame.quit()


def draw(bird, birdImage, walls, base, textToRender):
    birdRect = bird.getBirdRect()
    WINDOW.blit(BACKGROUND, (0, 0))
    drawWalls(walls)
    WINDOW.blit(BASSE_ASSET, (base.x, base.y))
    ARCADE_FONT.render_to(WINDOW, (15, 450), textToRender, WHITE)
    WINDOW.blit(birdImage, (birdRect.x,birdRect.y))
    pygame.display.update()

def drawWalls(walls):
    for wall in walls:
        wallTopRect, wallBottRect = wall.getWallRects()
        WINDOW.blit(TOP_WALL_ASSET, (wallTopRect.x, wallTopRect.y))
        WINDOW.blit(BOTTOM_WALL_ASSET, (wallBottRect.x, wallBottRect.y))


def drawOutsideGame(bird,base, texToRender, lose, points):
    birdRect = bird.getBirdRect()
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(BASSE_ASSET, (base.x, base.y))
    WINDOW.blit(BIRD_ASSETS, (birdRect.x, birdRect.y))
    if lose:
        ARCADE_FONT.render_to(WINDOW, (35,50), texToRender, WHITE)
        ARCADE_FONT.render_to(WINDOW, (32, 75), f"You Have {points}", WHITE)
        ARCADE_FONT.render_to(WINDOW, (15, 100), "PRESS SPACE", WHITE)
    else:
        ARCADE_FONT.render_to(WINDOW, (15, 50), texToRender, WHITE)
    pygame.display.update()


def controlBird(bird, walls):
    birdRect = bird.getBirdRect()
    birdColideWall(birdRect, walls)
    birdPassWall(birdRect, walls)
    if (birdRect.y + BIRD_HEIGHT) >= WINDOW_HEIGHT - 32:
        pygame.event.post(pygame.event.Event(BIRD_COLIDE_GROUND))
    elif birdRect.y <= 0:
        pygame.event.post(pygame.event.Event(BIRD_COLIDE_GROUND))

def wallsMove(walls):
    for wall in walls:
        wall.movingWalls()

def birdColideWall(birdRect, walls):
    for wall in walls:
        wallTopRect, wallBottRect = wall.getWallRects()
        if birdRect.colliderect(wallTopRect) or birdRect.colliderect(wallBottRect):
            pygame.event.post(pygame.event.Event(BIRD_COLIDE_WALL))

def birdPassWall(birdRect, walls):
    for wall in walls:
        rectToPass = wall.getPassWall()
        if birdRect.colliderect(rectToPass):
            pygame.event.post(pygame.event.Event(BIRD_PASS_WALL))