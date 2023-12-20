import pygame

class PlayButton:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.button1_rect = pygame.Rect(self.width / 2 - 125, self.height / 5, 250, 60)

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.update()

    def handle_events(self):
        pass

    def draw(self):
