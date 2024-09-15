import random

class Roulette():
    def __init__(self):
        choices = [n for n in range(37)]
        self.current_roll = None
        self.choices = choices
        self.round = 1
    
    def roll(self):
        index = random.randint(0, len(self.choices) - 1)
        self.current_roll = self.choices[index]

    def has_won(self, is_even: bool = True):
        remainder = 0 if is_even else 1
        if self.current_roll % 2 == remainder and self.current_roll != 0:
            return True
        return False