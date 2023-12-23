import pygame
import resources.constants as cst


class QuizDrawings:
    question = "Which country capital is this?:"

    def __init__(self, ui):
        self.hint_word = None
        self.ui = ui
        self.button_rects = [pygame.Rect(self.ui.width / 4 - cst.QUESTION_BUTTON_WIDTH / 2, self.ui.height / 5 * 4,
                                         cst.QUESTION_BUTTON_WIDTH,
                                         cst.QUESTION_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 - cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 5 * 4 - cst.QUESTION_BUTTON_GAP_HEIGHT,
                                         cst.QUESTION_BUTTON_WIDTH,
                                         cst.QUESTION_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 5 * 4,
                                         cst.QUESTION_BUTTON_WIDTH, cst.QUESTION_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - cst.QUESTION_BUTTON_WIDTH / 2,
                                         self.ui.height / 5 * 4 - cst.QUESTION_BUTTON_GAP_HEIGHT,
                                         cst.QUESTION_BUTTON_WIDTH, cst.QUESTION_BUTTON_HEIGHT)]
        self.arrow_rect = pygame.Rect(self.ui.width - cst.ARROW_WIDTH, self.ui.height / 4, cst.ARROW_WIDTH,
                                      cst.ARROW_HEIGHT)
        self.bulb_rect = pygame.Rect(50, self.ui.height / 5, cst.BULB_WIDTH, cst.BULB_HEIGHT)
        self.correct_answer_index = None
        self.clicked = None
        self.life = 3
        self.score = 0
        self.options_dict = None
        self.hint = False

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        rectangles = self.button_rects
        for i, rectangle in enumerate(rectangles):
            if self.clicked == i == self.correct_answer_index:
                pygame.draw.rect(self.ui.screen, cst.CORRECT_ANSWER_COLOR, rectangle)
            elif self.clicked == i != self.correct_answer_index:
                pygame.draw.rect(self.ui.screen, cst.WRONG_ANSWER_COLOR, rectangle)
            else:
                if rectangle.collidepoint(mouse):
                    pygame.draw.rect(self.ui.screen, cst.PRESSED_BUTTON_COLOR, rectangle)
                else:
                    pygame.draw.rect(self.ui.screen, cst.DEFAULT_BUTTON_COLOR, rectangle)

    def add_text_buttons(self):
        for i, option in enumerate(self.options_dict["country"]):
            option_word = option.split()
            if len(option_word) > 2:
                self.handle_long_words(option_word, i)
            else:
                text = self.ui.font.render(option, True, cst.TEXT_COLOR)
                text_rect = text.get_rect()
                text_rect.center = self.button_rects[i].center
                self.ui.screen.blit(text, text_rect)

    def draw_hearts(self):
        for i in range(3):
            if i <= self.life - 1:
                image = pygame.transform.scale(self.ui.red_heart, (35, 35))
                self.ui.screen.blit(image, (35 * i + 5, 5))
            else:
                image = pygame.transform.scale(self.ui.gray_heart, (35, 35))
                self.ui.screen.blit(image, (35 * i + 5, 5))

    def handle_long_words(self, option_word, i):
        option_line1 = " ".join(option_word[:((len(option_word) + 1) // 2)])
        option_line2 = " ".join(option_word[((len(option_word) + 1) // 2):])
        font = pygame.font.Font('resources/monof55.ttf', 30)
        text = font.render(option_line1, True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.button_rects[i].center[0], self.button_rects[i].center[1] - text.get_size()[1] / 2)
        self.ui.screen.blit(text, text_rect)
        text = font.render(option_line2, True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.button_rects[i].center[0], self.button_rects[i].center[1] + text.get_size()[1] / 2)
        self.ui.screen.blit(text, text_rect)

    def draw_image(self, mode):
        image = self.options_dict[mode][self.correct_answer_index]
        if mode == 'flags':
            image = pygame.transform.scale(image, (426, 213))
        image_rect = image.get_rect()
        image_rect.center = (self.ui.width / 2, self.ui.height / 4 + cst.DEFAULT_QUESTION_GAP)
        self.ui.screen.blit(image, image_rect)

    def draw_question(self):
        text = self.ui.font.render(self.question, True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 8 + cst.DEFAULT_QUESTION_GAP)
        self.ui.screen.blit(text, text_rect)

    def draw_text(self, mode):
        self.draw_question()
        font = pygame.font.Font('resources/monof55.ttf', 55)
        text = font.render(self.options_dict[mode][self.correct_answer_index], True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 3 + cst.DEFAULT_QUESTION_GAP)
        self.ui.screen.blit(text, text_rect)

    def draw_next_button(self):
        mouse = pygame.mouse.get_pos()
        if self.arrow_rect.collidepoint(mouse):
            self.ui.screen.blit(self.ui.arrow_clicked, self.arrow_rect)
        else:
            self.ui.screen.blit(self.ui.arrow_default, self.arrow_rect)

    def draw_light_bulb(self):
        if self.hint:
            self.ui.screen.blit(self.ui.bulb_yellow, self.bulb_rect)
        else:
            mouse = pygame.mouse.get_pos()
            if self.bulb_rect.collidepoint(mouse):
                self.ui.screen.blit(self.ui.bulb_yellow, self.bulb_rect)
            else:
                self.ui.screen.blit(self.ui.bulb_gray, self.bulb_rect)

    def draw_hint(self):
        font = pygame.font.Font('resources/monof55.ttf', 20)
        text = font.render(self.hint_word, True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.bulb_rect.center[0], self.bulb_rect.center[1] + self.bulb_rect.height / 2 + 10)
        self.ui.screen.blit(text, text_rect)

    def draw_score(self):
        font = pygame.font.Font('resources/monof55.ttf', 35)
        text = font.render(str(self.score), True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width - text.get_size()[0], 35)
        self.ui.screen.blit(text, text_rect)

