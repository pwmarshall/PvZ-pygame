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
    font = pg.font.Font(None, 64)
    text = font.render("Hello World", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()

    temp = Grass()
    temp.draw(background)
    temp2 = SunBalance((75, 100))
    # temp2.draw(background)

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
                if temp.clickedGrass(pos):
                    print(temp.getTile(pos))
                    temp2.updateSun(temp2.getSun()+25)
                    temp2.draw(frame)

        # Draw Everything
        screen.blit(background, (0, 0)) #cover everthing from last frame with background
        screen.blit(frame, (0,0))


        pg.display.flip()

    pg.quit()



class GrassTile:
    def __init__(self, rect: pg.Rect) -> None:
        self.rect = rect



class Grass:
    def __init__(self) -> None:
        self.matrix = []        # [y][x] matrix of grass tiles from top left out
        self.rows = 5           # y
        self.columns = 9        # x

        self.width = 1100
        self.height = 756 #divisable by columns for ease

        self.offset = (50, 100)

        self.rect = pg.Rect(self.offset, (self.width, self.height))
        
        self.xStep = self.width//self.columns
        self.yStep = self.height//self.rows
        for y in range(self.rows):
            row = []
            for x in range(self.columns):
                pos = (self.offset[0] + x * self.xStep, self.offset[1] + y * self.yStep)
                row.append(GrassTile(pg.Rect(pos, (self.xStep, self.yStep))))

            self.matrix.append(row)

        # print(self.matrix)

    def draw(self, surface: pg.Surface) -> None:
        # temp = pg.surface.Surface((1200, 900))
        for y in range(self.rows):
            for x in range(self.columns):
                pg.draw.rect(surface, "Green", self.matrix[y][x].rect, 10)


    def clickedGrass(self, pos: tuple):
        return self.rect.collidepoint(pos)
    
    def getTile(self, pos: tuple):
        x = (pos[0] - self.offset[0]) // self.xStep
        y = (pos[1] - self.offset[1]) // self.yStep
        return (x, y)


class PlantShop:

    def __init__(self) -> None:
        self.plants = 6          # 6 seeds plus spot for balance and shovel 

        self.arr = []        #SeedPacks

        self.width = 750
        self.height = 100 

        self.offset = (15, 0)

        self.rect = pg.Rect(self.offset, (self.width, self.height))



class SunBalance:
    
    def __init__(self, pos: tuple, sun: int = 0) -> None:
        self.font = pg.font.Font(None, 64)
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


class SeedPacks:

    def __init__(self) -> None:
        pass





if __name__ == "__main__":
    main()