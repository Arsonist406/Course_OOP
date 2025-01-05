from functions.poker_commands.baseCommand import BaseCommand

class CheckCommand(BaseCommand):
    def __init__(self, player, hash_player_bet):
        super().__init__(player=player, hash_player_bet=hash_player_bet)

    def execute(self):
        self.hash_player_bet[self.player] = str(0)