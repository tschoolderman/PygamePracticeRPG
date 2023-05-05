import pygame as pg

from config import *


class UI:
    def __init__(self) -> None:
        # general
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10, 48, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # convert stat to pixel
        ratio = current / max_amount  # 100/100 = 1 // 50/100 = 0.5
        current_width = bg_rect.width * ratio  # 400*1 or 0.5
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pg.draw.rect(self.display_surface, color, current_rect)

        # draw border around the bar. The 3 makes it a line, emptying the fill of the rect
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        # convert int to int to prevent decimals from showing and then convert to str
        text_surface = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright=(x, y))

        pg.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surface, text_rect)
        pg.draw.rect(
            self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )

    def selection_box(self, left, top):
        bg_rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def display(self, player):
        self.show_bar(
            player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR
        )
        self.show_bar(
            player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR
        )

        self.show_exp(player.exp)

        self.selection_box(20, 1080)  # weapon
        self.selection_box(90, 1110)  # magic
