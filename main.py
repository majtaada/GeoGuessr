# main.py
from game.src.application import Application
import pygame

if __name__ == "__main__":
    pygame.init()
    app = Application()
    app.run()