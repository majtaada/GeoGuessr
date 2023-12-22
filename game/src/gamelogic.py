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
        self.button_rects = [pygame.Rect(self.ui.width / 4 - self.cst.QUESTION_BUTTON_WIDTH / 2, self.ui.height / 5 * 4,
                                         self.cst.QUESTION_BUTTON_WIDTH,
                                         self.cst.QUESTION_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 - self.cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 5 * 4 - self.cst.QUESTION_BUTTON_GAP_HEIGHT,
                                         self.cst.QUESTION_BUTTON_WIDTH,
                                         self.cst.QUESTION_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 5 * 4,
                                         self.cst.QUESTION_BUTTON_WIDTH, self.cst.QUESTION_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 5 * 4 - self.cst.QUESTION_BUTTON_GAP_HEIGHT,
                                         self.cst.QUESTION_BUTTON_WIDTH, self.cst.QUESTION_BUTTON_HEIGHT)]
        self.correct_answer_index = None
        self.modes = ["flags", "capital", "shapes"]
        self.life = 3
        self.clicked = None
        self.all_in_one = False
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.button_rects)):
                    if self.button_rects[i].collidepoint(mouse):
                        self.clicked = i
                        if self.correct_answer_index == i:
                            self.correct_answer()
                        else:
                            self.incorrect_answer()

    def draw_next_button(self):
        self.score += 1
        pass

    def correct_answer(self):
        pass
        # draw_next_button

    def incorrect_answer(self):
        self.life -= 1
        pass

    def run(self):
        if self.mode == 'all_in_one':
            self.all_in_one = True
        while self.life != 0:
            if self.all_in_one and self.clicked is not None:
                self.mode = self.modes[random.randint(0, 2)]
            self.draw()
            self.handle_events()
            if self.clicked is not None:
                self.draw_next_button()
            self.ui.clock.tick(60)
            pygame.display.flip()
            pygame.display.update()

    def add_text_buttons(self):
        if self.options_dict is None:
            options = self.data.sample(n=4, replace=False)
            self.options_dict = self.fill_options_dict(options)
            self.correct_answer_index = random.randint(0, 3)
        for i, option in enumerate(self.options_dict["country"]):
            option_word = option.split()
            if len(option_word) > 2:
                self.handle_long_words(option_word, i)
            else:
                text = self.ui.font.render(option, True, self.cst.TEXT_COLOR)
                text_rect = text.get_rect()
                text_rect.center = self.button_rects[i].center
                self.ui.screen.blit(text, text_rect)

    def handle_long_words(self, option_word, i):
        option_line1 = " ".join(option_word[:((len(option_word) + 1) // 2)])
        option_line2 = " ".join(option_word[((len(option_word) + 1) // 2):])
        font = pygame.font.Font('resources/monof55.ttf', 30)
        text = font.render(option_line1, True, self.cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.button_rects[i].center[0], self.button_rects[i].center[1] - text.get_size()[1] / 2)
        self.ui.screen.blit(text, text_rect)
        text = font.render(option_line2, True, self.cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.button_rects[i].center[0], self.button_rects[i].center[1] + text.get_size()[1] / 2)
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
        for i, rectangle in enumerate(rectangles):
            if self.clicked == i == self.correct_answer_index:
                pygame.draw.rect(self.ui.screen, self.cst.CORRECT_ANSWER_COLOR, rectangle)
            elif self.clicked == i != self.correct_answer_index:
                pygame.draw.rect(self.ui.screen, self.cst.WRONG_ANSWER_COLOR, rectangle)
            else:
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
        if self.mode == 'flags':
            image = pygame.transform.scale(image, (426, 213))
        image_rect = image.get_rect()
        image_rect.center = (self.ui.width / 2, self.ui.height / 4 + 42)  # 42 is half of the height of the text
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
