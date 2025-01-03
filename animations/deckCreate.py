import pygame
import sys

# Ініціалізація pygame
pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Створення колоди")

# Завантаження зображень карт
card_image = pygame.image.load("D:\\Шарага\\Проекти_на_пітоні\\Course_OOP_v2\\icons\\cards\\card_back.png")
card_image = pygame.transform.scale(card_image, (100, 150))

# Завантаження зображень стола
table_image = pygame.image.load("../icons/backgrounds/game/table.png")
table_image = pygame.transform.scale(table_image, (1280, 720))

# Налаштування точок, куди карти будуть роздані
deck_position = [(948, 140), (950, 140), (952, 140), (954, 140), (956, 140), (958, 140), (960, 140)]

# Випадкові кути для кожної позиції
card_angles = [0, 0, 0, 0, 0, 0, 0, 0]

# Список для збереження позицій розданих карт
dealt_cards = []

# Параметри анімації
card_start_pos = (948, 140) # Початкова точка роздачі карт
animation_speed = 10  # Швидкість анімації

# Функція для анімації карти до цільової позиції
def animate_card(start_pos, end_pos, angle):
    x, y = start_pos
    end_x, end_y = end_pos
    while abs(x - end_x) > 1 or abs(y - end_y) > 1:  # Продовжуємо, поки карта не наблизиться до цілі
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обчислення напряму руху
        direction_x = (end_x - x) / animation_speed
        direction_y = (end_y - y) / animation_speed

        # Оновлення позиції карти
        x += direction_x
        y += direction_y

        # Малюємо стіл
        screen.blit(table_image, (0, 0))

        # Малюємо всі роздані карти
        for pos, ang in dealt_cards:
            rotated_card = pygame.transform.rotate(card_image, ang)
            rotated_rect = rotated_card.get_rect()  # Отримуємо прямокутник
            rotated_rect.center = pos  # Встановлюємо центр прямокутника
            screen.blit(rotated_card, rotated_rect.topleft)

        # Малюємо карту, яка зараз анімується
        rotated_card = pygame.transform.rotate(card_image, angle)
        rotated_rect = rotated_card.get_rect()
        rotated_rect.center = (x, y)  # Встановлюємо центр для анімації
        screen.blit(rotated_card, rotated_rect.topleft)

        pygame.display.flip()
        pygame.time.delay(20)  # Затримка для плавності анімації

    dealt_cards.append((end_pos, angle))

# Основний цикл для роздачі карт
for pos, angle in zip(deck_position, card_angles):
    animate_card(card_start_pos, pos, angle)

pygame.image.save(screen, "../icons/backgrounds/game/table_with_deck.png")
print("Зображення столу збережено як 'table_with_deck.png'")

pygame.time.delay(1000)  # Затримка для перегляду результату