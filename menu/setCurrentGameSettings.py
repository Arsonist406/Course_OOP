import sys
import pygame

from functions.drawButton import DrawButton
from functions.drawText import DrawText
from functions.loadImage import LoadImage
from game.game import Game

class SetCurrentGameSettings:
    def __init__(self, screen, amount_of_players):
        self.screen = screen
        self.amount_of_players = amount_of_players

        # Кольори та шрифт
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (127, 127, 127)
        self.FIELD_COLOR = (200, 200, 200)
        self.font = pygame.font.Font(None, 36)  # Використовуємо стандартний шрифт розміром 36
        self.title = pygame.font.Font(None, 54)

        # Задній фон
        if self.amount_of_players == 2:
            func = LoadImage("icons/backgrounds/menu/card_deal_for_2_players_menu.png",(1280, 720))
            self.background_image = func.execute()
        elif self.amount_of_players == 3:
            func = LoadImage("icons/backgrounds/menu/card_deal_for_3_players_menu.png",(1280, 720))
            self.background_image = func.execute()
        elif self.amount_of_players == 4:
            func = LoadImage("icons/backgrounds/menu/card_deal_for_4_players_menu.png",(1280, 720))
            self.background_image = func.execute()

        i = 0
        self.input_boxes = []
        self.names = []
        self.active_boxes = []
        while i != amount_of_players:
            self.input_boxes.append(pygame.Rect(540, 200 + (i * 70), 200, 50))
            self.names.append('')
            self.active_boxes.append(False)
            i += 1

        # Кнопки для збереження
        self.confirm_button = pygame.Rect(540, 200 + (i * 70), 200, 50)
        self.back_button = pygame.Rect(540, 270 + (i * 70), 200, 50)

    def execute(self):
        self.screen.blit(self.background_image, (0, 0))
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Перевірка на кліки по полях введення
                    for i, box in enumerate(self.input_boxes):
                        if box.collidepoint(event.pos):
                            self.active_boxes[i] = True
                        else:
                            self.active_boxes[i] = False

                    if self.confirm_button.collidepoint(event.pos):
                        game = Game(self.screen, self.amount_of_players, self.names)
                        game.execute()
                        running = False

                    elif self.back_button.collidepoint(event.pos):
                        running = False

                if event.type == pygame.KEYDOWN:
                    for i, active in enumerate(self.active_boxes):
                        if active:
                            if event.key == pygame.K_BACKSPACE:
                                self.names[i] = self.names[i][:-1]
                            elif len(self.names[i]) < 9:
                                self.names[i] += event.unicode

            for i, box in enumerate(self.input_boxes):
                pygame.draw.rect(self.screen, self.FIELD_COLOR, box)
                pygame.draw.rect(self.screen, self.BLACK, box, 2)
                func = DrawText(self.names[i], self.font, self.BLACK, self.screen, box.x + 10, box.y + 10)
                func.execute()

            pygame.display.flip()