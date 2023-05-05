import pygame as pg


class Weapon(pg.sprite.Sprite):
    """Create a class for managing weapons"""

    def __init__(self, player, groups) -> None:
        super().__init__(groups)
        # use the status in the Player class and split to only get up, down, left or right
        direction = player.status.split("_")[0]

        # graphic, create an image for weapon
        full_path = f"../graphics/weapons/{player.weapon}/{direction}.png"
        self.image = pg.image.load(full_path).convert_alpha()

        # placement, place image on center of player
        if direction == "right":
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pg.math.Vector2(0, 16)
            )
        elif direction == "left":
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pg.math.Vector2(0, 16)
            )
        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pg.math.Vector2(-10, 0)
            )
        else:
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pg.math.Vector2(-10, 0)
            )
