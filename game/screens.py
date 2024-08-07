import pygame
import time
from game.constants import BLACK, WHITE

def draw_winner_screen(screen, screen_width, screen_height, winner_text, blink_state, extra_ball_image, multi_ball_image, enlarge_paddle_image, score, end_time, start_time, collectables_count):
    screen.fill(BLACK)
    font_large = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)

    if blink_state:
        text_large = font_large.render(winner_text, True, WHITE)
        text_rect_large = text_large.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(text_large, text_rect_large)

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

def draw_game_over_screen(screen, screen_width, screen_height, score, end_time, start_time, extra_ball_image, multi_ball_image, enlarge_paddle_image, collectables_count):
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
