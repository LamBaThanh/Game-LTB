import pygame
from config import screen, colors
from util import draw_shape

class Card:
    def __init__(self, rect, shape, color):
        self.rect = rect
        self.shape = shape
        self.color = color
        self.flipped = False
        self.matched = False

    def draw(self):
        if self.matched:
            return
        pygame.draw.rect(screen, colors["card_front"] if self.flipped else colors["card_back"], self.rect, border_radius=10)
        pygame.draw.rect(screen, colors["card_border"], self.rect, 2, border_radius=10)

        if self.flipped:
            center = self.rect.center
            size = self.rect.width // 2 - 10
            draw_shape(screen, self.shape, self.color, center, size)
