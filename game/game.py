import pygame
from bank.bank import Bank
from cards.card import Card
from deck.deck import Deck
from functions.commands.bet_n_rais_command import BetNRaisCommand
from functions.commands.callCommand import CallCommand
from functions.commands.foldCommand import FoldCommand
from table.table import Table
from players.player import Player

import ctypes
from ctypes import POINTER, c_void_p, c_int, c_char_p
lib = ctypes.CDLL('cpp/lib/comb_calculator.dll')
class CtypesCard(ctypes.Structure):
    _fields_ = [("suit", ctypes.c_char_p), ("value", ctypes.c_char_p)]

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
        self.winner_comb = ""

        self.table = Table(self.screen, self.players_for_game, self.bank, self.deck, self.table_cards, self.hash_player_bet)

    def how_many_active_players(self):
        active_players = 0
        for player2 in self.players:
            if player2.getIs_active():
                active_players += 1
        return active_players

    def py_list_to_c_array_convert(self, list):
        array = (CtypesCard * len(list))(*[CtypesCard(card.getSuit().encode('utf-8'),
                                                            card.getValue().encode('utf-8')) for card in list])
        return array

    def c_interface_init(self):
        lib.CombinationSearcher_create.argtypes = [ctypes.POINTER(CtypesCard), ctypes.c_int,
                                                   ctypes.POINTER(CtypesCard), ctypes.c_int]
        lib.CombinationSearcher_create.restype = ctypes.c_void_p

        lib.CombinationSearcher_execute.argtypes = [ctypes.c_void_p]
        lib.CombinationSearcher_execute.restype = ctypes.c_char_p

        lib.CombinationSearcher_getCombScore.argtypes = [ctypes.c_void_p]
        lib.CombinationSearcher_getCombScore.restype = ctypes.c_int

        lib.CombinationSearcher_destroy.argtypes = [ctypes.c_void_p]
        lib.CombinationSearcher_destroy.restype = None

    def found_winner(self, list_of_potential_winners):
        # Ініціалізація інтерфейсу для взаємодії з класом CombinationSearcher
        self.c_interface_init()

        # Перетворення table_cards (list) в table_cards_array (ctypes array)
        table_cards_array = self.py_list_to_c_array_convert(self.table_cards)
        # Створення вказівника на table_cards_array
        table_cards_ptr = ctypes.cast(table_cards_array, ctypes.POINTER(CtypesCard))

        table_comb_searcher = lib.CombinationSearcher_create(table_cards_ptr, len(table_cards_array), None, 0)
        try:
            table_comb_bytes = lib.CombinationSearcher_execute(table_comb_searcher)
            table_comb = table_comb_bytes.decode('utf-8')

            table_comb_score = lib.CombinationSearcher_getCombScore(table_comb_searcher)
        finally:
            # Звільнення пам'яті
            lib.CombinationSearcher_destroy(table_comb_searcher)

        hash_player_comb = {}
        for player in list_of_potential_winners:
            # Перетворення list(player.getHand()) в hand_array (ctypes array)
            hand_array = self.py_list_to_c_array_convert(list(player.getHand()))
            # Створення вказівника на hand_array
            hand_ptr = ctypes.cast(hand_array, ctypes.POINTER(CtypesCard))

            comb_searcher = lib.CombinationSearcher_create(table_cards_ptr, len(table_cards_array), hand_ptr, len(hand_array))
            try:
                player_comb_bytes = lib.CombinationSearcher_execute(comb_searcher)
                player_comb = player_comb_bytes.decode('utf-8')

                player_comb_score = lib.CombinationSearcher_getCombScore(comb_searcher)

                hash_player_comb[player] = (player_comb, player_comb_score)
            finally:
                # Звільнення пам'яті
                lib.CombinationSearcher_destroy(comb_searcher)

        potential_draw = 0
        potential_draw_with_need_of_find_high_card = 0
        player_greatest_comb = []
        for player, comb in hash_player_comb.items():
            if comb[0] == "Royal flush":
                winner = [player]
                return winner

            if ((table_comb == comb[0] and table_comb_score == comb[1]) and
               (table_comb == "Straight flush" or table_comb == "Flush" or
                table_comb == "Straight" or table_comb == "Full house")):
                potential_draw += 1
                continue
            elif ((table_comb == comb[0] and table_comb_score == comb[1]) and
                 (table_comb == "Four of a kind" or table_comb == "Three of a kind" or
                  table_comb == "Two pair" or table_comb == "Pair")):
                potential_draw_with_need_of_find_high_card += 1
                continue

            if len(player_greatest_comb) == 0:
                player_greatest_comb.append((player, comb))
            else:
                if player_greatest_comb[0][1][0] == comb[0] and player_greatest_comb[0][1][1] == comb[1]:
                    player_greatest_comb.append((player, comb))
                elif player_greatest_comb[0][1][0] == comb[0] and player_greatest_comb[0][1][1] < comb[1]:
                    player_greatest_comb.clear()
                    player_greatest_comb.append((player, comb))
                elif player_greatest_comb[0][1][0] == comb[0] and player_greatest_comb[0][1][1] > comb[1]:
                    continue
                else:
                    comb_order = {'High': 1, 'Pair': 2, 'Two pair': 3, 'Three of a kind': 4, 'Straight': 5, 'Flush': 6,
                                  'Full house': 7, 'Four of a kind': 8, 'Straight flush': 9, 'Royal flush': 10}

                    greatest_comb_power = comb_order[player_greatest_comb[0][1][0]]
                    present_comb_power = comb_order[comb[0]]

                    if present_comb_power > greatest_comb_power:
                        player_greatest_comb.clear()
                        player_greatest_comb.append((player, comb))
                    elif present_comb_power < greatest_comb_power:
                        continue

        # Перевіряємо на ПОВНУ нічию
        if potential_draw == len(list_of_potential_winners):
            self.winner_comb = table_comb
            return list_of_potential_winners

        elif potential_draw_with_need_of_find_high_card == len(list_of_potential_winners):
            values_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

            player_score = []
            for player in list_of_potential_winners:
                first_card_score = values_order[player.getHand()[0].getValue()]
                second_card_score = values_order[player.getHand()[1].getValue()]
                if first_card_score > second_card_score:
                    player_score.append((player, first_card_score))
                elif second_card_score > first_card_score:
                    player_score.append((player, second_card_score))

            player_score = sorted(player_score, key=lambda x: x[1])
            last_elem = player_score[len(player_score) - 1]
            list_if_winners = []
            # Знаходимо гравців з найвагомішою картою
            for elem in reversed(player_score):
                if last_elem[1] == elem[1]:
                    list_if_winners.append(elem[0])

            self.winner_comb = table_comb
            return list_if_winners

        else:
            list_if_winners = []
            if len(player_greatest_comb) == 1:
                list_if_winners.append(player_greatest_comb[0][0])
            else:
                values_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                                '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

                player_score = []
                for player, comb in player_greatest_comb:
                    first_card_score = values_order[player.getHand()[0].getValue()]
                    second_card_score = values_order[player.getHand()[1].getValue()]
                    player_score.append((player, first_card_score + second_card_score))

                player_score = sorted(player_score, key=lambda x: x[1])
                last_elem = player_score[len(player_score) - 1]
                # Знаходимо гравців з найвагомішою картою
                for elem in reversed(player_score):
                    if last_elem[1] == elem[1]:
                        list_if_winners.append(elem[0])

            self.winner_comb = player_greatest_comb[0][1][0]
            return list_if_winners

    def command_execute(self, command_name, player):
        if command_name == "Fold":
            command = FoldCommand(self.screen, self.table.get_table_image(), self.table.get_card_back_image(),
                                  self.table.get_hash_player_pos(), self.table.get_deck_pos(), self.players, player)
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

                    list_of_potential_winners = []
                    for player in self.players:
                        if player.getIs_active():
                            self.table.open_player_cards(player)
                            list_of_potential_winners.append(player)

                    winners = self.found_winner(list_of_potential_winners)

                    if len(winners) == 1:
                        winners[0].setChips(winners[0].getChips() + self.bank.getBank())
                        self.table.print_player_chips(winners[0])
                    else:
                        for winner in winners:
                            winner.setChips(winner.getChips() + (self.bank.getBank() // len(winners)))
                            self.table.print_player_chips(winner)

                    self.bank.setBank(0)
                    self.table.print_bank()
                    self.table.show_winner_banner(winners, self.winner_comb)

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
                    winner = [winner]
                    self.table.show_winner_banner(winner, self.winner_comb)
                    self.table.clear_table(stage)
                    break

            if self.command_name == "Exit":
                break