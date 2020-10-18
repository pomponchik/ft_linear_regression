import os
import json
import pandas as pd
from config import learning_rate, iters_num
from config import data_folder, coefficients_filename, data_filename


class LinearRegression:
    def __init__(self, filename, folder='data'):
        self.folder = folder
        self.df = pd.read_csv(os.path.join(self.folder, filename))
        self.df = self.df.rename(columns={'km': 'x', 'price': 'y'})
        # Нормализация входных значений.
        self.df.x = (self.df['x'] - self.df['x'].mean()) / self.df['x'].std()
        self.teta_0 = None
        self.teta_1 = None

    def estimate_price(self, teta_0, teta_1):
        self.df['estimate_price'] = (self.df['x'] * teta_1) + teta_0

    def new_teta_0(self):
        result = (self.df['y'] - self.df['estimate_price']).mean()
        return result

    def new_teta_1(self):
        result = ((self.df['y'] - self.df['estimate_price']) * self.df['x']).mean()
        return result

    def searching_coefficients(self):
        self.teta_1 = 0
        self.teta_0 = 0
        for epoch in range(iters_num):
            self.estimate_price(self.teta_0, self.teta_1)
            self.teta_0 += self.new_teta_0()
            self.teta_1 += self.new_teta_1()
        return self.teta_0, self.teta_1

    def save_coefficients(self, filename='coefficients.json', folder='data'):
        result = {'teta_0': self.teta_0, 'teta_1': self.teta_1}
        with open(os.path.join(folder, filename), 'w') as file:
            file.write(json.dumps(result))


if __name__ == '__main__':
    regression = LinearRegression(data_filename, folder=data_folder)
    regression.searching_coefficients()
    regression.save_coefficients(filename=coefficients_filename, folder=data_folder)
