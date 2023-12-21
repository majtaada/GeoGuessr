import pygame
import sys
from game.src.game_modes import GameModes


class FlagsGamemode(GameModes):
    def __init__(self, ui):
        super().__init__(ui)
        self.ui = ui
        self.screen = ui.screen
        self.font = ui.font
        self.background = ui.background
        self.logo = ui.logo

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.update()


class FlagGamemode:
    pass
