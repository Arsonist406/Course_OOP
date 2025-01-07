import random

from classes.card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.createDeck()

    def createDeck(self):
        suit = 1
        while suit <= 4:
            value = 2
            while value <= 14:
                if suit == 1:
                    if value == 11:
                        self.cards.append(Card('clubs', 'jack'))
                    elif value == 12:
                        self.cards.append(Card('clubs', 'queen'))
                    elif value == 13:
                        self.cards.append(Card('clubs', 'king'))
                    elif value == 14:
                        self.cards.append(Card('clubs', 'ace'))
                    else:
                        self.cards.append(Card('clubs', str(value)))
                elif suit == 2:
                    if value == 11:
                        self.cards.append(Card('diamonds', 'jack'))
                    elif value == 12:
                        self.cards.append(Card('diamonds', 'queen'))
                    elif value == 13:
                        self.cards.append(Card('diamonds', 'king'))
                    elif value == 14:
                        self.cards.append(Card('diamonds', 'ace'))
                    else:
                        self.cards.append(Card('diamonds', str(value)))
                elif suit == 3:
                    if value == 11:
                        self.cards.append(Card('hearts', 'jack'))
                    elif value == 12:
                        self.cards.append(Card('hearts', 'queen'))
                    elif value == 13:
                        self.cards.append(Card('hearts', 'king'))
                    elif value == 14:
                        self.cards.append(Card('hearts', 'ace'))
                    else:
                        self.cards.append(Card('hearts', str(value)))
                elif suit == 4:
                    if value == 11:
                        self.cards.append(Card('spades', 'jack'))
                    elif value == 12:
                        self.cards.append(Card('spades', 'queen'))
                    elif value == 13:
                        self.cards.append(Card('spades', 'king'))
                    elif value == 14:
                        self.cards.append(Card('spades', 'ace'))
                    else:
                        self.cards.append(Card('spades', str(value)))
                value += 1
            suit += 1

    def shuffleCards(self):
        random.shuffle(self.cards)

    def getCards(self):
        return self.cards