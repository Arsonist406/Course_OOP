import pygame

from functions.animations.baseAnimation import BaseAnimation
from functions.animations.cardMoving import CardMoving


class TwoCardsMoving(BaseAnimation):
    def __init__(self, screen,  table_image, card_back_image, player_pos, discard_deck_pos):
        super().__init__(screen, table_image=table_image, start_pos=player_pos, card_back_image=card_back_image, end_pos=discard_deck_pos)
        self.card1_start, self.card2_start = player_pos

    def execute(self):
        card1 = CardMoving(self.screen, self.card2_start, self.end_pos, self.angle, self.table_image, self.card_back_image)
        card2 = CardMoving(self.screen, self.card1_start, self.end_pos, self.angle, self.table_image, self.card_back_image)

        x1, y1 = self.card1_start
        x2, y2 = self.card2_start
        end_x, end_y = self.end_pos

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

            # Малюємо картки без обертання
            rect1 = card1.card_image.get_rect()
            rect1.center = (x1, y1)
            self.screen.blit(card1.card_image, rect1.topleft)

            rect2 = card2.card_image.get_rect()
            rect2.center = (x2, y2)
            self.screen.blit(card2.card_image, rect2.topleft)

            pygame.display.update()
            pygame.time.delay(20)