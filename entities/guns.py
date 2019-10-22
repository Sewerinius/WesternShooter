import random
from abc import ABC, abstractmethod

import math
from copy import copy

from pygame.rect import Rect

import displayManager
from entities.bullet import Bullet


class Gun(ABC):
    def __init__(self, offsetX, offsetY, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound):
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.mainOffsetY = self.offsetY
        self.texture = texture
        self.rectangle = self.texture.get_rect()
        self.bulletDamage = bulletDamage
        self.bulletInMagazine = magazineSize
        self.bulletNumber = bulletNumber
        self.magazineSize = magazineSize
        self.bulletSpeed = bulletSpeed * displayManager.SCALE
        self.reloadTime = reloadTime
        self.shootDelay = shootDelay
        self.reloading = 0
        self.delaying = 0

        self.shootSound = shootSound

        self.timeOffset = random.random() * math.pi * 2

    def copy(self):
        gun = copy(self)
        gun.rectangle = Rect(self.rectangle)
        return gun

    @abstractmethod
    def shoot(self, shooter):
        pass

    def reload(self, reload=False):  # method called every frame
        if self.delaying > 0:
            self.delaying -= displayManager.getFrameTimeSeconds()
            if self.delaying <= 0:
                self.delaying = 0
        if self.bulletNumber == 0 or self.bulletInMagazine == self.magazineSize:
            return
        if reload and self.reloading <= 0:
            self.reloading = self.reloadTime
            if self.reloading <= 0:
                bulletsToReload = self.magazineSize - self.bulletInMagazine
                self.bulletInMagazine += min(bulletsToReload, self.bulletNumber)
                self.bulletNumber -= min(bulletsToReload, self.bulletNumber)
        else:
            if self.reloading > 0:
                self.reloading -= displayManager.getFrameTimeSeconds()
                if self.reloading <= 0:
                    self.reloading = 0
                    bulletsToReload = self.magazineSize - self.bulletInMagazine
                    self.bulletInMagazine += min(bulletsToReload, self.bulletNumber)
                    self.bulletNumber -= min(bulletsToReload, self.bulletNumber)

    def draw(self, shooter, camera):
        self.offsetY = self.mainOffsetY + 4 * math.sin(displayManager.getCurrentTime() / 512 + self.timeOffset) * displayManager.SCALE
        self.rectangle.center = (shooter.posX + self.offsetX, displayManager.HEIGHT - shooter.posY - shooter.posZ / 2 - self.offsetY)
        displayManager.display.blit(self.texture, self.rectangle.move(-camera.posX, -camera.posY))


class Pistol(Gun):
    def __init__(self, offsetX, offsetY, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound):
        super().__init__(offsetX, offsetY, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound)

    def shoot(self, shooter):
        if self.bulletInMagazine == 0:
            self.reload(True)
            return None
        if self.delaying <= 0 and self.reloading <= 0:
            self.shootSound.play()
            self.delaying = self.shootDelay
            self.bulletInMagazine -= 1
            direction = 1 if shooter.facingRight else -1
            return [Bullet(shooter.posX + self.offsetX, shooter.posY + self.offsetY, shooter.posZ, self.bulletSpeed * direction, 0, 0, self.bulletDamage, 16)]

class Shotgun(Gun):
    def __init__(self, offsetX, offsetY, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound):
        super().__init__(offsetX, offsetY, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound)

    def shoot(self, shooter):
        if self.bulletInMagazine == 0:
            self.reload(True)
            return None
        if self.delaying <= 0 and self.reloading <= 0:
            self.shootSound.play()
            self.delaying = self.shootDelay
            self.bulletInMagazine -= 1
            direction = 1 if shooter.facingRight else -1
            bullets = []
            bullets.append(Bullet(shooter.posX + self.offsetX, shooter.posY + self.offsetY, shooter.posZ,
                                  self.bulletSpeed * direction * math.cos(math.radians(  0)), 0, self.bulletSpeed * math.sin(math.radians(  0)), self.bulletDamage, 16))
            bullets.append(Bullet(shooter.posX + self.offsetX, shooter.posY + self.offsetY, shooter.posZ,
                                  self.bulletSpeed * direction * math.cos(math.radians( 20)), 0, self.bulletSpeed * math.sin(math.radians( 20)), self.bulletDamage, 16))
            bullets.append(Bullet(shooter.posX + self.offsetX, shooter.posY + self.offsetY, shooter.posZ,
                                  self.bulletSpeed * direction * math.cos(math.radians(-20)), 0, self.bulletSpeed * math.sin(math.radians(-20)), self.bulletDamage, 16))
            return bullets
