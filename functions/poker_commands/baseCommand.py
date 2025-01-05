from abc import ABC, abstractmethod

class BaseCommand(ABC):
    def __init__(self, bank=None, player=None, hash_player_bet=None):
        self.bank = bank
        self.player = player
        self.hash_player_bet = hash_player_bet
        pass

    @abstractmethod
    def execute(self):
        pass
