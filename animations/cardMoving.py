import pygame
import sys


class CardDealForPlayers:
    def __init__(self, screen, players, players_pos_ang):
        self.players = players
        self.players_pos_ang = players_pos_ang

        self.card_angles = []
        self.first_coordinates = []
        for player, ((coord1, coord2), angle) in self.players_pos_ang.items():
            self.first_coordinates.append(coord1)
            self.card_angles.append(angle)

        self.second_coordinates = []
        for player, ((coord1, coord2), angle) in self.players_pos_ang.items():
            self.second_coordinates.append(coord2)
            self.card_angles.append(angle)

        self.players_positions = self.first_coordinates + self.second_coordinates

        self.card_start_pos = (954, 180)  # Початкова точка роздачі карт
        self.animation_speed = 10  # Швидкість анімації

        # Для збереження позицій карт
        self.dealt_cards = []

        # Налаштування екрану
        self.screen = screen

        self.card_image = pygame.image.load("D:\\Шарага\\Проекти_на_пітоні\\Course_OOP_v2\\icons\\cards\\card_back.png")
        self.card_image = pygame.transform.scale(self.card_image, (100, 150))

        # Завантаження зображень стола
        self.table_image = pygame.image.load("D:\\Шарага\\Проекти_на_пітоні\\Course_OOP_v2\\icons\\backgrounds\\table_with_players_info.png")
        self.table_image = pygame.transform.scale(self.table_image, (1280, 720))

    # Функція для анімації карти до цільової позиції
    def animation(self, start_pos, end_pos, angle):
        x, y = start_pos
        end_x, end_y = end_pos
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

            # Малюємо стіл
            self.screen.blit(self.table_image, (0, 0))

            # Малюємо всі роздані карти
            for pos, ang in self.dealt_cards:
                rotated_card = pygame.transform.rotate(self.card_image, ang)
                rotated_rect = rotated_card.get_rect()  # Отримуємо прямокутник
                rotated_rect.center = pos  # Встановлюємо центр прямокутника
                self.screen.blit(rotated_card, rotated_rect.topleft)

            # Малюємо карту, яка зараз анімується
            rotated_card = pygame.transform.rotate(self.card_image, angle)
            rotated_rect = rotated_card.get_rect()
            rotated_rect.center = (x, y)  # Встановлюємо центр для анімації
            self.screen.blit(rotated_card, rotated_rect.topleft)

            pygame.display.update()
            pygame.time.delay(20)  # Затримка для плавності анімації

        self.dealt_cards.append((end_pos, angle))

    def execute(self):
        for pos, angle in zip(self.players_positions, self.card_angles):
            self.animation(self.card_start_pos, pos, angle)

        pygame.image.save(self.screen, "D:\\Шарага\\Проекти_на_пітоні\\Course_OOP_v2\\icons\\backgrounds\\table_with_players_cards.png")
        print("Зображення столу збережено як 'table_with_players_cards.png'")
