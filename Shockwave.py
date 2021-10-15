import random

import pygame.draw

import GlobalValues





class ShockwaveList:
    def __init__(self):
        self.list = []

    def add_shockwave(self, w):
        self.list.append(w)

    def tick_all(self):
        for s in self.list:
            s.tick()

    def draw_shockwaves(self, WIN):
        for s in self.list:
            pygame.draw.circle(WIN, s.color, (s.pos_x, s.pos_y), s.size, int((101-s.time)/0.8))
            print(int((101-s.time)/3))


