import pygame as pg

class Zombies:

    all = []

    def __init__(self, rect: pg.Rect, vel: tuple, filename: str, health: int = 200) -> None:
        self.rect = rect
        self.vel = vel
        self.img = pg.image.load(filename)
        self.img.convert()
        self.img = pg.transform.scale(self.img,(self.rect.width, self.rect.height))
        Zombies.all.append(self)
        self.health = health

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

    def move(self):
        self.rect = self.rect.move(self.vel)
    
    def drawAll(surface):
        for zombie in Zombies.all:
            zombie.draw(surface)
            zombie.move()




class Zombie(Zombies):

    def __init__(self, rect: pg.Rect) -> None:
        filename = "temp-files\\zombie.webp"
        vel = (-1,0)
        super().__init__(rect, vel, filename)