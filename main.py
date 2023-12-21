# main.py
from game.src.application import Application
import pygame

if __name__ == "__main__":
    pygame.init()

    # Set up the display and other pygame configurations


    app = Application(screen)
    app.run()