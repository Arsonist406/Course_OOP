from functions.draw_func.baseDrawable import BaseDrawable

class DrawText(BaseDrawable):
    def __init__(self, text, font, text_color, screen, x, y):
        super().__init__(screen, text=text, font=font, text_color=text_color)
        self.x = x
        self.y = y

    def draw(self):
        text_obj = self.font.render(self.text, True, self.text_color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (self.x, self.y)
        self.screen.blit(text_obj, text_rect)
