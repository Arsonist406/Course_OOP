from menu.setCurrentGameSettingsMenu import *

class ChooseAmountOfPlayers(BaseMenu):
    def __init__(self, screen):
        super().__init__("icons/backgrounds/menu/menu.png", screen)

        self.for_two_button = pygame.Rect(540, 200, 200, 50)
        self.for_three_button = pygame.Rect(540, 270, 200, 50)
        self.for_four_button = pygame.Rect(540, 340, 200, 50)
        self.back_button = pygame.Rect(540, 410, 200, 50)

    def draw_text(self):
        x = 570
        y = 140
        func = DrawText("Game", self.title, self.BLACK, self.screen, x + 1, y + 1)
        func.draw()
        func = DrawText("Game", self.title, self.BLACK, self.screen, x - 1, y - 1)
        func.draw()
        func = DrawText("Game", self.title, self.BLACK, self.screen, x + 1, y - 1)
        func.draw()
        func = DrawText("Game", self.title, self.BLACK, self.screen, x - 1, y + 1)
        func.draw()
        func = DrawText("Game", self.title, self.WHITE, self.screen, x, y)
        func.draw()

    def draw_buttons(self):
        func = DrawButton(self.screen, self.minor, "For two", self.for_two_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()
        func = DrawButton(self.screen, self.minor, "For three", self.for_three_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()
        func = DrawButton(self.screen, self.minor, "For four", self.for_four_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()
        func = DrawButton(self.screen, self.minor, "Back", self.back_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()

    def execute(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_text()
        self.draw_buttons()

        flag = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.for_two_button.collidepoint(event.pos):
                        menu = SetCurrentGameSettings(self.screen, 2)
                        flag = menu.execute()

                    elif self.for_three_button.collidepoint(event.pos):
                        menu = SetCurrentGameSettings(self.screen, 3)
                        flag = menu.execute()

                    elif self.for_four_button.collidepoint(event.pos):
                        menu = SetCurrentGameSettings(self.screen, 4)
                        flag = menu.execute()

                    elif self.back_button.collidepoint(event.pos):
                        return "back"
            
            if flag == "end":
                return "end"
            elif flag == "back":
                self.screen.blit(self.background_image, (0, 0))
                self.draw_text()
                self.draw_buttons()
                flag = ""
            
            pygame.display.flip()
