import pygame
import random
from game.ball import Ball
from game.constants import collectables_count, WHITE

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

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def apply_effect(self, balls, paddle, screen_width, screen_height, collectables_count):
        if self.power_type == "extra_ball":
            if balls:
                active_balls = [ball for ball in balls if not ball.in_wait and ball.rect.top <= screen_height]
                if active_balls:
                    random_ball = random.choice(active_balls)
                    collectables_count["extra_ball"] += 1
                    speed = (random_ball.speed[0] ** 2 + random_ball.speed[1] ** 2) ** 0.5
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
            active_balls = [ball for ball in balls if not ball.in_wait and ball.rect.top <= screen_height]  # Considerar apenas bolas ativas na tela
            collectables_count["multi_ball"] += 1
            new_balls = []
            for ball in active_balls:
                speed_x, speed_y = ball.speed
                x_spawn = ball.rect.centerx
                y_spawn = ball.rect.centery
                x_spawn = max(screen_width * 0.075, min(x_spawn, screen_width * 0.925))
                y_spawn = max(screen_height * 0.075, min(y_spawn, screen_height * 0.925))
                
                # Invertendo os componentes da velocidade para criar o ângulo oposto
                new_ball = Ball(x_spawn, y_spawn, -speed_x, -speed_y)
                new_balls.append(new_ball)
            balls.extend(new_balls)
        elif self.power_type == "enlarge_paddle":
            collectables_count["enlarge_paddle"] += 1
            paddle.enlarge()