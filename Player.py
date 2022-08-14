import math
import os
import random
import GlobalValues
import pygame
from Particles import PlayerShot, PlayerThrusterParticle, ParticleList


class Player:
    movement_forward = False
    movement_rotating = False
    movement_reverse = False

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    levelup_sound = pygame.mixer.Sound("SFX/levelup.wav")

    def __init__(self, hitbox, angle):

        # TODO: Add extra variable to remember the default values of the values modified by cards.
        self.projectile_speed = 7
        self.shoot_sound = pygame.mixer.Sound("SFX/shot.wav")
        self.level = 0
        self.experience = 0
        self.levelup_threshold = 100
        self.__coefficient = self.experience / self.levelup_threshold
        self.experience_bar_rect = pygame.Rect(0, 0, self.__coefficient * 1920, 16)
        self.skill_points = 0
        self.projectile_damage = 50
        self.crash_damage = 1
        self.projectile_fire_rate = 0.5
        self.projectiles_array = []
        self.movement_value_forward_speed = 4
        self.movement_value_reverse_speed = 2
        self.rotate_speed = 2.25
        self.angle = angle
        self.__hitbox = hitbox
        self.__default_image = pygame.image.load(os.path.join('Assets', 'Player1.png'))
        self.current_hitbox = hitbox
        self.current_image = self.__default_image
        self.posX = hitbox.x
        self.posY = hitbox.y
        self.health_max = 100
        self.health_current = self.health_max
        self.particles_booster_array = ParticleList(lambda time: time <= 0)
        self.default_projectile_fire_rate = 0.5
        self.modifier_attack_speed = 1
        self.modifier_movement_speed = 1
        self.modifier_rotation_speed = 1
        self.modifier_max_health = 1
        self.modifier_shot_count = 1
        self.modifier_on_death_shots = 0
        self.modifier_invincible = False
        self.modifier_can_shoot = True

        self.fire_rate_counter = 0
        self.fire_rate_counter_default = int(GlobalValues.FPS * self.projectile_fire_rate)

        pygame.font.init()
        self.font = pygame.font.Font("Assets/manaspc.ttf", 28)
        self.current_level_text = self.font.render(("LEVEL:" + str(self.level)), True,
                                                   GlobalValues.BLUE_0, GlobalValues.BLUE_4)
        self.current_level_text_rect = self.current_level_text.get_rect()
        self.current_level_text_rect.center = (960, 36)

    def grant_experience(self, amount):
        if amount + self.experience >= self.levelup_threshold:
            self.levelup_sound.play()
        if amount + self.experience >= self.levelup_threshold:
            self.level += 1
            self.skill_points += 1
            value = amount + self.experience - self.levelup_threshold  # must be calculated before setting exp
            self.experience = 0
            self.grant_experience(value)
            self.levelup_threshold += 10
            self.current_level_text = self.font.render(("LEVEL:" + str(self.level)), True,
                                                       GlobalValues.BLUE_0, GlobalValues.BLUE_4)
            return True  # levelup
        else:
            self.experience += amount
            return False  # no level up

    def rotate(self, amount):
        self.current_image = pygame.transform.rotozoom(self.__default_image, -(amount + self.angle), 1)
        self.current_hitbox = self.current_image.get_rect(center=(self.posX, self.posY))
        self.angle = self.angle % 360
        self.angle += amount

    def forward(self):
        self.posY += math.sin(math.radians(self.angle)) * self.movement_value_forward_speed
        self.posX += math.cos(math.radians(self.angle)) * self.movement_value_forward_speed
        color = random.choice([(218, 242, 233), (149, 224, 204)])
        self.particles_booster_array.append(PlayerThrusterParticle(self.posX, self.posY,
                                                                   4,
                                                                   self.angle,
                                                                   self.movement_value_forward_speed,
                                                                   color))

    def reverse(self):
        self.posY -= math.sin(math.radians(self.angle)) * self.movement_value_reverse_speed
        self.posX -= math.cos(math.radians(self.angle)) * self.movement_value_reverse_speed

    def shoot(self):
        if self.modifier_can_shoot:
            if self.fire_rate_counter == 0:
                self.shoot_sound.play()
                for i in range(0, self.modifier_shot_count):
                    self.projectiles_array.append(PlayerShot(self))
                self.fire_rate_counter = int(self.projectile_fire_rate * GlobalValues.FPS)

    def tick(self):
        for projectile in self.projectiles_array:
            if not projectile.tick():
                del projectile

        self.particles_booster_array.tick()

        if self.fire_rate_counter > 0:
            self.fire_rate_counter -= 1

    def draw(self, WIN):
        WIN.blit(self.current_image, self.current_hitbox)
        for projectile in self.projectiles_array:
            projectile.draw(WIN)

        self.particles_booster_array.draw(WIN)

        percentage = float(self.experience / self.levelup_threshold) + 0.001
        width_pixels = int(percentage * 1920)
        pygame.draw.rect(WIN, GlobalValues.BLUE_0, pygame.Rect(0, 0, width_pixels, 16))
        WIN.blit(self.current_level_text, self.current_level_text_rect)

    def spawn_random_shot(self, posX, posY):  # ugly af
        shot = PlayerShot(self)
        shot.randomize_angle()
        shot.posX = posY
        shot.posY = posX
        self.projectiles_array.append(shot)
