import sys

import pygame


class ShuffleDeck:
    def __init__(self, screen, deck_pos, table_image, card_back_image):
        self.start_pos = deck_pos
        self.right_end_pos = (deck_pos[0] + 120, deck_pos[1])
        self.left_end_pos = (deck_pos[0] - 120, deck_pos[1])
        self.angle = 0
        self.animation_speed = 10
        self.screen = screen
        self.card_back_image = card_back_image
        self.table_image = table_image

    def execute(self):
        for i in range(6):
            x, y = self.start_pos
            if i % 2 == 0:
                end_x, end_y = self.right_end_pos
            else:
                end_x, end_y = self.left_end_pos
            while abs(x - end_x) > 1 or abs(y - end_y) > 1:  # Продовжуємо, поки карта не наблизиться до цілі
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
                rotated_card = pygame.transform.rotate(self.card_back_image, self.angle)
                rotated_rect = rotated_card.get_rect()
                rotated_rect.center = (x, y)
                self.screen.blit(rotated_card, rotated_rect.topleft)

                self.screen.blit(self.card_back_image, (self.start_pos[0] - 50, self.start_pos[1] - 75))

                pygame.display.update()
                pygame.time.delay(20)


            if i % 2 == 0:
                x, y = self.right_end_pos
            else:
                x, y = self.left_end_pos
            end_x, end_y = self.start_pos
            while abs(x - end_x) > 1 or abs(y - end_y) > 1:  # Продовжуємо, поки карта не наблизиться до цілі
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
                rotated_card = pygame.transform.rotate(self.card_back_image, self.angle)
                rotated_rect = rotated_card.get_rect()
                rotated_rect.center = (x, y)
                self.screen.blit(rotated_card, rotated_rect.topleft)

                pygame.display.update()
                pygame.time.delay(20)