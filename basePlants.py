import pygame as pg
from enum import Enum

class PlantEnum(Enum):
    PEASHOOTER = 0
    SUNFLOWER = 1


class Plant:
    plants = []

    def __init__(self, rect: pg.Rect, filename: str, health: int = 300) -> None:
        # self.pos = rect.topleft
        self.rect = rect
        self.img = pg.image.load(filename)
        self.img.convert()
        self.img = pg.transform.scale(self.img,(self.rect.width, self.rect.height))
        Plant.plants.append(self)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.img, self.rect.topleft)

    def drawAll(surface: pg.Surface):
        for plant in Plant.plants:
            plant.draw(surface)
            plant.tick()

    def tick(self):
        #override in subclasses
        pass


class ShopPlant:

    def __init__(self, rect: pg.Rect, cost:int, filename: str) -> None:
        self.pos = rect.topleft
        self.img = pg.image.load(filename)
        self.img.convert()
        self.img = pg.transform.scale(self.img,(rect.width,rect.height))

        self.cost = cost

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.img, self.pos)

    def getCost(self):
        return self.cost




    