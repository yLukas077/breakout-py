import pygame
import math
from game.constants import BLUE

class Paddle:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
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
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def enlarge(self):
        self.width += 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=self.rect.center)

    def reflect_ball(self, ball):
        paddle_center = self.rect.centerx
        ball_center = ball.rect.centerx
        offset = ball_center - paddle_center
        max_angle = 60  # Ângulo máximo de desvio em graus

        # Calcula o ângulo de reflexão baseado na posição de impacto
        relative_offset = offset / (self.rect.width / 2)
        bounce_angle = relative_offset * max_angle

        # Converte o ângulo de graus para radianos para cálculo
        bounce_angle_rad = bounce_angle * (math.pi / 180)

        # Mantém a velocidade atual da bola, mas ajusta a direção
        speed = math.sqrt(ball.speed[0]**2 + ball.speed[1]**2)
        ball.speed[0] = speed * math.sin(bounce_angle_rad)
        ball.speed[1] = -speed * math.cos(bounce_angle_rad)
