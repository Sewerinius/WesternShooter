import displayManager


class Floor:
    def __init__(self, texture, rectangle, length):
        self.texture = texture
        self.rectangle = rectangle
        self.length = length

    def draw(self, camera):
        for i in range(self.length):
            displayManager.display.blit(self.texture, self.rectangle.move(i * self.texture.get_width() - camera.posX, -camera.posY))