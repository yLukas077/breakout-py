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
    def __init__(self):
        # Inicializa a barra do jogador
        self.width = 150  # Largura inicial da barra
        self.height = 10  # Altura da barra
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (512, 940)  # Posição inicial da barra na tela
        self.speed = 20  # Velocidade de movimento da barra

    def move(self, dx):
        # Move a barra do jogador horizontalmente.
        # dx (int): Direção do movimento (-1 para esquerda, 1 para direita)
        self.rect.x += dx * self.speed
        # Impede a barra de sair da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1024:
            self.rect.right = 1024

    def increase_size(self):
        # Aumenta o tamanho da barra em 10%
        self.width = int(self.width * 1.1)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_size(self):
        # Reseta o tamanho da barra para o valor inicial
        self.width = 150
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(512, 940))

    def draw(self, screen):
        # Desenha a barra na tela
        screen.blit(self.image, self.rect.topleft)

# Classe da Bola
class Ball:
    def __init__(self, size, in_play=True):
        # Inicializa a bola.
        # size (int): Raio da bola
        # in_play (bool): Indica se a bola está em jogo ou aguardando lançamento
        self.radius = size
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (512, 480)  # Posição inicial da bola na tela
        self.speed = [7, -7]  # Velocidade inicial da bola
        self.in_play = in_play  # Estado da bola (em jogo ou aguardando lançamento)

    def move(self):
        # Movimenta a bola na tela
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Verifica colisão com as laterais da tela
        if self.rect.left <= 0 or self.rect.right >= 1024:
            self.speed[0] = -self.speed[0]
        # Verifica colisão com o topo da tela
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

    def increase_speed(self):
        # Aumenta a velocidade da bola em 5%
        self.speed[0] *= 1.05
        self.speed[1] *= 1.05

    def reset(self, paddle_rect):
        # Reseta a posição da bola e a define como não em jogo.
        # paddle_rect (pygame.Rect): Retângulo da barra do jogador
        self.rect.midbottom = paddle_rect.midtop
        self.in_play = False

    def draw(self, screen):
        # Desenha a bola na tela
        screen.blit(self.image, self.rect.topleft)
