from baseClasses import Projectile
from basePlants import *
from constants import *
from zombies import *

class Peashooter(Plant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, "temp-files\\peashooter.webp")
        # self.row = row
        self.tickCount = 0

    def tick(self):
        pass

    def checkZombie(self):
        pass


class Sunflower(Plant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, "temp-files\\sunflower.webp")
        self.tickCount = FRAME_RATE*20      #first sun only 4 seconds after place

    def tick(self):
        self.tickCount += 1

        if self.tickCount % (FRAME_RATE*24) == 0: #60 ticks a second, every 24 seconds
            self.spawnSun()

    def spawnSun(self):
        Sun(self.rect.topleft, self.rect.bottom)
        

class ShopPeashooter(ShopPlant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, 100, "temp-files\\peashooter.webp")
        self.plant = Peashooter

class ShopSunflower(ShopPlant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, 50, "temp-files\\sunflower.webp")
        self.plant = Sunflower


class Sun(Projectile):

    def __init__(self, pos: tuple, stop: int) -> None:
        rect = pg.Rect(pos, (50,50))
        vel = (0, 1)
        filename = "shitty-files\\Sun2.png"
        super().__init__(rect, vel, filename)
        self.stop = stop
        self.clickable = True

    def move(self):
        if self.rect.top >= self.stop:
            self.vel = (0,0)

        return super().move()
    
    def checkClick(self, pos) -> bool:
        return self.rect.collidepoint(pos)
    
    def clicked(self):
        pg.event.post(pg.event.Event(SUN_CLICKED, {"sun": 25}))
        Projectile.all.remove(self)

    

    


        

