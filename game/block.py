import pygame
import random
from game.powerup import PowerUp

class Block:
    def __init__(self, x, y, width, height, color):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.has_dropped = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def spawn_powerup(self):
        if not self.has_dropped:
            drop_chance = random.randint(1, 100)
            self.has_dropped = True
            if drop_chance <= 6:
                return PowerUp(self.rect.centerx, self.rect.centery, "extra_ball")
            elif 46 < drop_chance <= 60:
                return PowerUp(self.rect.centerx, self.rect.centery, "multi_ball")
            elif 60 < drop_chance <= 62:
                return PowerUp(self.rect.centerx, self.rect.centery, "enlarge_paddle")
        return None
