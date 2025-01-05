import pygame
from functions.draw_func.drawCheckBox import DrawCheckbox


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Checkbox Example")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    checkbox = DrawCheckbox(
        screen=screen,
        rect=pygame.Rect(50, 50, 30, 30),
        box_color=(200, 200, 200),
        check_color=(0, 255, 0),
    )

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            checkbox.handle_event(event)

        checkbox.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
