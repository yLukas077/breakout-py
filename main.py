import pygame
import random
import time
import math

pygame.init()

# Configurações de tela
screen_info = pygame.display.Info()
screen_width = int(screen_info.current_w * 0.5)
screen_height = int(screen_info.current_h * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)

# Carregar e definir ícone
icon_image = pygame.image.load('images/logo-brokeout.png')
pygame.display.set_icon(icon_image)

# Carregar imagem de coração
heart_image = pygame.image.load('images/heart-pixel.png')
heart_image = pygame.transform.scale(heart_image, (50, 50))

# Carregar imagens dos power-ups
extra_ball_image = pygame.image.load('images/+1-frame.png').convert_alpha()
multi_ball_image = pygame.image.load('images/x2-frame.png').convert_alpha()
enlarge_paddle_image = pygame.image.load('images/growth-frame.png').convert_alpha()


# Adicionar uma estrutura para armazenar a contagem de coletáveis
collectables_count = {
    "extra_ball": 0,
    "multi_ball": 0,
    "enlarge_paddle": 0
}

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

class Ball:
    def __init__(self, x, y, speed_x=0, speed_y=0):
        self.radius = 3
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = [speed_x, speed_y] 
        self.in_wait = speed_x == 0 and speed_y == 0

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



class Block:
    def __init__(self, x, y, width, height, color):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.has_dropped = False

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def spawn_powerup(self):
        if not self.has_dropped:
            drop_chance = random.randint(1, 100)
            self.has_dropped = True
            if drop_chance <= 6:
                return PowerUp(self.rect.centerx, self.rect.centery, "extra_ball")
            elif 46 < drop_chance <= 48:
                return PowerUp(self.rect.centerx, self.rect.centery, "multi_ball")
            elif 60 < drop_chance <= 62:
                return PowerUp(self.rect.centerx, self.rect.centery, "enlarge_paddle")
        return None

class PowerUp:
    def __init__(self, x, y, power_type):
        self.power_type = power_type
        self.speed = 3

        try:
            if power_type == "extra_ball":
                self.image = pygame.image.load('images/+1-frame.png').convert_alpha()
            elif power_type == "multi_ball":
                self.image = pygame.image.load('images/x2-frame.png').convert_alpha()
            elif power_type == "enlarge_paddle":
                self.image = pygame.image.load('images/growth-frame.png').convert_alpha()
            else:
                raise ValueError(f"PowerUp type {power_type} is not recognized.")
        except pygame.error as e:
            print(f"Failed to load image for {power_type}: {e}")
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            self.image.fill(WHITE)

        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def apply_effect(self, balls, paddle):
        if self.power_type == "extra_ball":
            if balls:
                random_ball = random.choice(balls)
                collectables_count["extra_ball"] += 1
                speed = (random_ball.speed[0] ** 2 + random_ball.speed[1] ** 2) ** 0.5  # Manter a velocidade da bola original
                angle = random.uniform(-1.0, 1.0)
                speed_x = speed * angle
                speed_y = (speed ** 2 - speed_x ** 2) ** 0.5
                
                x_spawn = random_ball.rect.centerx
                y_spawn = random_ball.rect.centery
                x_spawn = max(screen_width * 0.075, min(x_spawn, screen_width * 0.925))
                y_spawn = max(screen_height * 0.075, min(y_spawn, screen_height * 0.925))
                
                new_ball = Ball(x_spawn, y_spawn, speed_x, -speed_y)
                balls.append(new_ball)
        elif self.power_type == "multi_ball":
            num_balls = len(balls)
            collectables_count["multi_ball"] += 1
            for _ in range(num_balls): 
                random_ball = random.choice(balls)
                speed = (random_ball.speed[0] ** 2 + random_ball.speed[1] ** 2) ** 0.5  # Manter a velocidade da bola original
                angle = random.uniform(-1.0, 1.0)
                speed_x = speed * angle
                speed_y = (speed ** 2 - speed_x ** 2) ** 0.5
                
                x_spawn = random_ball.rect.centerx
                y_spawn = random_ball.rect.centery
                x_spawn = max(screen_width * 0.075, min(x_spawn, screen_width * 0.925))
                y_spawn = max(screen_height * 0.075, min(y_spawn, screen_height * 0.925))
                
                new_ball = Ball(x_spawn, y_spawn, speed_x, -speed_y)
                balls.append(new_ball)
        elif self.power_type == "enlarge_paddle":
            collectables_count["enlarge_paddle"] += 1
            paddle.enlarge()

# Carregar as músicas de fundo
pygame.mixer.music.load('sons/pienso.mp3')
pygame.mixer.music.set_volume(0.3) 
pygame.mixer.music.play(-1)  # Toca a música em loop

# Carregar a segunda música
second_music_path = 'sons/parapara.mp3'

# Inicializar variáveis de controle para música
music_playing = 'normal' 

paddle = Paddle()
balls = [Ball(screen_width // 2, screen_height // 2)]

block_width = 16
block_height = 16
block_spacing = 4
blocks_area_width = screen_width * 0.9
num_blocks_x = int(blocks_area_width // (block_width + block_spacing))
x_start = (screen_width - (num_blocks_x * (block_width + block_spacing))) // 2

# Cores dos blocos
block_colors = [BLUE, GREEN, LIGHT_BLUE, ORANGE]

blocks = [Block(x * (block_width + block_spacing) + x_start, y * (block_height + block_spacing) + 50, block_width, block_height, random.choice(block_colors)) 
          for x in range(num_blocks_x) for y in range(10)]

powerups = []
score = 0
lives = 3
running = True
game_over = False
show_start_screen = True
winner = False
start_time = None 
end_time = None

# Variáveis para animação de vitória
winner_text = "YOU WIN!"
display_text = ""
text_index = 0
typing_finished = False
start_typing_time = 0
blink_count = 0
blink_state = True

# Função para verificar e trocar a música
def check_and_change_music():
    global music_playing
    try:
        if len(balls) > 10 and music_playing != 'intense':
            pygame.mixer.music.load(second_music_path)
            pygame.mixer.music.set_volume(0.2)  # Volume baixo para a segunda música
            pygame.mixer.music.play(-1)
            music_playing = 'intense'
        elif len(balls) <= 10 and music_playing != 'normal':
            pygame.mixer.music.load('sons/pienso.mp3')
            pygame.mixer.music.set_volume(0.3)  # Volume para a música normal
            pygame.mixer.music.play(-1)
            music_playing = 'normal'
    except pygame.error as e:
        print(f"Erro ao trocar música: {e}")

def draw_winner_screen():
    global display_text, text_index, typing_finished, start_typing_time, blink_count, blink_state
    screen.fill(BLACK)
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    if not typing_finished:
        if pygame.time.get_ticks() - start_typing_time > 150:
            if text_index < len(winner_text):
                display_text += winner_text[text_index]
                text_index += 1
                start_typing_time = pygame.time.get_ticks()
            else:
                typing_finished = True
                start_typing_time = pygame.time.get_ticks()

    if typing_finished:
        if pygame.time.get_ticks() - start_typing_time > 500:
            blink_state = not blink_state
            start_typing_time = pygame.time.get_ticks()
            blink_count += 1

    if blink_state or not typing_finished:
        text_large = font_large.render(display_text, True, WHITE)
        text_rect_large = text_large.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text_large, text_rect_large)

    if blink_count >= 6:
        text_large = font_large.render(winner_text, True, WHITE)
        screen.blit(text_large, text_rect_large)
        typing_finished = False
        blink_count = 0

    final_time = time.strftime("%M:%S", time.gmtime(end_time - start_time))

    text_score = font_small.render(f"Final Score: {score}", True, WHITE)
    text_rect_score = text_score.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(text_score, text_rect_score)

    text_time = font_small.render(f"Time: {final_time}", True, WHITE)
    text_rect_time = text_time.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
    screen.blit(text_time, text_rect_time)

    text_congrats = font_small.render("Congratulations!", True, WHITE)
    text_rect_congrats = text_congrats.get_rect(center=(screen_width // 2, screen_height // 2 + 70))
    screen.blit(text_congrats, text_rect_congrats)

    icons = [
        (extra_ball_image, collectables_count["extra_ball"]),
        (multi_ball_image, collectables_count["multi_ball"]),
        (enlarge_paddle_image, collectables_count["enlarge_paddle"]),
    ]
    
    y_offset = screen_height // 2 + 120
    total_width = (len(icons) - 1) * 150  
    x_offset_start = screen_width // 2 - total_width // 2 - 40  
    for i, (icon, count) in enumerate(icons):
        x_offset = x_offset_start + i * 150
        
        screen.blit(icon, (x_offset, y_offset))
        collectable_text = font_small.render(f"{count}x", True, WHITE)
        collectable_rect = collectable_text.get_rect(midleft=(x_offset + 50, y_offset + 16))
        screen.blit(collectable_text, collectable_rect)

    text_restart = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
    text_rect_restart = text_restart.get_rect(center=(screen_width // 2, y_offset + 70))
    screen.blit(text_restart, text_rect_restart)

    pygame.display.flip()

def draw_game_over_screen():
    global end_time
    screen.fill(BLACK)
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    text_large = font_large.render("GAME OVER", True, WHITE)
    text_rect_large = text_large.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text_large, text_rect_large)

    text_small = font_small.render(f"Final Score: {score}", True, WHITE)
    text_rect_small = text_small.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_small, text_rect_small)

    final_time = time.strftime("%M:%S", time.gmtime(end_time - start_time))
    text_small2 = font_small.render(f"Time: {final_time}", True, WHITE)
    text_rect_small2 = text_small2.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(text_small2, text_rect_small2)

    # Desenhar os colecionáveis em uma linha de 3 colunas
    icons = [
        (extra_ball_image, collectables_count["extra_ball"]),
        (multi_ball_image, collectables_count["multi_ball"]),
        (enlarge_paddle_image, collectables_count["enlarge_paddle"]),
    ]
    
    y_offset = screen_height // 2 + 120
    total_width = (len(icons) - 1) * 150 
    x_offset_start = screen_width // 2 - total_width // 2 - 35

    for i, (icon, count) in enumerate(icons):
        x_offset = x_offset_start + i * 150
        
        screen.blit(icon, (x_offset, y_offset))
        collectable_text = font_small.render(f"{count}x", True, WHITE)
        collectable_rect = collectable_text.get_rect(midleft=(x_offset + 50, y_offset + 16))
        screen.blit(collectable_text, collectable_rect)

    text_small3 = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
    text_rect_small3 = text_small3.get_rect(center=(screen_width // 2, y_offset + 70))
    screen.blit(text_small3, text_rect_small3)

    pygame.display.flip()


while running:
    if show_start_screen:
        screen.fill(BLACK)
        font_large = pygame.font.Font(None, 74)
        text_large = font_large.render("Press SPACE to Start", True, WHITE)
        text_rect_large = text_large.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_large, text_rect_large)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_start_screen = False
                start_time = time.time() 
    elif winner:
        draw_winner_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paddle = Paddle()
                    balls = [Ball(screen_width // 2, screen_height // 2)]
                    blocks = [Block(x * (block_width + block_spacing) + x_start, y * (block_height + block_spacing) + 50, block_width, block_height, random.choice(block_colors)) 
                              for x in range(num_blocks_x) for y in range(10)]
                    powerups = []
                    score = 0
                    lives = 3
                    winner = False
                    game_over = False
                    start_time = time.time()
                    # Reset animação
                    display_text = ""
                    text_index = 0
                    typing_finished = False
                    blink_count = 0
                    blink_state = True
                    collectables_count = {
                        "extra_ball": 0,
                        "multi_ball": 0,
                        "enlarge_paddle": 0
                    }
                if event.key == pygame.K_q:
                    running = False
    else:
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for ball in balls:
                        if ball.in_wait:
                            ball.speed = [0, -12]
                            ball.in_wait = False

            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1

            paddle.move(dx)

            for ball in balls:
                if ball.in_wait:
                    ball.reset_position(paddle)
                ball.move()

            for ball in balls:
                if ball.rect.colliderect(paddle.rect):
                    paddle.reflect_ball(ball)

            for ball in balls:
                collision_detected = False
                for block in blocks[:]:
                    if ball.rect.colliderect(block.rect):
                        if abs(ball.rect.bottom - block.rect.top) < 10 and ball.speed[1] > 0:
                            ball.speed[1] = -ball.speed[1]
                        elif abs(ball.rect.top - block.rect.bottom) < 10 and ball.speed[1] < 0:
                            ball.speed[1] = -ball.speed[1]
                        elif abs(ball.rect.right - block.rect.left) < 10 and ball.speed[0] > 0:
                            ball.speed[0] = -ball.speed[0]
                        elif abs(ball.rect.left - block.rect.right) < 10 and ball.speed[0] < 0:
                            ball.speed[0] = -ball.speed[0]

                        powerup = block.spawn_powerup()
                        if powerup:
                            powerups.append(powerup)

                        blocks.remove(block)
                        score += 1
                        collision_detected = True
                        break
                if collision_detected:
                    break

            if not blocks:  # Se não houver mais blocos, o jogador venceu
                winner = True
                end_time = time.time()
                start_typing_time = pygame.time.get_ticks()  # Inicializa o temporizador de animação

            for powerup in powerups[:]:
                powerup.move()
                if powerup.rect.top > screen_height:
                    powerups.remove(powerup)
                elif powerup.rect.colliderect(paddle.rect):
                    powerup.apply_effect(balls, paddle)
                    powerups.remove(powerup)

            screen.fill(BLACK)
            paddle.draw()
            for ball in balls:
                ball.draw()
            for block in blocks:
                block.draw()
            for powerup in powerups:
                powerup.draw()

            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))

            if start_time is not None:  # Verificar se o tempo foi inicializado
                current_time = time.time() - start_time
                current_time_str = time.strftime("%M:%S", time.gmtime(current_time))
                time_text = font.render(f"Time: {current_time_str}", True, WHITE)
                screen.blit(time_text, (150, 10)) 

            # Mostrar vidas
            for i in range(lives):
                screen.blit(heart_image, (screen_width - 50 - i * 30, 1))
            pygame.display.flip()
            pygame.time.wait(30)

            # Verificar se todas as bolas foram perdidas
            if all(ball.rect.top > screen_height for ball in balls):  # Verificar se todas as bolas caíram fora da tela
                balls.clear()  # Remover todas as bolas
                lives -= 1  # Reduzir uma vida
                powerups.clear()  # Limpar os power-ups
                if lives == 0:
                    game_over = True
                    end_time = time.time()  
                else:
                    balls.append(Ball(screen_width // 2, paddle.rect.top - 10, 0, 0))  # Adicionar nova bola em espera

            check_and_change_music()  # Verifica e troca a música conforme o número de bolas
        else:
            draw_game_over_screen()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paddle = Paddle()
                        balls = [Ball(screen_width // 2, screen_height // 2)]
                        blocks = [Block(x * (block_width + block_spacing) + x_start, y * (block_height + block_spacing) + 50, block_width, block_height, random.choice(block_colors)) 
                                  for x in range(num_blocks_x) for y in range(10)]
                        powerups = []
                        score = 0
                        lives = 3
                        game_over = False
                        start_time = time.time()
                        collectables_count = {
                            "extra_ball": 0,
                            "multi_ball": 0,
                            "enlarge_paddle": 0
                        }
                    if event.key == pygame.K_q:
                        running = False

pygame.quit()