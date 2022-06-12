import abc
import collections
import math
from abc import ABC

import pygame
import random
import GlobalValues
from GameFlowHandler import RoundHandler
from Particles import CoreExplosionSmoke, CoreExplosionParticle
from Player import Player
from BasicEnemy import BasicEnemy
from Particles import Shockwave, ParticleList, BasicEnemyParticle
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

# sound stuff
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
player_forward_sound = pygame.mixer.Sound("SFX/thruster3.wav")
BasicEnemy_explosion_sound = pygame.mixer.Sound("SFX/BasicEnemyExplosion.wav")
core_explosion_sound = pygame.mixer.Sound("SFX/CoreDeathSound.wav")
# vroom = pygame.mixer.Sound("SFX/thruster.wav")

# font stuff
pygame.font.init()
font_36 = pygame.font.Font("Assets/manaspc.ttf", 36)
font_50 = pygame.font.Font("Assets/manaspc.ttf", 50)


def draw_window(player, core, enemy_list, death_particle_list=None, core_death_particle_list=None, shockwave_list=None,
                core_death_smoke=None):
    WIN.blit(background, background_rect)
    player.draw(WIN)
    WIN.blit(core.current_image, core.current_hitbox)
    WIN.blit(core.current_health_text, core.current_health_rect)

    for enemy in enemy_list:
        enemy.draw(WIN)

    if death_particle_list is not None:
        death_particle_list.draw(WIN)

    if core_death_smoke is not None:
        core_death_smoke.draw(WIN)

    if core_death_particle_list is not None:
        core_death_particle_list.draw(WIN)

    if shockwave_list is not None:
        shockwave_list.draw(WIN)

    pygame.display.update()


def movement_handler_enemies(enemies_list, core, player, particle_list):
    for enemy in enemies_list:
        enemy.forward()
        if enemy.current_hitbox.colliderect(core.current_hitbox):
            core.damage(enemy.core_damage)
            enemies_list.remove(enemy)
        if enemy.current_hitbox.colliderect(player.current_hitbox):
            if player.crash_damage > enemy.health:
                enemy.death(player, None, particle_list, enemies_list, BasicEnemy_explosion_sound)
            else:
                enemy.damage(player.crash_damage)


def movement_handler_player(player, rotation):
    if player.movement_forward:
        player.forward()
        if not pygame.mixer.get_busy():
            player_forward_sound.play()
    if player.movement_reverse:
        player.reverse()
    player.rotate(rotation)


def movement_check_projectiles(player, enemies_list, death_particle_list):
    for projectile in player.projectiles_array:
        for enemy in enemies_list:
            if projectile.hitbox.colliderect(enemy.current_hitbox):
                if player.projectile_damage >= enemy.health:
                    enemy.death(player, projectile, death_particle_list, enemies_list, BasicEnemy_explosion_sound)
                else:
                    enemy.damage(player.projectile_damage)
                if projectile in player.projectiles_array:
                    player.projectiles_array.remove(projectile)


def main():
    player = Player(pygame.Rect(200, 200, DOT_SIDE, DOT_SIDE), 0)
    current_enemies_list = []
    death_particle_list = ParticleList(lambda time: time <= 0)

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
            current_blue = (current_blue[0] - 15, current_blue[1], current_blue[2])
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
                    # Having this here is not really optimal, since i have a plaer movement handler...
                    if not pygame.mixer.get_busy():
                        player_forward_sound.play()
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
                    player_forward_sound.stop()
                    # Having this here is not really optimal, since i have a player movement handler...

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
        death_particle_list.tick()
        player.tick()
        if is_shooting:
            player.shoot()

        if game_flow.tick():
            current_enemies_list = game_flow.enemies_list

        draw_window(player, core, current_enemies_list, death_particle_list)
        movement_handler_player(player, player_movement_rotation)
        movement_handler_enemies(current_enemies_list, core, player, death_particle_list)
        movement_check_projectiles(player, current_enemies_list, death_particle_list)
        if core.current_health <= 0:
            core_death(player, core, current_enemies_list, death_particle_list, clock)
            run = False
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


#   TODO: Disable checking collisions during core_death, since it causes performance issues.

#   TODO: Add a unique sound for an enemy colliding with the core

#   TODO: Add a sound for opening an empty shop

#   TODO: Add a sound for opening the shop when filled

#   TODO: New level up sound?

#   TODO: New shockwave sound?


def core_death(player, core, current_enemies_list, current_particle_list, clock):
    counter = 0
    shockwave_list = ParticleList(lambda time: time >= 100)
    smoke_particle_list = ParticleList(lambda time: time >= 80)
    core_explosion_particle_list = ParticleList(lambda time: time >= 50)

    run = True
    while counter < GlobalValues.FPS * 5 and run:  # 5 second end screen
        clock.tick(GlobalValues.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        core_explosion_particle_list.append(CoreExplosionParticle())

        if random.randint(1, 2) == 1:
            smoke_particle_list.append(CoreExplosionSmoke())

        if random.randint(1, 35) == 30:
            new_shockwave = Shockwave(960 + random.randint(0, 125), 540 + random.randint(0, 125))
            shockwave_list.append(new_shockwave)
            core_explosion_sound.play()

        core_explosion_particle_list.tick()
        shockwave_list.tick()
        smoke_particle_list.tick()
        draw_window(player, core, current_enemies_list, current_particle_list, core_explosion_particle_list,
                    shockwave_list,
                    smoke_particle_list)
        counter += 1
    pygame.quit()


if __name__ == "__main__":
    main()
