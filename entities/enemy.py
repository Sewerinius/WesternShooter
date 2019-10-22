import random

import pygame
import math

import displayManager
import loader
from entities import GRAVITY
from entities.entity import Entity
from myMath import sign


class Enemy(Entity):
    def __init__(self, posX, posZ, texture, health, gun):
        super().__init__(posX, 0, posZ)
        self.mainPosZ = posZ
        self.texture = texture
        self.facingRight = True
        self.rectangle = self.texture.get_rect()
        self.rectangle.centerx = self.posX
        self.rectangle.bottom = displayManager.HEIGHT - self.posY - self.mainPosZ / 2
        self.gun = gun
        self.active = False
        self.health = health
        self.jumpPower = 13 * displayManager.SCALE
        self.jump = 0
        self.speed = 600 * displayManager.SCALE

        self.dead = False

        self.timeOffset = random.random() * math.pi * 2

    def move(self, player):
        if self.health <= 0:
            self.dead = True
            return True
        if not self.active and abs(player.posX - self.posX) < displayManager.WIDTH * .8:
            self.active = True
        elif self.active:
            if abs(player.posX - self.posX) > displayManager.WIDTH * .9:
                self.active = False

            if abs(player.posX - self.posX) > displayManager.WIDTH * .8:
                self.posX += self.speed * sign(player.posX - self.posX) * displayManager.getFrameTimeSeconds()

            self.mainPosZ += min(self.speed * sign(player.posZ - self.mainPosZ), player.posZ - self.mainPosZ, key=lambda x: abs(x)) * displayManager.getFrameTimeSeconds()
            self.posZ = self.mainPosZ + 200 * math.sin(displayManager.getCurrentTime() / 128 + self.timeOffset) * displayManager.SCALE
            if self.posZ < 0:
                self.posZ = 0
            elif self.posZ > 1000 * displayManager.SCALE:
                self.posZ = 1000 * displayManager.SCALE

            if player.posX - self.posX > 0 and not self.facingRight:
                self.facingRight = True
                self.texture = pygame.transform.flip(self.texture, True, False)
                self.gun.offsetX *= -1
                self.gun.texture = pygame.transform.flip(self.gun.texture, True, False)
            elif player.posX - self.posX < 0 and self.facingRight:
                self.facingRight = False
                self.texture = pygame.transform.flip(self.texture, True, False)
                self.gun.offsetX *= -1
                self.gun.texture = pygame.transform.flip(self.gun.texture, True, False)

            self.jump -= GRAVITY * displayManager.getFrameTimeSeconds()
            self.posY += self.jump
            if self.posY < 0:
                self.posY = 0

            self.rectangle.centerx = self.posX
            self.rectangle.bottom = displayManager.HEIGHT - self.posY - self.posZ / 2

            self.gun.reload()

            bullets = self.gun.shoot(self)
            if bullets is not None:
                for bullet in bullets:
                    bullet.texture.fill((0xCC, 0, 0))
                    loader.data.enemyBullets.append(bullet)

            return False

    def hit(self, damage):
        self.health -= damage
        self.jump = self.jumpPower

    def draw(self, camera):
        displayManager.display.blit(self.texture, self.rectangle.move(-camera.posX, -camera.posY))
        self.gun.draw(self, camera)
