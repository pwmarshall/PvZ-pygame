
from basePlants import *

class Peashooter(Plant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, "temp-files\\peashooter.webp")

        # test = pg.image.load("temp-files\\peashooter.webp")
        # test.convert()

class Sunflower(Plant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, "temp-files\\sunflower.webp")

class ShopPeashooter(ShopPlant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, 100, "temp-files\\peashooter.webp")
        self.plant = Peashooter

class ShopSunflower(ShopPlant):

    def __init__(self, rect: pg.Rect) -> None:
        super().__init__(rect, 50, "temp-files\\sunflower.webp")
        self.plant = Sunflower


        

