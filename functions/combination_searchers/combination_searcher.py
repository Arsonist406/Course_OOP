class Combination_Searcher:
    def __init__(self, hand, table):
        self.hand = hand
        self.cards = table + list(hand)

    def execute(self):

        if self.isRoyalFlush():
            return "Royal flush"
        '''
        if self.isStraightFlush():
            return "Straight flush"
        if self.isFourOfAKind():
            return "Four of a kind"
        if self.isFullHouse():
            return "Full house"
        if self.isFlush():
            return "Flush"
        if self.isStraight():
            return "Straight"
        if self.isThreeOfAKind():
            return "Three of a kind"
        if self.isTwoPair():
            return "Two pair"
        if self.isPair():
            return "Pair"
        '''

        return self.highCard()

    def isRoyalFlush(self):
        royal_flush_values = ['10', 'jack', 'queen', 'king', 'ace']

        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.cards:
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
        value_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                      '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

        values_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

        # Ділимо карти по масті
        hash_suit_values = {}
        for card in self.cards:
            suit = card.getSuit()
            if suit in hash_suit_values:
                hash_suit_values[suit].append(card.getValue())
            else:
                hash_suit_values[suit] = [card.getValue()]

        # Для кожної масті перевіряємо умову Straight flush
        for values in hash_suit_values.values():
            if len(values) >= 5:
                return True
        return False

    def isFourOfAKind(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Перевірка, чи є хоча б один ранг, що зустрічається 4 рази
        for count in value_count.values():
            if count == 4:
                return True

        return False

    def isFullHouse(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Для фулл-хауса потрібно, щоб було 1 трійка і 1 пара
        counts = list(value_count.values())

        # Перевірка, чи є 1 трійка (3 однакові карти) і 1 пара (2 однакові карти)
        if sorted(counts) == [2, 3]:
            return True
        return False

    def isFlush(self):
        # Перевірка, чи всі карти однієї масті
        suits = {card.getSuit() for card in self.cards}  # Множина мастей карт
        return len(suits) == 1  # Якщо всі карти однієї масті, то множина містить тільки 1 елемент

    def isStraight(self):
        value_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                      '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        # Отримуємо список значень карт і перетворюємо їх в числа
        values = sorted([value_order[card.getValue()] for card in self.cards])

        # Перевіряємо, чи є п'ять карт підряд
        for i in range(1, len(values)):
            if values[i] != values[i - 1] + 1:
                return False

        return True

    def isThreeOfAKind(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Перевірка, чи є хоча б один ранг, що зустрічається 3 рази
        for count in value_count.values():
            if count == 3:
                return True
        return False

    def isTwoPair(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Підрахунок кількості пар (дві карти одного значення)
        pairs = 0
        for count in value_count.values():
            if count == 2:
                pairs += 1

        # Перевірка на дві пари
        return pairs == 2

    def isPair(self):
        value_count = {}  # Словник для підрахунку карт за рангами

        # Підрахунок кількості кожного рангу
        for card in self.cards:
            if card.getValue() in value_count:
                value_count[card.getValue()] += 1
            else:
                value_count[card.getValue()] = 1

        # Перевірка, чи є хоча б один ранг, що зустрічається 2 рази
        for count in value_count.values():
            if count == 2:
                return True
        return False

    def highCard(self):
        # Створюємо словник для відповідності рангу карт числовим значенням
        value_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                      '10': 10, 'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

        # Знаходимо картку з найвищим значенням
        value = self.hand[0].getValue()
        first_card_score = value_order[value]
        value = self.hand[1].getValue()
        second_card_score = value_order[value]

        return self.hand[0] if first_card_score > second_card_score else self.hand[1]