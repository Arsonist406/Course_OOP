import pygame
from functions.draw_func.baseDrawable import Drawable
from functions.draw_func.drawText import DrawText

class DrawInputBox(Drawable):
    def __init__(self, screen, rect, font, field_color, text_color, border_color, text=""):
        super().__init__(screen, text=text, font=font, text_color=text_color, rect_color=field_color, border_color=border_color, rect=rect)

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.rect)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)
        func = DrawText(self.text, self.font, self.text_color, self.screen,
                        self.rect.x + 10, self.rect.y + 10)
        func.draw()
