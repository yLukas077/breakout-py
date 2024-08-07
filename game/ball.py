import pygame
from game.constants import RED

class Ball:
    def __init__(self, x, y, speed_x=0, speed_y=0):
        self.radius = 5 
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = [speed_x, speed_y] 
        self.in_wait = speed_x == 0 and speed_y == 0

    def move(self, screen_width):
        if not self.in_wait:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.speed[0] = -self.speed[0]
            if self.rect.top <= 0:
                self.speed[1] = -self.speed[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def reset_position(self, paddle):
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top

    def handle_collision(self, block):
        if self.rect.colliderect(block.rect):
            # Detectar colisão horizontal
            if self.rect.right >= block.rect.left and self.rect.left < block.rect.left:
                self.speed[0] = -self.speed[0]
                self.rect.right = block.rect.left
            elif self.rect.left <= block.rect.right and self.rect.right > block.rect.right:
                self.speed[0] = -self.speed[0]
                self.rect.left = block.rect.right

            # Detectar colisão vertical
            if self.rect.bottom >= block.rect.top and self.rect.top < block.rect.top:
                self.speed[1] = -self.speed[1]
                self.rect.bottom = block.rect.top
            elif self.rect.top <= block.rect.bottom and self.rect.bottom > block.rect.bottom:
                self.speed[1] = -self.speed[1]
                self.rect.top = block.rect.bottom
