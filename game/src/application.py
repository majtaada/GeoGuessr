from game.src.main_menu import MainMenu
import pygame


class Application:
    def __init__(self):
        self.UI = UI()
        self.main_menu = MainMenu(self.UI)

    def run(self):
        while True:
            self.main_menu.run()


class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GeoQuizzr")
        self.clock = pygame.time.Clock()
        self.state = "main_menu"
        self.font = pygame.font.Font('graphics/monof55.ttf', 35)
        self.background = pygame.image.load('graphics/background.jpeg')
        self.logo = pygame.image.load('graphics/logo.png')
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, ((self.screen.get_width() - self.logo.get_width()) / 2, 0))


class Constants:
    DEFAULT_BUTTON_COLOR = "#90accc"
    PRESSED_BUTTON_COLOR = "#b4d7ff"
    BUTTON_WIDTH = 255
    BUTTON_HEIGHT = 60
    TEXT_INPUT_WIDTH = 500
    TEXT_INPUT_HEIGHT = 85
    TEXT_INPUT_BORDER = 1
    TEXT_INPUT_OUTLINE_COLOR = "#000000"
    TEXT_COLOR = "#000000"
    CORRECT_ANSWER_COLOR = "#00ff00"
    WRONG_ANSWER_COLOR = "#ff0000"
