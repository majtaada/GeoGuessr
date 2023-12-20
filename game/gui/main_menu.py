import pygame
import sys
from .play_button import PlayButton
from .highscore_button import HighScoreButton


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('graphics/background.jpeg')
        self.clock = pygame.time.Clock()
        self.logo = pygame.image.load('graphics/logo.png')
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.button1_rect = pygame.Rect(self.width / 2 - 125, self.height / 4, 250, 60)
        self.button2_rect = pygame.Rect(self.width / 2 - 125, self.height / 4 + 100, 250, 60)
        self.button3_rect = pygame.Rect(self.width / 2 - 125, self.height / 4 + 200, 250, 60)
        self.font = pygame.font.Font('graphics/monof55.ttf', 35)

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo, ((self.width - self.logo.get_width()) / 2, 0))

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()

        if self.width / 2 - 100 <= mouse[0] <= self.width / 2 + 100 and self.height / 4 <= mouse[
            1] <= self.height / 4 + 60:
            pygame.draw.rect(self.screen, "#b4d7ff", self.button1_rect)
        else:
            pygame.draw.rect(self.screen, "#90accc", self.button1_rect)

        if self.width / 2 - 100 <= mouse[0] <= self.width / 2 + 100 and self.height / 4 + 100 <= mouse[
            1] <= self.height / 4 + 160:
            pygame.draw.rect(self.screen, "#b4d7ff", self.button2_rect)
        else:
            pygame.draw.rect(self.screen, "#90accc", self.button2_rect)

        if self.width / 2 - 100 <= mouse[0] <= self.width / 2 + 100 and self.height / 4 + 200 <= mouse[
            1] <= self.height / 4 + 260:
            pygame.draw.rect(self.screen, "#b4d7ff", self.button3_rect)
        else:
            pygame.draw.rect(self.screen, "#90accc", self.button3_rect)

    def add_text_buttons(self):
        text = self.font.render('Play', True, "#000000")
        textRect = text.get_rect()
        textRect.center = (self.width / 2, self.height / 4 + 30)
        self.screen.blit(text, textRect)

        text = self.font.render('High Scores', True, "#000000")
        textRect = text.get_rect()
        textRect.center = (self.width / 2, self.height / 4 + 130)
        self.screen.blit(text, textRect)

        text = self.font.render('Quit', True, "#000000")
        textRect = text.get_rect()
        textRect.center = (self.width / 2, self.height / 4 + 230)
        self.screen.blit(text, textRect)

    def draw(self):
        self.draw_buttons()
        self.add_text_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button1_rect.collidepoint(event.pos):
                play_button = PlayButton(self.screen)
                play_button.run()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button2_rect.collidepoint(event.pos):
                highscore_button = HighScoreButton(self.screen)
                highscore_button.run()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button3_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            pygame.display.update()
