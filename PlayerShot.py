
import os
import pygame
import math
import random


class PlayerShot():

    __PLAYER_SHOT_IMAGE = pygame.image.load(os.path.join('Assets', 'Player_Projectile.png'))

    current_image = __PLAYER_SHOT_IMAGE
    angle = 0
    speed = 1
    size = 0
    __default_length = 25
    __default_width = 10

    def __init__(self, source_player):
        self.speed = source_player.projectile_speed
        self.angle = source_player.angle % 360 + random.randint(-5, 5)
        self.hitbox = pygame.Rect(source_player.posX - self.__default_width / 2,
                                  source_player.posY - self.__default_length / 2,
                                  self.__default_width,
                                  self.__default_length)
        self.current_image = pygame.transform.rotozoom(self.__PLAYER_SHOT_IMAGE, -self.angle, 1)
        self.posX = self.hitbox.x
        self.posY = self.hitbox.y

    def forward(self):
        self.posY += math.sin(math.radians(self.angle)) * self.speed
        self.posX += math.cos(math.radians(self.angle)) * self.speed
        self.hitbox.y = self.posY
        self.hitbox.x = self.posX

    def randomize_angle(self):
        self.angle = random.random() * 360
        print(self.angle)
        self.current_image = pygame.transform.rotozoom(self.__PLAYER_SHOT_IMAGE, -self.angle, 1)


