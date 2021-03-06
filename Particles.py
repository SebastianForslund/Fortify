import random
import GlobalValues
import math
import pygame
import os


# Class used for containing time-dependant particles. Has a draw method to draw all particles in the list.
# Pass in the deletion condition for a particle in the init.
class ParticleList:

    def __init__(self, delete_condition_lambda):
        self.list = []
        self.delete_condition = delete_condition_lambda

    def append(self, particle):
        self.list.append(particle)

    def tick(self):
        for particle in self.list:
            particle.tick()
            if self.delete_condition(particle.time):
                self.list.remove(particle)
                del particle

    def draw(self, WIN):
        for particle in self.list:
            particle.draw(WIN)

    def __len__(self):
        return len(self.list)


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

    def draw(self, WIN):
        pygame.draw.circle(WIN, self.color, (self.pos_x, self.pos_y), self.size, int((101 - self.time) / 0.8))


class PlayerShot:
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

    def tick(self):
        self.posY += math.sin(math.radians(self.angle)) * self.speed
        self.posX += math.cos(math.radians(self.angle)) * self.speed
        self.hitbox.y = self.posY
        self.hitbox.x = self.posX
        return 0 <= self.hitbox.x <= GlobalValues.WIDTH and 0 <= self.hitbox.y <= GlobalValues.HEIGHT

    def randomize_angle(self):
        self.angle = random.random() * 360
        self.current_image = pygame.transform.rotozoom(self.__PLAYER_SHOT_IMAGE, -self.angle, 1)

    def draw(self, WIN):
        WIN.blit(self.current_image, self.hitbox)


class PlayerThrusterParticle:

    def __init__(self, posX, posY, timer, angle, player_speed, color):
        self.color = color
        self.posX = posX - math.cos(math.radians(angle)) * 35
        self.posY = posY - math.sin(math.radians(angle)) * 35
        self.time = timer + random.randint(-7, 7)
        self.angle = angle + random.randint(-40, 40)
        self.player_speed = player_speed

    def tick(self):
        self.posX -= math.cos(math.radians(self.angle)) * 2 * (self.player_speed * 0.25)
        self.posY -= math.sin(math.radians(self.angle)) * 2 * (self.player_speed * 0.25)
        self.time -= 0.1

    def draw(self, WIN):
        rect = pygame.Rect(self.posX, self.posY, self.time, self.time)
        pygame.draw.rect(WIN, self.color, rect)


class CoreExplosionSmoke:
    def __init__(self):
        self.color = GlobalValues.BLUE_1
        self.angle = random.randint(0, 360)
        self.size = random.randint(10, 30)
        self.speed = 2
        self.posX = random.randint(960 - 100, 960 + 100)
        self.posY = random.randint(540 - 100, 540 + 100)
        self.time = 0

    def tick(self):
        self.forward()
        self.time += 1

    def draw(self, WIN):
        pygame.draw.circle(WIN, self.color, (self.posX, self.posY), self.size + self.time)

    def forward(self):
        self.posX += self.speed * math.cos(math.radians(self.angle))
        self.posY += self.speed * math.sin(math.radians(self.angle))


class BasicEnemyParticle:

    def __init__(self, posX, posY, timer):
        self.posX = posY  # Don't ask me why switching these makes it work
        self.posY = posX
        self.speed = 1 + random.uniform(-0.5, 2)
        self.angle = random.randint(0, 360)
        self.time = timer + random.randint(3, 7)
        self.color = GlobalValues.BLUE_1

    def tick(self):
        self.posX += self.speed * math.cos(math.radians(self.angle))
        self.posY += self.speed * math.sin(math.radians(self.angle))
        self.time -= 1
        self.color = random.choice([GlobalValues.BLUE_0, GlobalValues.BLUE_1, GlobalValues.BLUE_2, GlobalValues.RED_0])

    def draw(self, WIN):
        rect = pygame.Rect(self.posX, self.posY, self.time / 6, self.time / 6)
        pygame.draw.rect(WIN, self.color, rect)


#   TODO: class CoreCollisionParticle:

class CoreExplosionParticle:
    def __init__(self):
        self.color = random.choice((GlobalValues.RED_1, GlobalValues.RED_0, GlobalValues.BLUE_2))
        self.angle = random.randint(0, 360)
        self.size = 10
        self.speed = 2
        self.posX = random.randint(960 - 100, 960 + 100)
        self.posY = random.randint(540 - 100, 540 + 100)
        self.time = 0

    def tick(self):
        self.forward()
        self.time += 1

    def draw(self, WIN):
        rect = pygame.Rect(self.posX, self.posY, self.size, self.size)
        pygame.draw.rect(WIN, self.color, rect)

    def forward(self):
        self.posX += self.speed * math.cos(math.radians(self.angle))
        self.posY += self.speed * math.sin(math.radians(self.angle))
