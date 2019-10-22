import pygame
from pygame.constants import K_w, K_s, K_a, K_d, K_SPACE

import displayManager
import eventState
import loader
from entities.entity import Entity
from entities import GRAVITY


class Player(Entity):
    def __init__(self, posX, posY, posZ, texture, gun, health, walkSound):
        super().__init__(posX, posY, posZ)

        self.texture = texture
        self.facingRight = True

        self.rectangle = self.texture.get_rect()
        self.rectangle.centerx = self.posX
        self.rectangle.bottom = displayManager.HEIGHT - self.posY - self.posZ / 2

        self.guns = [gun]
        self.activeGun = 0

        self.speed = 1200 * displayManager.SCALE
        self.jumpPower = 13 * displayManager.SCALE
        self.jump = 0

        self.maxHealth = health
        self.health = health

        self.walkSound = walkSound
        self.walkChannel = None

        self.active = True

    def move(self):
        playSound = False

        if eventState.getState(K_w):
            self.posZ += self.speed * displayManager.getFrameTimeSeconds()
            playSound = True
            if self.posZ > 1000 * displayManager.SCALE:
                self.posZ = 1000 * displayManager.SCALE
        if eventState.getState(K_s):
            self.posZ -= self.speed * displayManager.getFrameTimeSeconds()
            playSound = True
            if self.posZ < 0:
                self.posZ = 0
        if eventState.getState(K_a):
            self.posX -= self.speed * displayManager.getFrameTimeSeconds() * .7
            playSound = True
            if self.posX < 0:
                self.posX = 0
            if self.facingRight:
                self.facingRight = False
                self.texture = pygame.transform.flip(self.texture, True, False)
                for gun in self.guns:
                    gun.offsetX *= -1
                    gun.texture = pygame.transform.flip(gun.texture, True, False)
        if eventState.getState(K_d):
            self.posX += self.speed * displayManager.getFrameTimeSeconds() * .7
            playSound = True
            if not self.facingRight:
                self.facingRight = True
                self.texture = pygame.transform.flip(self.texture, True, False)
                for gun in self.guns:
                    gun.offsetX *= -1
                    gun.texture = pygame.transform.flip(gun.texture, True, False)

        if self.walkSound.get_num_channels() == 0:
            self.walkChannel = self.walkSound.play(-1)
        if playSound:
            self.walkChannel.unpause()
        else:
            self.walkChannel.pause()

        if eventState.getState(K_SPACE):
            if self.posY == 0:
                self.jump = self.jumpPower
        self.jump -= GRAVITY * displayManager.getFrameTimeSeconds()
        self.posY += self.jump
        if self.posY < 0:
            self.posY = 0

        self.rectangle.centerx = self.posX
        self.rectangle.bottom = displayManager.HEIGHT - self.posY - self.posZ / 2

        self.guns[self.activeGun].reload()

    def shoot(self):
        bullets = self.guns[self.activeGun].shoot(self)
        if bullets is not None:
            for bullet in bullets:
                bullet.texture.fill((0xFF, 0xFF, 0xFF))
                loader.data.myBullets.append(bullet)

    def hit(self, damage):
        self.health -= damage

    def draw(self, camera):
        displayManager.display.blit(self.texture, self.rectangle.move(-camera.posX, -camera.posY))
        self.guns[self.activeGun].draw(self, camera)
