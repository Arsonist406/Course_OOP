import sys
from functions.functions import *

pygame.init()

resolutions = [(800, 600), (1024, 768), (1280, 720), (1366, 768), (1600, 900)]  # Список можливих роздільних здатностей
current_resolution_index = 0  # Індекс поточної роздільної здатності

screen_width, screen_height = resolutions[current_resolution_index]
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Poker Game Settings")

# Кольори та шрифт
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)

font = pygame.font.Font(None, 36)  # Використовуємо стандартний шрифт розміром 36
title = pygame.font.Font(None, 54)

# Задній фон
background_image = pygame.image.load("../icons/backgrounds/menu.png")

# Структура кнопок
buttons = {
    "Sound": pygame.Rect(580, 200, 200, 50),
    "Resolution": pygame.Rect(580, 270, 200, 50),
    "Back to Menu": pygame.Rect(580, 340, 200, 50)
}

# Функція для зміни роздільної здатності
def change_resolution():
    global screen, screen_width, screen_height, current_resolution_index
    current_resolution_index = (current_resolution_index + 1) % len(resolutions)  # Перемикаємось між роздільними здатностями
    screen_width, screen_height = resolutions[current_resolution_index]
    screen = pygame.display.set_mode((screen_width, screen_height))  # Оновлюємо розміри екрана
    print(f"Resolution changed to {screen_width}x{screen_height}")

# Функція для меню налаштувань
def settings_menu():
    running = True
    while running:
        # Малюємо фон
        screen.blit(background_image, (0, 0))  # Малюємо фон у верхньому лівому куті

        # Заголовок меню
        draw_text("Settings", title, BLACK, screen, 602, 120)
        draw_text("Settings", title, BLACK, screen, 598, 120)

        draw_text("Settings", title, BLACK, screen, 600, 122)
        draw_text("Settings", title, BLACK, screen, 600, 118)

        draw_text("Settings", title, WHITE, screen, 600, 120)

        # Малюємо кнопки
        draw_buttons(screen, font, buttons, GRAY, WHITE)

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Перевірка кліку мишкою
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Перевірка, чи натиснута одна з кнопок
                for button_text, rect in buttons.items():
                    if rect.collidepoint(mouse_x, mouse_y):
                        if button_text == "Sound":
                            print("Changing sound settings...")
                            # Тут можна додати код для зміни звуку
                        elif button_text == "Resolution":
                            print("Changing resolution...")
                            change_resolution()
                            # Вибір нової роздільної здатності
                        elif button_text == "Back to Menu":
                            running = False  # Повернення до головного меню

        pygame.display.flip()
