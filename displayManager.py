import os

import pygame

os.environ["SDL_VIDEO_CENTERED"] = "1"
WIDTH = 1600
HEIGHT = int(round(WIDTH * 9 / 16))
SCALE = WIDTH / 1920
display = None
FPS_CAP = 60
TIMER = pygame.time.Clock()
lastFrameTime = pygame.time.get_ticks()
delta = 0
avgDelta = 0
i = 0

def createDisplay():
    global display
    display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Game")


def updateDisplay():
    TIMER.tick(FPS_CAP)
    pygame.display.flip()
    currentFrameTime = pygame.time.get_ticks()
    global lastFrameTime, delta, avgDelta, i
    delta = (currentFrameTime - lastFrameTime) / 1000.0
    avgDelta += delta
    i += 1
    if i >= 10:
        avgDelta /= i
        pygame.display.set_caption("Game            FPS: {0:.2f}".format(1 / avgDelta))
        i = 0
        avgDelta = 0
    lastFrameTime = currentFrameTime

def getFrameTimeSeconds():
    return delta

def getCurrentTime():
    return pygame.time.get_ticks()
