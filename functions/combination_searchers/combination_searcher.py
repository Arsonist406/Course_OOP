class Combination_Searcher:
    def __init__(self, table, hand):
        self.playing_cards = table + list(hand)
        self.values_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}
        self.comb_score = 0
        self.has_ace = False

    def getCombScore(self):
        return self.comb_score

    def is_there_a_ace(self):
        for card in self.playing_cards:
            if card.getValue() == "ace":
                self.has_ace = True
                break

    def execute(self):
        self.is_there_a_ace()

        if self.isRoyalFlush():
            return f"Royal flush"
        if self.isStraightFlush():
            return f"Straight flush"
        if self.isFourOfAKind():
            return f"Four of a kind"
        if self.isFullHouse():
            return f"Full house"
        if self.isFlush():
            return f"Flush"
        if self.isStraight():
            return f"Straight"
        if self.isThreeOfAKind():
            return f"Three of a kind"
        if self.isTwoPair():
            return f"Two pair"
        if self.isPair():
            return f"Pair"
        return self.highCard()

    def isRoyalFlush(self):
        royal_flush_values = ['10', 'jack', 'queen', 'king', 'ace']

        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.playing_cards:
            suit = card.getSuit()
            if suit in hash_suit_values:
                hash_suit_values[suit].append(card.getValue())
            else:
                hash_suit_values[suit] = [card.getValue()]

        # Для кожної масті перевіряємо умову Royal flush
        for values in hash_suit_values.values():
            if len(values) >= 5 and set(royal_flush_values).issubset(values):
                return True
        return False

    def isStraightFlush(self):
        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.playing_cards:
            suit = card.getSuit()
            if suit in hash_suit_values:
                hash_suit_values[suit].append(card.getValue())
            else:
                hash_suit_values[suit] = [card.getValue()]

        # Отримуємо список значень карт
        comb_found = False
        for suit, values in hash_suit_values.items():
           if len(values) >= 5:
               temp = []
               for value in values:
                   temp.append(self.values_order[value])

               if self.has_ace:
                   temp.append(1)

               temp = sorted(temp)
               for i in range(len(temp) - 4):
                   if (temp[i] == temp[i + 1] - 1 and temp[i + 1] == temp[i + 2] - 1 and
                       temp[i + 2] == temp[i + 3] - 1 and temp[i + 3] == temp[i + 4] - 1):
                       comb_found = True
                       self.comb_score = 0
                       for j in range(i, i + 5):
                           self.comb_score += temp[j]

        if comb_found:
            return True
        else:
            return False

    def isFourOfAKind(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.playing_cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Перевірка, чи є хоча б один ранг, що зустрічається 4 рази
        for value, count in value_count.items():
            if count == 4:
                self.comb_score = 0
                self.comb_score = self.values_order[value] * 4
                return True

        return False

    def isFullHouse(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.playing_cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Для фулл-хауса потрібно, щоб було 1 трійка і 1 пара
        counts = sorted(list(value_count.values()))

        # Перевірка, чи є 1 трійка (3 однакові карти) і 1 пара (2 однакові карти)
        if counts == [1, 3, 3]:
            temp = []
            for value, count in value_count.items():
                if count == 3:
                    temp.append(self.values_order[value])
            temp = sorted(temp)
            self.comb_score = 0
            self.comb_score += temp[0] * 2
            self.comb_score += temp[1] * 3
            return True
        elif counts == [2, 2, 3]:
            temp = []
            three = None
            for value, count in value_count.items():
                if count == 3:
                    three = self.values_order[value]
                else:
                    temp.append(self.values_order[value])
            temp = sorted(temp)
            self.comb_score = 0
            self.comb_score += temp[1] * 2
            self.comb_score += three * 3
            return True
        elif counts == [1, 1, 2, 3]:
            self.comb_score = 0
            counts_with_value = sorted(list(value_count.items()), key=lambda x: x[1])
            self.comb_score += self.values_order[counts_with_value[-2][0]] * 2
            self.comb_score += self.values_order[counts_with_value[-1][0]] * 3
            return True
        return False

    def isFlush(self):
        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.playing_cards:
            suit = card.getSuit()
            if suit in hash_suit_values:
                hash_suit_values[suit].append(card.getValue())
            else:
                hash_suit_values[suit] = [card.getValue()]

        # Для кожної масті перевіряємо умову flush
        for values in hash_suit_values.values():
            if len(values) >= 5:
                temp = []
                for value in values:
                    temp.append(self.values_order[value])
                temp = sorted(temp)

                self.comb_score = 0
                for elem, _ in zip(reversed(temp), range(5)):
                    self.comb_score += elem
                return True
        return False

    def isStraight(self):
        # Отримуємо список значень карт і перетворюємо їх в числа
        temp = []
        for card in self.playing_cards:
            if self.values_order[card.getValue()] in temp:
                continue
            else:
                temp.append(self.values_order[card.getValue()])

        if self.has_ace:
            temp.append(1)

        temp = sorted(temp)

        comb_found = False
        for i in range(len(temp) - 4):
            if (temp[i] == temp[i + 1] - 1 and temp[i + 1] == temp[i + 2] - 1 and
                temp[i + 2] == temp[i + 3] - 1 and temp[i + 3] == temp[i + 4] - 1):
                comb_found = True
                self.comb_score = 0
                for j in range(i, i + 5):
                    self.comb_score += temp[j]

        if comb_found:
            return True
        else:
            return False

    def isThreeOfAKind(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.playing_cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Перевірка, чи є хоча б один ранг, що зустрічається 3 рази
        for value, count in value_count.items():
            if count == 3:
                self.comb_score = 0
                self.comb_score = self.values_order[value] * 3
                return True
        return False

    def isTwoPair(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.playing_cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Підрахунок кількості пар (дві карти одного значення)
        pairs = []
        self.comb_score = 0
        for value, count in value_count.items():
            if count == 2:
                pairs.append(value)

        if len(pairs) == 2:
            self.comb_score += self.values_order[pairs[0]] * 2
            self.comb_score += self.values_order[pairs[1]] * 2
            return True
        elif len(pairs) == 3:
            temp = sorted([self.values_order[pairs[0]], self.values_order[pairs[1]], self.values_order[pairs[2]]])
            self.comb_score += temp[-1] * 2
            self.comb_score += temp[-2] * 2
            return True
        return False

    def isPair(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.playing_cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Перевірка, чи є хоча б один ранг, що зустрічається 2 рази
        for value, count in value_count.items():
            if count == 2:
                self.comb_score = 0
                self.comb_score = self.values_order[value] * 2
                return True
        return False

    def highCard(self):
        # Знаходимо картку з найвищим значенням
        biggest_score = 0
        for card in self.playing_cards:
            value = card.getValue()
            score = self.values_order[value]
            if score > biggest_score:
                biggest_score = score

        self.comb_score = biggest_score
        return "High"