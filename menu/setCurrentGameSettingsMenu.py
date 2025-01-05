import sys
import pygame
from functions.draw_func.drawButton import DrawButton
from functions.draw_func.drawCheckBox import DrawCheckbox
from functions.draw_func.drawInputBox import DrawInputBox
from functions.draw_func.drawText import DrawText
from game.game import Game
from menu.baseMenu import BaseMenu

class SetCurrentGameSettings(BaseMenu):
    def __init__(self, screen, amount_of_players):
        super().__init__(f"icons/backgrounds/menu/menu.png", screen)
        self.amount_of_players = amount_of_players

        self.FIELD_COLOR = (200, 200, 200)

        self.names = []
        self.name_active_boxes = []
        self.name_input_boxes = []
        for i in range(amount_of_players):
            self.names.append('')
            self.name_active_boxes.append(False)
            self.name_input_boxes.append(pygame.Rect(540, 150 + (i * 70), 200, 50))

        self.chips = ''
        self.chips_active_boxes = False
        self.chips_input_boxes = pygame.Rect(540, 220 + ((len(self.name_input_boxes) - 1) * 70), 200, 50)

        self.checkbox_rect = pygame.Rect(620, 290 + ((len(self.name_input_boxes) - 1) * 70), 50, 50)
        self.checkbox_checked = False

        self.confirm_button = pygame.Rect(540, 360 + ((len(self.name_input_boxes) - 1) * 70), 200, 50)
        self.back_button = pygame.Rect(540, 430 + ((len(self.name_input_boxes) - 1) * 70), 200, 50)

    def draw_text(self):
        x = 570
        y = 90
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

        for i in range(self.amount_of_players):
            x = self.name_input_boxes[i].x - 250
            y = self.name_input_boxes[i].y + 10
            func = DrawText(f"Нік гравця номер {i + 1}", self.minor, self.BLACK, self.screen, x + 1, y + 1)
            func.draw()
            func = DrawText(f"Нік гравця номер {i + 1}", self.minor, self.BLACK, self.screen, x - 1, y - 1)
            func.draw()
            func = DrawText(f"Нік гравця номер {i + 1}", self.minor, self.BLACK, self.screen, x + 1, y - 1)
            func.draw()
            func = DrawText(f"Нік гравця номер {i + 1}", self.minor, self.BLACK, self.screen, x - 1, y + 1)
            func.draw()
            func = DrawText(f"Нік гравця номер {i + 1}", self.minor, self.WHITE, self.screen, x, y)
            func.draw()

        x = self.chips_input_boxes.x - 450
        y = self.chips_input_boxes.y + 10
        func = DrawText("Cтартові фішки (100<=x<=1.000.000)", self.minor, self.BLACK, self.screen, x + 1, y + 1)
        func.draw()
        func = DrawText("Cтартові фішки (100<=x<=1.000.000)", self.minor, self.BLACK, self.screen, x - 1, y - 1)
        func.draw()
        func = DrawText("Cтартові фішки (100<=x<=1.000.000)", self.minor, self.BLACK, self.screen, x + 1, y - 1)
        func.draw()
        func = DrawText("Cтартові фішки (100<=x<=1.000.000)", self.minor, self.BLACK, self.screen, x - 1, y + 1)
        func.draw()
        func = DrawText("Cтартові фішки (100<=x<=1.000.000)", self.minor, self.WHITE, self.screen, x, y)
        func.draw()

        x = self.checkbox_rect.x - 250
        y = self.checkbox_rect.y + 10
        func = DrawText("Показати туторіал?", self.minor, self.BLACK, self.screen, x + 1, y + 1)
        func.draw()
        func = DrawText("Показати туторіал?", self.minor, self.BLACK, self.screen, x - 1, y - 1)
        func.draw()
        func = DrawText("Показати туторіал?", self.minor, self.BLACK, self.screen, x + 1, y - 1)
        func.draw()
        func = DrawText("Показати туторіал?", self.minor, self.BLACK, self.screen, x - 1, y + 1)
        func.draw()
        func = DrawText("Показати туторіал?", self.minor, self.WHITE, self.screen, x, y)
        func.draw()

    def draw_buttons(self):
        func = DrawButton(self.screen, self.minor, "Confirm", self.confirm_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()
        func = DrawButton(self.screen, self.minor, "Back", self.back_button, self.GRAY, self.WHITE, 0, 0)
        func.draw()

    def draw_input_boxes(self, chips_input_box_red_alpha):
        for i, box in enumerate(self.name_input_boxes):
            func = DrawInputBox(self.screen, box, self.minor, self.FIELD_COLOR, self.BLACK, self.BLACK, self.names[i])
            func.draw()

        func = DrawInputBox(self.screen, self.chips_input_boxes, self.minor, self.FIELD_COLOR, self.BLACK, self.BLACK, self.chips)
        func.draw()

        chips_input_box_with_alpha = pygame.Surface((self.chips_input_boxes.width, self.chips_input_boxes.height), pygame.SRCALPHA)
        pygame.draw.rect(
            chips_input_box_with_alpha,
            (255, 0, 0, chips_input_box_red_alpha),
            chips_input_box_with_alpha.get_rect(),
            border_radius=5
        )
        self.screen.blit(chips_input_box_with_alpha, (self.chips_input_boxes.x, self.chips_input_boxes.y))

    def draw_check_box(self):
        func = DrawCheckbox(self.screen, self.checkbox_rect, self.WHITE, self.BLACK, self.BLACK, self.checkbox_checked)
        func.draw()

    def execute(self):
        self.screen.blit(self.background_image, (0, 0))
        self.draw_text()
        self.draw_buttons()

        chips_input_box_red_alpha = 0

        running = True
        while running:
            self.draw_input_boxes(chips_input_box_red_alpha)
            self.draw_check_box()

            # На кожному циклі зменшуємо рівень прозорості
            if chips_input_box_red_alpha > 0:
                chips_input_box_red_alpha -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Перевірка на кліки по полях введення
                    if self.checkbox_rect.collidepoint(event.pos):
                        self.checkbox_checked = not self.checkbox_checked

                    # Перевірка на кліки по полях введення
                    for i, box in enumerate(self.name_input_boxes):
                        if box.collidepoint(event.pos):
                            self.name_active_boxes[i] = True
                        else:
                            self.name_active_boxes[i] = False

                    if self.chips_input_boxes.collidepoint(event.pos):
                        self.chips_active_boxes = True
                    else:
                        self.chips_active_boxes = False

                    if self.confirm_button.collidepoint(event.pos):
                        if self.chips == "" or int(self.chips) < 100:
                            chips_input_box_red_alpha = 148
                        else:
                            game = Game(self.screen, self.amount_of_players, self.names, int(self.chips), self.checkbox_checked)
                            game.execute()
                            return "end"

                    elif self.back_button.collidepoint(event.pos):
                        return "back"

                if event.type == pygame.KEYDOWN:
                    for i, active in enumerate(self.name_active_boxes):
                        if active:
                            if event.key == pygame.K_BACKSPACE:
                                self.names[i] = self.names[i][:-1]

                            elif len(self.names[i]) < 9:
                                self.names[i] += event.unicode

                    if self.chips_active_boxes:
                        if event.key == pygame.K_BACKSPACE:
                            self.chips = self.chips[:-1]

                        elif event.unicode.isdigit() and int(self.chips + event.unicode) <= 1000000:
                            if self.chips == "" and int(event.unicode) == 0:
                                self.chips = ""
                            else:
                                self.chips += event.unicode

            pygame.display.flip()
