import pygame
import sys
import random
from resources.constants import Constants


class GameLogic:
    def __init__(self, ui, data, mode):
        self.ui = ui
        self.data = data
        self.mode = mode
        self.cst = Constants()
        self.button_rects = [pygame.Rect(self.ui.width / 4 - self.cst.MENU_BUTTON_WIDTH / 2, self.ui.height / 4,
                                         self.cst.MENU_BUTTON_WIDTH,
                                         self.cst.MENU_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 - self.cst.MENU_BUTTON_WIDTH / 2, self.ui.height / 4,
                                         self.cst.MENU_BUTTON_WIDTH,
                                         self.cst.MENU_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.MENU_BUTTON_WIDTH / 2,
                                         self.ui.height / 4 - 100,
                                         self.cst.MENU_BUTTON_WIDTH, self.cst.MENU_BUTTON_HEIGHT),
                             pygame.Rect(self.ui.width / 4 * 3 - self.cst.MENU_BUTTON_WIDTH / 2,
                                         self.ui.height / 4 - 100,
                                         self.cst.MENU_BUTTON_WIDTH, self.cst.MENU_BUTTON_HEIGHT)]
        self.correct_answer_index = None
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
        options = self.data.sample(n=4, replace=False)
        options_dict = to_dict()
        self.correct_answer_index = random.randint(0, 3)
        for i, option in enumerate(options_dict.keys()):
            text = self.ui.font.render(option, True, "#000000")
            text_rect = text.get_rect()
            text_rect.center = (self.ui.width / 4 * (i + 1), self.ui.height / 4 + 30)
            self.ui.screen.blit(text, text_rect)

    def to_dict(self):
        
    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        rectangles = self.button_rects
        for rectangle in rectangles:
            if rectangle.collidepoint(mouse):
                pygame.draw.rect(self.ui.screen, self.cst.PRESSED_BUTTON_COLOR, rectangle)
            else:
                pygame.draw.rect(self.ui.screen, self.cst.DEFAULT_BUTTON_COLOR, rectangle)

    def draw(self):
        self.ui.draw_background()
        self.draw_buttons()
        self.add_text_buttons()
