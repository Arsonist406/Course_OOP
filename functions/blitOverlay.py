from functions.loadImage import LoadImage


class BlitOverlay:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos

    def execute(self):
        if self.pos == (620, 620):
            func = LoadImage("icons/backgrounds/game/table.png", (140, 160))
            overlay = func.execute()
            self.screen.blit(overlay, (635 - 140 // 2, 620 - 160 // 2))

        elif self.pos == (620, 100):
            func = LoadImage("icons/backgrounds/game/table.png", (140, 160))
            overlay = func.execute()
            self.screen.blit(overlay, (635 - 140 // 2, 100 - 160 // 2))

        elif self.pos == (1180, 360):
            func = LoadImage("icons/backgrounds/game/table.png", (160, 140))
            overlay = func.execute()
            self.screen.blit(overlay, (1180 - 160 // 2, 375 - 140 // 2))

        elif self.pos == (100, 360):
            func = LoadImage("icons/backgrounds/game/table.png", (160, 140))
            overlay = func.execute()
            self.screen.blit(overlay, (100 - 160 // 2, 375 - 140 // 2))

        else:   # Для покривання спільних карт на столі
            func = LoadImage("icons/backgrounds/game/table.png", (110, 160))
            overlay = func.execute()
            self.screen.blit(overlay, (self.pos[0] - 110 // 2, self.pos[1] - 160 // 2))
