import pygame

from functions.draw_func.baseDrawable import Drawable
from functions.draw_func.drawText import DrawText


class DrawButton(Drawable):
    def __init__(self, screen, font, text, rect, rect_color, text_color, outline_width, border_radius):
        super().__init__(screen, font=font, text=text, rect=rect, rect_color=rect_color, text_color=text_color, border_color=(0, 0, 0), border_width=outline_width)
        self.outline_width = outline_width
        self.border_radius = border_radius

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.rect, border_radius=self.border_radius)
        if self.outline_width > 0:
            pygame.draw.rect(self.screen, self.border_color, self.rect, border_radius=self.border_radius, width=self.outline_width)
        func = DrawText(self.text, self.font, self.text_color, self.screen, self.rect.x + 10, self.rect.y + 10)
        func.draw()
        pygame.display.update()