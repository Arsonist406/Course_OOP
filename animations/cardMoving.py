import sys

import pygame


class CardMoving:
    def __init__(self, screen, start_pos, end_pos, angle, table_image, card_image):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.angle = angle
        self.animation_speed = 10
        self.screen = screen
        self.card_image = card_image
        self.table_image = table_image

    # Функція для анімації карти до цільової позиції
    def execute(self):
        x, y = self.start_pos
        end_x, end_y = self.end_pos
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
            rotated_card = pygame.transform.rotate(self.card_image, self.angle)
            rotated_rect = rotated_card.get_rect()
            rotated_rect.center = (x, y)
            self.screen.blit(rotated_card, rotated_rect.topleft)

            pygame.display.update()
            pygame.time.delay(20)
