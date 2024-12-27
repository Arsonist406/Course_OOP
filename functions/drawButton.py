import pygame
from functions.drawtext import DrawText

class DrawButton:
    def __init__(self, screen, font, button_text, button_rect, rect_color, text_color):
        self.screen = screen
        self.font = font
        self.button_text = button_text
        self.button_rect = button_rect
        self.rect_color = rect_color
        self.text_color = text_color
        self.BLACK = (0, 0, 0)

    def execute(self):
        pygame.draw.rect(self.screen, self.rect_color, self.button_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, self.button_rect, border_radius=10, width=2)
        func = DrawText(self.button_text, self.font, self.text_color, self.screen, self.button_rect.x + 10, self.button_rect.y + 10)
        func.execute()
        pygame.display.update()