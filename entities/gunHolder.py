import displayManager
from entities.entity import Entity


class GunHolder(Entity):
    def __init__(self, posX, posY, posZ, gun):
        super().__init__(posX, posY, posZ)
        self.gun = gun
        self.rectangle = self.gun.rectangle

        self.active = False  # For compatibility

    def move(self, player):
        self.rectangle = self.gun.rectangle
        if abs(player.posZ - self.posZ) < 200 * displayManager.SCALE and self.rectangle.colliderect(player.rectangle):
            self.gun.offsetX = player.guns[player.activeGun].offsetX
            self.gun.mainOffsetY = player.guns[player.activeGun].mainOffsetY
            player.guns.append(self.gun)
            player.activeGun = len(player.guns) - 1
            return True

    def draw(self, camera):
        self.gun.draw(self, camera)
