"""Getting nickname from user and running game modes"""

import sys
import pygame
from .data_handler import DataHandler
from .gamelogic import GameLogic
from .loading_screen import LoadScreen
from . import constants as cst


class GameModes:
    """Class for handling game modes"""

    def __init__(self, ui):
        """Initialize game modes"""
        self.nick = None
        self.options = None
        self.mode = None
        self.ui = ui
        self.text_background = pygame.Rect(
            self.ui.width / 2 - cst.TEXT_INPUT_WIDTH / 2,
            self.ui.height / 2 - cst.TEXT_INPUT_HEIGHT / 2,
            cst.TEXT_INPUT_WIDTH,
            cst.TEXT_INPUT_HEIGHT)
        self.data_handler = DataHandler()
        self.load_screen = LoadScreen(self.ui)

    def draw_rect(self, outline_color=(0, 0, 0), border=1):
        """Draw rectangle"""
        fill_color = cst.DEFAULT_BUTTON_COLOR
        self.ui.screen.fill(outline_color, self.text_background)
        self.ui.screen.fill(
            fill_color, self.text_background.inflate(-border * 2, -border * 2))

    def add_text_button(self):
        """Add text button"""
        x, y, w, h = self.text_background
        pygame.draw.rect(self.ui.screen, (255, 255, 255), self.text_background)
        for i in range(4):
            pygame.draw.rect(self.ui.screen, (0, 0, 0),
                             (x - i, y - i, w, h), 1)

    def add_text(self):
        """Add text"""
        self.draw_rect()
        text = self.ui.font.render("Enter your nickname:", True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 4)
        self.ui.screen.blit(text, text_rect)

    def add_text_input(self, nick):
        """Add text input"""
        text = self.ui.font.render(nick, True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 2)
        self.ui.screen.blit(text, text_rect)

    def get_nick(self):
        """Get nickname"""
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

    def save_score(self, score):
        """Save score to file"""
        with open("game/data/high_scores/high_scores.txt", "a", encoding="utf-8") as file:
            if self.mode == "all_in_one":
                file.write(f"AllInOne {self.nick[:5]} {score}\n")
            else:
                file.write(
                    f"{self.mode.capitalize()} {self.nick.replace(' ', '')} {score}\n")

    def run(self, mode):
        """Get nick and run game modes"""
        self.mode = mode
        data = self.data_handler.get_data(mode)
        if self.nick is None:
            self.nick = self.get_nick()
        gamelogic = GameLogic(self.ui, data, self.mode)
        self.load_screen.run()
        gamelogic.run()
        self.save_score(gamelogic.get_score())
