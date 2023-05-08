from math import sin

import pygame as pg


class Entity(pg.sprite.Sprite):
    """An entity class from which the player and enemies enherit."""

    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pg.math.Vector2()

    def move(self, speed):
        """A method for movement input."""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Creating a class for collisions with static tiles"""
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # moving to the right
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    # moving to the left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # moving down
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # moving up
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
