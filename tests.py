import unittest
import pygame
import pandas as pd
import os


class Tests(unittest.TestCase):
    def setUp(self):
        self.images = ["background.jpeg", "logo.png", "heart_gray.png", "heart_red.png", "arrow_clicked.png",
                       "arrow_default.png", "bulb_gray.png", "bulb_yellow.png"]
        self.font = "monof55.ttf"
        self.high_scores_file = "game/data/high_scores/high_scores.txt"
        self.datasets = ["countries.csv", "countries2.csv"]

    def test_load_images(self):
        for image in self.images:
            with self.subTest(image=image):
                self.assertTrue(test_load_images(image), f"Image {image} not found")

    def test_load_fonts(self):
        self.assertTrue(test_load_fonts(self.font), f"Font {self.font} not found")

    def test_load_high_scores(self):
        self.assertTrue(load_high_scores(self.high_scores_file), "High scores file not found")

    def test_check_high_scores(self):
        with open("temp_high_scores.txt", "w") as temp_file:
            temp_file.write("Easy Player1 100\nMedium Player2 150\nHard Player3 200\n")

        self.assertTrue(check_high_scores("temp_high_scores.txt"), "High scores file is corrupted")

    def test_load_dataset(self):
        for dataset in self.datasets:
            with self.subTest(dataset=dataset):
                self.assertTrue(load_dataset(dataset), f"Dataset {dataset} not found")

    def tearDown(self):
        try:
            os.remove("temp_high_scores.txt")
        except FileNotFoundError:
            pass


def test_load_images(image):
    try:
        pygame.image.load('resources/' + image)
    except pygame.error:
        return False
    else:
        return True


def test_load_fonts(font):
    try:
        pygame.font.Font('resources/' + font, 50)
    except pygame.error:
        return False
    else:
        return True


def load_high_scores(file_path):
    try:
        with open(file_path, "r") as high_scores_file:
            pass
    except FileNotFoundError:
        return False
    else:
        return True


def check_high_scores(file_path):
    try:
        with open(file_path, "r") as file:
            data = file.readlines()
            data = [line.strip().split() for line in data]
            if len(data) == 0:
                return True
            else:
                data = pd.DataFrame(data, columns=["Mode", "Nickname", "Score"])
                data["Score"] = data["Score"].astype(int)
    except (FileNotFoundError, pd.errors.ParserError):
        return False
    else:
        return True


def load_dataset(dataset):
    try:
        data = pd.read_csv("game/data/datasets/" + dataset)
    except FileNotFoundError:
        return False
    else:
        return True


if __name__ == '__main__':
    pygame.init()
    unittest.main()
