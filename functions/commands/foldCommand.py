import pygame
import random
from animations.twoCardsMoving import TwoCardsMoving
from functions.blitOverlay import BlitOverlay
from functions.loadImage import LoadImage

class FoldCommand:
    def __init__(self, screen, table_image, card_back_image, hash_player_pos,
                 hash_player_ang, discard_deck_pos, players, player):
        self.screen = screen
        self.table_image = table_image
        self.card_back_image = card_back_image
        self.player_pos = hash_player_pos[player]
        self.coord1, self.coord2 = self.player_pos
        self.card_ang = hash_player_ang[player]
        self.discard_deck_pos = discard_deck_pos
        self.players = players
        self.player = player

    def execute(self):
        self.player.setIs_active(False)

        func = BlitOverlay(self.screen, self.coord1)
        func.execute()

        pygame.image.save(self.screen, "icons/backgrounds/table_with_players_cards.png")
        func = LoadImage("icons/backgrounds/table_with_players_cards.png",
                         (1280, 720))
        self.table_image = func.execute()

        animation = TwoCardsMoving(self.screen, self.table_image, self.card_back_image, self.player_pos,
                              self.card_ang + random.randint(0, 180), self.discard_deck_pos)
        animation.execute()

        pygame.image.save(self.screen, "icons/backgrounds/table_with_players_cards.png")
        func = LoadImage("icons/backgrounds/table_with_players_cards.png",
                         (1280, 720))
        self.table_image = func.execute()
