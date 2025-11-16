import pygame,random,math
from config import screen, screen_width, colors, font_small, font_huge

def draw_button(rect, text, hover=False):
    color = colors["button_hover"] if hover else colors["button"]
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, colors["button_border"], rect, 2, border_radius=12)
    label = font_small.render(text, True, colors["button_text"])
    screen.blit(label, label.get_rect(center=rect.center))


def draw_icon_button(rect, icon_text, hover=False):
    color = colors["button_hover"] if hover else colors["button"]
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, colors["button_border"], rect, 2, border_radius=12)
    label = font_small.render(icon_text, True, colors["button_text"])
    screen.blit(label, label.get_rect(center=rect.center))


def draw_info_panel(score, timer):
    time_text = font_small.render(f"Thời gian: {timer.get_remaining_time()}s", True, colors["text"])
    score_text = font_small.render(f"Điểm: {score.points}", True, colors["text"])

    screen.blit(time_text, (screen_width - 250, 20))
    screen.blit(score_text, (screen_width - 250, 50))


def draw_result_popup(result_text, final_score, buttons):
    result_label = font_huge.render(result_text, True, colors["title"])
    screen.blit(result_label, result_label.get_rect(center=(screen_width // 2, 200)))

    score_label = font_small.render(f"Điểm: {final_score}", True, colors["text_score"])
    screen.blit(score_label, score_label.get_rect(center=(screen_width // 2, 260)))

    for rect, text in buttons:
        pygame.draw.rect(screen, colors["button"], rect, border_radius=12)
        pygame.draw.rect(screen, colors["button_border"], rect, 2, border_radius=12)
        label = font_small.render(text, True, colors["button_text"])
        screen.blit(label, label.get_rect(center=rect.center))


def draw_popup_menu(menu_rect, buttons):
    pygame.draw.rect(screen, colors["background"], menu_rect, border_radius=15)
    pygame.draw.rect(screen, colors["button_border"], menu_rect, 2, border_radius=15)
    for rect, text in buttons:
        draw_button(rect, text, rect.collidepoint(pygame.mouse.get_pos()))

def draw_toast(message, start_time, duration=2000):
    if message and pygame.time.get_ticks() - start_time < duration:
        toast_surface = font_small.render(message, True, colors["text"])
        rect = toast_surface.get_rect(center=(screen.get_width() // 2, 100))
        pygame.draw.rect(screen, colors["button"], rect.inflate(20, 10), border_radius=8)
        pygame.draw.rect(screen, colors["button_border"], rect.inflate(20, 10), 2, border_radius=8)
        screen.blit(toast_surface, rect)
        return True
    return False

class Firework:
    def __init__(self, pos, particle_count=50, speed_range=(2, 5)):
        self.particles = []
        self.create(pos, particle_count, speed_range)

    def create(self, pos, particle_count, speed_range):
        for _ in range(particle_count):
            angle = random.uniform(0, 360)
            speed = random.uniform(*speed_range)
            vector = pygame.math.Vector2(speed, 0).rotate(angle)
            color = random.choice([
                colors["red"], colors["green"], colors["blue"],
                colors["yellow"], colors["purple"]
            ])
            self.particles.append([pos[0], pos[1], vector.x, vector.y, color, 255])

    def update(self):
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[5] -= 4
        self.particles = [p for p in self.particles if p[5] > 0]

    def draw(self):
        for p in self.particles:
            s = pygame.Surface((5, 5), pygame.SRCALPHA)
            s.fill((*p[4], max(0, p[5])))
            screen.blit(s, (p[0], p[1]))

    def is_finished(self):
        return len(self.particles) == 0

