from functions.commands.command import Command

class CheckCommand(Command):
    def __init__(self, hash_player_bet, player):
        super().__init__()
        self.hash_player_bet = hash_player_bet
        self.player = player

    def execute(self):
        self.hash_player_bet[self.player] = str(0)