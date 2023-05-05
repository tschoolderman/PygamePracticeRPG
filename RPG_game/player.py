import pygame as pg

from config import *
from support import import_folder


class Player(pg.sprite.Sprite):
    def __init__(
        self, pos, groups, obstacle_sprites, create_attack, destroy_attack
    ) -> None:
        super().__init__(groups)
        # Load a sprite image from file
        self.image = pg.image.load("../graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pg.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # weapon
        # get the create attack from the Level class
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # stats
        self.stats = {
            "health": 100,
            "energy": 60,
            "attack": 10,
            "magic": 4,
            "speed": 5,
        }
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 123
        self.speed = self.stats["speed"]

    def import_player_assets(self):
        character_path = "../graphics/player/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_attack": [],
            "left_attack": [],
            "up_attack": [],
            "down_attack": [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """Get keyboard input"""
        if not self.attacking:
            keys = pg.key.get_pressed()

            # movement input
            if keys[pg.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pg.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pg.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # attack input
            if keys[pg.K_SPACE]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                self.create_attack()

            # magic input
            if keys[pg.K_LCTRL]:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                print("magic")

            # change weapon
            if keys[pg.K_z] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pg.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status and "attack" not in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def move(self, speed):
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

    def cooldowns(self):
        current_time = pg.time.get_ticks()
        if self.attacking:
            if (current_time - self.attack_time) >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if (
                current_time - self.weapon_switch_time
            ) >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self) -> None:
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
