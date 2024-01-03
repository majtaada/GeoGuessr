import pygame
import sys
import resources.constants as cst


class LoadScreen:
    texts = ["Collect most points to win!", "Question after using hint", "is worth half the points ",
             "Press arrow to continue"]

    def __init__(self, ui):
        self.ui = ui
        self.arrow_rect = pygame.Rect(self.ui.width / 2 - cst.ARROW_WIDTH / 2, self.ui.height - cst.ARROW_HEIGHT,
                                      cst.ARROW_WIDTH,
                                      cst.ARROW_HEIGHT)

    def run(self):
        while True:
            self.ui.draw_background()
            self.add_texts()
            self.add_arrow()
            pygame.display.update()
            self.ui.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    if self.arrow_rect.collidepoint(mouse):
                        return True
            pygame.display.flip()
            pygame.display.update()

    def add_arrow(self):
        mouse = pygame.mouse.get_pos()
        if self.arrow_rect.collidepoint(mouse):
            self.ui.screen.blit(self.ui.arrow_clicked, self.arrow_rect)
        else:
            self.ui.screen.blit(self.ui.arrow_default, self.arrow_rect)

    def add_texts(self):
        for i in range(len(self.texts)):
            font = pygame.font.Font('resources/monof55.ttf', 50)
            text = font.render(self.texts[i], True, "#000000")
            text_rect = text.get_rect()
            text_rect.center = (self.ui.width / 2, self.ui.height / 2 - 125 + i * cst.TEXT_INPUT_HEIGHT)
            self.ui.screen.blit(text, text_rect)
