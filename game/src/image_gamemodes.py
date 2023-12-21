import pygame
import sys
from game.src.gamelogic import GameLogic


class FlagsGamemode:
    def __init__(self, ui):
        self.ui = ui
    def draw_image(self,image):
        image_rect = image.get_rect()
        image_rect.center = (self.ui.width / 2, self.ui.height / 4)
        self.ui.screen.blit(image, image_rect)
