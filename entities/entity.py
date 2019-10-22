from abc import ABC


class Entity(ABC):
    def __init__(self, posX, posY, posZ):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ