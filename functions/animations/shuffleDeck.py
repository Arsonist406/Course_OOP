import sys

import pygame

from functions.animations.baseAnimation import BaseAnimation


class ShuffleDeck(BaseAnimation):
    def __init__(self, screen, deck_pos, table_image, card_back_image):
        super().__init__(screen, table_image=table_image, start_pos=deck_pos, card_back_image=card_back_image)
        self.right_end_pos = (deck_pos[0] + 120, deck_pos[1])
        self.left_end_pos = (deck_pos[0] - 120, deck_pos[1])

    def execute(self):
        for i in range(6):
            x, y = self.start_pos
            if i % 2 == 0:
                end_x, end_y = self.right_end_pos
            else:
                end_x, end_y = self.left_end_pos

            # Переміщаємо карту до кінцевої точки
            while abs(x - end_x) > 1 or abs(y - end_y) > 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Обчислення напряму руху
                direction_x = (end_x - x) / self.animation_speed
                direction_y = (end_y - y) / self.animation_speed

                # Оновлення позиції карти
                x += direction_x
                y += direction_y

                self.screen.blit(self.table_image, (0, 0))

                # Малюємо карту, яка зараз анімується
                rect = self.card_back_image.get_rect()
                rect.center = (x, y)
                self.screen.blit(self.card_back_image, rect.topleft)

                self.screen.blit(self.card_back_image, (self.start_pos[0] - 50, self.start_pos[1] - 75))

                pygame.display.update()
                pygame.time.delay(20)

            if i % 2 == 0:
                x, y = self.right_end_pos
            else:
                x, y = self.left_end_pos
            end_x, end_y = self.start_pos

            # Повертаємо карту назад до початкової позиції
            while abs(x - end_x) > 1 or abs(y - end_y) > 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Обчислення напряму руху
                direction_x = (end_x - x) / self.animation_speed
                direction_y = (end_y - y) / self.animation_speed

                # Оновлення позиції карти
                x += direction_x
                y += direction_y

                self.screen.blit(self.table_image, (0, 0))
                self.screen.blit(self.card_back_image, (self.start_pos[0] - 50, self.start_pos[1] - 75))

                # Малюємо карту, яка зараз анімується
                rect = self.card_back_image.get_rect()
                rect.center = (x, y)
                self.screen.blit(self.card_back_image, rect.topleft)

                pygame.display.update()
                pygame.time.delay(20)
