"""This module contains the loading screen class"""

import sys
import pygame
from . import constants as cst


class LoadScreen:
    """Class for loading screen"""
    texts = [
        "You have 3 lives",
        "Collect most points to win!",
        "Question after using hint",
        "  is worth half the points ",
        "Press arrow to continue..."]

    def __init__(self, ui):
        """Initialize loading screen"""
        self.ui = ui
        self.arrow_rect = pygame.Rect(
            self.ui.width / 2 - cst.ARROW_WIDTH / 2,
            self.ui.height - cst.ARROW_HEIGHT,
            cst.ARROW_WIDTH,
            cst.ARROW_HEIGHT)

    def run(self):
        """Run loading screen"""
        while True:
            self.ui.draw_background()
            self.add_texts()
            self.add_arrow()
            pygame.display.update()
            self.ui.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.arrow_rect.collidepoint(mouse):
                        return True
            self.ui.update_screen()

    def add_arrow(self):
        """Add arrow to continue"""
        mouse = pygame.mouse.get_pos()
        if self.arrow_rect.collidepoint(mouse):
            self.ui.screen.blit(self.ui.arrow_clicked, self.arrow_rect)
        else:
            self.ui.screen.blit(self.ui.arrow_default, self.arrow_rect)

    def add_texts(self):
        """Add texts"""
        for i, text in enumerate(self.texts):
            font = pygame.font.Font('resources/monof55.ttf', 50)
            pygame_text = font.render(text, True, "#000000")
            text_rect = pygame_text.get_rect()
            if i == 3:
                text_rect.center = (
                    self.ui.width /
                    2,
                    self.ui.height /
                    2 -
                    175 +
                    i *
                    cst.TEXT_INPUT_HEIGHT -
                    25)
            else:
                text_rect.center = (
                    self.ui.width /
                    2,
                    self.ui.height /
                    2 -
                    175 +
                    i *
                    cst.TEXT_INPUT_HEIGHT)
            self.ui.screen.blit(pygame_text, text_rect)
