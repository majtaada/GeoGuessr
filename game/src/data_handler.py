import pandas as pd
import pygame
import os
import resources.constants as cst


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
    scalers = ['flags', 'shapes', 'capital']

    def __init__(self):
        self.data = pd.DataFrame()
        self.flags = read_images("game/data/flags/")
        self.shapes = read_images("game/data/country_shapes/256_img/")
        self.create_data()

    def add_images_to_data(self):
        self.data["flags"] = self.data["abbreviation"].map(self.flags)
        self.data["shapes"] = self.data["abbreviation"].map(self.shapes)

    def create_data(self):
        data1 = pd.read_csv('game/data/datasets/countries.csv')
        data2 = pd.read_csv('game/data/datasets/countries2.csv')
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
        datamerged = datamerged.rename(
            columns={'Country': 'country', 'Population': 'population', 'Abbreviation': 'abbreviation',
                     'capital_city': 'capital'})
        self.data = datamerged
        self.add_images_to_data()
        self.add_scalers_to_data()

    def add_scalers_to_data(self):
        scalers_data = self.read_scalers_jsons()
        for scaler in self.scalers:
            self.data = pd.merge(self.data, scalers_data[scaler], left_on='country', right_on='country_scale',
                                 how='outer')

    def get_scaler(self, country, mode):
        print(self.data.columns)
        scale = self.data.loc[self.data['country'] == country, [mode + '_scale']]
        scale = scale.iloc[0][mode + '_scale']
        print(scale)
        return scale

    def read_scalers_jsons(self):
        scalers = {}
        for scaler in self.scalers:
            df = pd.read_json(f"game/data/datasets/{scaler}_scale.json", orient='index', typ='series')
            scalers[scaler] = df.rename_axis('country_scale').reset_index(name=f'{scaler}_scale')
        return scalers

    def get_hint(self, country):
        return self.data.loc[self.data['country'] == country, ['region']]

    def get_data(self, state):
        if state == "flags":
            return self.data[["country", "flags"]]
        if state == "capital":
            nan_rows = self.data[self.data.isna().any(axis=1) == True]
            print(nan_rows)
            return self.data[["country", "capital"]].dropna()
        if state == "shapes":
            return self.data[["country", "shapes"]].dropna()
        if state == "all_in_one":
            return self.data[['country', 'capital', 'flags', 'shapes']].dropna()
