from random import randint

import pygame as pg

from config import TILESIZE


class MagicPlayer:
    def __init__(self, animation_player) -> None:
        self.animation_player = animation_player
        self.sounds = {
            "heal": pg.mixer.Sound("../audio/heal.wav"),
            "flame": pg.mixer.Sound("../audio/Fire.wav"),
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds["heal"].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            self.animation_player.create_particles("aura", player.rect.center, groups)
            self.animation_player.create_particles(
                "heal", player.rect.center + pg.math.Vector2(0, -60), groups
            )

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds["flame"].play()

            if player.status.split("_")[0] == "right":
                direction = pg.math.Vector2(1, 0)
            elif player.status.split("_")[0] == "left":
                direction = pg.math.Vector2(-1, 0)
            elif player.status.split("_")[0] == "up":
                direction = pg.math.Vector2(0, -1)
            elif player.status.split("_")[0] == "down":
                direction = pg.math.Vector2(0, 1)

            for i in range(1, 6):
                # horizontal flame movement
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = (
                        player.rect.centerx
                        + offset_x
                        + randint(-TILESIZE // 3, TILESIZE // 3)
                    )
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles("flame", (x, y), groups)
                # vertical flame movement
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = (
                        player.rect.centery
                        + offset_y
                        + randint(-TILESIZE // 3, TILESIZE // 3)
                    )
                    self.animation_player.create_particles("flame", (x, y), groups)
