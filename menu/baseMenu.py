
import pygame

from functions.loadImage import LoadImage


class BaseMenu:
    def __init__(self, background_image_path, screen=None):
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((1280, 720))
            pygame.display.set_caption("Poker Game Menu")
        else:
            self.screen = screen

        func = LoadImage(background_image_path, (1280, 720))
        self.background_image = func.execute()

        self.BLACK = (0, 0, 0)
        self.GRAY = (127, 127, 127)
        self.WHITE = (255, 255, 255)
        self.minor = pygame.font.Font(None, 36)
        self.title = pygame.font.Font(None, 64)

    def draw_text(self):
        pass

    def draw_buttons(self):
        pass

    def execute(self):
        pass