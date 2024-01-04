"""Play button module"""

import sys
import pygame
from .nickname_getter import GameModes
from . import constants as cst


class PlayButton:
    """Class for handling play button"""

    def __init__(self, ui):
        """Initialize play button"""
        self.ui = ui
        self.button_rects = [
            pygame.Rect(
                self.ui.width / 2 - cst.MENU_BUTTON_WIDTH / 2,
                self.ui.height / 5,
                cst.MENU_BUTTON_WIDTH,
                cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(
                self.ui.width / 2 - cst.MENU_BUTTON_WIDTH / 2,
                self.ui.height / 5 + 100,
                cst.MENU_BUTTON_WIDTH,
                cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(
                self.ui.width / 2 - cst.MENU_BUTTON_WIDTH / 2,
                self.ui.height / 5 + 200,
                cst.MENU_BUTTON_WIDTH,
                cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(
                self.ui.width / 2 - cst.MENU_BUTTON_WIDTH / 2,
                self.ui.height / 5 + 300,
                cst.MENU_BUTTON_WIDTH,
                cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(
                self.ui.width / 2 - cst.MENU_BUTTON_WIDTH / 2,
                self.ui.height / 5 + 400,
                cst.MENU_BUTTON_WIDTH,
                cst.MENU_BUTTON_HEIGHT)]
        self.game_modes = GameModes(ui)
        self.modes = ["flags", "capital", "shapes", "all_in_one"]

    def run(self):
        """Run play button"""
        while True:
            mode = self.handle_events()
            if mode == "main_menu":
                return
            if mode is not None:
                self.game_modes.run(mode)
            self.draw()
            self.ui.update_screen()

    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + \
                        100 and self.ui.height / 5 <= mouse[1] <= self.ui.height / 5 + 80:
                    return "flags"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + \
                        100 and self.ui.height / 5 + 100 <= mouse[1] <= self.ui.height / 5 + 180:
                    return "capital"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + \
                        100 and self.ui.height / 5 + 200 <= mouse[1] <= self.ui.height / 5 + 280:
                    return "shapes"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + \
                        100 and self.ui.height / 5 + 300 <= mouse[1] <= self.ui.height / 5 + 380:
                    return "all_in_one"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + \
                        100 and self.ui.height / 5 + 400 <= mouse[1] <= self.ui.height / 5 + 480:
                    return "main_menu"
            return None

    def draw_buttons(self):
        """Draw buttons"""
        mouse = pygame.mouse.get_pos()
        texts = ["Flags", "Capitals", "Country Shapes", "All in one", "Back"]
        rects = self.button_rects
        for i in range(len(self.button_rects)):
            if rects[i].collidepoint(mouse):
                pygame.draw.rect(
                    self.ui.screen,
                    cst.PRESSED_BUTTON_COLOR,
                    rects[i])
            else:
                pygame.draw.rect(
                    self.ui.screen,
                    cst.DEFAULT_BUTTON_COLOR,
                    rects[i])
            text = self.ui.font.render(texts[i], True, "#000000")
            text_rect = text.get_rect()
            text_rect.center = rects[i].center
            self.ui.screen.blit(text, text_rect)

    def draw(self):
        """Draw play button"""
        self.ui.draw_background()
        self.draw_buttons()
