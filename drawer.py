import displayManager
import gui


def draw(data, camera):
    displayManager.display.fill((135, 206, 250))
    for background in data.backgrounds:
        background.draw(camera)
    for floor in data.floors:
        floor.draw(camera)
    elements = data.entities + [data.player] + data.myBullets + data.enemyBullets
    elements.sort(key=lambda x: x.posZ, reverse=True)
    for element in elements:
        element.draw(camera)
    gui.draw(data.player)
