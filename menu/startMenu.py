from menu.chooseAmountOfPlayersMenu import *

class StartMenu(BaseMenu):
    def __init__(self):
        super().__init__("icons/backgrounds/menu/menu.png")

        self.title = pygame.font.Font(None, 84)

        self.start_button = pygame.Rect(540, 200, 200, 50)
        self.exit_button = pygame.Rect(540, 270, 200, 50)

    def draw_text(self):
        x = 560
        y = 130
        func = DrawText("Poker", self.title, self.BLACK, self.screen, x + 2, y + 2)
        func.draw()
        func = DrawText("Poker", self.title, self.BLACK, self.screen, x - 2, y - 2)
        func.draw()
        func = DrawText("Poker", self.title, self.BLACK, self.screen, x + 2, y - 2)
        func.draw()
        func = DrawText("Poker", self.title, self.BLACK, self.screen, x - 2, y + 2)
        func.draw()
        func = DrawText("Poker", self.title, self.WHITE, self.screen, x, y)
        func.draw()

    def draw_buttons(self):
        func = DrawButton(self.screen, self.minor, "Start Game", self.start_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()
        func = DrawButton(self.screen, self.minor, "Exit", self.exit_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()

    def execute(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_text()
        self.draw_buttons()

        flag = ""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        menu = ChooseAmountOfPlayers(self.screen)
                        flag = menu.execute()

                    elif self.exit_button.collidepoint(event.pos):
                        return

            if flag == "back":
                self.screen.blit(self.background_image, (0, 0))
                self.draw_text()
                self.draw_buttons()
                flag = ""

            pygame.display.flip()
        pygame.quit()
