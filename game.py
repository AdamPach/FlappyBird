import pygame
import os
import birdy

pygame.init()

# WINDOW_OPTION
WINDOW_HEIGHT = 512
WINDOW_WIDTH = 288
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("FlappyBird")

FPS = 30

BACKGROUND = pygame.image.load(os.path.join("assets", "bg.png"))
BIRD_ASSETS = pygame.image.load(os.path.join("assets", "bird2.png"))

BIRD_WIDTH = 34
BIRD_HEIGHT = 24

BIRD_COLIDE_WALL = pygame.USEREVENT + 1

def game():
    clock = pygame.time.Clock()
    run = True
    bird = birdy.Bird(WINDOW_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT)
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
        controlBird(bird)
        for event in pygame.event.get():
            if event.type == BIRD_COLIDE_WALL:
                run = False
        draw(bird, birdImage)


def draw(bird, birdImage):
    birdRect = bird.getBirdRect()
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(birdImage, (birdRect.x,birdRect.y))
    pygame.display.update()

def controlBird(bird):
    birdRect = bird.getBirdRect()
    if (birdRect.y + BIRD_HEIGHT) >= WINDOW_HEIGHT:
        pygame.event.post(pygame.event.Event(BIRD_COLIDE_WALL))
    elif birdRect.y <= 0:
        pygame.event.post(pygame.event.Event(BIRD_COLIDE_WALL))