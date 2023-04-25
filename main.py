import pygame as pg
import numpy
import random
# from level import Grass, PlantShop
from baseClasses import *
from basePlants import *
from plants import *
from constants import *



def main():
    pg.init()
    screen = pg.display.set_mode((1200, 900)) #, pg.SCALED
    pg.display.set_caption("Plants vs Zombies")
    # pg.mouse.set_visible(False)

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill("Blue")

    field = Grass()
    field.draw(background)
    shop = PlantShop()
    shop.draw(background)


    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
    sun = SunBalance(shop.sunRect.center)
    # test = Sun((500,0), 500)
    skySun = Sky()

    # peashooter = Peashooter((100,100))


    # Main Loop
    going = True
    # bought = False
    plant = None
    while going:
        clock.tick(FRAME_RATE)
        frame = pg.Surface(screen.get_size())
        frame = frame.convert()

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                Projectile.checkClickAll(pos)
                if field.checkClick(pos) and plant:
                    print(f"Field: {field.getTile(pos)}")
                    tile = field.getTile(pos)
                    good = field.place(tile, plant)
                    if good:
                        plant = None

                elif shop.checkClickSeeds(pos) and not plant:
                    print(f"Shop: {shop.getTile(pos)}")
                    tile = shop.getTile(pos)
                    plant = shop.buy(tile, sun)
                    if plant == -1:
                        plant = None
                    elif not plant:
                        sun.blink()


                elif shop.checkClickShovel(pos):
                    print(shop.getTile(pos))

                elif shop.checkClickSun(pos):
                    # usually do nothing
                    sun.updateSun(200)
            
            elif event.type == SUN_CLICKED:
                # print("custom")
                sun.addSun(event.sun)
                    

        # Draw Everything
        screen.blit(background, (0, 0)) #cover everthing from last frame with background
        # temp3.drawChanging(screen)
        sun.draw(screen)
        Plant.drawAll(screen)
        Projectile.drawAll(screen)
        skySun.tick()
        # test.draw(screen)
        # test.move()
        # peashooter.draw(screen)
        # screen.blit(frame, (0,0))


        pg.display.flip()

    pg.quit()


class GrassTile(BackgroundObject):
    def __init__(self, rect: pg.Rect, plant: Plant = None) -> None:
        super().__init__(rect)
        self.plant = plant
        if self.plant:
            self.initPlant()

    def initPlant(self):
        self.plant = self.plant(self.rect)



class Grass(BackgroundContainer):
    def __init__(self) -> None:
        pos = (50, 100)
        super().__init__(pg.Rect(pos, (1100, 756)), (9,5), GrassTile)

    def place(self, tile, plant: Plant) -> bool:
        grassTile = self.matrix[tile[1]][tile[0]]
        if not grassTile.plant:
            grassTile.plant = plant
            grassTile.initPlant()
            return True
        else:
            return False





class SunBalance:
    
    def __init__(self, pos: tuple, sun: int = 0) -> None:
        self.size = 32
        self.font = pg.font.Font(None, self.size)
        self.pos = pos          #center of text
        self.sun = 50
        self.color = "Black"

    def draw(self, surface: pg.Surface) -> None:
        text = self.font.render(str(self.sun), True, self.color)
        textpos = text.get_rect(center = self.pos)

        surface.blit(text, textpos)

    def updateSun(self, sun: int) -> None:
        self.sun = sun

    def getSun(self) -> int:
        return self.sun
    
    def addSun(self, amount: int) -> None:
        self.sun += amount
    
    def blink(self):
        print("blink")
        self.color = "Red"
        


class PlantShop:

    def __init__(self) -> None:

        self.rect = pg.Rect((20,0), (750, 100))

        sunImageSquare = 100
        shovelSquare = 80

        shovelPos = (self.rect.right-shovelSquare, self.rect.top)
        self.shovel = Shovel(pg.Rect(shovelPos, (shovelSquare, shovelSquare)))

        seedsPos = (self.rect.left + sunImageSquare, self.rect.top)
        self.seeds = SeedPacks(pg.Rect(seedsPos, (self.rect.width - sunImageSquare - shovelSquare, self.rect.height)))

        self.sunRect = pg.Rect(self.rect.topleft, (sunImageSquare, sunImageSquare))

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "Yellow", self.sunRect)
        self.seeds.draw(surface)
        self.shovel.draw(surface)

    def checkClickSeeds(self, pos: tuple) -> bool:
        return self.seeds.checkClick(pos)
    
    def checkClickShovel(self, pos: tuple) -> bool:
        return self.shovel.rect.collidepoint(pos)
    
    def checkClickSun(self, pos: tuple) -> bool:
        return self.sunRect.collidepoint(pos)
    
    def getTile(self, pos: tuple) -> int:
        if self.shovel.rect.collidepoint(pos):
            # print("Shovel")
            return "Shovel"
        elif self.seeds.checkClick(pos):
            # print("Seeds")
            # self.seeds.getTile(pos)
            return self.seeds.getTile(pos)
        elif self.sunRect.collidepoint(pos):
            return "Sun"
        
    def buy(self, tile: tuple, sun: SunBalance):
        currentSun = sun.getSun()
        cost = self.seeds.matrix[tile[1]][tile[0]].getCost()
        if cost == -1:
            print("No plant")
            return -1
        elif cost <= currentSun:
            sun.updateSun(currentSun- cost)
            return self.seeds.matrix[tile[1]][tile[0]].plant.plant
        else:
            return None

    

class Shovel(BackgroundObject):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect)


class SeedPacks(BackgroundContainer):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, (6, 1), SeedPack)
        # self.matrix[0][0].plant = Peashooter
        self.addPlant(ShopPeashooter)
        self.addPlant(ShopSunflower)

    def addPlant(self, plant: ShopPlant):
        for slot in self.matrix[0]:
            if not slot.plant:
                slot.plant = plant
                slot.initPlant()
                break


class SeedPack(BackgroundObject):

    def __init__(self, rect: pg.Rect, plant: ShopPlant = None) -> None:
        super().__init__(rect)
        self.cost = -1
        self.plant = plant
        if self.plant:
            self.initPlant()

    def getCost(self) -> int:
        return self.cost
    
    def draw(self, surface: pg.Surface):
        if self.plant:
            self.plant.draw(surface)
        else:
            BackgroundObject.draw(self, surface)

    def initPlant(self):
        self.plant = self.plant(self.rect)
        self.cost = self.plant.getCost()


class Sky:

    def __init__(self) -> None:
        self.cooldown = 10 #numpy.random.normal(10,1) #secs
        self.tickCount = 0
        self.spawnSun()

    def tick(self):
        self.tickCount += 1
        if self.tickCount % int(FRAME_RATE * self.cooldown) == 0:
            self.spawnSun()
            self.cooldown = numpy.random.normal(10,1)
            self.tickCount = 0

    def spawnSun(self):
        Sun((random.uniform(100, 1000), 0), random.uniform(300,800))


if __name__ == "__main__":
    main()
    # test()