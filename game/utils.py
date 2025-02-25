import pygame

def check_and_change_music(balls, second_music_path, music_playing, screen_height):
    active_balls = [ball for ball in balls if ball.rect.top <= screen_height]  # Apenas bolas ativas
    try:
        if len(active_balls) > 10 and music_playing != 'intense':
            pygame.mixer.music.load(second_music_path)
            pygame.mixer.music.set_volume(0.2)  # Volume baixo para a segunda música
            pygame.mixer.music.play(-1)
            return 'intense'
        elif len(active_balls) <= 10 and music_playing != 'normal':
            pygame.mixer.music.load('sounds/pienso.mp3')
            pygame.mixer.music.set_volume(0.3)  # Volume para a música normal
            pygame.mixer.music.play(-1)
            return 'normal'
    except pygame.error as e:
        print(f"Erro ao trocar música: {e}")
    return music_playing