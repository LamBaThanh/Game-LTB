import pygame, random
from card import Card
from config import screen_width, screen_height, shape_color_combinations

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.first_card = None
        self.second_card = None
        self.waiting = False
        self.wait_start_time = 0
        self.wait_time = 800
        self.card_size = 80 if max(rows, cols) <= 6 else 60
        self.padding = 10
        self.create_cards()

    def create_cards(self):
        total_cards = self.rows * self.cols
        if (self.rows, self.cols) == (4, 4):
            group_size = 4
            num_groups = total_cards // 4
        elif (self.rows, self.cols) == (6, 6):
            group_size = 6
            num_groups = total_cards // 6
        else:
            group_size = 8
            num_groups = total_cards // 8

        selected_pairs = random.sample(shape_color_combinations, num_groups)
        values = selected_pairs * group_size
        random.shuffle(values)

        grid_width = self.cols * self.card_size + (self.cols - 1) * self.padding
        grid_height = self.rows * self.card_size + (self.rows - 1) * self.padding
        offset_x = (screen_width - grid_width) // 2
        offset_y = (screen_height - grid_height) // 2 + 30

        index = 0
        for row in range(self.rows):
            row_cards = []
            for col in range(self.cols):
                x = offset_x + col * (self.card_size + self.padding)
                y = offset_y + row * (self.card_size + self.padding)
                rect = pygame.Rect(x, y, self.card_size, self.card_size)
                shape, color = values[index]
                row_cards.append(Card(rect, shape, color))
                index += 1
            self.cards.append(row_cards)

    def draw(self):
        for row in self.cards:
            for card in row:
                card.draw()

    def handle_click(self, pos):
        if self.waiting:
            return None

        for row in self.cards:
            for card in row:
                if card.rect.collidepoint(pos) and not card.flipped and not card.matched:
                    card.flipped = True
                    if not self.first_card:
                        self.first_card = card
                    elif not self.second_card:
                        self.second_card = card
                        self.waiting = True
                        self.wait_start_time = pygame.time.get_ticks()
                    return card
        return None

    def update(self):
        if self.waiting and pygame.time.get_ticks() - self.wait_start_time > self.wait_time:
            match = False
            if (self.first_card.shape == self.second_card.shape) and (self.first_card.color == self.second_card.color):
                self.first_card.matched = self.second_card.matched = True
                match = True
            else:
                self.first_card.flipped = self.second_card.flipped = False

            self.first_card = self.second_card = None
            self.waiting = False
            return match
        return None

    def all_matched(self):
        return all(card.matched for row in self.cards for card in row)
    
    def find_matching_card(self, target_card):
        for row in self.cards:
            for card in row:
                if card is not target_card and not card.matched:
                    if card.shape == target_card.shape and card.color == target_card.color:
                        return card
        return None
    
    def get_hint_pair(self):
        for row in self.cards:
            for card in row:
                if not card.matched:
                    match = self.find_matching_card(card)
                    if match:
                        return (card, match)
        return None
