from random import choice

import pygame as pg

from config import *
from debug import debug
from player import Player
from support import import_csv_layout, import_folder
from tile import Tile


class Level:
    """Class for handling sprites"""

    def __init__(self) -> None:
        # get the display surface
        self.display_surface = pg.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layout = {
            "boundary": import_csv_layout("../maps/map_FloorBlocks.csv"),
            "grass": import_csv_layout("../maps/map_Grass.csv"),
            "object": import_csv_layout("../maps/map_Objects.csv"),
        }
        graphics = {
            "grass": import_folder("../graphics/grass"),
            "object": import_folder("../graphics/objects"),
        }
        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile(
                                (x, y),
                                self.obstacle_sprites,
                                "invisible",
                            )
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "grass",
                                random_grass_image,
                            )
                        if style == "object":
                            surface = graphics["object"][int(col)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surface,
                            )

        self.player = Player(
            (2000, 1430), [self.visible_sprites], self.obstacle_sprites
        )

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pg.sprite.Group):
    """Create a group to function of the camera on the y-axis"""

    def __init__(self) -> None:
        # general setup
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

        # creating the floor
        self.floor_surface = pg.image.load("../graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
