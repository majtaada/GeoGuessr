import pygame
import sys
from game.src.highscore_button import HighScoreButton
from game.src.play_button import PlayButton
from game.src.game_modes import GameModes
from resources.constants import Constants


class MainMenu:

    def __init__(self, ui):
        self.mode = None
        self.ui = ui
        self.cst = Constants()
        self.width = self.ui.screen.get_width()
        self.height = self.ui.screen.get_height()
        self.button_rects = [
            pygame.Rect(self.width / 2 - 125, self.height / 4, self.cst.MENU_BUTTON_WIDTH, self.cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(self.width / 2 - 125, self.height / 4 + 100, self.cst.MENU_BUTTON_WIDTH,
                        self.cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(self.width / 2 - 125, self.height / 4 + 200, self.cst.MENU_BUTTON_WIDTH,
                        self.cst.MENU_BUTTON_HEIGHT)]

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        rectangles = self.button_rects
        for rectangle in rectangles:
            if rectangle.collidepoint(mouse):
                pygame.draw.rect(self.ui.screen, self.cst.PRESSED_BUTTON_COLOR, rectangle)
            else:
                pygame.draw.rect(self.ui.screen, self.cst.DEFAULT_BUTTON_COLOR, rectangle)

    def add_text_buttons(self):
        texts = ["Play", "High Scores", "Quit"]
        for i, t in enumerate(texts):
            text = self.ui.font.render(t, True, "#000000")
            text_rect = text.get_rect()
            text_rect.center = (self.width / 2, self.height / 4 + 30 + i * 100)
            self.ui.screen.blit(text, text_rect)

    def draw(self):
        self.ui.draw_background()
        self.draw_buttons()
        self.add_text_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rects[0].collidepoint(
                    event.pos):
                play_button = PlayButton(self.ui)
                play_button.run()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rects[1].collidepoint(
                    event.pos):
                highscore_button = HighScoreButton(self.ui)
                highscore_button.run()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rects[2].collidepoint(
                    event.pos):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            if self.mode is not None:
                game_modes = GameModes(self.ui)
                game_modes.run(self.mode)
                self.mode = None
            self.handle_events()
            self.draw()
            self.ui.clock.tick(60)
            pygame.display.flip()
            pygame.display.update()
