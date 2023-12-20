# main.py
from game.gui.main_menu import MainMenu
import pygame

if __name__ == "__main__":
    pygame.init()

    # Set up the display and other pygame configurations
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GeoQuizzr")

    clock = pygame.time.Clock()

    main_menu = MainMenu(screen)
    main_menu.run()