import pygame, sys
from config import screen, screen_width, font_small, colors, sounds, font_huge, background_img
from ui import draw_button
import config as setting

def show_menu():
    difficulty_selecting = False
    settings_open = False

    selected_difficulty = (4, 4)

    play_button = pygame.Rect(screen_width // 2 - 150, 200, 300, 60)
    difficulty_button = pygame.Rect(screen_width // 2 - 150, 290, 300, 60)
    settings_button = pygame.Rect(screen_width // 2 - 150, 380, 300, 60)
    exit_button = pygame.Rect(screen_width // 2 - 150, 470, 300, 60)
    
    difficulty_buttons = [
        (pygame.Rect(screen_width // 2 - 150, 200, 300, 60), "Dễ (4x4)"),
        (pygame.Rect(screen_width // 2 - 150, 290, 300, 60), "Trung Bình (6x6)"),
        (pygame.Rect(screen_width // 2 - 150, 380, 300, 60), "Khó (8x8)"),
    ]

    music_slider = pygame.Rect(screen_width // 2 - 100, 250, 200, 10)
    sound_slider = pygame.Rect(screen_width // 2 - 100, 330, 200, 10)
    music_handle = pygame.Rect(music_slider.x + int(setting.volume_music * music_slider.width) - 5, music_slider.y - 5, 10, 20)
    sound_handle = pygame.Rect(sound_slider.x + int(setting.volume_sound * sound_slider.width) - 5, sound_slider.y - 5, 10, 20)

    dragging_music = False
    dragging_sound = False

    close_settings = pygame.Rect(screen_width // 2 - 150, 400, 300, 60)

    while True:
        screen.blit(background_img, (0, 0))
        title = font_huge.render("Game Lật Thẻ", True, colors["title"])
        screen.blit(title, title.get_rect(center=(screen_width // 2, 120)))

        if settings_open:
            label_music = font_small.render("Nhạc nền", True, colors["text"])
            label_sound = font_small.render("Hiệu ứng", True, colors["text"])
            screen.blit(label_music, (music_slider.x + 50, music_slider.y - 50))
            screen.blit(label_sound, (sound_slider.x + 50, sound_slider.y - 50))

            pygame.draw.rect(screen, colors["button"], music_slider)
            pygame.draw.rect(screen, colors["button_border"], music_slider, 2)
            pygame.draw.rect(screen, colors["title"], music_handle)

            music_percent = font_small.render(f"{int(setting.volume_music * 100)}%", True, colors["text"])
            screen.blit(music_percent, (music_slider.x + music_slider.width + 10, music_slider.y - 10))

            pygame.draw.rect(screen, colors["button"], sound_slider)
            pygame.draw.rect(screen, colors["button_border"], sound_slider, 2)
            pygame.draw.rect(screen, colors["title"], sound_handle)

            sound_percent = font_small.render(f"{int(setting.volume_sound * 100)}%", True, colors["text"])
            screen.blit(sound_percent, (sound_slider.x + sound_slider.width + 10, sound_slider.y - 10))

            draw_button(close_settings, "Đóng", close_settings.collidepoint(pygame.mouse.get_pos()))

        elif difficulty_selecting:
            for rect, text in difficulty_buttons:
                draw_button(rect, text, rect.collidepoint(pygame.mouse.get_pos()))

        else:
            draw_button(play_button, "Bắt Đầu Chơi", play_button.collidepoint(pygame.mouse.get_pos()))
            draw_button(difficulty_button, "Độ Khó", difficulty_button.collidepoint(pygame.mouse.get_pos()))
            draw_button(settings_button, "Cài Đặt", settings_button.collidepoint(pygame.mouse.get_pos()))
            draw_button(exit_button, "Thoát Game", exit_button.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                else:
                    pos = (event.x * screen.get_width(), event.y * screen.get_height())

                if settings_open:
                    if music_slider.collidepoint(pos) or music_handle.collidepoint(pos):
                        dragging_music = True
                    elif sound_slider.collidepoint(pos) or sound_handle.collidepoint(pos):
                        dragging_sound = True
                    elif close_settings.collidepoint(pos):
                        settings_open = False

                elif difficulty_selecting:
                    for rect, text in difficulty_buttons:
                        if rect.collidepoint(pos):
                            if text == "Dễ (4x4)":
                                selected_difficulty = (4, 4)
                            elif text == "Trung Bình (6x6)":
                                selected_difficulty = (6, 6)
                            elif text == "Khó (8x8)":
                                selected_difficulty = (8, 8)
                            difficulty_selecting = False

                else:
                    if play_button.collidepoint(pos):
                        return selected_difficulty
                    elif difficulty_button.collidepoint(pos):
                        difficulty_selecting = True
                    elif settings_button.collidepoint(pos):
                        settings_open = True
                    elif exit_button.collidepoint(pos):
                        pygame.quit()
                        sys.exit()

            elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                dragging_music = False
                dragging_sound = False

            elif event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                else:
                    pos = (event.x * screen.get_width(), event.y * screen.get_height())

                if settings_open:
                    if dragging_music:
                        rel_x = max(0, min(pos[0] - music_slider.x, music_slider.width))
                        music_handle.x = music_slider.x + rel_x - music_handle.width // 2
                        setting.volume_music = rel_x / music_slider.width
                        pygame.mixer.music.set_volume(setting.volume_music)

                    if dragging_sound:
                        rel_x = max(0, min(pos[0] - sound_slider.x, sound_slider.width))
                        sound_handle.x = sound_slider.x + rel_x - sound_handle.width // 2
                        setting.volume_sound = rel_x / sound_slider.width
                        for s in sounds.values():
                            s.set_volume(setting.volume_sound)