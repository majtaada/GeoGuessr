import pygame
import sys
from game.src.data_handler import DataHandler
from game.src.gamelogic import GameLogic
from application import Constants
import random

class GameModes:


    def __init__(self, ui):
        self.options = None
        self.data = None
        self.mode = None
        self.ui = ui
        self.cst = Constants()
        self.set_buttons()
        self.text_background = pygame.Rect(self.ui.width / 2 - self.TEXT_INPUT_WIDTH / 2,
                                           self.ui.height / 2 - self.TEXT_INPUT_HEIGHT / 2, self.TEXT_INPUT_WIDTH,
                                           self.TEXT_INPUT_HEIGHT)
        self.data_handler = DataHandler()
        self.button_rects = [pygame.Rect(self.ui.width / 4 - self.cst.BUTTON_WIDTH / 2, self.ui.height / 4, self.cst.BUTTON_WIDTH,
                                         self.BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 - self.cst.BUTTON_WIDTH / 2, self.ui.height / 4, self.cst.BUTTON_WIDTH,
                                         self.BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.BUTTON_WIDTH / 2, self.ui.height / 4 - 100,
                                         self.cst.BUTTON_WIDTH, self.cst.BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.BUTTON_WIDTH / 2, self.ui.height / 4 - 100,
                                         self.cst.BUTTON_WIDTH, self.cst.BUTTON_HEIGHT)]


    def draw_rect(self, fill_color=DEFAULT_BUTTON_COLOR, outline_color=(0, 0, 0), border=1):
        self.ui.screen.fill(outline_color, self.text_background)
        self.ui.screen.fill(fill_color, self.text_background.inflate(-border * 2, -border * 2))

    def add_text_button(self):
        x, y, w, h = self.text_background
        pygame.draw.rect(self.ui.screen, (255, 255, 255), self.text_background)
        for i in range(4):
            pygame.draw.rect(self.ui.screen, (0, 0, 0), (x - i, y - i, w, h), 1)

    def add_text(self):
        self.draw_rect()
        text = self.ui.font.render("Enter your nickname:", True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.width / 2, self.ui.height / 4)
        self.ui.screen.blit(text, text_rect)

    def add_text_input(self, nick):
        text = self.ui.font.render(nick, True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.width / 2, self.ui.height / 2)
        self.ui.screen.blit(text, text_rect)

    def get_nick(self):
        nick = ""
        while True:
            self.draw_background()
            self.add_text()
            self.add_text_input(nick)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    return nick
                if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                if event.type == pygame.KEYUP and event.key != pygame.K_BACKSPACE:
                    nick += event.unicode
                if len(nick) > 27:
                    nick = nick[:27]

    def run(self, mode):
        self.mode = mode
        self.data = self.data_handler.get_data(mode)
        self.get_nick()
        while True:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.ui.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rects[0].collidepoint(mouse):
                    self.modes_run[self.modes[0]](self.modes[0])
                if self.button_rects[1].collidepoint(mouse):
                    self.modes_run[self.modes[1]](self.modes[1])
                if self.button_rects[2].collidepoint(mouse):
                    self.modes_run[self.modes[2]](self.modes[2])
                if self.button_rects[3].collidepoint(mouse):
                    self.modes_run[self.modes[3]](self.modes[3])

    def draw(self):
        self.draw_background()
        self.draw_buttons()
        self.add_text_buttons()
        self.add_question()

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        rectangles = self.button_rects
        for rectangle in rectangles:
            if rectangle.collidepoint(mouse):
                pygame.draw.rect(self.ui.screen, self.PRESSED_BUTTON_COLOR, rectangle)
            else:
                pygame.draw.rect(self.screen, self.DEFAULT_BUTTON_COLOR, rectangle)

    def add_text_buttons(self):
        options = self.get_options()
        for i in range(4):
            text = self.ui.font.render(options[i]['country'], True, "#000000")
            text_rect = text.get_rect()
            text_rect.center = (self.width / 4 * (i + 1), self.height / 4 + 30)
            self.ui.screen.blit(text, text_rect)

    def get_options(self):
        self.options = []
        for i in range(4):
            option = random.choice(self.data)
            self.options.append(option)

    def add_question(self):
        question = random.choice(self.data)
        text = self.ui.font.render(question['country'], True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.width / 2, self.ui.height / 4 - 100)
        self.ui.screen.blit(text, text_rect)