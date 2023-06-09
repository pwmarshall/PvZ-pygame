import pygame as pg

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
    

class Projectile:
    all = []

    def __init__(self, rect: pg.Rect, vel: tuple, filename: str) -> None:
        self.rect = rect
        self.vel = vel
        self.img = pg.image.load(filename)
        self.img.convert()
        self.img = pg.transform.scale(self.img,(self.rect.width, self.rect.height))
        Projectile.all.append(self)
        self.clickable = False

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

    def move(self):
        self.rect = self.rect.move(self.vel)
    
    def drawAll(surface):
        for proj in Projectile.all:
            proj.draw(surface)
            proj.move()

    def checkClickAll(pos):     #check but also action
        for proj in Projectile.all:
            if proj.clickable:
                if proj.checkClick(pos):
                    proj.clicked()
            
