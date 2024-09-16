from roulette import Roulette


class Player:
    def __init__(self, bankroll, rounds = 1000):
        self.max_consecutive_losses = 0
        self.bankroll = bankroll
        self.max_round = rounds
        self.game = Roulette()
    
    def print_round(self, bet):
        print(f"Bet: {bet} - {'Won' if self.game.has_won() else 'Lost'} - Bank {self.bankroll}")

    # Initial bet as int or float
    def martingale_system(self, initial_bet):
        previous_bet = None
        consecutive_losses = 0
        
        while self.bankroll > 0 and self.game.round < self.max_round:
            if previous_bet is not None:
                bet = previous_bet * 2
            else: bet = initial_bet
            
            self.game.roll()
            if self.game.has_won():
                consecutive_losses = 0
                previous_bet = None
                self.bankroll += bet
                self.game.round += 1
            else:
                consecutive_losses += 1
                if consecutive_losses > self.max_consecutive_losses:
                    self.max_consecutive_losses = consecutive_losses
                previous_bet = bet
                self.bankroll -= bet
    
    # Base unit percentage as float n where 0 <= n <= 1 
    def d_alembert_system(self, base_unit):
        base_value = self.bankroll * base_unit
        consecutive_losses = 0
        units = 1

        while self.bankroll > 0 and self.game.round < self.max_round:
            bet = base_value * units
            self.game.roll()

            if self.game.has_won():
                consecutive_losses = 0
                self.bankroll += bet
                self.game.round += 1
                if units != 1:
                    units -= 1
            else:
                consecutive_losses += 1
                if consecutive_losses > self.max_consecutive_losses:
                    self.max_consecutive_losses = consecutive_losses
                self.bankroll -= bet
                units += 1

losses = 0
repeat = 100
for i in range(repeat):
    player = Player(10000)
    player.martingale_system(initial_bet=1)
    if player.bankroll < 0:
        losses += 1

print("Lost", losses, "- with martingale system")

losses = 0
for i in range(1):
    player = Player(10000, 25)
    player.d_alembert_system(base_unit=0.01)
    if player.bankroll < 0:
        losses += 1

print("Lost", losses, "- with d'alembert system")