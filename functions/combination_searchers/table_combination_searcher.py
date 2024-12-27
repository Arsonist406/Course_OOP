class Table_Combination_Searcher:
    def __init__(self, table):
        self.table = table
        self.values_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                            '9': 9, '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}
        self.comb_score = 0

    def getCombScore(self):
        return self.comb_score

    def execute(self):
        if self.isRoyalFlush():
            return f"Royal flush"
        if self.isStraightFlush():
            return f"Straight flush {self.comb_score}"
        if self.isFourOfAKind():
            return f"Four of a kind {self.comb_score}"
        if self.isFullHouse():
            return f"Full house {self.comb_score}"
        if self.isFlush():
            return f"Flush {self.comb_score}"
        if self.isStraight():
            return f"Straight {self.comb_score}"
        if self.isThreeOfAKind():
            return f"Three of a kind {self.comb_score}"
        if self.isTwoPair():
            return f"Two pair {self.comb_score}"
        if self.isPair():
            return f"Pair {self.comb_score}"
        return self.highCard()

    def isRoyalFlush(self):
        royal_flush_values = ['10', 'jack', 'queen', 'king', 'ace']

        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.table:
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
        # Перевірка на одну масть
        suits = {card.suit for card in self.table}
        if len(suits) != 1:  # Якщо карти не однієї масті
            return False

        # Отримуємо список значень карт
        values = sorted([self.values_order[card.getValue()] for card in self.table])

        # Перевірка на підрядність
        self.comb_score = 0
        for i in range(1, len(values)):
            if values[i] != values[i - 1] + 1:
                return False
            self.comb_score += values[i]
        self.comb_score += values[0]

        return True

    def isFourOfAKind(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.table:
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
        for card in self.table:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Для фулл-хауса потрібно, щоб було 1 трійка і 1 пара
        counts = sorted(list(value_count.values()))

        # Перевірка, чи є 1 трійка (3 однакові карти) і 1 пара (2 однакові карти)
        if counts == [2, 3]:
            self.comb_score = 0
            counts_with_value = sorted(list(value_count.items()), key=lambda x: x[1])
            self.comb_score += self.values_order[counts_with_value[0][0]] * 2
            self.comb_score += self.values_order[counts_with_value[1][0]] * 3
            return True
        return False

    def isFlush(self):
        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.table:
            suit = card.getSuit()
            if suit in hash_suit_values:
                hash_suit_values[suit].append(card.getValue())
            else:
                hash_suit_values[suit] = [card.getValue()]

        # Для кожної масті перевіряємо умову flush
        for values in hash_suit_values.values():
            if len(values) == 5:
                self.comb_score = 0
                for value in values:
                    self.comb_score += self.values_order[value]
                return True
        return False

    def isStraight(self):
        # Отримуємо список значень карт і перетворюємо їх в числа
        values = sorted([self.values_order[card.getValue()] for card in self.table])

        # Перевіряємо, чи є п'ять карт підряд
        self.comb_score = 0
        for i in range(1, len(values)):
            if values[i] != values[i - 1] + 1:
                return False
            self.comb_score += values[i]
        self.comb_score += values[0]

        return True

    def isThreeOfAKind(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.table:
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
        for card in self.table:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Підрахунок кількості пар (дві карти одного значення)
        pairs = 0
        self.comb_score = 0
        for value, count in value_count.items():
            if count == 2:
                pairs += 1
                self.comb_score += self.values_order[value] * 2

        # Перевірка на дві пари
        return pairs == 2

    def isPair(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.table:
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
        for card in self.table:
            value = card.getValue()
            score = self.values_order[value]
            if score > biggest_score:
                biggest_score = score

        return biggest_score