import pandas as pd
import numpy as np
import pygame
import shutil
import os


def read_images(path):
    files = os.listdir(path)
    images = {}
    for file in files:
        images[file[:2]] = pygame.image.load(path + file)
    return images


class DataHandler:
    country_mapping = {
        'Slovak Republic': 'Slovakia',
        'São Tomé and Principe': 'Sao Tome and Principe ',
        "Côte d'Ivoire": 'Ivory Coast',
        'St. Kitts and Nevis': 'Saint Kitts and Nevis',
        "Dem. People's Rep. Korea": 'North Korea',
        'Timor-Leste': 'East Timor',
        'West Bank and Gaza': 'Palestinian National Authority',
        'Lao PDR': 'Laos',
        'Dem. Rep. Congo': 'Democratic Republic of the Congo',
        'Congo': 'Republic of the Congo',
        'Korea': 'South Korea',
        'Kyrgyz Republic': 'Kyrgyzstan',
        'Micronesia': 'Federated States of Micronesia',
        'Ireland': 'Republic of Ireland',
        'St. Vincent and the Grenadines': 'Saint Vincent and the Grenadines',
        'St. Lucia': 'Saint Lucia',
        'Syrian Arab Republic': 'Syria',
        'Cabo Verde': 'Cape Verde'
    }

    country_abbreviations = {
        'Republic of the Congo': 'cg',
        'Eswatini': 'sz',
        'Vatican City': 'va',
        'Republic of Ireland': 'ie',
        'Namibia': 'na',
        'North Macedonia': 'mk',
        'Palestinian National Authority': 'ps'
    }

    def __init__(self):
        self.data = pd.DataFrame()
        self.flags = read_images("game/data/flags/")
        self.shapes = read_images("game/data/country_shapes/256_img/")
        self.create_data()

    def add_images_to_data(self):
        self.data["flags"] = self.data["abbreviation"].map(self.flags)
        self.data["shapes"] = self.data["abbreviation"].map(self.shapes)

    def create_data(self):
        data1 = pd.read_csv('game/data/countries.csv')
        data2 = pd.read_csv('game/data/countries2.csv')
        data1['Abbreviation'] = data1["Abbreviation"].str.lower()
        data1 = data1[['Country', 'Abbreviation']]
        data2 = data2[['country', 'capital_city', 'region']]
        data2['country'] = data2['country'].replace(self.country_mapping)
        datamerged = pd.merge(data1, data2, left_on='Country', right_on='country', how='outer')
        datamerged = datamerged.drop('country', axis='columns')
        datamerged['Abbreviation'] = datamerged['Abbreviation'].fillna(
            datamerged['Country'].map(self.country_abbreviations))
        datamerged.loc[datamerged['Country'] == 'Vatican City', ['capital_city', 'region']] = datamerged.loc[
            datamerged['Country'] == 'Vatican City', ['capital_city', 'region']].fillna(
            value={'capital_city': 'Vatican City', 'region': 'Southern Europe'})
        # datamerged.loc[datamerged['Country'] == 'Palestinian National Authority', ['Population']] = datamerged.loc[
        #     datamerged['Country'] == 'Palestinian National Authority', ['Population']].fillna(
        #     value={'Population': 5429722})
        datamerged = datamerged.rename(
            columns={'Country': 'country', 'Population': 'population', 'Abbreviation': 'abbreviation',
                     'capital_city': 'capital'})
        self.data = datamerged
        self.add_images_to_data()

    def get_hint(self, country):
        return self.data.loc[self.data['country'] == country, ['region']]
    def get_data(self, state):
        if state == "flags":
            return self.data[["country", "flags"]]
        if state == "capital":
            return self.data[["country", "capital"]]
        if state == "shapes":
            return self.data[["country", "shapes"]].dropna()
        if state == "all_in_one":
            return self.data[['country', 'capital', 'flags', 'shapes']].dropna()
