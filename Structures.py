import os
import pygame
import GlobalValues


class Core:

    def __init__(self, startingHealth):
        self.current_image = pygame.image.load(os.path.join('Assets', 'Core.png'))
        self.starting_health = startingHealth
        self.current_health = startingHealth
        self.current_hitbox = pygame.Rect(910, 490, 100, 100)
        pygame.font.init()
        self.font = pygame.font.Font("Assets/manaspc.ttf", 28)
        self.current_health_text = self.font.render((str(self.current_health) + "/" + str(self.starting_health)), True,
                                                    GlobalValues.BLUE_1, GlobalValues.BLUE_4) #doing this here is rly ugly
        self.current_health_rect = self.current_health_text.get_rect()
        self.current_health_rect.center = (975, 470)

    def damage(self, damage_amount):
        self.current_health -= damage_amount
        self.current_health_text = self.font.render((str(int(self.current_health)) + "/" + str(self.starting_health)), True,
                                                    GlobalValues.BLUE_1, GlobalValues.BLUE_4) #doing this here is rly ugly