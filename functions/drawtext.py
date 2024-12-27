class DrawText:
    def __init__(self, text, font, color, screen, x, y):
        self.text = text
        self.font = font
        self.color = color
        self.screen = screen
        self.x = x
        self.y = y

    def execute(self):
        text_obj = self.font.render(self.text, True, self.color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (self.x, self.y)
        self.screen.blit(text_obj, text_rect)
