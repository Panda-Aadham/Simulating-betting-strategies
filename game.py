import random

class Game:
    def __init__(self, choices: list):
        self.choices = choices
        self.current_roll = None
    
    def roll(self):
        index = random.randint(0, len(self.choices) - 1)
        print(index)
        self.current_roll = self.choices[index]
        print(self.current_roll)
