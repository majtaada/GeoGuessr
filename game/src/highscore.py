"""High score module"""
import sys
import pygame
import pandas as pd
from . import constants as cst


class HighScore:
    """Class for handling high score"""
    columns = ["Rank", "Mode", "Nickname", "Score"]

    def __init__(self, ui):
        """Initialize high score"""
        self.data = None
        self.ui = ui
        self.back_to_menu_rect = pygame.Rect(
            ui.width / 2 - cst.ARROW_WIDTH / 2,
            ui.height - cst.ARROW_HEIGHT,
            cst.ARROW_WIDTH,
            cst.ARROW_HEIGHT)
        self.get_high_scores()

    def run(self):
        """Run high score"""
        while True:
            if self.handle_events():
                return
            self.draw()
            self.ui.update_screen()

    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if self.back_to_menu_rect.collidepoint(mouse):
                    return True
        return False

    def draw(self):
        """Draw high score"""
        self.ui.draw_background()
        self.draw_texts()
        self.draw_back_to_menu_button()
        self.draw_high_scores()

    def draw_high_scores(self):
        """Draw high scores"""
        for i in range(len(self.data)):
            for j, column in enumerate(self.columns):
                text = self.ui.font.render(
                    str(self.data[column].iloc[i]), True, cst.TEXT_COLOR)
                text_rect = text.get_rect()
                text_rect.center = (self.ui.width /
                                    5 *
                                    (j +
                                     1), 0 +
                                    text.get_height() /
                                    2 +
                                    self.ui.logo.get_height() +
                                    50 +
                                    50 *
                                    (i +
                                     1))
                self.ui.screen.blit(text, text_rect)

    def draw_texts(self):
        """Draw texts"""
        text = self.ui.font.render("High Scores", True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (
            self.ui.width /
            2,
            0 +
            text.get_height() /
            2 +
            self.ui.logo.get_height())
        self.ui.screen.blit(text, text_rect)
        for i, column in enumerate(self.columns):
            text = self.ui.font.render(column, True, cst.TEXT_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (self.ui.width / 5 * (i + 1),
                                0 + text.get_height() / 2 + self.ui.logo.get_height() + 50)
            self.ui.screen.blit(text, text_rect)

    def get_high_scores(self):
        """Get high scores for visualization"""
        with open("game/data/high_scores/high_scores.txt", "r", encoding="utf-8") as file:
            self.data = file.readlines()
        self.data = [line.strip().split() for line in self.data]
        self.data = pd.DataFrame(
            self.data, columns=[
                "Mode", "Nickname", "Score"])
        self.data["Score"] = self.data["Score"].astype(int)
        self.data = self.data.sort_values(by=["Score"], ascending=False)
        self.data = self.data.head(5)
        self.data = self.data.reset_index(drop=True)
        self.data.insert(0, 'Rank', self.data.index + 1)

    def draw_back_to_menu_button(self):
        """Draw back to menu button"""
        mouse = pygame.mouse.get_pos()
        if self.back_to_menu_rect.collidepoint(mouse):
            self.ui.screen.blit(
                pygame.transform.rotate(
                    self.ui.arrow_clicked,
                    180),
                self.back_to_menu_rect)
        else:
            self.ui.screen.blit(
                pygame.transform.rotate(
                    self.ui.arrow_default,
                    180),
                self.back_to_menu_rect)
