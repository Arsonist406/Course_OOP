from functions.poker_commands.baseCommand import BaseCommand

class BetNRaisCommand(BaseCommand):
    def __init__(self, bank, player, player_bet, hash_player_bet):
        super().__init__(bank, player, hash_player_bet)
        self.player_bet = player_bet

    def execute(self):
        self.bank.setBank(self.bank.getBank() + int(self.player_bet))
        self.player.setChips(self.player.getChips() - int(self.player_bet))
        self.hash_player_bet[self.player] = str(int(self.hash_player_bet[self.player]) + int(self.player_bet))
