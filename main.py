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
    else:
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for ball in balls:
                        if ball.in_wait:
                            ball.speed = [random.choice([-8, 8]), -8]
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
                    ball.speed[1] = -ball.speed[1]

            for ball in balls:
                collision_detected = False
                for block in blocks:
                    if ball.rect.colliderect(block.rect):
                        if abs(ball.rect.bottom - block.rect.top) < 10 and ball.speed[1] > 0:
                            ball.speed[1] = -ball.speed[1]
                        elif abs(ball.rect.top - block.rect.bottom) < 10 and ball.speed[1] < 0:
                            ball.speed[1] = -ball.speed[1]
                        elif abs(ball.rect.right - block.rect.left) < 10 and ball.speed[0] > 0:
                            ball.speed[0] = -ball.speed[0]
                        elif abs(ball.rect.left - block.rect.right) < 10 and ball.speed[0] < 0:
                            ball.speed[0] = -ball.speed[0]

                        blocks.remove(block)
                        score += 1
                        collision_detected = True
                        break
                if collision_detected:
                    break

            screen.fill(BLACK)
            paddle.draw()
            for ball in balls:
                ball.draw()
            for block in blocks:
                block.draw()

            font = pygame.font.Font(None, 36)
            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))

            pygame.display.flip()
            pygame.time.wait(30)

            for ball in balls[:]:
                if ball.rect.top > screen_height:
                    balls.remove(ball)
            if not balls:
                game_over = True

            if not blocks:
                game_over = True
        else:
            screen.fill(BLACK)
            font_large = pygame.font.Font(None, 74)
            font_small = pygame.font.Font(None, 36)

            text_large = font_large.render("GAME OVER", True, WHITE)
            text_rect_large = text_large.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_large, text_rect_large)

            text_small = font_small.render(f"Final Score: {score}", True, WHITE)
            text_rect_small = text_small.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
            screen.blit(text_small, text_rect_small)

            text_small2 = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
            text_rect_small2 = text_small2.get_rect(center=(screen_width // 2, screen_height // 2 + 120))
            screen.blit(text_small2, text_rect_small2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paddle = Paddle()
                        balls = [Ball(screen_width // 2, screen_height // 2)]
                        blocks = [Block(x * (block_width + block_spacing) + x_start, y * (block_height + block_spacing) + 50, block_width, block_height) 
                                  for x in range(num_blocks_x) for y in range(10)]
                        score = 0
                        game_over = False
                    if event.key == pygame.K_q:
                        running = False

pygame.quit()
