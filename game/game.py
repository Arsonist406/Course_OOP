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

    def found_winner(self, players):
        # Ініціалізація інтерфейсу для взаємодії з класом CombinationSearcher
        self.c_interface_init()

        # Перетворення table_cards (list) в table_cards_array (ctypes array)
        table_cards_array = self.py_list_to_c_array_convert(self.table_cards)
        # Створення вказівника на table_cards_array
        table_cards_ptr = ctypes.cast(table_cards_array, ctypes.POINTER(CtypesCard))

        # Знаходження найзначущих комбінацій гравіцв
        hash_player_comb_str_int = {}
        for player in players:
            hand = list(player.getHand())
            # Перетворення hand (list) в hand_array (ctypes array)
            hand_array = self.py_list_to_c_array_convert(hand)
            # Створення вказівника на hand_array
            hand_ptr = ctypes.cast(hand_array, ctypes.POINTER(CtypesCard))

            comb_searcher = lib.CombinationSearcher_create(table_cards_ptr, len(table_cards_array),
                                                           hand_ptr, len(hand_array))
            try:
                # Знаходження найзначущої комбінації в table_cards + hand
                player_comb_bytes = lib.CombinationSearcher_execute(comb_searcher)
                player_comb = player_comb_bytes.decode('utf-8')

                player_comb_score = lib.CombinationSearcher_getCombScore(comb_searcher)

                hash_player_comb_str_int[player] = (player_comb, player_comb_score)
            finally:
                # Звільнення пам'яті
                lib.CombinationSearcher_destroy(comb_searcher)

        comb_order = {'High': 1, 'Pair': 2, 'Two pair': 3, 'Three of a kind': 4, 'Straight': 5, 'Flush': 6,
                      'Full house': 7, 'Four of a kind': 8, 'Straight flush': 9, 'Royal flush': 10}
        hash_player_comb_int_int = {}
        # Перетворення назви комбінації в номер
        for player in players:
            hash_player_comb_int_int[player] = (
            comb_order[hash_player_comb_str_int[player][0]], hash_player_comb_str_int[player][1])

        hash_greatest_comb_players = {}
        for player, comb in hash_player_comb_int_int.items():

            if len(hash_greatest_comb_players) == 0:
                hash_greatest_comb_players[comb] = [player]
            else:
                greatest_comb = next(iter(hash_greatest_comb_players))

                if greatest_comb[0] > comb[0]:
                    continue
                elif greatest_comb[0] < comb[0]:
                    hash_greatest_comb_players.clear()
                    hash_greatest_comb_players[comb] = [player]
                elif greatest_comb[0] == comb[0] and greatest_comb[1] > comb[1]:
                    continue
                elif greatest_comb[0] == comb[0] and greatest_comb[1] < comb[1]:
                    hash_greatest_comb_players.clear()
                    hash_greatest_comb_players[comb] = [player]
                elif greatest_comb[0] == comb[0] and greatest_comb[1] == comb[1]:
                    hash_greatest_comb_players[greatest_comb].append(player)

        list_of_winners = []
        list_of_potential_winners = next(iter(hash_greatest_comb_players.values()))
        greatest_comb_str = hash_player_comb_str_int[list_of_potential_winners[0]][0]
        if len(list_of_potential_winners) == 1:
            list_of_winners = list_of_potential_winners

        elif (greatest_comb_str == "Straight flush" or greatest_comb_str == "Flush" or
              greatest_comb_str == "Straight" or greatest_comb_str == "Full house"):
            list_of_winners = list_of_potential_winners

        elif (greatest_comb_str == "Four of a kind" or greatest_comb_str == "Three of a kind" or
              greatest_comb_str == "Two pair" or greatest_comb_str == "Pair" or greatest_comb_str == "High"):
            values_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

            greatest_hand_score = 0
            for player in list_of_potential_winners:
                first_card_score = values_order[player.getHand()[0].getValue()]
                second_card_score = values_order[player.getHand()[1].getValue()]

                if len(list_of_winners) == 0:
                    list_of_winners.append(player)
                    greatest_hand_score = first_card_score + second_card_score

                elif greatest_hand_score > first_card_score + second_card_score:
                    continue

                elif greatest_hand_score < first_card_score + second_card_score:
                    list_of_winners.clear()
                    list_of_winners.append(player)
                    greatest_hand_score = first_card_score + second_card_score

                elif greatest_hand_score == first_card_score + second_card_score:
                    list_of_winners.append(player)

        self.winner_comb = greatest_comb_str
        return list_of_winners

    def execute(self):
        command = None
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

                # Торги
                while True:
                    for player in self.players:
                        if self.how_many_active_players() == 1:
                            break
                        else:
                            if player.getIs_active():
                                self.table.print_bank()
                                self.table.print_player_info(player)
                                self.table.draw_nimbus(player)

                                self.biggest_bet = max(int(value) for value in self.hash_player_bet.values())

                                command = self.table.turn(player)
                                if command == "Exit":
                                    break

                                command.execute()

                                self.table.print_bank()
                                self.table.print_player_info(player)
                                self.biggest_bet = max(int(value) for value in self.hash_player_bet.values())

                    if command == "Exit":
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
                        if all_equal:
                            break

                if command == "Exit":
                    break

                if winner is not None:
                    self.table.print_bank()
                    for player in self.players:
                        self.table.print_player_info(player)
                    winner = [winner]
                    self.table.show_winner_banner(winner, self.winner_comb)
                    self.table.clear_table(stage)
                    break

            if command == "Exit":
                break
