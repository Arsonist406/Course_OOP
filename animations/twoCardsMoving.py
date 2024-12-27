import pygame
from animations.cardMoving import CardMoving

class TwoCardsMoving:
    def __init__(self, screen,  table_image, card_back_image, player_pos, card_ang, discard_deck_pos):
        self.screen = screen
        self.table_image = table_image
        self.card_back_image = card_back_image
        self.coord1, self.coord2 = player_pos
        self.card_ang = card_ang
        self.discard_deck_pos = discard_deck_pos

    def execute(self):
        card1 = CardMoving(self.screen, self.coord2, self.discard_deck_pos, self.card_ang, self.table_image, self.card_back_image)
        card2 = CardMoving(self.screen, self.coord1, self.discard_deck_pos, self.card_ang, self.table_image, self.card_back_image)

        x1, y1 = self.coord1
        x2, y2 = self.coord2
        end_x, end_y = self.discard_deck_pos

        while abs(x1 - end_x) > 1 or abs(y1 - end_y) > 1 or abs(x2 - end_x) > 1 or abs(y2 - end_y) > 1:
            # Оновлення позицій обох карт
            direction_x1 = (end_x - x1) / card1.animation_speed
            direction_y1 = (end_y - y1) / card1.animation_speed
            x1 += direction_x1
            y1 += direction_y1

            direction_x2 = (end_x - x2) / card2.animation_speed
            direction_y2 = (end_y - y2) / card2.animation_speed
            x2 += direction_x2
            y2 += direction_y2

            self.screen.blit(self.table_image, (0, 0))

            rotated_card1 = pygame.transform.rotate(card1.card_image, card1.angle)
            rotated_rect1 = rotated_card1.get_rect()
            rotated_rect1.center = (x1, y1)
            self.screen.blit(rotated_card1, rotated_rect1.topleft)

            rotated_card2 = pygame.transform.rotate(card2.card_image, card2.angle)
            rotated_rect2 = rotated_card2.get_rect()
            rotated_rect2.center = (x2, y2)
            self.screen.blit(rotated_card2, rotated_rect2.topleft)

            pygame.display.update()
            pygame.time.delay(20)