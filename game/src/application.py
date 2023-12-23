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
        self.font = pygame.font.Font('resources/monof55.ttf', 35)
        self.background = pygame.image.load('resources/background.jpeg')
        self.logo = pygame.image.load('resources/logo.png')
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.gray_heart = pygame.image.load('resources/heart_gray.png')
        self.red_heart = pygame.image.load('resources/heart_red.png')
        self.arrow_clicked = pygame.image.load('resources/arrow_clicked.png')
        self.arrow_default = pygame.image.load('resources/arrow_default.png')
        self.bulb_gray = pygame.image.load('resources/bulb_gray.png')
        self.bulb_yellow = pygame.image.load('resources/bulb_yellow.png')

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, ((self.screen.get_width() - self.logo.get_width()) / 2, 0))

