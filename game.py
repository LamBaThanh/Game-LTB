import pygame, sys
from config import screen, colors, clock, sounds, font_large, font_small, background_img
from board import Board
from timer import GameTimer
from score import ScoreManager
from ui import draw_icon_button, draw_info_panel, draw_result_popup, draw_popup_menu, draw_toast, Firework
import config as setting

def run_game(rows, cols, carry_score=0):
    dragging_music = False
    dragging_sound = False

    time_limit = {4: 60, 6: 120, 8: 240}.get(rows, 60)

    board = Board(rows, cols)
    timer = GameTimer(time_limit)
    score = ScoreManager(carry_score)

    menu_icon_button = pygame.Rect(20, 20, 50, 50)
    menu_open = False
    settings_open = False

    music_slider = pygame.Rect(300, 330, 200, 10)
    sound_slider = pygame.Rect(300, 410, 200, 10)
    music_handle = pygame.Rect(music_slider.x + int(music_slider.width * setting.volume_music) - 5, music_slider.y - 5, 10, 20)
    sound_handle = pygame.Rect(sound_slider.x + int(sound_slider.width * setting.volume_sound) - 5, sound_slider.y - 5, 10, 20)

    popup_rect = pygame.Rect(20, 80, 200, 210)
    popup_buttons = [
        (pygame.Rect(40, 100, 160, 50), "Về Menu"),
        (pygame.Rect(40, 160, 160, 50), "Cài Đặt"),
        (pygame.Rect(40, 220, 160, 50), "Gợi Ý"),
    ]

    result_buttons = [
        (pygame.Rect(250, 300, 300, 60), "Chơi tiếp"),
        (pygame.Rect(250, 380, 300, 60), "Chọn độ khó mới"),
        (pygame.Rect(250, 460, 300, 60), "Menu"),
    ]

    difficulty_buttons = [
        (pygame.Rect(250, 300, 300, 60), "Dễ (4x4)"),
        (pygame.Rect(250, 380, 300, 60), "Trung Bình (6x6)"),
        (pygame.Rect(250, 460, 300, 60), "Khó (8x8)"),
    ]

    toast_message = ""
    toast_timer = 0

    hint_cards = None
    hint_timer = 0

    result_text = ""
    game_over = False
    hint_active = False
    difficulty_selecting = False

    fireworks = []

    timer.start()

    def get_event_pos(event):
        if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
            return (event.x * screen.get_width(), event.y * screen.get_height())
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            return event.pos
        return None

    while True:
        screen.blit(background_img, (0, 0))

        if timer.is_time_up() and not board.all_matched():
            game_over = True
            result_text = "Thua rồi!"
            timer.pause()
            sounds["lose"].play()

        if board.all_matched() and not game_over:
            hint_active = False
            game_over = True
            result_text = "Bạn thắng!"
            timer.pause()
            sounds["win"].play()

            fireworks = []
            positions = [
                (100, 100),
                (screen.get_width() - 100, 100),
                (100, screen.get_height() - 100),
                (screen.get_width() - 100, screen.get_height() - 100)
            ]
            for pos in positions:
                fireworks.append(Firework(pos, particle_count=80, speed_range=(3, 7)))

        board.draw()
        draw_info_panel(score, timer)
        draw_toast(toast_message, toast_timer)

        if game_over:
            for fw in fireworks:
                fw.update()
                fw.draw()
            fireworks = [fw for fw in fireworks if not fw.is_finished()]

        if game_over and not difficulty_selecting:
            if game_over and not difficulty_selecting:
                overlay_rect = pygame.Rect(150, 150, screen.get_width() - 300, screen.get_height() - 300)
                pygame.draw.rect(screen, (255, 255, 255), overlay_rect, border_radius=20)
                pygame.draw.rect(screen, (200, 200, 200), overlay_rect, 4, border_radius=20)
                final_score = score.calculate_final_score(timer.get_remaining_time())
                draw_result_popup(result_text, final_score, result_buttons)

        if difficulty_selecting:
            for rect, text in difficulty_buttons:
                pygame.draw.rect(screen, colors["button"], rect, border_radius=12)
                pygame.draw.rect(screen, colors["button_border"], rect, 2, border_radius=12)
                label = font_large.render(text, True, colors["button_text"])
                screen.blit(label, label.get_rect(center=rect.center))

        if settings_open:
            pygame.draw.rect(screen, colors["button"], (200, 200, 400, 300), border_radius=15)
            pygame.draw.rect(screen, colors["button_border"], (200, 200, 400, 300), 3, border_radius=15)

            label = font_large.render("Cài Đặt", True, colors["title"])
            screen.blit(label, label.get_rect(center=(screen.get_width() // 2, 230)))

            for slider, handle, label_text, value in [
                (music_slider, music_handle, "Nhạc nền", setting.volume_music),
                (sound_slider, sound_handle, "Hiệu ứng", setting.volume_sound)
            ]:
                pygame.draw.rect(screen, colors["button"], slider)
                pygame.draw.rect(screen, colors["button_border"], slider, 2)
                pygame.draw.rect(screen, colors["title"], handle)

                label = font_small.render(label_text, True, colors["text"])
                screen.blit(label, (slider.x + 50, slider.y - 50))
                percent = font_small.render(f"{int(value * 100)}%", True, colors["text"])
                screen.blit(percent, (slider.x + slider.width + 10, slider.y - 10))

            close_button = pygame.Rect(350, 470, 100, 40)
            pygame.draw.rect(screen, colors["button"], close_button, border_radius=8)
            pygame.draw.rect(screen, colors["button_border"], close_button, 2, border_radius=8)
            close_text = font_small.render("Đóng", True, colors["button_text"])
            screen.blit(close_text, close_text.get_rect(center=close_button.center))

        draw_icon_button(menu_icon_button, "| |", menu_icon_button.collidepoint(pygame.mouse.get_pos()))

        if menu_open:
            draw_popup_menu(popup_rect, popup_buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN]:
                pos = get_event_pos(event)

                if settings_open:
                    if music_slider.collidepoint(pos) or music_handle.collidepoint(pos):
                        dragging_music = True
                    elif sound_slider.collidepoint(pos) or sound_handle.collidepoint(pos):
                        dragging_sound = True
                    elif close_button.collidepoint(pos):
                        settings_open = False
                        if not menu_open and not game_over:
                            timer.resume()

                elif difficulty_selecting:
                    for rect, text in difficulty_buttons:
                        if rect.collidepoint(pos):
                            run_game(*((4, 4) if text == "Dễ (4x4)" else (6, 6) if text == "Trung Bình (6x6)" else (8, 8)), carry_score=score.points)
                            return

                elif game_over:
                    for rect, text in result_buttons:
                        if rect.collidepoint(pos):
                            if text == "Chơi tiếp":
                                run_game(rows, cols, carry_score=score.points)
                                return
                            elif text == "Chọn độ khó mới":
                                difficulty_selecting = True
                            elif text == "Menu":
                                from menu import show_menu
                                show_menu()
                                return

                elif menu_icon_button.collidepoint(pos):
                    menu_open = not menu_open
                    if menu_open:
                        if not game_over:
                            timer.pause()
                        if board.first_card:
                            board.first_card.flipped = False
                        if board.second_card:
                            board.second_card.flipped = False
                        board.first_card = board.second_card = None
                        board.waiting = False
                    else:
                        if not game_over:
                            timer.resume()

                elif menu_open:
                    for rect, text in popup_buttons:
                        if rect.collidepoint(pos):
                            if text == "Về Menu":
                                return
                            elif text == "Cài Đặt":
                                settings_open = True
                                timer.pause()
                            elif text == "Gợi Ý":
                                if not game_over:
                                    if score.can_use_hint():
                                        hint_pair = board.get_hint_pair()
                                        if hint_pair:
                                            c1, c2 = hint_pair
                                            c1.flipped = True
                                            c2.flipped = True
                                            hint_cards = (c1, c2)
                                            hint_timer = pygame.time.get_ticks()

                                            score.use_hint()
                                            toast_message = "Sử dụng gợi ý thành công!"
                                            toast_timer = pygame.time.get_ticks()
                                        else:
                                            toast_message = "Không còn cặp nào để gợi ý!"
                                            toast_timer = pygame.time.get_ticks()
                                    else:
                                        toast_message = "Không đủ điểm để dùng gợi ý!"
                                        toast_timer = pygame.time.get_ticks()
                                menu_open = False
                                timer.resume()

                elif not game_over and not hint_active:
                    clicked = board.handle_click(pos)
                    if clicked:
                        sounds["flip"].play()

            elif event.type in [pygame.MOUSEBUTTONUP, pygame.FINGERUP]:
                dragging_music = False
                dragging_sound = False

            elif event.type in [pygame.MOUSEMOTION, pygame.FINGERMOTION]:
                pos = get_event_pos(event)
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

        result = board.update()
        if result is True:
            score.add_match()
            sounds["matched"].play()
        elif result is False:
            score.add_mistake()
            sounds["wrong"].play()

        if hint_cards:
            if pygame.time.get_ticks() - hint_timer > 1250:
                c1, c2 = hint_cards
                if not c1.matched:
                    c1.flipped = False
                if not c2.matched:
                    c2.flipped = False
                hint_cards = None

        pygame.display.flip()
        clock.tick(60)
