import pygame as pg


def main():
    pg.init()
    screen = pg.display.set_mode((1200, 900)) #, pg.SCALED
    pg.display.set_caption("Plants vs Zombies")
    # pg.mouse.set_visible(False)

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill("Blue")

    # test = pg.image.load("refrance.jpg")
    # test.convert()
    # test = pg.transform.scale(test,(1200,900))
    # background.blit(test, (0,0))

    # Put Text On The Background, Centered
    # font = pg.font.Font(None, 64)
    # text = font.render("Hello World", True, (10, 10, 10))
    # textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    # background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()

    field = Grass()
    field.draw(background)
    shop = PlantShop()
    shop.draw(background)
    # seedpacks = SeedPacks(pg.Rect((120, 0), (550, 100)))
    # seedpacks.draw(background)
    # temp2 = SunBalance((75, 100))
    # temp3 = PlantShop()

    sun = SunBalance(shop.sunRect.center)


    # background.blit(temp2, (0,0))

    # Main Loop
    going = True
    while going:
        clock.tick(60)
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
                if field.checkClick(pos):
                    print(f"Field: {field.getTile(pos)}")
                    tile = shop.getTile(pos)
                    gain = field.place(tile)
                    sun.updateSun(sun.getSun() + gain)

                elif shop.checkClick(pos):
                    print(f"Shop: {shop.getTile(pos)}")
                    tile = shop.getTile(pos)
                    if shop.buy(tile, sun):
                        bought = True
                    else:
                        sun.blink()
                    

        # Draw Everything
        screen.blit(background, (0, 0)) #cover everthing from last frame with background
        # temp3.drawChanging(screen)
        sun.draw(screen)
        # screen.blit(frame, (0,0))


        pg.display.flip()

    pg.quit()


class BackgroundObject:

    def __init__(self, rect: pg.Rect) -> None:
        self.rect = rect

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "Green", self.rect, 10)


class BackgroundContainer:

    def __init__(self, rect: pg.Rect, size: tuple, object: BackgroundObject) -> None:
        self.rect = rect
        self.matrix = []
        self.size = size

        rows = size[1]      # y
        columns = size[0]   # x

        xStep = self.rect.width//columns
        yStep = self.rect.height//rows
        for y in range(rows):
            row = []
            for x in range(columns):
                pos = (self.rect.left + x * xStep, self.rect.top + y * yStep)
                row.append(object(pg.Rect(pos, (xStep, yStep))))

            self.matrix.append(row)


    def draw(self, surface: pg.Surface) -> None:
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.matrix[y][x].draw(surface)

    def checkClick(self, pos: tuple) -> bool:
        return self.rect.collidepoint(pos)
    
    def getTile(self, pos: tuple) -> tuple:
        xStep = self.rect.width//self.size[0]
        yStep = self.rect.height//self.size[1]
        x = (pos[0] - self.rect.left) // xStep
        y = (pos[1] - self.rect.top) // yStep
        return (x, y) 



class GrassTile(BackgroundObject):
    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect)



class Grass(BackgroundContainer):
    def __init__(self) -> None:
        pos = (50, 100)
        super().__init__(pg.Rect(pos, (1100, 756)), (9,5), GrassTile)

    def place(self, tile):
        return 100



class SunBalance:
    
    def __init__(self, pos: tuple, sun: int = 0) -> None:
        self.size = 32
        self.font = pg.font.Font(None, self.size)
        self.pos = pos          #center of text
        self.sun = 0

    def draw(self, surface: pg.Surface) -> None:
        text = self.font.render(str(self.sun), True, "Black")
        textpos = text.get_rect(center = self.pos)

        surface.blit(text, textpos)

    def updateSun(self, sun: int) -> None:
        self.sun = sun

    def getSun(self) -> int:
        return self.sun
    
    def blink(self):
        print("blink")


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

        # sunPos = (sunImageSquare//2 + self.offset[0], sunImageSquare-40)
        # self.sunBalance = SunBalance(sunPos)

    # def drawChanging(self, surface: pg.Surface) -> None:
    #     self.sunBalance.drawChanging(surface)

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, "Yellow", self.sunRect)
        self.seeds.draw(surface)
        self.shovel.draw(surface)

    # def updateSun(self, sun: int) -> None:
    #     self.sunBalance.updateSun(sun)

    # def getSun(self) -> int:
    #     return self.sunBalance.getSun()

    def checkClick(self, pos: tuple) -> bool:
        return self.rect.collidepoint(pos)
    
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
        if cost <= currentSun:
            sun.updateSun(currentSun- cost)
            return True
        else:
            return False

    

class Shovel(BackgroundObject):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect)


class SeedPacks(BackgroundContainer):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, (6, 1), SeedPack)


class SeedPack(BackgroundObject):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect)
        self.cost = 100

    def getCost(self) -> int:
        return self.cost




if __name__ == "__main__":
    main()