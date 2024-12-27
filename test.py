import pygame
import math

# Ініціалізація Pygame
pygame.init()

# Параметри екрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Затемнення з виділенням")

# Основні кольори
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Координати чисел
coords = {
    "1": (200, 300),
    "4": (400, 300),
    "5": (600, 300)
}

# Функція для створення затемнення
def draw_fade_overlay(surface, target_pos, max_radius):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            distance = math.hypot(x - target_pos[0], y - target_pos[1])
            alpha = min(230, max(20, int(255 * (distance / max_radius))))
            overlay.fill((0, 0, 0, alpha), (x, y, 1, 1))
    surface.blit(overlay, (0, 0))

# Основний цикл
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(RED)

    # Малюємо числа
    font = pygame.font.Font(None, 74)
    for num, pos in coords.items():
        text = font.render(num, True, WHITE)
        screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2))

    # Малюємо затемнення, виділяючи "4"
    draw_fade_overlay(screen, coords["4"], 60)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    clock.tick(60)

pygame.quit()
