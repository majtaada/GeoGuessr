import pygame
import sys
from game.src.data_handler import DataHandler
from game.src.gamelogic import GameLogic
from resources.constants import Constants
import random


class GameModes:

    def __init__(self, ui):
        self.options = None
        self.data = None
        self.mode = None
        self.ui = ui
        self.cst = Constants()
        self.text_background = pygame.Rect(self.ui.width / 2 - self.cst.TEXT_INPUT_WIDTH / 2,
                                           self.ui.height / 2 - self.cst.TEXT_INPUT_HEIGHT / 2,
                                           self.cst.TEXT_INPUT_WIDTH,
                                           self.cst.TEXT_INPUT_HEIGHT)
        self.data_handler = DataHandler()

    def draw_rect(self, outline_color=(0, 0, 0), border=1):
        fill_color = self.cst.DEFAULT_BUTTON_COLOR
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
        text_rect.center = (self.ui.width / 2, self.ui.height / 4)
        self.ui.screen.blit(text, text_rect)

    def add_text_input(self, nick):
        text = self.ui.font.render(nick, True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 2)
        self.ui.screen.blit(text, text_rect)

    def get_nick(self):
        nick = ""
        while True:
            self.ui.draw_background()
            self.add_text()
            self.add_text_input(nick)
            pygame.display.update()
            self.ui.clock.tick(60)
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
        print(mode)
        self.data = self.data_handler.get_data(mode)
        print(len(self.data))
        self.get_nick()
        gamelogic = GameLogic(self.ui, self.data, self.mode)
        gamelogic.run()


