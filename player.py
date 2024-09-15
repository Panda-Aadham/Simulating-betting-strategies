from roulette import Roulette


class Player:
    def __init__(self, bankroll, initial_bet, rounds = 1000):
        self.max_consecutive_losses = 0
        self.initial_bet = initial_bet
        self.bankroll = bankroll
        self.max_round = rounds
        self.game = Roulette()

    def martingale_system(self):
        previous_bet = None
        consecutive_losses = 0
        while self.bankroll > 0 and self.game.round < self.max_round:
            if previous_bet is not None:
                bet = previous_bet * 2
            else: bet = self.initial_bet
            
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

losses = 0
for i in range(100):
    player = Player(10000, 0.25)
    player.martingale_system()
    if player.bankroll < 0:
        print(player.max_consecutive_losses)
        losses += 1

print("Lost", losses)