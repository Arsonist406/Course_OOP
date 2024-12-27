class CallCommand:
    def __init__(self, bank, player, biggest_bet, hash_player_bet):
        self.bank = bank
        self.player = player
        self.biggest_bet = biggest_bet
        self.hash_player_bet = hash_player_bet

    def execute(self):
        self.bank.setBank(self.bank.getBank() + self.biggest_bet - int(self.hash_player_bet[self.player]))
        self.player.setChips(self.player.getChips() - self.biggest_bet + int(self.hash_player_bet[self.player]))
        self.hash_player_bet[self.player] = str(self.biggest_bet)