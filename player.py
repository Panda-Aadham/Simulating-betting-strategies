from roulette import Roulette
import numpy as np


def matrix_power(matrix, n):
    result = np.eye(2, dtype=int)
    while n:
        if n % 2:
            result = np.dot(result, matrix)
        matrix = np.dot(matrix, matrix)
        n //= 2
    return result

def fast_fibonacci(n):
    if n == 0:
        return 0
    matrix = np.array([[1, 1], [1, 0]], dtype=int)
    return matrix_power(matrix, n-1)[0, 0]


class Player:
    def __init__(self, bankroll, rounds = 1000):
        self.max_consecutive_losses = 0
        self.bankroll = bankroll
        self.max_round = rounds
        self.game = Roulette()
    
    def print_round(self, bet):
        print(f"Round {self.game.round} - Bet: {bet} - {'Won' if self.game.has_won() else 'Lost'} - Bank {self.bankroll}")

    # Initial bet as int or float
    def martingale_system(self, initial_bet):
        previous_bet = None
        consecutive_losses = 0
        
        while self.bankroll > 0 and self.game.round < self.max_round:
            if previous_bet is not None:
                bet = previous_bet * 2
            else: bet = initial_bet
            bet = min(self.bankroll, bet)
            
            self.game.roll()
            if self.game.has_won():
                consecutive_losses = 0
                previous_bet = None
                self.bankroll += bet
                self.game.round += 1
            else:
                consecutive_losses += 1
                previous_bet = bet
                self.bankroll -= bet
                if consecutive_losses > self.max_consecutive_losses:
                    self.max_consecutive_losses = consecutive_losses
    
    # Base unit percentage as float n where 0 <= n <= 1 
    def d_alembert_system(self, base_unit):
        base_value = self.bankroll * base_unit
        consecutive_losses = 0
        units = 1

        while self.bankroll > 0 and self.game.round < self.max_round:
            bet = base_value * units
            bet = min(self.bankroll, bet)
            self.game.roll()

            if self.game.has_won():
                consecutive_losses = 0
                self.bankroll += bet
                self.game.round += 1
                if units != 1:
                    units -= 1
            else:
                consecutive_losses += 1
                self.bankroll -= bet
                units += 1
                if consecutive_losses > self.max_consecutive_losses:
                    self.max_consecutive_losses = consecutive_losses
    
    # Base unit percentage as float n where 0 <= n <= 1 
    def fibonacci_system(self, base_unit):
        base_value = self.bankroll * base_unit
        consecutive_losses = 0
        units = 1

        while self.bankroll > 0 and self.game.round < self.max_round:
            bet = base_value * fast_fibonacci(units + 1)
            bet = min(self.bankroll, bet)
            self.game.roll()

            if self.game.has_won():
                consecutive_losses = 0
                self.bankroll += bet
                self.game.round += 1
                if units != 1:
                    units = max(1, units - 2)
            else:
                consecutive_losses += 1
                self.bankroll -= bet
                units += 1
                if consecutive_losses > self.max_consecutive_losses:
                    self.max_consecutive_losses = consecutive_losses
    
    def labouchere_system(self, target):
        divisor = 10
        nums = [target/divisor for _ in range(divisor)]

        consecutive_losses = 0
        while (self.game.round < self.max_round
               and self.bankroll > 0
               and len(nums) > 0):
            bet = nums[0] + nums[-1]
            bet = min(self.bankroll, bet)

            self.game.roll()
            if self.game.has_won():
                nums = nums[1:-1]
                consecutive_losses = 0
                self.bankroll += bet
                self.game.round += 1
            else:
                consecutive_losses += 1
                self.bankroll -= bet
                nums.append(bet)
                if consecutive_losses > self.max_consecutive_losses:
                    self.max_consecutive_losses = consecutive_losses
            # self.print_round(bet)


repeat = 100
bankroll = 10000

losses = 0
for _ in range(repeat):
    player = Player(bankroll)
    player.labouchere_system(target=500)
    if player.bankroll <= 0:
        losses += 1

print("Lost", losses, "- with labouchere system")

losses = 0
for _ in range(repeat):
    player = Player(bankroll)
    player.martingale_system(initial_bet=1)
    if player.bankroll <= 0:
        losses += 1

print("Lost", losses, "- with martingale system")

losses = 0
for _ in range(repeat):
    player = Player(bankroll)
    player.fibonacci_system(base_unit=0.001)
    if player.bankroll <= 0:
        losses += 1

print("Lost", losses, "- with fibonacci system")

losses = 0
for _ in range(repeat):
    player = Player(bankroll)
    player.d_alembert_system(base_unit=0.01)
    if player.bankroll <= 0:
        losses += 1

print("Lost", losses, "- with d'alembert system")