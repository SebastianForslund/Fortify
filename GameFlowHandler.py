
import random


from BasicEnemy import BasicEnemy

pause_time = 5


class RoundHandler:

    def __init__(self, starting_difficulty, core): #TODO: Redo round system
        self.difficutly_increaser = 5
        self.round_number = 0
        self.difficulty_default = starting_difficulty
        self.difficulty_current = self.difficulty_default
        self.enemies_unspawned_left = int(self.difficulty_current / 5)
        self.enemies_list = []
        self.core = core
        self.round_cooldown_period = 3 #3 second rest period
        self.round_cooldown_counter = self.round_cooldown_period
        self.roundActive = False
        self.enemy_spawn_counter_default = 100
        self.enemy_spawn_counter_current = 100

    def __next_round(self):
        self.roundActive = True
        self.round_number += 1
        self.difficulty_current += self.difficutly_increaser
        self.difficulty_temp = self.difficulty_current
        self.enemies_unspawned_left = int(self.difficulty_current / 5)

    def __enemy_spawn_handler(self):
        if self.roundActive:
            self.enemy_spawn_counter_current -= 1
            if self.enemy_spawn_counter_current <= 0:
                self.enemy_spawn_counter_current = self.enemy_spawn_counter_default
                if self.enemies_unspawned_left > 0:
                    # spawns the enemy
                    health = 80 + 10 * self.round_number
                    speed = 1.5 * (random.random() + 0.7)
                    damage = self.difficulty_current / 2
                    target = (960, 540)
                    spawn_choices = self.__get_random_spawn()
                    posX = spawn_choices[0]
                    posY = spawn_choices[1]
                    self.enemies_list.append(BasicEnemy(posX, posY, target, damage, speed, health))
                    self.difficulty_temp -= 5
                    #self.enemy_spawn_counter_current = self.enemy_spawn_counter_default
                    self.enemies_unspawned_left -= 1



    def __get_random_spawn(self):
        side = random.getrandbits(2) #randomly selects one side of the game window
        if side == 0: #left side of the window
            x = -200
            y = random.randint(0, 1080)
            return (x, y)
        if side == 1: #bottom side of the window
            x = random.randint(0, 1920)
            y = 1280
            return (x, y)
        if side == 2: #right side of the window
            x = 2120
            y = random.randint(0, 1080)
            return (x, y)
        if side == 3: #top side of the window
            x = random.randint(0, 1920)
            y = -200
            return (x, y)


    def tick(self): #returns True if there's a enemies_list update
        self.__enemy_spawn_handler()
        if not self.enemies_list: #if list is empty
            self.round_cooldown_counter -= 1/144
            if self.round_cooldown_counter <= 0:
                self.__next_round() #updates enemies_list
                self.round_cooldown_counter = self.round_cooldown_period #resets cooldown counter for next round end
                return True
            return False
        return False
