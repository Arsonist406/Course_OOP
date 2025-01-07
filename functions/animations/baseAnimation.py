class BaseAnimation:
    def __init__(self, screen, table_image=None, start_pos=None, end_pos=None, angle=0, animation_speed=10, card_image=None, card_back_image=None):
        self.screen = screen
        self.table_image = table_image
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.angle = angle
        self.animation_speed = animation_speed
        self.card_image = card_image
        self.card_back_image = card_back_image

    def execute(self):
        pass
