import pygame

def draw_shape(surface, shape, color, center, size):
    x, y = center
    if shape == "circle":
        pygame.draw.circle(surface, color, center, size)
    elif shape == "square":
        rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
        pygame.draw.rect(surface, color, rect, border_radius=8)
    elif shape == "triangle":
        points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
        pygame.draw.polygon(surface, color, points)
    elif shape == "star":
        points = [
            (x, y - size),
            (x + size * 0.3, y - size * 0.3),
            (x + size, y - size * 0.3),
            (x + size * 0.5, y + size * 0.1),
            (x + size * 0.7, y + size),
            (x, y + size * 0.5),
            (x - size * 0.7, y + size),
            (x - size * 0.5, y + size * 0.1),
            (x - size, y - size * 0.3),
            (x - size * 0.3, y - size * 0.3),
        ]
        pygame.draw.polygon(surface, color, points)
    elif shape == "hexagon":
        points = [
            (x - size, y),
            (x - size // 2, y - int(size * 0.87)),
            (x + size // 2, y - int(size * 0.87)),
            (x + size, y),
            (x + size // 2, y + int(size * 0.87)),
            (x - size // 2, y + int(size * 0.87)),
        ]
        pygame.draw.polygon(surface, color, points)
