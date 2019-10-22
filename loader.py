import operator
from copy import copy
from xml.etree import cElementTree

import pygame

import displayManager
from entities.floor import Floor
from entities.enemy import Enemy
from entities.gunHolder import GunHolder
from entities.guns import Pistol, Shotgun
from entities.player import Player
from events.exitGame import ExitGame
from events.instantEvent import InstantEvent
from events.spawnEntity import SpawnEntity
from events.textPause import TextPause

data = None
font = None

class LoadedData:
    def __init__(self):
        self.floors = []
        self.backgrounds = []
        self.foregrounds = []
        self.objects = []
        self.entities = []
        self.player = None
        self.myBullets = []
        self.enemyBullets = []
        self.events = []

def loadLevel(levelName):
    global data, font
    font = pygame.font.Font("_res/Exo2.ttf", int(round(60 * displayManager.SCALE)))
    resources = "_res/"
    textures = {}
    sounds = {}
    guns = {}
    entities = {}
    data = LoadedData()
    tree = cElementTree.parse(resources + levelName + ".xml")
    root = tree.getroot()

    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.load(resources + "GameMusic.ogg")
    pygame.mixer.music.play(-1)
    
    for element in root:
        if element.tag == "resources":
            resources = element.text
        elif element.tag == "textures":
            for texture in element:
                textureName = texture.findtext("name")
                if textureName is None:
                    continue
                image = pygame.image.load(resources + textureName + ".png")
                scale = 4 * displayManager.SCALE
                textures[textureName] = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale))).convert_alpha()
        elif element.tag == "sounds":
            for sound in element:
                soundName = sound.findtext("name")
                if soundName is None:
                    continue
                sounds[soundName] = pygame.mixer.Sound(file=resources + soundName + ".ogg")
        elif element.tag == "guns":
            for gun in element:
                name = gun.findtext("name")
                gunType = gun.findtext("type")
                texture = textures[gun.findtext("texture")]
                bulletDamage = float(gun.findtext("bulletDamage"))
                bulletNumber = int(gun.findtext("bulletNumber"))
                magazineSize = int(gun.findtext("magazineSize"))
                bulletSpeed = int(gun.findtext("bulletSpeed"))
                reloadTime = float(gun.findtext("reloadTime"))
                shootDelay = float(gun.findtext("shootDelay"))
                shootSound = sounds[gun.findtext("shootSound")]
                if gunType == "Pistol":
                    guns[name] = Pistol(0, 0, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound)
                elif gunType == "Shotgun":
                    guns[name] = Shotgun(0, 0, texture, bulletDamage, bulletNumber, magazineSize, bulletSpeed, reloadTime, shootDelay, shootSound)
                else:
                    print(gunType)
        elif element.tag == "player":
            player = element
            texture = textures[player.findtext("texture")]
            posX = displayManager.WIDTH * float(player.findtext("posX"))
            posZ = 1000 * displayManager.SCALE * float(player.findtext("posZ"))
            health = float(player.findtext("health"))
            gunData = player.find("gun")
            gun = copy(guns[gunData.findtext("name")])
            gun.offsetX = int(gunData.findtext("offsetX")) * displayManager.SCALE
            gun.mainOffsetY = int(gunData.findtext("offsetY")) * displayManager.SCALE
            walkSound = sounds[player.findtext("walkSound")]
            data.player = Player(posX, 0, posZ, texture, gun, health, walkSound)
            name = player.findtext("name")
            if name is not None:
                entities[name] = data.player
        elif element.tag == "level":
            for level in element:
                if level.tag == "floors":
                    startX = 0
                    for floor in level:
                        length = int(floor.findtext("length"))
                        texture = textures[floor.findtext("texture")]
                        rectangle = texture.get_rect()
                        rectangle.move_ip(startX, displayManager.HEIGHT - rectangle.height)
                        startX += rectangle.width * length

                        data.floors.append(Floor(texture, rectangle, length))

                elif level.tag == "backgrounds":
                    startX = 0
                    for background in level:
                        length = int(background.findtext("length"))

                elif level.tag == "foregrounds":
                    startX = 0
                    for foreground in level:
                        length = int(foreground.findtext("length"))

                elif level.tag == "entities":
                    for entity in level:
                        data.entities.append(loadEntity(entity, textures, guns, entities))
                        
                else:
                    print(level.tag)

        elif element.tag == "events":
            for event in element:
                eventType = event.findtext("type")
                onData = event.find("on")
                entity = entities[onData.findtext("entityName")]
                attribute = onData.findtext("attributeName")
                value = onData.find("value")
                compFunc = getattr(operator, value.attrib["mode"])
                scaled = bool(int(value.attrib["scaled"]))
                value = evalBoolFloat(value.text)
                if scaled:
                    value *= displayManager.WIDTH
                effects = []
                effectsData = event.find("effects")
                if effectsData is not None:
                    for effect in effectsData:
                        if effect.tag == "exitGame":
                            effects.append(ExitGame())
                        elif effect.tag == "spawnEntity":
                            spawnEntities = []
                            for entityElem in effect:
                                spawnEntities.append(loadEntity(entityElem, textures, guns, entities))
                            effects.append(SpawnEntity(spawnEntities))
                        else:
                            print(effect.tag)
                eventData = event.find("data")
                if eventType == "textPause":
                    texts = eventData.findtext("text").split("\n")
                    for i in range(len(texts)):
                        texts[i] = texts[i].strip()
                    if texts[0] == "":
                        del texts[0]
                    if texts[-1] == "":
                        del texts[-1]
                    cameraPos = eventData.findtext("cameraPos")
                    if cameraPos is not None:
                        cameraPos = float(cameraPos) * displayManager.WIDTH
                    data.events.append(TextPause(entity, attribute, value, compFunc, effects, texts, cameraPos))
                elif eventType == "instantEvent":
                    data.events.append(InstantEvent(entity, attribute, value, compFunc, effects))
                else:
                    print(eventType)
        else:
            print(element.tag)

    return data

def loadEntity(entity, textures, guns, entities):
    if entity.tag == "enemy":
        return loadEnemy(entity, textures, guns, entities)
    elif entity.tag == "gunHolder":
        return loadGunHolder(entity, guns)
    else:
        print(entity.tag)
        quit()

def loadEnemy(enemyElem, textures, guns, entities):
    texture = textures[enemyElem.findtext("texture")]
    posX = displayManager.WIDTH * float(enemyElem.findtext("posX"))
    posZ = 1000 * displayManager.SCALE * float(enemyElem.findtext("posZ"))
    health = float(enemyElem.findtext("health"))
    gunData = enemyElem.find("gun")
    gun = guns[gunData.findtext("name")].copy()
    gun.offsetX = int(gunData.findtext("offsetX")) * displayManager.SCALE
    offsetY = int(gunData.findtext("offsetY")) * displayManager.SCALE
    gun.offsetY = offsetY
    gun.mainOffsetY = offsetY
    enemy = Enemy(posX, posZ, texture, health, gun)
    name = enemyElem.findtext("name")
    if name is not None:
        entities[name] = enemy
    return enemy

def loadGunHolder(gunHolderElem, guns):
    posX = displayManager.WIDTH * float(gunHolderElem.findtext("posX"))
    posZ = 1000 * displayManager.SCALE * float(gunHolderElem.findtext("posZ"))
    gunData = gunHolderElem.find("gun")
    gun = guns[gunData.findtext("name")].copy()
    gunHolder = GunHolder(posX, 0, posZ, gun)
    return gunHolder

def evalBoolFloat(string):
    if string[0] == "T":
        return True
    elif string[0] == "F":
        return False
    else:
        return float(string)
