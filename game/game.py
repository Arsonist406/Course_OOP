import pygame
from bank.bank import Bank
from cards.card import Card
from deck.deck import Deck
from functions.combination_searchers.table_combination_searcher import Table_Combination_Searcher
from functions.commands.bet_n_rais_command import BetNRaisCommand
from functions.commands.callCommand import CallCommand
from functions.commands.foldCommand import FoldCommand
from table.table import Table
from players.player import Player


class Game:
    def __init__(self, screen, amount_of_players, names):
        self.screen = screen
        pygame.display.set_caption("Гра")

        self.names = names
        self.players = []
        self.hash_player_bet = {}
        i = 0
        while i != amount_of_players:
            self.players.append(Player(self.names[i], (Card(None, None), Card(None, None)), 1000000))
            i += 1

        self.players_for_game = self.players

        self.deck = Deck()
        self.bank = Bank()
        self.biggest_bet = 0
        self.table_cards = [None] * 5
        self.playing = True
        self.command_name = None

        self.table = Table(self.screen, self.players_for_game, self.deck, self.bank, self.table_cards, self.hash_player_bet)

    def how_many_active_players(self):
        active_players = 0
        for player2 in self.players:
            if player2.getIs_active():
                active_players += 1
        return active_players

    def command_execute(self, command_name, player):
        if command_name == "Fold":
            command = FoldCommand(self.screen, self.table.get_table_image(), self.table.get_card_back_image(),
                                  self.table.get_hash_player_pos(), self.table.get_hash_player_ang(),
                                  self.table.get_discard_deck_pos(), self.players, player)
            command.execute()

        elif command_name == "Call":
            command = CallCommand(self.bank, player, self.biggest_bet, self.hash_player_bet)
            command.execute()

        elif command_name == "Bet" or command_name == "Rais":
            command = BetNRaisCommand(self.bank, player, self.table.get_player_bet(), self.hash_player_bet)
            command.execute()

    def execute(self):
        self.table.create_table()

        while self.playing:
            self.deck.shuffleCards()

            for player in self.players:
                self.hash_player_bet[player] = "0"
                self.table.print_player_info(player)

            pygame.display.update()

            self.table.card_deal_for_players()
            self.table.board_deal()

            i = 0
            for player in self.players:
                first = self.deck.getCards()[i]
                i += 1
                second = self.deck.getCards()[i]
                i += 1
                player.setHand((first, second))
                player.setIs_active(True)

            self.table_cards.clear()
            for j in range(i, len(self.players) * 2 + 5):
                self.table_cards.append(self.deck.getCards()[j])

            winner = None

            stages = ["Pre-flop", "Flop", "Turn", "River", "Showdown"]
            for stage in stages:
                self.biggest_bet = 0
                self.table.print_bank()

                for player in self.players:
                    self.hash_player_bet[player] = "0"
                    self.table.print_player_info(player)

                if stage == "Pre-flop":
                    print("Pre-flop")

                elif stage == "Flop":
                    print("Flop")
                    self.table.open_board_card(0)
                    self.table.open_board_card(1)
                    self.table.open_board_card(2)

                elif stage == "Turn":
                    print("Turn")
                    self.table.open_board_card(3)

                elif stage == "River":
                    print("River")
                    self.table.open_board_card(4)

                elif stage == "Showdown":
                    print("Showdown")

                    for player in self.players:
                        if player.getIs_active():
                            self.table.open_player_cards(player)

                    func = Table_Combination_Searcher(self.table_cards)
                    table_comb = func.execute()
                    print(table_comb)
                    pygame.time.delay(2000 * len(self.players))

                    self.table.clear_table(stage)
                    break

                betting = True # Торги
                while betting:
                    for player in self.players:
                        if self.how_many_active_players() == 1:
                            break
                        else:
                            if player.getIs_active():
                                self.table.print_bank()
                                self.table.print_player_info(player)
                                self.table.draw_nimbus(player)

                                self.biggest_bet = max(int(value) for value in self.hash_player_bet.values())

                                self.command_name = self.table.turn(player)
                                if self.command_name == "Exit":
                                    break

                                self.command_execute(self.command_name, player)

                                self.table.print_bank()
                                self.table.print_player_info(player)
                                self.biggest_bet = max(int(value) for value in self.hash_player_bet.values())

                    if self.command_name == "Exit":
                        break

                    # Якщо один гравець активний (інші зафолдили), цього гравця визначаємо переможцем
                    if self.how_many_active_players() == 1:
                        for player in self.players:
                            if player.getIs_active():
                                winner = player
                                break

                        winner.setChips(winner.getChips() + self.bank.getBank())
                        self.bank.setBank(0)
                        break

                    if winner is not None:
                        break
                    else:
                        hash_player_bet = {}
                        for player in self.players:
                            if player.getIs_active():
                                hash_player_bet[player] = self.hash_player_bet[player]

                        values = [int(value) for value in hash_player_bet.values()]
                        all_equal = all(value == values[0] for value in values)

                        # Якщо не у всіх ставки рівні - продовжуємо торги
                        betting = not all_equal

                if self.command_name == "Exit":
                    break

                if winner is not None:
                    self.table.print_bank()
                    for player in self.players:
                        self.table.print_player_info(player)
                    self.table.clear_table(stage)
                    break

            if self.command_name == "Exit":
                break