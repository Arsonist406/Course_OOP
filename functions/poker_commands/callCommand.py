from functions.poker_commands.baseCommand import BaseCommand

class CallCommand(BaseCommand):
    def __init__(self, bank, player, biggest_bet, hash_player_bet):
        super().__init__(bank, player, hash_player_bet)
        self.biggest_bet = biggest_bet

    def execute(self):
        if self.player.getChips() < self.biggest_bet:
            self.bank.setBank(self.bank.getBank() + self.player.getChips())
            self.player.setChips(0)
            self.hash_player_bet[self.player] = "All in"
        else:
            self.bank.setBank(self.bank.getBank() + self.biggest_bet - int(self.hash_player_bet[self.player]))
            self.player.setChips(self.player.getChips() - self.biggest_bet + int(self.hash_player_bet[self.player]))
            self.hash_player_bet[self.player] = str(self.biggest_bet)