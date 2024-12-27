import pygame
from functions.drawtext import DrawText

class DrawButtons:
    def __init__(self, screen, font, buttons, rect_color, text_color):
        self.screen = screen
        self.font = font
        self.buttons = buttons
        self.rect_color = rect_color
        self.text_color = text_color

    def execute(self):
        for button_text, rect in self.buttons.items():
            pygame.draw.rect(self.screen, self.rect_color, rect)
            func = DrawText(button_text, self.font, self.text_color, self.screen, rect.x + 10, rect.y + 10)
            func.execute()
        pygame.display.update()