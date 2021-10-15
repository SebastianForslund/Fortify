import math
import pygame
import random
import GlobalValues
from pygame import font
from GameFlowHandler import RoundHandler
from Player import Player
from BasicEnemy import BasicEnemy, BasicEnemyParticle
from Shockwave import Shockwave, ShockwaveList
from Store import Store
from Structures import Core

WIN = pygame.display.set_mode((GlobalValues.WIDTH, GlobalValues.HEIGHT))
pygame.display.set_caption("Fortify")

DOT_SIDE = 64
starting_core_health = 100
CENTER = (960, 540)

background = pygame.image.load("Assets/background_1080.png").convert()
background_rect = pygame.Rect(0, 0, 1920, 1080)

empty_store = pygame.image.load("Assets/EmptyStore.png").convert()
empty_store_rect = pygame.Rect(260, 160, 1440, 760)

#sound stuff
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
BasicEnemy_explosion_sound = pygame.mixer.Sound("SFX/BasicEnemyExplosion.wav")
#vroom = pygame.mixer.Sound("SFX/thruster.wav")

#font stuff
pygame.font.init()
font_36 = pygame.font.Font("Assets/manaspc.ttf", 36)
font_50 = pygame.font.Font("Assets/manaspc.ttf", 50)

def draw_window(player, core, enemy_list, particle_list, core_particle_list = None, shockwave_list = None):

    WIN.blit(background, background_rect)
    WIN.blit(player.current_image, player.current_hitbox)
    WIN.blit(core.current_image, core.current_hitbox)
    WIN.blit(core.current_health_text, core.current_health_rect)

    if core_particle_list != None:
        __draw_core_death_particles(core_particle_list)

    if shockwave_list != None:
        shockwave_list.draw_shockwaves(WIN)
        shockwave_list.tick_all()


    __draw_experience(player)
    __draw_enemies(enemy_list)
    __draw_player_booster_particles(player.particles_booster_array)
    __draw_death_particles(particle_list)
    __player_shot_drawer(player.projectiles_array)
    pygame.display.update()


def __draw_experience(player):
    p = float(player.experience / player.levelup_threshold) + 0.001
    pipi = int(p * 1920)
    pygame.draw.rect(WIN, GlobalValues.BLUE_0, pygame.Rect(0, 0, pipi, 16))
    WIN.blit(player.current_level_text, player.current_level_text_rect)


def __draw_enemies(enemies):
    for enemy in enemies:
        WIN.blit(enemy.current_image, enemy.current_hitbox)
        enemy.draw_health_bar(WIN)


def __player_shot_drawer(projectiles):
    for projectile in projectiles:
        if 0 <= projectile.hitbox.x <= GlobalValues.WIDTH and 0 <= projectile.hitbox.y <= GlobalValues.HEIGHT:
            WIN.blit(projectile.current_image, projectile.hitbox)
        else:
            projectiles.remove(projectile)  #removes projectiles outside of the window
            del projectile


def movement_check_enemies(enemies_list, core, player, particle_list):
    for enemy in enemies_list:
        enemy.forward()
        enemy.draw_health_bar(WIN)
        if enemy.current_hitbox.colliderect(core.current_hitbox):
            core.damage(enemy.core_damage)
            enemies_list.remove(enemy)
        if enemy.current_hitbox.colliderect(player.current_hitbox):
            if player.crash_damage > enemy.health:
                enemy_death(player, enemy, None, particle_list, enemies_list)
            else:
                enemy.damage(player.crash_damage)


def movement_check_player(player, rotation):
    if player.movement_forward:
        #TODO: thruster movement sound
        player.forward()
    if player.movement_reverse:
        player.reverse()
    player.rotate(rotation)


def __draw_player_booster_particles(player_booster_particles):
    for particle in player_booster_particles:
        particle.posX -= math.cos(math.radians(particle.angle)) * 2 * (particle.player_speed * 0.25)
        particle.posY -= math.sin(math.radians(particle.angle)) * 2 * (particle.player_speed * 0.25)
        particle.timer -= 0.1
        rect = pygame.Rect(particle.posX, particle.posY, particle.timer, particle.timer)
        pygame.draw.rect(WIN, particle.color, rect)
        if particle.timer <= 0:
            player_booster_particles.remove(particle)
            del particle


def __draw_core_death_particles(particle_list):
    for particle in particle_list:
        particle.timer -= 0.2
        particle.posX -= math.cos(math.radians(particle.angle))*particle.speed
        particle.posY -= math.sin(math.radians(particle.angle))*particle.speed
        rect = pygame.Rect(particle.posY, particle.posX, particle.timer, particle.timer)
        pygame.draw.rect(WIN, particle.color, rect)
        if particle.timer <= 0:
            particle_list.remove(particle)
            del particle


def __draw_death_particles(particle_list):
    for particle in particle_list:
        particle.posX += particle.speedX
        particle.posY += particle.speedY
        particle.timer -= 0.1
        color = random.choice([GlobalValues.BLUE_0, GlobalValues.BLUE_1, GlobalValues.BLUE_2, GlobalValues.RED_0])
        rect = pygame.Rect(particle.posY, particle.posX, particle.timer, particle.timer)
        pygame.draw.rect(WIN, color, rect)
        if particle.timer <= 0:
            particle_list.remove(particle)
            del particle


def movement_check_projectiles(player, enemies_list, particle_list):
    for projectile in player.projectiles_array:
        projectile.forward()
        for enemy in enemies_list:
            if projectile.hitbox.colliderect(enemy.current_hitbox):
                if player.projectile_damage >= enemy.health:
                    enemy_death(player, enemy, projectile, particle_list, enemies_list)
                else:
                    enemy.damage(player.projectile_damage)
                if projectile in player.projectiles_array:
                    player.projectiles_array.remove(projectile)


def enemy_death(player, enemy, projectile, particle_list, enemies_list):
    BasicEnemy_explosion_sound.play()
    player.grant_experience(80)
    if projectile is not None:
        if projectile in player.projectiles_array:
            player.projectiles_array.remove(projectile)

    for particle_number in range(25):
        particle_list.append(BasicEnemyParticle(enemy.posX, enemy.posY, 4))

    for i in range(player.modifier_on_death_shots):
        player.spawn_random_shot(enemy.posX, enemy.posY)
    if enemy in enemies_list:
        enemies_list.remove(enemy)


def main():
    player = Player(pygame.Rect(200, 200, DOT_SIDE, DOT_SIDE), 0)
    current_enemies_list = []
    current_particle_list = []

    store = Store()
    store.generate_store_supply()

    is_shooting = False

    core = Core(starting_core_health)
    difficulty = 10
    game_flow = RoundHandler(difficulty, core)

    clock = pygame.time.Clock()

    intro = True
    current_blue = GlobalValues.BLUE_0

    while intro:
        intro_background = pygame.image.load("Assets/StartMenu.png")
        intro_text = font_50.render("Press 'Q' to Start the game", True, current_blue)
        if current_blue[0] > 15:
            current_blue = (current_blue[0]-15, current_blue[1], current_blue[2])
        else:
            current_blue = GlobalValues.BLUE_0

        WIN.blit(intro_background, pygame.Rect(0, 0, 1920, 1080))
        WIN.blit(intro_text, pygame.Rect(565, 700, 100, 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    intro = False
        pygame.time.wait(50)
    run = True
    player_movement_rotation = 0
    while run:
        clock.tick(GlobalValues.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.movement_forward = True
                if event.key == pygame.K_s:
                    player.movement_reverse = True
                if event.key == pygame.K_d:
                    player_movement_rotation += player.rotate_speed
                if event.key == pygame.K_a:
                    player_movement_rotation += -player.rotate_speed
                if event.key == pygame.K_SPACE:
                    is_shooting = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_b:
                    if player.skill_points > 0:
                        store.generate_store_supply()
                        open_buy_menu(WIN, store, player)
                    else:
                        open_empty_buy_menu(WIN)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.movement_forward = False
                if event.key == pygame.K_d:
                    player_movement_rotation += -player.rotate_speed
                if event.key == pygame.K_a:
                    player_movement_rotation += player.rotate_speed
                if event.key == pygame.K_s:
                    player.movement_reverse = False
                if event.key == pygame.K_SPACE:
                    is_shooting = False
                if event.key == pygame.K_f:
                    current_enemies_list.append(BasicEnemy(player.posX, player.posY, CENTER, 25, 1, 1))

        player.tick()
        if is_shooting:
            player.shoot()

        if game_flow.tick():
            current_enemies_list = game_flow.enemies_list

        draw_window(player, core, current_enemies_list, current_particle_list)
        movement_check_player(player, player_movement_rotation)
        movement_check_enemies(current_enemies_list, core, player, current_particle_list)
        movement_check_projectiles(player, current_enemies_list, current_particle_list)
        if core.current_health <= 0:
            core_death(player, core, current_enemies_list, current_particle_list, clock)
            run = False
            dead = True
    pygame.quit()


def open_buy_menu(WIN, store, player):
    clock = pygame.time.Clock()
    while True:
        clock.tick(GlobalValues.FPS)
        store.draw(WIN, store.selected)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                player.skill_points -= 1
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                if store.selected < 2:
                    store.selected += 1
                else:
                    store.selected = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if store.selected > 0:
                    store.selected -= 1
                else:
                    store.selected = 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                store.current_supply[store.selected].store_item.apply(player)
                player.skill_points -= 1
                return


def open_empty_buy_menu(WIN):
    clock = pygame.time.Clock()
    while True:
        clock.tick(GlobalValues.FPS)
        WIN.blit(empty_store, empty_store_rect)
        txt = font_36.render("The store currently has no items, check back later!", True, GlobalValues.RED_0)
        txt_rect = txt.get_rect()
        txt_rect.x = 360
        txt_rect.y = 500
        WIN.blit(txt, txt_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return


def core_death(player, core, current_enemies_list, current_particle_list, clock):

    counter = 0
    core_death_particles = []
    shockwave_list = ShockwaveList()
    while counter < GlobalValues.FPS*5:     #5 second end screen
        clock.tick(GlobalValues.FPS)
        for i in range(2):
            new_particle = CoreExplosionParticle(core.current_hitbox.x, core.current_hitbox.y,
                                                 15, 0, GlobalValues.RED_0)
            core_death_particles.append(new_particle)

        if random.randint(1, 35) == 30:
            new_shockwave = Shockwave(960 + random.randint(0, 125), 540 + random.randint(0, 125))
            shockwave_list.add_shockwave(new_shockwave)

        draw_window(player, core, current_enemies_list, current_particle_list, core_death_particles, shockwave_list)
        counter += 1
    pygame.quit()


class CoreExplosionParticle:

    def __init__(self, posX, posY, timer, angle, color):
        self.speed = 4
        self.color = color
        self.posX = posY + random.randint(0, 128)
        self.posY = posX + random.randint(0, 128)
        self.timer = timer + random.randint(-5, 5)
        self.angle = angle + random.randint(0, 360)
        self.color = random.choice([GlobalValues.BLUE_0, GlobalValues.BLUE_1,
                                    GlobalValues.BLUE_2, GlobalValues.RED_0])



if __name__ == "__main__":
    main()
