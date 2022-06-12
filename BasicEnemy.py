import math
import pygame
import os

from Particles import BasicEnemyParticle

class BasicEnemy:
    __default_image = pygame.image.load(os.path.join('Assets', 'basicEnemy.png'))

    def __init__(self, posX, posY, target, damage, speed, health):
        self.default_health = health
        self.health = health
        self.speed = speed
        self.current_hitbox = pygame.Rect((posX, posY), (64, 64))
        self.posX = posY  # dont ask why this works
        self.posY = posX  # dont ask why this works
        self.experience = 10
        target_x = target[0]
        target_y = target[1]
        rad = math.atan2(target_x - posX, target_y - posY)
        self.rad = rad
        self.current_image = self.__default_image
        self.core_damage = damage

        self.health_bar_background_rect = pygame.Rect(self.posY, self.posX + 70, 64, 10)
        self.health_bar_rect = pygame.Rect(self.posY, self.posX + 70, 64, 10)
        # draw healthbar

    def forward(self):
        self.posY += math.sin(self.rad) * self.speed
        self.posX += math.cos(self.rad) * self.speed
        self.current_hitbox.x = self.posY
        self.current_hitbox.y = self.posX
        self.health_bar_rect = pygame.Rect(self.posY, self.posX + 70, int(self.health / self.default_health * 64), 10)
        self.health_bar_background_rect = pygame.Rect(self.posY, self.posX + 70, 64, 10)

    def __draw_health_bar(self, WIN):
        pygame.draw.rect(WIN, (35, 73, 93), self.health_bar_background_rect)
        pygame.draw.rect(WIN, (155, 34, 43), self.health_bar_rect)

    def damage(self, damage_amount):
        self.health -= damage_amount

    def draw(self, WIN):
        WIN.blit(self.current_image, self.current_hitbox)
        self.__draw_health_bar(WIN)

    def death(self, player, projectile, death_particle_list, enemies_list, death_sound):
        death_sound.play()
        player.grant_experience(80)
        if projectile is not None and projectile in player.projectiles_array:
            player.projectiles_array.remove(projectile)

        for particle_number in range(25):
            death_particle_list.append(BasicEnemyParticle(self.posX, self.posY, 100))

        for i in range(player.modifier_on_death_shots):
            player.spawn_random_shot(self.posX, self.posY)
        if self in enemies_list:
            enemies_list.remove(self)