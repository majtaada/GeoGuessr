import pygame
import sys
from game.src.nickname_getter import GameModes
from resources.constants import Constants


class PlayButton:
    def __init__(self, ui):
        self.ui = ui
        self.cst = Constants()
        self.button_rects = [
            pygame.Rect(self.ui.width / 2 - 125, self.ui.height / 5, self.cst.MENU_BUTTON_WIDTH, self.cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(self.ui.width / 2 - 125, self.ui.height / 5 + 100, self.cst.MENU_BUTTON_WIDTH,
                        self.cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(self.ui.width / 2 - 125, self.ui.height / 5 + 200, self.cst.MENU_BUTTON_WIDTH,
                        self.cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(self.ui.width / 2 - 125, self.ui.height / 5 + 300, self.cst.MENU_BUTTON_WIDTH,
                        self.cst.MENU_BUTTON_HEIGHT),
            pygame.Rect(self.ui.width / 2 - 125, self.ui.height / 5 + 400, self.cst.MENU_BUTTON_WIDTH,
                        self.cst.MENU_BUTTON_HEIGHT)]
        self.game_modes = GameModes(ui)
        self.modes = ["flags", "capital", "shapes", "all_in_one"]
    def run(self):
        while True:
            mode = self.handle_events()
            if mode == "main_menu":
                return
            if mode is not None:
                self.game_modes.run(mode)
            self.draw()
            self.ui.clock.tick(60)
            pygame.display.flip()
            pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + 100 and self.ui.height / 5 <= mouse[
                    1] <= self.ui.height / 5 + 80:
                    return "flags"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + 100 and self.ui.height / 5 + 100 <= mouse[
                    1] <= self.ui.height / 5 + 180:
                    return "capital"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + 100 and self.ui.height / 5 + 200 <= mouse[
                    1] <= self.ui.height / 5 + 280:
                    return "shapes"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + 100 and self.ui.height / 5 + 300 <= mouse[
                    1] <= self.ui.height / 5 + 380:
                    return "all_in_one"

                if self.ui.width / 2 - 100 <= mouse[0] <= self.ui.width / 2 + 100 and self.ui.height / 5 + 400 <= mouse[
                    1] <= self.ui.height / 5 + 480:
                    return "main_menu"

    def draw_buttons(self):
        mouse = pygame.mouse.get_pos()
        for rect in self.button_rects:
            if rect.collidepoint(mouse):
                pygame.draw.rect(self.ui.screen, self.cst.PRESSED_BUTTON_COLOR, rect)
            else:
                pygame.draw.rect(self.ui.screen, self.cst.DEFAULT_BUTTON_COLOR, rect)

    def add_text_buttons(self):
        texts = ["Flags", "Capitals", "Country Shapes", "All in one", "Back"]

        for i in range(len(texts)):
            text = self.ui.font.render(texts[i], True, "#000000")
            text_rect = text.get_rect()
            text_rect.center = (self.ui.width / 2, self.ui.height / 5 + 30 + 100 * i)
            self.ui.screen.blit(text, text_rect)

    def draw(self):
        self.ui.draw_background()
        self.draw_buttons()
        self.add_text_buttons()
