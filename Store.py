from StoreItems import *
import GlobalValues


class Store:

    def __init__(self):
        self.current_supply = []
        self.buymenu = pygame.image.load("Assets/BuyMenu.png").convert()
        self.buymenu_rect = pygame.Rect(260, 160, 1440, 760)
        self.buymenu_selector = pygame.image.load("Assets/StoreSelector.png")
        self.buymenu_selector_rect = pygame.Rect(336, 220, 332, 388)
        self.selected = 0
        self.card_types_normal = [ItemAttackSpeed, ItemRotationSpeed, ItemForwardSpeed, ItemAttackDamage]   #TODO: Create more normal card types.
        self.card_types_keystone = [KeyStoneAddedProjectiles, KeyStoneOnDeathShots, KeyStoneJuggernaut]   #TODO: Create more Keystone card types.
        self.skill_points_used = 0
        pygame.font.init()
        self.font_item_title = pygame.font.Font("Assets/manaspc.ttf", 20)
        self.font_item_description = pygame.font.Font("Assets/manaspc.ttf", 32)

    def generate_store_supply(self):
        self.current_supply.clear()
        self.skill_points_used += 1
        if self.skill_points_used % 5 != 0 or self.skill_points_used == 0:
            for i in range(3):
                random_item = random.choice(self.card_types_normal)()
                self.current_supply.append(StoreCard(random_item, i))   #append 3 new store items.
        else:
            for i in range(3):
                random_keystone_item = random.choice(self.card_types_keystone)()
                self.current_supply.append(StoreCard(random_keystone_item, i))

    def draw(self, window, selected):
        self.buymenu_selector_rect.x = 336 + selected * 480
        window.blit(self.buymenu, self.buymenu_rect)    #draw the buymenu
        window.blit(self.buymenu_selector, self.buymenu_selector_rect)
        for card in self.current_supply:    #draw the cards
            card.draw(window)

        description_text = self.current_supply[self.selected].store_item.description()
        description_text_surface = self.font_item_description.render(description_text, False, (125, 125, 0))
        window.blit(description_text_surface, (620, 750))

        for card in self.current_supply:
            title_text = card.store_item.title()
            title_text_surface = self.font_item_title.render(title_text, False, (125, 125, 125))
            window.blit(title_text_surface, (345+485*card.position, 480))

        pygame.display.update()


class StoreCard:

    def __init__(self, store_item, position):
        self.store_item = store_item
        #card_dimensions = (290, 348)  # 72, 87 (/4)
        self.position = position
        self.posX = 354 + 480 * position
        self.posY = 240  # position of each card
        self.card_area_rect = pygame.Rect(self.posX, self.posY, 292, 348)
        self.card_picture_rect = pygame.Rect(self.posX + (30 * 4) - 38, self.posY + 8, 128, 128)

    def draw(self, window):
        #blit card frame
        #pygame.draw.rect(window, (120, 120, 120), self.card_area_rect)
        if self.store_item.rarity_value == 1:
            pygame.draw.rect(window, GlobalValues.COLOR_COMMON, self.card_picture_rect)
        elif self.store_item.rarity_value == 2:
            pygame.draw.rect(window, GlobalValues.COLOR_RARE, self.card_picture_rect)
        elif self.store_item.rarity_value == 3:
            pygame.draw.rect(window, GlobalValues.COLOR_EPIC, self.card_picture_rect)
        elif self.store_item.rarity_value == 4:
            pygame.draw.rect(window, GlobalValues.COLOR_LEGENDARY, self.card_picture_rect)

        window.blit(self.store_item.item_picture, self.card_picture_rect)
