import pygame
import sys
import random
import math
import resources.constants as cst
from game.src.quiz_drawings import QuizDrawings
from game.src.data_handler import DataHandler
from game.src.end_screen import EndScreen


class GameLogic:
    """Class for handling game logic."""
    def __init__(self, ui, data, mode):
        """Initialize game logic."""
        self.options_dict = None
        self.ui = ui
        self.data = data
        self.data_handler = DataHandler()
        self.mode = mode
        self.modes = ["flags", "capital", "shapes"]
        self.all_in_one = False
        self.changed_mode = False
        self.quiz_draw = QuizDrawings(self.ui)

    def handle_events(self):
        """Handle events."""
        button_rects = self.quiz_draw.button_rects
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quiz_draw.clicked is None:
                    for i in range(len(button_rects)):
                        if button_rects[i].collidepoint(mouse):
                            if self.quiz_draw.correct_answer_index == i:
                                self.correct_answer()
                            elif self.quiz_draw.correct_answer_index != i:
                                self.incorrect_answer()
                            self.quiz_draw.clicked = i

                    if self.quiz_draw.bulb_rect.collidepoint(mouse):
                        self.set_hint()
                if self.quiz_draw.arrow_rect.collidepoint(mouse) and self.quiz_draw.clicked is not None:
                    self.next_question()

    def set_hint(self):
        """Set hint"""
        self.quiz_draw.hint = True
        hint = self.data_handler.get_hint(self.quiz_draw.options_dict["country"][self.quiz_draw.correct_answer_index])
        self.quiz_draw.hint_word = hint.iloc[0]['region']

    def next_question(self):
        """Reset all variables for next question."""
        self.quiz_draw.clicked = None
        self.quiz_draw.correct_answer_index = None
        self.quiz_draw.options_dict = None
        self.quiz_draw.hint = False
        self.changed_mode = False

    def correct_answer(self):
        """Handle correct answer."""
        scaler = self.data_handler.get_scaler(
            self.quiz_draw.options_dict["country"][self.quiz_draw.correct_answer_index],
            self.mode)
        scaler = 100 - scaler
        to_add = cst.DEFAULT_SCORE * math.sqrt(scaler / 100)
        if self.quiz_draw.hint:
            to_add *= 0.5
        self.quiz_draw.score += round(to_add)

    def incorrect_answer(self):
        """Handle incorrect answer."""
        self.quiz_draw.life -= 1

    def run(self):
        """Run game logic."""
        if self.mode == 'all_in_one':
            self.all_in_one = True
        while self.quiz_draw.life != 0:
            if self.all_in_one and not self.changed_mode:
                self.mode = self.modes[random.randint(0, 2)]
                self.changed_mode = True
            self.draw()
            self.handle_events()
            self.ui.clock.tick(60)
            pygame.display.flip()
            pygame.display.update()
        end_screen = EndScreen(self.ui, self.quiz_draw.score)
        end_screen.run()

    def get_score(self):
        """Return score."""
        return self.quiz_draw.score

    def fill_options_dict(self, options):
        """Fill options dictionary."""
        if self.all_in_one:
            options = options[["country", self.mode]]
        self.quiz_draw.options_dict = {"country": [], f"{self.mode}": []}
        for column in options.columns:
            for value in options[column]:
                self.quiz_draw.options_dict[column].append(value)

    def get_random_options(self):
        """Get random options."""
        if self.quiz_draw.options_dict is None:
            options = self.data.sample(n=4, replace=False)
            self.fill_options_dict(options)
            self.quiz_draw.correct_answer_index = random.randint(0, 3)

    def draw(self):
        """Drawings for game logic."""
        self.ui.draw_background()
        self.quiz_draw.draw_hearts()
        self.quiz_draw.draw_buttons()
        self.get_random_options()
        self.quiz_draw.add_text_buttons()
        self.quiz_draw.draw_light_bulb()
        self.quiz_draw.draw_score()
        if self.quiz_draw.hint:
            self.quiz_draw.draw_hint()
        if self.quiz_draw.clicked is not None:
            self.quiz_draw.draw_next_button()
        if self.mode == "flags" or self.mode == "shapes":
            self.quiz_draw.draw_image(self.mode)
        if self.mode == "capital":
            self.quiz_draw.draw_text(self.mode)
