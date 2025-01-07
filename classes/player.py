
class Player:
    def __init__(self, name, hand, chips):
        self.name = name
        self.hand = hand
        self.chips = chips
        self.is_active = True

    def getName(self):
        return self.name

    def getHand(self):
        return self.hand

    def setHand(self, hand):
        self.hand = hand

    def getChips(self):
        return self.chips

    def setChips(self, chips):
        self.chips = chips

    def getIs_active(self):
        return self.is_active

    def setIs_active(self, is_active):
        self.is_active = is_active