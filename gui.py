from math import pi

import pygame

import displayManager
import loader


def draw(player):
    ammo = str(player.guns[player.activeGun].bulletInMagazine) + "/" + str(player.guns[player.activeGun].bulletNumber)
    drawAmmo(ammo)
    drawHealth(player)
    drawGunDelays(player.guns[player.activeGun])

def drawAmmo(ammo):
    ammoBackground = pygame.Surface(loader.font.size(ammo), pygame.SRCALPHA)
    ammoBackground.fill((0x7F, 0x7F, 0x7F, 0x7F))
    ammoSurf = loader.font.render(ammo, True, (0, 0, 0))
    ammoRect = ammoSurf.get_rect()
    ammoBackground.blit(ammoSurf, (0, 0))
    ammoRect.bottomright = (displayManager.WIDTH, displayManager.HEIGHT)
    displayManager.display.blit(ammoBackground, ammoRect)

def drawHealth(player):
    healthBar = pygame.Rect(0, 0, int(round(displayManager.WIDTH * player.health / player.maxHealth)), int(round(20 * displayManager.SCALE)))
    pygame.draw.rect(displayManager.display, (0xFF, 0, 0), healthBar)


def drawGunDelays(gun):
    mousePos = pygame.mouse.get_pos()
    shootRect = pygame.Rect(mousePos[0] - 15, mousePos[1] - 15, 30, 30)
    try:
        pygame.draw.arc(displayManager.display, (0, 0, 0xFF), shootRect, -gun.delaying / gun.shootDelay * pi * 2 + pi / 2, pi / 2, 5)
    except ZeroDivisionError:
        pass
    reloadRect = pygame.Rect(mousePos[0] - 20, mousePos[1] - 20, 40, 40)
    try:
        pygame.draw.arc(displayManager.display, (0, 0xFF, 0), reloadRect, -gun.reloading / gun.reloadTime * pi * 2 + pi / 2, pi / 2, 5)
    except ZeroDivisionError:
        pass
