import pandas as pd
import pygame
import os


def read_images(path):
    """ Reads images from given path and returns them in a dictionary with country abbreviations as keys"""
    files = os.listdir(path)
    images = {}
    for file in files:
        images[file[:2]] = pygame.image.load(path + file)
    return images


class DataHandler:
    """Class for handling data."""
    country_mapping = {
        'Slovak Republic': 'Slovakia',
        'São Tomé and Principe': 'Sao Tome and Principe',
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
    scalers = ['flags', 'shapes', 'capital']

    def __init__(self):
        """Initialize data."""
        self.data = pd.DataFrame()
        self.flags = read_images("game/data/flags/")
        self.shapes = read_images("game/data/country_shapes/256_img/")
        self.create_data()

    def add_images_to_data(self):
        """Adds flags and shapes to data"""
        self.data["flags"] = self.data["abbreviation"].map(self.flags)
        self.data["shapes"] = self.data["abbreviation"].map(self.shapes)

    def create_data(self):
        """Creates data from datasets"""
        data1 = pd.read_csv('game/data/datasets/countries.csv')
        data2 = pd.read_csv('game/data/datasets/countries2.csv')
        data1['Abbreviation'] = data1["Abbreviation"].str.lower()
        data1 = data1[['Country', 'Abbreviation']]
        data2 = data2[['country', 'capital_city', 'region']]
        data2['country'] = data2['country'].replace(self.country_mapping)
        datamerged = pd.merge(data1, data2, left_on='Country', right_on='country', how='outer')
        datamerged = datamerged.drop('country', axis='columns')
        datamerged.loc[datamerged['region'] == "Australia and New Zealand", ['region']] = 'Oceania'
        datamerged.loc[datamerged['region'] == "South-Eastern Asia", ['region']] = 'South-East Asia'
        datamerged['Abbreviation'] = datamerged['Abbreviation'].fillna(
            datamerged['Country'].map(self.country_abbreviations))
        datamerged.loc[datamerged['Country'] == 'Vatican City', ['capital_city', 'region']] = datamerged.loc[
            datamerged['Country'] == 'Vatican City', ['capital_city', 'region']].fillna(
            value={'capital_city': 'Vatican City', 'region': 'Southern Europe'})
        datamerged = datamerged.rename(
            columns={'Country': 'country', 'Population': 'population', 'Abbreviation': 'abbreviation',
                     'capital_city': 'capital'})
        self.data = datamerged
        self.add_images_to_data()
        self.add_scalers_to_data()
        self.print_data()

    def add_scalers_to_data(self):
        """Adds scalers to data"""
        scalers_data = self.read_scalers_jsons()
        for scaler in self.scalers:
            self.data = pd.merge(self.data, scalers_data[scaler], left_on='country', right_on='country_scale',
                                 how='outer')
            self.data = self.data.drop('country_scale', axis='columns')

    def get_scaler(self, country, mode):
        """Returns scaler for given country and mode"""
        scale = self.data.loc[self.data['country'] == country, [mode + '_scale']]
        scale = scale.iloc[0][mode + '_scale']
        return scale

    def read_scalers_jsons(self):
        """Reads scalers from json files and returns them in a dictionary with scaler names as keys"""
        scalers = {}
        for scaler in self.scalers:
            df = pd.read_json(f"game/data/datasets/{scaler}_scale.json", orient='index', typ='series')
            scalers[scaler] = df.rename_axis('country_scale').reset_index(name=f'{scaler}_scale')
        return scalers

    def get_hint(self, country):
        """Returns hint for given country"""
        return self.data.loc[self.data['country'] == country, ['region']]

    def get_data(self, state):
        """Returns data for given state"""
        if state == "flags":
            return self.data[["country", "flags"]].dropna()
        if state == "capital":
            return self.data[["country", "capital"]].dropna()
        if state == "shapes":
            return self.data[["country", "shapes"]].dropna()
        if state == "all_in_one":
            return self.data[['country', 'capital', 'flags', 'shapes']].dropna()

    def print_data(self):
        """Prints data"""
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(self.data)
