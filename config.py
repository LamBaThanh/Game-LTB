import pygame,sys, os

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 800, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Lật Thẻ Bài")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

colors = {
    "background": (15, 15, 30),

    "card_front": (240, 240, 255),
    "card_back": (0, 120, 200),
    "card_border": (200, 200, 255),
    "matched_overlay": (255, 200, 50, 120),

    "button": (60, 60, 128),
    "button_hover": (80, 170, 220),
    "button_border": (220, 220, 255),
    "button_text": (240, 240, 255),

    "text": (230, 230, 240),
    "text_score": (255, 50, 50),
    "title": (255, 220, 100),

    "red": (255, 50, 50),
    "green": (118, 201, 94),
    "blue": (80, 80, 255),
    "yellow": (255, 170, 0),
    "purple": (180, 0, 255),
}


shapes = ["circle", "square", "triangle", "star", "hexagon"]
shape_colors = ["red", "green", "blue", "yellow", "purple"]
shape_color_combinations = [(shape, colors[color]) for shape in shapes for color in shape_colors]

pygame.font.init()
font_huge = pygame.font.SysFont('tahoma', 72)
font_large = pygame.font.SysFont('tahoma', 36)
font_small = pygame.font.SysFont('tahoma', 28)

clock = pygame.time.Clock()

background_img = pygame.transform.scale(pygame.image.load(resource_path("assets/pictures/bg2.jpg")).convert(), (screen.get_width(), screen.get_height()))

volume_music = 0.15
volume_sound = 0.5

sounds = {
    "matched": pygame.mixer.Sound(resource_path("assets/sounds/matched.mp3")),
    "wrong": pygame.mixer.Sound(resource_path("assets/sounds/wrong.mp3")),
    "flip": pygame.mixer.Sound(resource_path("assets/sounds/flip.mp3")),
    "win": pygame.mixer.Sound(resource_path("assets/sounds/win.mp3")),
    "lose": pygame.mixer.Sound(resource_path("assets/sounds/lose.mp3")),
}

for sound in sounds.values():
    sound.set_volume(volume_music)
    sound.set_volume(volume_sound)

pygame.mixer.music.load(resource_path("assets/sounds/bgm1.mp3"))
pygame.mixer.music.set_volume(volume_music)
pygame.mixer.music.play(-1)
