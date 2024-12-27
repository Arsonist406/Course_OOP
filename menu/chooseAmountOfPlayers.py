from functions.loadImage import LoadImage
from menu.setCurrentGameSettings import *

class ChooseAmountOfPlayers:
    def __init__(self, screen):
        self.screen = screen

        func = LoadImage("D:\\Шарага\Проекти_на_пітоні\\Course_OOP_v2\\icons\\backgrounds\\choose_amount_of_players_menu.png", (1280, 720))
        self.background_image = func.execute()

        self.for_two_button = pygame.Rect(540, 200, 200, 50)
        self.for_three_button = pygame.Rect(540, 270, 200, 50)
        self.for_four_button = pygame.Rect(540, 340, 200, 50)
        self.back_button = pygame.Rect(540, 410, 200, 50)

    def execute(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.for_two_button.collidepoint(event.pos):
                        menu = SetCurrentGameSettings(self.screen, 2)
                        menu.execute()
                        running = False

                    elif self.for_three_button.collidepoint(event.pos):
                        menu = SetCurrentGameSettings(self.screen, 3)
                        menu.execute()
                        running = False

                    elif self.for_four_button.collidepoint(event.pos):
                        menu = SetCurrentGameSettings(self.screen, 4)
                        menu.execute()
                        running = False

                    elif self.back_button.collidepoint(event.pos):
                        running = False

            pygame.display.update()
