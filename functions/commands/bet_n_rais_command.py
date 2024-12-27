class BetCommand:
    def __init__(self, bank, player_bet, player):
        self.bank = bank
        self.player_bet = player_bet
        self.player = player_bet

    def execute(self):
        self.bank.setBank(self.bank.getBank() + int(self.player_bet))
        player.setChips(player.getChips() - int(self.player_bet))
        self.hash_player_bet[player] = str(int(self.hash_player_bet[player]) + int(self.player_bet))

        pygame.image.save(self.screen,
                          "D:\\Шарага\\Проекти_на_пітоні\\Course_OOP_v2\\icons\\backgrounds\\table_with_players_info.png")
        func = LoadImage(
            "D:\\Шарага\\Проекти_на_пітоні\\Course_OOP_v2\\icons\\backgrounds\\table_with_players_info.png",
            (1280, 720))
        self.table_image = func.execute()