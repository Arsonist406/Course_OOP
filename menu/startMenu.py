from functions.loadImage import LoadImage
from menu.chooseAmountOfPlayers import *

class StartMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Poker Game Menu")

        func = LoadImage("D:\\Шарага\Проекти_на_пітоні\\Course_OOP_v2\\icons\\backgrounds\\start_menu.png", (1280, 720))
        self.background_image = func.execute()

        self.start_button = pygame.Rect(540, 200, 200, 50)
        self.settings_button = pygame.Rect(540, 270, 200, 50)
        self.exit_button = pygame.Rect(540, 340, 200, 50)

    def execute(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        menu = ChooseAmountOfPlayers(self.screen)
                        menu.execute()

                    elif self.settings_button.collidepoint(event.pos):
                        print("Opening settings...")

                    elif self.exit_button.collidepoint(event.pos):
                        running = False

            pygame.display.update()

        pygame.quit()
