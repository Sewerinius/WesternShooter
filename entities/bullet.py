import pygame

import displayManager
from entities.entity import Entity


class Bullet(Entity):
    def __init__(self, posX, posY, posZ, speedX, speedY, speedZ, damage, size):
        super().__init__(posX, posY, posZ)
        self.speedX = speedX
        self.speedY = speedY
        self.speedZ = speedZ
        self.damage = damage
        size = int(round(size * displayManager.SCALE))
        self.texture = pygame.Surface((size, size)).convert_alpha()
        self.rotatedTexture = self.texture
        self.rectangle = self.texture.get_rect()
        self.rectangle.center = (self.posX, displayManager.HEIGHT - self.posY - self.posZ / 2)
        self.angle = 0
        self.active = 5

    def move(self, enemies):
        self.speedY -= 0.05
        self.speedX *= .999
        self.posX += self.speedX * displayManager.getFrameTimeSeconds()
        self.posY += self.speedY * displayManager.getFrameTimeSeconds()
        self.posZ += self.speedZ * displayManager.getFrameTimeSeconds()

        if self.posY < 0 or abs(self.posZ - 500 * displayManager.SCALE) > 500 * displayManager.SCALE:
            return True

        self.angle -= 5
        self.rotatedTexture = pygame.transform.rotate(self.texture, self.angle)
        self.rectangle = self.rotatedTexture.get_rect()
        self.rectangle.center = (self.posX, displayManager.HEIGHT - self.posY - self.posZ / 2)

        if self.active == 0:
            for enemy in enemies:
                if enemy.active and abs(enemy.posZ - self.posZ) < 100 * displayManager.SCALE and self.rectangle.colliderect(enemy.rectangle):
                    enemy.hit(self.damage)
                    return True
        else:
            self.active -= 1
        return False

    def draw(self, camera):
        displayManager.display.blit(self.rotatedTexture, self.rectangle.move(-camera.posX, -camera.posY))