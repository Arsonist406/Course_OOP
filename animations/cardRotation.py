import pygame

class CardRotation:
    def __init__(self, screen, up_image, back_image, pos, angle):
        self.screen = screen
        self.up_image = up_image
        self.back_image = back_image
        self.card_width = 100
        self.card_height = 150
        self.card_x, self.card_y = pos
        self.card_x -= self.card_width // 2
        self.card_y -= self.card_height // 2
        self.angle = angle

    def execute(self):
        flipping = True
        scale = 1.0
        showing_front = False

        while flipping:
            scale -= 0.05
            if scale <= 0:
                # Перемикання сторони
                showing_front = not showing_front
                scale = 1.0
                flipping = False  # Завершення анімації

            # Вибір зображення
            image = self.up_image if showing_front else self.back_image

            # Масштабування
            scaled_width = int(self.card_width * scale)
            scaled_image = pygame.transform.scale(image, (scaled_width, self.card_height))

            # Обертання
            rotated_image = pygame.transform.rotate(scaled_image, self.angle)
            rotated_rect = rotated_image.get_rect(center=(self.card_x + self.card_width // 2, self.card_y + self.card_height // 2))

            self.screen.blit(rotated_image, rotated_rect.topleft)

            pygame.display.flip()
            pygame.time.delay(30)
