import pygame

import displayManager
from entities.entity import Entity


class Camera(Entity):
    def __init__(self, posX, posY):
        super().__init__(posX, posY, 0)
        self.speed = 10
        self.lastLength = False

    def move(self, player=None, entities=None, posX=None):
        if posX is None:
            minX = player.posX
            maxX = player.posX
            for entity in entities:
                if entity.active:
                    if entity.posX < minX:
                        minX = entity.posX
                    elif entity.posX > maxX:
                        maxX = entity.posX
        else:
            minX = posX
            maxX = posX
        cursorX = pygame.mouse.get_pos()[0] - displayManager.WIDTH / 2
        cursorX /= 10
        length = self.posX - (minX + maxX) / 2 + displayManager.WIDTH / 2 - cursorX
        if (abs(length) < 10 and not self.lastLength) or (abs(length) < 1.5 and self.lastLength):
            self.posX -= length
            self.lastLength = False
        else:
            self.posX -= length * 3 * displayManager.getFrameTimeSeconds()
            self.lastLength = True
        if self.posX < 0:
            self.posX = 0
            self.lastLength = False
