import pygame
from pygame.locals import *

import displayManager
import drawer
import eventState
import loader


class TextPause:  # event
    def __init__(self, entity, attribute, targetValue, checkMethod, effects, text, cameraPos=None):
        self.entity = entity
        self.attribute = attribute
        self.targetValue = targetValue
        self.checkMethod = checkMethod
        self.effects = effects

        self.text = text
        self.cameraPos = cameraPos

        self.messageSurf = pygame.Surface((displayManager.WIDTH - 100 * displayManager.SCALE, loader.font.get_linesize() * 3 + 50 * displayManager.SCALE), pygame.SRCALPHA)
        self.messageSurf.fill((0, 0, 255, 127))
        self.messageRect = self.messageSurf.get_rect()
        self.messageRect.midtop = (displayManager.WIDTH / 2, 50 * displayManager.SCALE)

    def run(self, data, camera):
        if self.checkMethod(getattr(self.entity, self.attribute), self.targetValue):
            return self.loop(data, camera)
        else:
            return False

    def loop(self, data, camera):
        i = 0
        while i < len(self.text):
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_BACKQUOTE:
                        exec(input())
                    else:
                        eventState.setState(event.key, True)
                if event.type == KEYUP:
                    eventState.setState(event.key, False)
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        i += 3

            camera.move(data.player, data.entities, posX=self.cameraPos)

            drawer.draw(data, camera)

            displayManager.display.blit(self.messageSurf, self.messageRect)

            if i < len(self.text):
                text = loader.font.render(self.text[i], True, (0xFF, 0xFF, 0xFF))
                textRect = text.get_rect()
                textRect.left = 70 * displayManager.SCALE
                textRect.top = 70 * displayManager.SCALE
                displayManager.display.blit(text, textRect)
            if i + 1 < len(self.text):
                text = loader.font.render(self.text[i+1], True, (0xFF, 0xFF, 0xFF))
                textRect = text.get_rect()
                textRect.left = 70 * displayManager.SCALE
                textRect.top = 70 * displayManager.SCALE + text.get_height()
                displayManager.display.blit(text, textRect)
            if i + 2 < len(self.text):
                text = loader.font.render(self.text[i+2], True, (0xFF, 0xFF, 0xFF))
                textRect = text.get_rect()
                textRect.left = 70 * displayManager.SCALE
                textRect.top = 70 * displayManager.SCALE + text.get_height() * 2
                displayManager.display.blit(text, textRect)

            displayManager.updateDisplay()

        for effect in self.effects:
            effect.run()
        return True
