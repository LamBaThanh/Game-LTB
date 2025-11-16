import pygame

class GameTimer:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        self.start_time = None
        self.paused = False
        self.pause_time = 0

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = 0

    def pause(self):
        if not self.paused:
            self.pause_time = pygame.time.get_ticks()
            self.paused = True

    def resume(self):
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_time
            self.start_time += paused_duration
            self.paused = False

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        if self.paused:
            return (self.pause_time - self.start_time) // 1000
        else:
            return (pygame.time.get_ticks() - self.start_time) // 1000

    def get_remaining_time(self):
        return max(0, self.time_limit - self.get_elapsed_time())

    def is_time_up(self):
        return self.get_remaining_time() <= 0
