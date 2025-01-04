import pygame
from functions.commands.command import Command
from animations.twoCardsMoving import TwoCardsMoving
from functions.blitOverlay import BlitOverlay
from functions.loadImage import LoadImage

class FoldCommand(Command):
    def __init__(self, screen, table_image, card_back_image, hash_player_pos, deck_pos, player):
        super().__init__()
        self.screen = screen
        self.table_image = table_image
        self.card_back_image = card_back_image
        self.player_pos = hash_player_pos[player]
        self.coord1, self.coord2 = self.player_pos
        self.card_ang = 0
        self.deck_pos = deck_pos
        self.player = player

    def execute(self):
        self.player.setIs_active(False)

        func = BlitOverlay(self.screen, self.coord1)
        func.execute()

        pygame.image.save(self.screen, "icons/backgrounds/game/table_with_players_cards.png")
        func = LoadImage("icons/backgrounds/game/table_with_players_cards.png",(1280, 720))
        self.table_image = func.execute()

        animation = TwoCardsMoving(self.screen, self.table_image, self.card_back_image, self.player_pos, self.deck_pos)
        animation.execute()

        pygame.image.save(self.screen, "icons/backgrounds/game/table_with_players_cards.png")
        func = LoadImage("icons/backgrounds/game/table_with_players_cards.png",(1280, 720))
        self.table_image = func.execute()
