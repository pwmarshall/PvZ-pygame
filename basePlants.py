import pygame as pg
from enum import Enum

class PlantEnum(Enum):
    PEASHOOTER = 0
    SUNFLOWER = 1


class Plant:

    def __init__(self, rect: pg.Rect, filename: str) -> None:
        self.pos = rect.topleft
        self.img = pg.image.load(filename)
        self.img.convert()
        self.img = pg.transform.scale(self.img,(rect.width,rect.height))


    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.img, self.pos)

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


class Plants:

    def __init__(self) -> None:
        self.plants = []

    def addPlant(self, plant: Plant):
        self.plants.append(plant)

    def draw(self, surface: pg.Surface):
        for plant in self.plants:
            plant.draw(surface)



    