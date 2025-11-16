class ScoreManager:
    def __init__(self, carry_score=0):
        self.matches = 0
        self.mistakes = 0
        self.points = carry_score

    def add_match(self):
        self.matches += 1
        self.points += 100

    def add_mistake(self):
        self.mistakes += 1
        self.points -= 5
        if self.points < 0:
            self.points = 0

    def calculate_final_score(self, remaining_time):
        if not hasattr(self, 'finalized'):
            bonus = remaining_time * 5
            self.points += bonus
            self.finalized = True
        return self.points


    def can_use_hint(self):
        return self.points >= 600

    def use_hint(self):
        if self.can_use_hint():
            self.points -= 600
            return True
        return False
