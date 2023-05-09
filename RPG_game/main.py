import sys

import pygame as pg

from config import FPS, HEIGHT, WATER_COLOR, WIDTH
from level import Level


class Game:
    """The base class of the game"""

    def __init__(self) -> None:
        # general setup
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Loot or Die")
        self.clock = pg.time.Clock()

        self.level = Level()

        # sound
        main_sound = pg.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.6)
        main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pg.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
