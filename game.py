import builtins
import pygame
from pygame.locals import *

import displayManager
import drawer
import eventState
import loader
from entities.camera import Camera

builtins.EXIT = False

def main():
    pygame.init()
    displayManager.createDisplay()

    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    data = loader.loadLevel("level")

    camera = Camera(0, 0)

    while True:
        if builtins.EXIT:
            return
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN:
                if event.key == K_BACKQUOTE:
                    exec(input())
                elif event.key == K_r:
                    data.player.gun.reload(True)
                elif event.key == K_KP_PLUS:
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + .05)
                elif event.key == K_KP_MINUS:
                    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - .05)
                else:
                    eventState.setState(event.key, True)
            if event.type == KEYUP:
                eventState.setState(event.key, False)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    data.player.shoot()

        data.player.move()
        for entity in data.entities:
            dead = entity.move(data.player)
            if dead:
                data.entities.remove(entity)
        for bullet in data.myBullets:
            dead = bullet.move(data.entities)
            if dead:
                data.myBullets.remove(bullet)
        for bullet in data.enemyBullets:
            dead = bullet.move(data.entities + [data.player])
            if dead:
                data.enemyBullets.remove(bullet)
        camera.move(data.player, data.entities)

        for event in data.events:
            delete = event.run(data, camera)
            if delete:
                data.events.remove(event)

        drawer.draw(data, camera)
        displayManager.updateDisplay()

def debug():
    pygame.init()
    pygame.display.set_mode((100, 100))
    sound = pygame.mixer.Sound(file="_res/GameMusic.ogg")
    print(sound.get_raw())
    sound2 = pygame.mixer.Sound(file="_res/walk.ogg")
    channel = sound.play(-1)
    print(sound.get_num_channels())
    pygame.time.delay(100)
    for i in range(20):
        print(sound2.play(-1))
        pygame.time.delay(100)

    print(sound.get_num_channels())
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return


if __name__ == "__main__":
    main()
