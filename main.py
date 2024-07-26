import pygame
import random

pygame.init()

screen_info = pygame.display.Info()
screen_width = int(screen_info.current_w * 0.5)
screen_height = int(screen_info.current_h * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Paddle:
    def __init__(self):
        self.width = 105
        self.height = 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen_width // 2, screen_height - 20)
        self.speed = 20

    def move(self, dx):
        self.rect.x += dx * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

class Ball:
    def __init__(self, x, y):
        self.radius = 3
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = [0, 0]
        self.in_wait = True

    def move(self):
        if not self.in_wait:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.speed[0] = -self.speed[0]
            if self.rect.top <= 0:
                self.speed[1] = -self.speed[1]

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def reset_position(self, paddle):
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top

class Block:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

paddle = Paddle()
balls = [Ball(screen_width // 2, screen_height // 2)]

block_width = 16
block_height = 16
block_spacing = 4
blocks_area_width = screen_width * 0.9
num_blocks_x = int(blocks_area_width // (block_width + block_spacing))
x_start = (screen_width - (num_blocks_x * (block_width + block_spacing))) // 2

blocks = [Block(x * (block_width + block_spacing) + x_start, y * (block_height + block_spacing) + 50, block_width, block_height) 
          for x in range(num_blocks_x) for y in range(10)]

score = 0
running = True
game_over = False
show_start_screen = True
