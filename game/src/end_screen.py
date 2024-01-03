import pygame
import sys
import resources.constants as cst


class EndScreen:
    def __init__(self, ui, score):
        self.back_to_menu_rect = pygame.Rect(ui.width / 2 - cst.ARROW_WIDTH / 2, ui.height / 4 * 3,
                                             cst.ARROW_WIDTH, cst.ARROW_HEIGHT)
        self.ui = ui
        self.score = score

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.back_to_menu_rect.collidepoint(mouse):
                        return
            self.draw()
            self.ui.clock.tick(60)
            pygame.display.flip()
            pygame.display.update()

    def draw(self):
        self.ui.draw_background()
        text = self.ui.font.render("Your score is: ", True, cst.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 3)
        self.ui.screen.blit(text, text_rect)
        font = pygame.font.Font('resources/monof55.ttf', 65)
        text = font.render(str(self.score), True, "#000000")
        text_rect = text.get_rect()
        text_rect.center = (self.ui.width / 2, self.ui.height / 2)
        self.ui.screen.blit(text, text_rect)
        self.draw_back_to_menu_button()

    def draw_back_to_menu_button(self):
        mouse = pygame.mouse.get_pos()
        if self.back_to_menu_rect.collidepoint(mouse):
            self.ui.screen.blit(self.ui.arrow_clicked, self.back_to_menu_rect)
        else:
            self.ui.screen.blit(self.ui.arrow_default, self.back_to_menu_rect)
