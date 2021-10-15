import random

import pygame.draw

import GlobalValues


class Shockwave:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = 0
        self.time = 0
        self.size_increaser = random.randint(4, 10)
        self.color = random.choice((GlobalValues.RED_1, GlobalValues.RED_0, GlobalValues.BLUE_2, GlobalValues.BLUE_0))

    def tick(self):
        self.time += 2
        self.size += self.size_increaser

class ShockwaveList:
    def __init__(self):
        self.list = []

    def add_shockwave(self, w):
        self.list.append(w)

    def tick_all(self):
        for s in self.list:
            s.tick()
            if (s.time >= 100):
                self.list.remove(s)
                del(s)

    def draw_shockwaves(self, WIN):
        for s in self.list:
            pygame.draw.circle(WIN, s.color, (s.pos_x, s.pos_y), s.size, int((101-s.time)/0.8))
            print(int((101-s.time)/3))
