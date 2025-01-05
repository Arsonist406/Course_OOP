from abc import ABC, abstractmethod

class Drawable(ABC):
    def __init__(self, screen, text=None, font=None, text_color=None, rect_color=None, border_color=None, border_width=None, rect=None):
        self.screen = screen
        self.text = text
        self.font = font
        self.text_color = text_color
        self.rect_color = rect_color
        self.border_color = border_color
        self.border_width = border_width
        self.rect = rect

    @abstractmethod
    def draw(self):
        pass
