import pygame
import time
import random
from game.constants import *
from game.paddle import Paddle
from game.ball import Ball
from game.block import Block
from game.powerup import PowerUp
from game.screens import draw_winner_screen, draw_game_over_screen
from game.utils import check_and_change_music

pygame.init()

# Configurações de tela
screen_info = pygame.display.Info()
screen_width = int(screen_info.current_w * 0.5)
screen_height = int(screen_info.current_h * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Carregar e definir ícone
icon_image = pygame.image.load('images/logo-breakout.png')
pygame.display.set_icon(icon_image)

# Carregar imagem de coração
heart_image = pygame.image.load('images/heart-pixel.png')
heart_image = pygame.transform.scale(heart_image, (50, 50))

# Carregar imagens dos power-ups
extra_ball_image = pygame.image.load('images/+1-frame.png').convert_alpha()
multi_ball_image = pygame.image.load('images/x2-frame.png').convert_alpha()
enlarge_paddle_image = pygame.image.load('images/growth-frame.png').convert_alpha()

# Carregar as músicas de fundo
pygame.mixer.music.load('sounds/pienso.mp3')
pygame.mixer.music.set_volume(0.3) 
pygame.mixer.music.play(-1)  # Toca a música em loop

# Carregar a segunda música
second_music_path = 'sounds/parapara.mp3'

# Inicializar variáveis de controle para música
music_playing = 'normal' 

paddle = Paddle(screen_width, screen_height)
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
blink_state = True
start_typing_time = 0

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
        current_time = pygame.time.get_ticks()
        if current_time - start_typing_time > 500:
            blink_state = not blink_state
            start_typing_time = current_time

        draw_winner_screen(screen, screen_width, screen_height, winner_text, blink_state, extra_ball_image, multi_ball_image, enlarge_paddle_image, score, end_time, start_time, collectables_count)
        
        pygame.mixer.music.stop()  # Parar a música ao entrar na tela de vitória
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.play(-1)  # Reiniciar a música ao reiniciar o jogo
                    paddle = Paddle(screen_width, screen_height)
                    balls = [Ball(screen_width // 2, screen_height // 2)]
                    blocks = [Block(x * (block_width + block_spacing) + x_start, y * (block_height + block_spacing) + 50, block_width, block_height, random.choice(block_colors)) 
                              for x in range(num_blocks_x) for y in range(10)]
                    powerups = []
                    score = 0
                    lives = 3
                    winner = False
                    game_over = False
                    start_time = time.time()
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
                ball.move(screen_width)

            for ball in balls:
                if ball.rect.colliderect(paddle.rect):
                    paddle.reflect_ball(ball)

            for ball in balls:
                collision_detected = False
                for block in blocks[:]:
                    if ball.rect.colliderect(block.rect):
                        ball.handle_collision(block)

                        if not block.has_dropped:  # Certifica-se de que apenas um power-up é gerado por bloco
                            powerup = block.spawn_powerup()
                            if powerup:
                                powerups.append(powerup)
                            block.has_dropped = True

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
                pygame.mixer.music.stop()  # Parar a música ao vencer

            for powerup in powerups[:]:
                powerup.move()
                if powerup.rect.top > screen_height:
                    powerups.remove(powerup)
                elif powerup.rect.colliderect(paddle.rect):
                    powerup.apply_effect(balls, paddle, screen_width, screen_height, collectables_count)
                    powerups.remove(powerup)

            screen.fill(BLACK)
            paddle.draw(screen)
            for ball in balls:
                ball.draw(screen)
            for block in blocks:
                block.draw(screen)
            for powerup in powerups:
                powerup.draw(screen)

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
                    pygame.mixer.music.stop()  # Parar a música ao entrar na tela de game over
                else:
                    balls.append(Ball(screen_width // 2, paddle.rect.top - 10, 0, 0))  # Adicionar nova bola em espera

            music_playing = check_and_change_music(balls, second_music_path, music_playing)  # Verifica e troca a música conforme o número de bolas
        else:
            draw_game_over_screen(screen, screen_width, screen_height, score, end_time, start_time, extra_ball_image, multi_ball_image, enlarge_paddle_image, collectables_count)
            
            pygame.mixer.music.stop()  # Parar a música ao entrar na tela de game over

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.play(-1)  # Reiniciar a música ao reiniciar o jogo
                        paddle = Paddle(screen_width, screen_height)
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
