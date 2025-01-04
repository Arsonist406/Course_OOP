import ctypes
from ctypes import POINTER, c_void_p, c_int, c_char_p
lib = ctypes.CDLL('cpp/lib/comb_calculator.dll')
class CtypesCard(ctypes.Structure):
    _fields_ = [("suit", ctypes.c_char_p), ("value", ctypes.c_char_p)]

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

    table_comb_searcher = lib.CombinationSearcher_create(table_cards_ptr, len(table_cards_array), None, 0)
    try:
        table_comb_bytes = lib.CombinationSearcher_execute(table_comb_searcher)
        table_comb = table_comb_bytes.decode('utf-8')

        table_comb_score = lib.CombinationSearcher_getCombScore(table_comb_searcher)
    finally:
        # Звільнення пам'яті
        lib.CombinationSearcher_destroy(table_comb_searcher)

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

    # Перетворення назви комбінації в номер
    hash_player_comb_int_int = {}
    for player in players:
        comb_order = {'High': 1, 'Pair': 2, 'Two pair': 3, 'Three of a kind': 4, 'Straight': 5, 'Flush': 6,
                      'Full house': 7, 'Four of a kind': 8, 'Straight flush': 9, 'Royal flush': 10}

        hash_player_comb_int_int[player] = (comb_order[hash_player_comb_str_int[player][0]], hash_player_comb_str_int[player][1])

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
                hash_greatest_comb_players[greatest_comb].append[player]

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