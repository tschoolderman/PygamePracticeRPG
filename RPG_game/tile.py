import pygame as pg

from config import HITBOX_OFFSET, TILESIZE


class Tile(pg.sprite.Sprite):
    def __init__(
        self, pos, groups, sprite_type, surface=pg.Surface((TILESIZE, TILESIZE))
    ) -> None:
        super().__init__(groups)
        # Load a sprite image from file
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == "object":
            # do an offset
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        # Create a smaller hitbox than the image
        # Same width as image, but shorter top and bottom
        self.hitbox = self.rect.inflate(0, y_offset)
