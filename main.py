import pygame

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
screen = pygame.display.set_mode((1024, 960))  
pygame.display.set_caption("Breakout")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Classe do Jogador (Barra)
class Paddle:
    def _init_(self):
        self.width = 150  # Largura inicial da barra
        self.height = 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (512, 940)  # Posição inicial com base no novo tamanho da tela
        self.speed = 20  # Velocidade da barra

    def move(self, dx):
        self.rect.x += dx * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1024: 
            self.rect.right = 1024

    def increase_size(self):
        self.width = int(self.width * 1.1)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_size(self):
        self.width = 150  # Resetar a largura para o valor inicial
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(512, 940))  # Resetar a posição inicial

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Classe da Bola
class Ball:
    def _init_(self, size, in_play=True):
        self.radius = size
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (512, 480)  
        self.speed = [7, -7]  # Aumentando a velocidade da bola
        self.in_play = in_play  # Bola aguardando para ser lançada

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.left <= 0 or self.rect.right >= 1024:  
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

    def increase_speed(self):
        self.speed[0] *= 1.05
        self.speed[1] *= 1.05

    def reset(self, paddle_rect):
        self.rect.midbottom = paddle_rect.midtop
        self.in_play = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)