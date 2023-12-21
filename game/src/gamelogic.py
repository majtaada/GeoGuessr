import pygame
import sys
import random
from resources.constants import Constants


class GameLogic:
    question = "Which country capital is this?:"

    def __init__(self, ui, data, mode):
        self.options_dict = None
        self.ui = ui
        self.data = data
        self.mode = mode
        self.cst = Constants()
        self.button_rects = [pygame.Rect(self.ui.width / 4 - self.cst.QUESTION_BUTTON_WIDTH / 2, self.ui.height / 4 * 3,
                                         self.cst.QUESTION_BUTTON_WIDTH,
                                         self.cst.MENU_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 - self.cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 4 * 3 - 100,
                                         self.cst.QUESTION_BUTTON_WIDTH,
                                         self.cst.MENU_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 4 * 3,
                                         self.cst.QUESTION_BUTTON_WIDTH, self.cst.MENU_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 4 * 3 - 100,
                                         self.cst.QUESTION_BUTTON_WIDTH, self.cst.MENU_BUTTON_HEIGHT)]
        self.correct_answer_index = None
        self.modes = ["flags", "capital", "shapes", "all_in_one"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.ui.clock.tick(60)
            pygame.display.flip()
            pygame.display.update()

    def add_text_buttons(self):
        if self.options_dict is None:
            options = self.data.sample(n=4, replace=False)
            self.options_dict = self.fill_options_dict(options)
            print(self.options_dict)
            self.correct_answer_index = random.randint(0, 3)
        for i, option in enumerate(self.options_dict["country"]):
            text = self.ui.font.render(option, True, "#000000")
            text_rect = text.get_rect()
            if i < 2:
                text_rect.center = (self.ui.width / 4, self.ui.height / 4 * 3 - i * 100 + 30)
            else:
                text_rect.center = (self.ui.width / 4 * 3, self.ui.height / 4 * 3 - (i - 2) * 100 + 30)
            self.ui.screen.blit(text, text_rect)

    def fill_options_dict(self, options):
        options_dict = {"country": [], f"{self.mode}": []}
        for column in options.columns:
            for value in options[column]:
                options_dict[column].append(value)
        return options_dict

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        rectangles = self.button_rects
        for rectangle in rectangles:
            if rectangle.collidepoint(mouse):
                pygame.draw.rect(self.ui.screen, self.cst.PRESSED_BUTTON_COLOR, rectangle)
            else:
                pygame.draw.rect(self.ui.screen, self.cst.DEFAULT_BUTTON_COLOR, rectangle)
        self.add_text_buttons()

    def draw(self):
        self.ui.draw_background()
        self.draw_buttons()
        if self.mode == "flags" or self.mode == "shapes":
            self.draw_image()
        if self.mode == "capital":
            self.draw_text()

    def draw_image(self):
        image = self.options_dict[self.mode][self.correct_answer_index]
        image = pygame.transform.scale(image, (426, 213))
        image_rect = image.get_rect()
        image_rect.center = (self.ui.width / 2 , self.ui.height / 4 + 42 ) # 42 is half of the height of the text
        self.ui.screen.blit(image, image_rect)

    def draw_question(self):
        text = self.ui.font.render(self.question, True, self.cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 8 + 42)
        self.ui.screen.blit(text, text_rect)

    def draw_text(self):
        self.draw_question()
        font = pygame.font.Font('resources/monof55.ttf', 55)
        text = font.render(self.options_dict[self.mode][self.correct_answer_index], True, self.cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 3 + 42)
        self.ui.screen.blit(text, text_rect)
