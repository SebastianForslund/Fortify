import math
import pygame
import os
import random

class BasicEnemyParticle:
    def __init__(self, posX, posY, timer):
        self.posX = posX
        self.posY = posY
        self.speedX = random.uniform(-1, 1) * 3
        self.speedY = random.uniform(-1, 1) * 3
        self.timer = timer + random.randint(3, 7)

class BasicEnemy():

    __default_image = pygame.image.load(os.path.join('Assets', 'basicEnemy.png'))

    def __init__(self, posX, posY, target, damage, speed, health):
        self.default_health = health
        self.health = health
        self.speed = speed
        self.current_hitbox = pygame.Rect((posX, posY), (64, 64))
        self.posX = posY #dont ask why this works
        self.posY = posX #dont ask why this works
        self.experience = 10
        targetX = target[0]
        targetY = target[1]
        rad = math.atan2(targetX - posX, targetY - posY)
        self.rad = rad
        self.current_image = self.__default_image
        self.core_damage = damage

        self.health_bar_background_rect = pygame.Rect(self.posY, self.posX + 70, 64, 10)
        self.health_bar_rect = pygame.Rect(self.posY, self.posX + 70, 64, 10)
        #draw healthbar

    def forward(self):
        self.posY += math.sin(self.rad) * self.speed
        self.posX += math.cos(self.rad) * self.speed
        self.current_hitbox.x = self.posY
        self.current_hitbox.y = self.posX
        self.health_bar_rect = pygame.Rect(self.posY, self.posX + 70, int(self.health / self.default_health * 64), 10)
        self.health_bar_background_rect = pygame.Rect(self.posY, self.posX + 70, 64, 10)

    def draw_health_bar(self, WIN):
        pygame.draw.rect(WIN, (35, 73, 93), self.health_bar_background_rect)
        pygame.draw.rect(WIN, (155, 34, 43), self.health_bar_rect)

    def damage(self, damage_amount):
        self.health -= damage_amount

