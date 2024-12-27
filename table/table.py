import sys
import math
import pygame
import random
import threading
import tkinter as tk
from PIL import Image, ImageTk
from animations.cardMoving import CardMoving
from animations.cardRotation import CardRotation
from animations.twoCardsMoving import TwoCardsMoving
from functions.blitOverlay import BlitOverlay
from functions.drawButton import DrawButton
from functions.drawtext import DrawText
from functions.loadImage import LoadImage


class Table:
    def __init__(self, screen, players, deck, bank, table_cards, hash_player_bet):
        self.screen = screen

        # Для відкриття окремого вікна з комбінаціями карт
        self.thread = None

        func = LoadImage("icons/backgrounds/table_with_deck.png", (1280, 720))
        self.table_image = func.execute()

        func = LoadImage("icons/cards/card_back.png", (100, 150))
        self.card_back_image = func.execute()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (127, 127, 127)
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.SysFont('verdana', 36)

        # Активні поля
        self.view_card_rect = None
        self.fold_button_rect = pygame.Rect(50, 612, 140, 70)
        self.bet_n_rais_button_rect = pygame.Rect(220, 612, 140, 70)
        self.check_n_call_button_rect = pygame.Rect(390, 612, 140, 70)
        self.input_box_rect = pygame.Rect(230, 515, 120, 40)

        self.bet_n_rais_button_text = None
        self.check_n_call_button_text = None

        self.view_card_status = "Back"
        self.active_box = False

        # Фото деяких активних полів
        func = LoadImage("icons/buttons/buttons_up.png",(1075//15, 630//15))
        self.up_button_image = func.execute()
        self.up_button_rect = self.up_button_image.get_rect(center=(290, 488))

        func = LoadImage("icons/buttons/buttons_down.png",(1075//15, 630//15))
        self.down_button_image = func.execute()
        self.down_button_rect = self.down_button_image.get_rect(center=(290, 581))

        func = LoadImage("icons/buttons/combination_button.png",
                         (1034//22, 1034//22))
        self.combination_button_image = func.execute()
        self.combinations_button_rect = self.combination_button_image.get_rect(center=(390, 535))

        func = LoadImage("icons/buttons/menu_button.png",
                         (2048//40, 2048//40))
        self.menu_button_image = func.execute()
        self.menu_button_rect = self.menu_button_image.get_rect(center=(1240, 40))

        func = LoadImage("icons/buttons/question_button.png",
                         (256//5, 256//5))
        self.question_button_image = func.execute()
        self.question_button_rect = self.question_button_image.get_rect(center=(1180, 40))

        self.deck = deck

        # Прив'язуємо фото карти до об'єкта карти
        self.hash_card_image = {}
        for card in self.deck.getCards():
            suit = card.getSuit()
            value = card.getValue()
            path = ("icons/cards/" + str(suit) + "/" + str(value) + "_of_" + str(suit) + ".png")
            func = LoadImage(path, (100, 150))
            self.hash_card_image[card] = func.execute()

        self.deck_pos = (954, 180)
        self.discard_deck_pos = (300, 180)

        self.deal_card_pos = [(355, 360), (495, 360), (635, 360), (775, 360), (915, 360)]
        self.deal_card_ang = [0, 0, 0, 0, 0]

        self.players = players

        # Позиції гравців
        pos1 = (620, 620), (650, 620)
        pos2 = (1180, 360), (1180, 390)
        pos3 = (620, 100), (650, 100)
        pos4 = (100, 360), (100, 390)
        self.pos = [pos3, pos4, pos1, pos2]
        self.ang = [0, 90, 180, 270]
        self.hash_player_pos = {}
        self.hash_player_ang = {}
        for player, pos, ang in zip(self.players, self.pos, self.ang):
            self.hash_player_pos[player] = pos
            self.hash_player_ang[player] = ang

        self.bank = bank
        self.biggest_bet = None
        self.player_bet = None
        self.table_cards = table_cards
        self.hash_player_bet = hash_player_bet

    def get_table_image(self):
        return self.table_image

    def get_card_back_image(self):
        return self.card_back_image

    def get_hash_player_pos(self):
        return self.hash_player_pos

    def get_hash_player_ang(self):
        return self.hash_player_ang

    def get_discard_deck_pos(self):
        return self.discard_deck_pos

    def get_player_bet(self):
        return self.player_bet

    def create_table(self):
        self.screen.blit(self.table_image, (0, 0))

    def print_player_name(self, player):
        coord1, coord2 = self.hash_player_pos[player]
        x = None
        y = None
        if coord1 == (620, 620):
            x = 560
            y = 474
        elif coord1 == (620, 100):
            x = 560
            y = 184
        elif coord1 == (1180, 360):
            x = 1105
            y = 240
        elif coord1 == (100, 360):
            x = 27
            y = 240

        pygame.draw.rect(self.screen, self.GRAY, ((x, y), (150, 30)))
        func = DrawText(player.getName(), self.font, self.WHITE, self.screen, x + 5, y + 5)
        func.execute()

    def print_player_chips(self, player):
        coord1, coord2 = self.hash_player_pos[player]
        x = None
        y = None
        if coord1 == (620, 620):
            x = 560
            y = 504
        elif coord1 == (620, 100):
            x = 560
            y = 214
        elif coord1 == (1180, 360):
            x = 1105
            y = 270
        elif coord1 == (100, 360):
            x = 27
            y = 270

        pygame.draw.rect(self.screen, self.GRAY, ((x, y), (150, 30)))
        func = DrawText(str(player.getChips()) + " $", self.font, self.WHITE, self.screen, x + 5, y + 5)
        func.execute()

    def print_player_info(self, player):
        self.print_player_name(player)
        self.print_player_chips(player)

        pygame.image.save(self.screen, "icons/backgrounds/table_with_players_info.png")
        func = LoadImage("icons/backgrounds/table_with_players_info.png",
                         (1280, 720))
        self.table_image = func.execute()

    def card_deal_for_players(self):
        card_angles = []
        first_coordinates = []
        second_coordinates = []
        for player, (coord1, coord2) in self.hash_player_pos.items():
            first_coordinates.append(coord1)
            second_coordinates.append(coord2)

        players_cards_pos = first_coordinates + second_coordinates  # end_pos

        for player, angle in self.hash_player_ang.items():
            card_angles.append(angle)
        for player, angle in self.hash_player_ang.items():
            card_angles.append(angle)

        for end_pos, angle in zip(players_cards_pos, card_angles):
            animation = CardMoving(self.screen, self.deck_pos, end_pos, angle, self.table_image, self.card_back_image)
            animation.execute()

            pygame.image.save(self.screen,"icons/backgrounds/table_with_players_cards.png")
            func = LoadImage("icons/backgrounds/table_with_players_cards.png",(1280, 720))
            self.table_image = func.execute()

    def board_deal(self):
        for end_pos, angle in zip(self.deal_card_pos, self.deal_card_ang):
            animation = CardMoving(self.screen, self.deck_pos, end_pos, angle, self.table_image, self.card_back_image)
            animation.execute()

            pygame.image.save(self.screen,"icons/backgrounds/table_with_players_cards.png")
            func = LoadImage("icons/backgrounds/table_with_players_cards.png",(1280, 720))
            self.table_image = func.execute()

    def draw_active_zones(self, player, input_box_red_alpha):
        RED = (211, 47, 47)
        func = DrawButton(self.screen, self.button_font, "Fold", self.fold_button_rect, RED, self.WHITE)
        func.execute()

        BLUE = (58, 164, 197)
        if self.biggest_bet == 0:
            self.bet_n_rais_button_text = "Bet"
            func = DrawButton(self.screen, self.button_font, self.bet_n_rais_button_text, self.bet_n_rais_button_rect, BLUE, self.WHITE)
            func.execute()
        else:
            self.bet_n_rais_button_text = "Rais"
            func = DrawButton(self.screen, self.button_font, self.bet_n_rais_button_text, self.bet_n_rais_button_rect, BLUE, self.WHITE)
            func.execute()

        GREEN = (67, 160, 71)
        if self.biggest_bet == 0 or self.biggest_bet == int(self.hash_player_bet[player]):
            self.check_n_call_button_text = "Check"
            func = DrawButton(self.screen, self.button_font, self.check_n_call_button_text, self.check_n_call_button_rect, GREEN, self.WHITE)
            func.execute()
        else:
            self.check_n_call_button_text = "Call"
            func = DrawButton(self.screen, self.button_font, self.check_n_call_button_text, self.check_n_call_button_rect, GREEN, self.WHITE)
            func.execute()

        self.screen.blit(self.up_button_image, self.up_button_rect)
        self.screen.blit(self.down_button_image, self.down_button_rect)
        self.screen.blit(self.combination_button_image, self.combinations_button_rect)
        self.screen.blit(self.menu_button_image, self.menu_button_rect)
        self.screen.blit(self.question_button_image, self.question_button_rect)

        # Малюємо поле для введення ставок
        pygame.draw.rect(self.screen, self.GRAY, self.input_box_rect, border_radius=5)
        func = DrawText(self.player_bet, self.font, self.BLACK, self.screen,
                        self.input_box_rect.x + 10, self.input_box_rect.y + 10)
        func.execute()

        # Малюємо на місці поля для введення червоний прямокутник з заданим рівним прозорості
        input_box_with_alpha = pygame.Surface((self.input_box_rect.width, self.input_box_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            input_box_with_alpha,
            (255, 0, 0, input_box_red_alpha),
            input_box_with_alpha.get_rect(),
            border_radius=5
        )
        self.screen.blit(input_box_with_alpha, (self.input_box_rect.x, self.input_box_rect.y))

        pygame.display.update()

    def open_board_card(self, index):
        animation = CardRotation(self.screen, self.hash_card_image[self.table_cards[index]], self.card_back_image,
                                 self.deal_card_pos[index], self.deal_card_ang[index])
        animation.execute()

    def show_combinations(self):
        comb_window = tk.Tk()
        comb_window.title("Комбінації")
        comb_window.geometry("325x427")
        comb_window.resizable(False, False)

        image_path = "icons/combinations/Poker-Hand-Rankings-In-Order-650x855.png"
        image = Image.open(image_path)
        image = image.resize((325, 427))
        photo = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(comb_window, width=325, height=427)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=photo)

        comb_window.image = photo

        # Функція, яка виконується перед закриттям
        def on_closing():
            print("Вікно комбінацій було закрито користувачем!")
            comb_window.destroy()
            self.thread = None

        # Перехоплення події закриття вікна
        comb_window.protocol("WM_DELETE_WINDOW", on_closing)

        comb_window.mainloop()

    def set_view_card_rect(self, player):
        if self.hash_player_ang[player] == 0 or self.hash_player_ang[player] == 180:
            self.view_card_rect = pygame.Rect(self.hash_player_pos[player][0][0] - 100 // 2,
                                              self.hash_player_pos[player][0][1] - 150 // 2, 130, 150)

        elif self.hash_player_ang[player] == 90 or self.hash_player_ang[player] == 270:
            self.view_card_rect = pygame.Rect(self.hash_player_pos[player][0][0] - 150 // 2,
                                              self.hash_player_pos[player][0][1] - 100 // 2, 150, 130)

    def draw_nimbus(self, player):
        coord1, coord2 = self.hash_player_pos[player]

        x = None
        y = None
        if coord1 == (620, 620):
            x = 560
            y = 474
        elif coord1 == (620, 100):
            x = 560
            y = 184
        elif coord1 == (1180, 360):
            x = 1105
            y = 240
        elif coord1 == (100, 360):
            x = 27
            y = 240

        nimbus = pygame.Surface((150, 60), pygame.SRCALPHA)
        yellow_with_alpha = (255, 255, 0, 80)
        nimbus.fill(yellow_with_alpha)

        self.screen.blit(nimbus, (x, y))

    def print_bank(self):
        x = 850
        y = 475
        pygame.draw.rect(self.screen, self.GRAY, ((x, y), (300, 40)))
        pygame.draw.rect(self.screen, self.BLACK, ((x, y + 40), (300, 3)))

        text = "Bank: " + str(self.bank.getBank()) + " $"
        font = pygame.font.Font(None, 40)
        func = DrawText(text, font, self.WHITE, self.screen, x + 5, y + 5)
        func.execute()

        font = pygame.font.Font(None, 36)
        for player, i in zip(self.players, range(len(self.players))):
            if player.getIs_active():
                pygame.draw.rect(self.screen, self.GRAY, ((x, y + 43 + 40 * i), (300, 40)))
                text = player.getName() + ": " + self.hash_player_bet[player] + " $"
                func = DrawText(text, font, self.WHITE, self.screen, x + 5, y + 48 + 40 * i)
                func.execute()
            else:
                pygame.draw.rect(self.screen, self.GRAY, ((x, y + 43 + 40 * i), (300, 40)))
                text = player.getName() + ": " + "Fold"
                func = DrawText(text, font, self.WHITE, self.screen, x + 5, y + 48 + 40 * i)
                func.execute()

    def open_player_cards(self, player):
        animation = CardRotation(self.screen, self.hash_card_image[player.getHand()[0]], self.card_back_image,
                                 self.hash_player_pos[player][0], self.hash_player_ang[player])
        animation.execute()
        animation = CardRotation(self.screen, self.hash_card_image[player.getHand()[1]], self.card_back_image,
                                 self.hash_player_pos[player][1], self.hash_player_ang[player])
        animation.execute()

    def close_player_cards(self, player):
        animation = CardRotation(self.screen, self.card_back_image, self.hash_card_image[player.getHand()[0]],
                                 self.hash_player_pos[player][0], self.hash_player_ang[player])
        animation.execute()
        animation = CardRotation(self.screen, self.card_back_image, self.hash_card_image[player.getHand()[1]],
                                 self.hash_player_pos[player][1], self.hash_player_ang[player])
        animation.execute()

    def clear_table(self, current_stage):
        active_players = 0
        for player in self.players:
            if player.getIs_active():
                active_players += 1

        for player in self.players:
            if player.getIs_active():
                if active_players != 1:
                    self.close_player_cards(player)

                coord1, coord2 = self.hash_player_pos[player]
                func = BlitOverlay(self.screen, coord1) # Закриває карти гравця закладкою кольору столу
                func.execute()

                pygame.image.save(self.screen,"icons/backgrounds/table_with_players_cards.png")
                func = LoadImage("icons/backgrounds/table_with_players_cards.png", (1280, 720))
                self.table_image = func.execute()

                # "Скидує" карти у відбій
                func = TwoCardsMoving(self.screen, self.table_image, self.card_back_image, self.hash_player_pos[player],
                                      self.hash_player_ang[player] + random.randint(0, 180), self.discard_deck_pos)
                func.execute()

        if current_stage == "Flop":
            # Відкриваємо закриті карти
            for i in range(3, 5):
                animation = CardRotation(self.screen, self.hash_card_image[self.table_cards[i]], self.card_back_image,
                                         self.deal_card_pos[i], self.deal_card_ang[i])
                animation.execute()

            pygame.time.delay(3000)

            # Закриваємо всі карти
            for pos, ang, card in zip(self.deal_card_pos, self.deal_card_ang, self.table_cards):
                animation = CardRotation(self.screen, self.card_back_image, self.hash_card_image[card], pos, ang)
                animation.execute()

        elif current_stage == "Turn":
            # Відкриваємо закриту карту
            animation = CardRotation(self.screen, self.hash_card_image[4], self.card_back_image,
                                     self.deal_card_pos[4], self.deal_card_ang[4])
            animation.execute()

            pygame.time.delay(3000)

            # Закриваємо всі карти
            for pos, ang, card in zip(self.deal_card_pos, self.deal_card_ang, self.table_cards):
                animation = CardRotation(self.screen, self.card_back_image, self.hash_card_image[card], pos, ang)
                animation.execute()

        elif current_stage == "River" or current_stage == "Showdown":
            # Закриваємо всі карти
            for pos, ang, card in zip(self.deal_card_pos, self.deal_card_ang, self.table_cards):
                animation = CardRotation(self.screen, self.card_back_image, self.hash_card_image[card], pos, ang)
                animation.execute()

        for pos, ang, card in zip(self.deal_card_pos, self.deal_card_ang, self.table_cards):
            func = BlitOverlay(self.screen, pos) # Закриває карту на столі закладкою кольору столу
            func.execute()

            pygame.image.save(self.screen,"icons/backgrounds/table_with_players_cards.png")
            func = LoadImage("icons/backgrounds/table_with_players_cards.png",
                (1280, 720))
            self.table_image = func.execute()

            # "Скидує" карти у відбій
            func = CardMoving(self.screen, pos, self.discard_deck_pos, ang + random.randint(0, 180),
                              self.table_image, self.card_back_image)
            func.execute()

    def show_tutorial(self, player):
        def draw_fade_overlay(surface, target_pos, max_radius):
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            for y in range(720):
                for x in range(1280):
                    distance = math.hypot(x - target_pos[0], y - target_pos[1])
                    alpha = min(230, max(0, int(255 * (distance / max_radius))))
                    overlay.fill((0, 0, 0, alpha), (x, y, 1, 1))
            surface.blit(overlay, (0, 0))

        pygame.image.save(self.screen, "icons/backgrounds/table_with_players_cards.png")
        func = LoadImage("icons/backgrounds/table_with_players_cards.png", (1280, 720))
        self.table_image = func.execute()

        func = LoadImage("icons/clippy/clippy.png", (int(97 * 0.7), int(187 * 0.7)))
        clippy_image = func.execute()

        hash_explanation_fade_overlay_coord = {
            "Жовтим підсвічена інформація гравця, що зараз ходить":
                (635, 204),
            "Для того щоб подивитись чи закрити карти - натисніть на них":
                (self.hash_player_pos[player][0][0] + 50, self.hash_player_pos[player][0][1]),
            "Щоб збільшити чи зменшити ставку використовуйте стрілки. Також ставку можна ввести через клавіатуру, " +
            "для цього натисніть на поле введення.": (290, 534)
        }

        LIGHT_GRAY = (211, 211, 211)
        text = "Для продовження натисніть будь-де"
        for explanation, fade_overlay_coord in hash_explanation_fade_overlay_coord.items():
            running = True
            while running:
                self.screen.blit(self.table_image, (0, 0))

                draw_fade_overlay(self.screen, fade_overlay_coord, 100)

                func = DrawText(text, self.font, LIGHT_GRAY, self.screen, 495, 360)
                func.execute()
                self.screen.blit(clippy_image, (200, 600))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        running = False

        self.screen.blit(self.table_image, (0, 0))


    def turn(self, player):
        self.set_view_card_rect(player)

        self.player_bet = self.hash_player_bet[player]
        self.biggest_bet = max(int(value) for value in self.hash_player_bet.values())

        input_box_red_alpha = 0
        command = None

        running = True
        while running:

            self.draw_active_zones(player, input_box_red_alpha)

            # На кожному циклі зменшуємо рівень прозорості
            if input_box_red_alpha > 0:
                input_box_red_alpha -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box_rect.collidepoint(event.pos):
                        self.active_box = True
                    else:
                        self.active_box = False

                    if self.view_card_rect.collidepoint(event.pos):
                        if self.view_card_status == "Back":
                            self.open_player_cards(player)
                            self.view_card_status = "Front"

                        elif self.view_card_status == "Front":
                            self.close_player_cards(player)
                            self.view_card_status = "Back"

                    elif self.combinations_button_rect.collidepoint(event.pos):
                        if self.thread is None:
                            self.thread = threading.Thread(target=self.show_combinations, daemon=True)
                            self.thread.start()

                    elif self.menu_button_rect.collidepoint(event.pos):
                        print("menu")
                        return "Exit"

                    elif self.question_button_rect.collidepoint(event.pos):
                        print("question")
                        self.show_tutorial(player)

                    elif self.up_button_rect.collidepoint(event.pos):
                        if int(self.player_bet) < player.getChips():
                            if int(self.player_bet) + 10 > player.getChips():
                                self.player_bet = player.getChips()
                            else:
                                self.player_bet = str(int(self.player_bet) + 10)

                    elif self.down_button_rect.collidepoint(event.pos):
                        if int(self.player_bet) > 0:
                            if int(self.player_bet) <= 10:
                                self.player_bet = "0"
                            else:
                                self.player_bet = str(int(self.player_bet) - 10)

                    elif self.fold_button_rect.collidepoint(event.pos):
                        command = "Fold"
                        running = False

                    elif self.check_n_call_button_rect.collidepoint(event.pos):
                        if self.check_n_call_button_text == "Check":
                            command = "Check"
                            running = False

                        elif self.check_n_call_button_text == "Call":
                            command = "Call"
                            running = False

                    elif self.bet_n_rais_button_rect.collidepoint(event.pos):
                        if self.bet_n_rais_button_text == "Bet":
                            command = "Bet"
                            running = False

                        elif self.bet_n_rais_button_text == "Rais":
                            if int(self.player_bet) >= self.biggest_bet * 2:
                                command = "Rais"
                                running = False
                            else:
                                input_box_red_alpha = 148

                if event.type == pygame.KEYDOWN:
                    if self.active_box:
                        if event.key == pygame.K_BACKSPACE and len(self.player_bet) != 1:
                            self.player_bet = self.player_bet[:-1]

                        elif event.key == pygame.K_BACKSPACE and len(self.player_bet) == 1:
                            self.player_bet = "0"

                        elif event.unicode.isdigit() and int(self.player_bet + event.unicode) <= player.getChips():
                            if int(self.player_bet) == 0:
                                self.player_bet = event.unicode
                            else:
                                self.player_bet += event.unicode

        if self.view_card_status == "Front":
            self.close_player_cards(player)
            self.view_card_status = "Back"

        return command
