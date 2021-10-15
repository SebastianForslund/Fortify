import random
import pygame


class StoreItem:

    def __init__(self):
        rarity_list = []
        for i in range(1, 4):
            rarity_list.append(random.randint(1, 4))
        self.rarity_value = min(rarity_list)
        pass

    def apply(self, player, core=None):
        pass

    def title(self):
        pass

    def description(self):
        pass


class ItemAttackSpeed(StoreItem):

    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/ItemAttackSpeed.png").convert_alpha()

        if self.rarity_value == 1:
            self.modifier = 0.05
        elif self.rarity_value == 2:
            self.modifier = 0.10
        elif self.rarity_value == 3:
            self.modifier = 0.15
        elif self.rarity_value == 4:
            self.modifier = 0.25

    def apply(self, player, core=None):
        player.modifier_attack_speed *= 1 - self.modifier
        player.projectile_fire_rate = player.modifier_attack_speed * player.default_projectile_fire_rate
        print(player.modifier_attack_speed)

    def title(self):
        return "Increased Attack Speed"

    def description(self):
        return "Increases your Attack Speed by " + str(self.modifier*100) + "%."


class ItemAttackDamage(StoreItem):

    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/ItemAttackDamage.png").convert_alpha()

        if self.rarity_value == 1:
            self.modifier = 20
        elif self.rarity_value == 2:
            self.modifier = 30
        elif self.rarity_value == 3:
            self.modifier = 60
        elif self.rarity_value == 4:
            self.modifier = 100

    def apply(self, player, core=None):
        player.projectile_damage += self.modifier

    def title(self):
        return "Increased Attack Damage"

    def description(self):
        return "Adds #" + str(self.modifier) + " Attack Damage to your Attacks."


class ItemRotationSpeed(StoreItem):

    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/ItemRotationSpeed.png").convert_alpha()

        if self.rarity_value == 1:
            self.modifier = 0.08
        elif self.rarity_value == 2:
            self.modifier = 0.12
        elif self.rarity_value == 3:
            self.modifier = 0.16
        elif self.rarity_value == 4:
            self.modifier = 0.20

    def apply(self, player, core=None):
        player.modifier_rotation_speed += self.modifier
        player.rotate_speed *= player.modifier_rotation_speed

    def title(self):
        return "Increased Rotation Speed"

    def description(self):
        return "Increases your Rotation Speed by " + str(self.modifier * 100) + "%."


class ItemPlayerIncreasedMaxHealth(StoreItem):

    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/ItemIncreasedHealth.png").convert_alpha()

        if self.rarity_value == 1:
            self.modifier = 0.05
        elif self.rarity_value == 2:
            self.modifier = 0.08
        elif self.rarity_value == 3:
            self.modifier = 0.12
        elif self.rarity_value == 4:
            self.modifier = 0.15

    def apply(self, player, core=None):
        player.modifier_max_health += self.modifier
        player.health_max *= player.modifier_max_health

    def title(self):
        return "Increased Player Health"

    def description(self):
        return "Increases your health by " + str(self.modifier * 100) + "%."


class ItemForwardSpeed(StoreItem):

    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/ItemForwardSpeed.png").convert_alpha()

        if self.rarity_value == 1:
            self.modifier = 0.1
        elif self.rarity_value == 2:
            self.modifier = 0.2
        elif self.rarity_value == 3:
            self.modifier = 0.3
        elif self.rarity_value == 4:
            self.modifier = 0.4

    def apply(self, player, core=None):
        player.modifier_movement_speed += self.modifier
        player.movement_value_forward_speed *= player.modifier_movement_speed

    def title(self):
        return "Increased Forward Speed"

    def description(self):
        return "Increases your forward speed by " + str(self.modifier * 100) + "%."


class KeyStoneAddedProjectiles(StoreItem):

    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/KeyStoneAddedProjectiles.png").convert_alpha()
        self.modifier = self.rarity_value

    def apply(self, player, core=None):
        player.modifier_attack_speed *= 2 - (1/(0.5+self.modifier))
        print(str(2 - (1/(0.5+self.modifier))) + "keystone")
        player.projectile_fire_rate = player.modifier_attack_speed * player.default_projectile_fire_rate
        player.modifier_shot_count += self.modifier

    def title(self):
        return "Added Projectiles"

    def description(self):
        return "Adds " + str(self.modifier) + "projectile(s) to your shots, but decreases your Attack Speed by " + str(1 - (1/(0.5+self.modifier))) + "."


class KeyStoneOnDeathShots(StoreItem):
    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/KeyStoneOnDeathShots.png").convert_alpha()
        if self.rarity_value == 1:
            self.modifier = 1
        elif self.rarity_value == 2:
            self.modifier = 2
        elif self.rarity_value == 3:
            self.modifier = 3
        elif self.rarity_value == 4:
            self.modifier = 4

    def apply(self, player, core=None):
        player.modifier_on_death_shots += self.modifier
        player.projectile_damage -= 0 #TODO placeholder, currently no damage penalty when choosing this keystone

    def title(self):
        return "Random Shots on Enemy Death"

    def description(self):
        return "Adds " + str(self.modifier) + "projectile(s) that spawn on enemy deathbs, but decreases your Attack damage by " + str(self.rarity_value*10) + "."


class KeyStoneJuggernaut(StoreItem):
    def __init__(self):
        super().__init__()
        self.item_picture = pygame.image.load("Assets/KeyStoneJuggernaut.png").convert_alpha()
        self.modifier = self.rarity_value * 2


    def apply(self, player, core=None):
        player.modifier_invincible = True
        player.crash_damage += self.modifier
        player.modifier_can_shoot = False

    def title(self):
        return "Juggernaut"

    def description(self):
        return "You can no longer shoot. Adds #" + str(self.modifier) + " to your Crash Damage."
