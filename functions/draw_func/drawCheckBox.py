import pygame

from functions.draw_func.baseDrawable import Drawable


class DrawCheckbox(Drawable):
    def __init__(self, screen, rect, box_color, border_color, check_color, checkbox_checked):
        super().__init__(screen, rect=rect, rect_color=box_color, border_color=border_color)
        self.check_color = check_color
        self.checked = checkbox_checked

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.rect, border_radius=5)
        pygame.draw.rect(self.screen, self.border_color, self.rect, width=2, border_radius=5)

        if self.checked:
            pygame.draw.line(self.screen, self.check_color,
                             (self.rect.left + 5, self.rect.centery),
                             (self.rect.centerx, self.rect.bottom - 5), 6)
            pygame.draw.line(self.screen, self.check_color,
                             (self.rect.centerx, self.rect.bottom - 5),
                             (self.rect.right - 5, self.rect.top + 5), 6)
