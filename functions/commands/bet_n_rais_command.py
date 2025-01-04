from functions.commands.command import Command

class BetNRaisCommand(Command):
    def __init__(self, bank, player, player_bet, hash_player_bet):
        super().__init__()
        self.bank = bank
        self.player = player
        self.player_bet = player_bet
        self.hash_player_bet = hash_player_bet

    def execute(self):
        self.bank.setBank(self.bank.getBank() + int(self.player_bet))
        self.player.setChips(self.player.getChips() - int(self.player_bet))
        self.hash_player_bet[self.player] = str(int(self.hash_player_bet[self.player]) + int(self.player_bet))
