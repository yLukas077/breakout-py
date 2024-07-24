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