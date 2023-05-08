import pygame as pg

from config import (
    BAR_HEIGHT,
    ENERGY_BAR_WIDTH,
    ENERGY_COLOR,
    HEALTH_BAR_WIDTH,
    HEALTH_COLOR,
    ITEM_BOX_SIZE,
    TEXT_COLOR,
    UI_BG_COLOR,
    UI_BORDER_COLOR,
    UI_BORDER_COLOR_ACTIVE,
    UI_FONT,
    UI_FONT_SIZE,
    magic_data,
    weapon_data,
)


class UI:
    """A class for displaying User Interface elements."""

    def __init__(self) -> None:
        # general
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10, 48, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary to list
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon["graphic"]
            weapon = pg.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert magic dictionary to list
        self.magic_graphics = []
        for magic in magic_data.values():
            path = magic["graphic"]
            magic = pg.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        """Create a generic function for displaying the health and energy bars."""
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
        """Define where the exp is shown on the display."""
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

    def selection_box(self, left, top, has_switched):
        """Create a background for the selection box."""
        bg_rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        """Create an overlay for the selection box of the weapon."""
        bg_rect = self.selection_box(20, 1080, has_switched)  # weapon
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        """Create an overlay for the selection box of magic."""
        bg_rect = self.selection_box(90, 1110, has_switched)  # magic
        magic_surface = self.magic_graphics[magic_index]
        magic_rect = magic_surface.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surface, magic_rect)

    def display(self, player):
        """Put all elements to the screen."""
        self.show_bar(
            player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR
        )
        self.show_bar(
            player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR
        )

        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
