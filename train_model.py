import os
import json
import pandas as pd
from config import learning_rate, iters_num
from config import data_folder, coefficients_filename, data_filename
import matplotlib.pyplot as plt


class LinearRegression:
    def __init__(self, filename, folder='data'):
        self.folder = folder
        self.df = pd.read_csv(os.path.join(self.folder, filename))
        self.df = self.df.rename(columns={'km': 'x', 'price': 'y'})

        # Нормализация входных значений.
        self.std = self.df['x'].std()
        self.mean = self.df['x'].mean()
        self.df['x'] = (self.df['x'] - self.mean) / self.std
        #self.df['y'] = (self.df['y'] - self.df['y'].mean()) / self.df['y'].std()
        #self.df['x'] = (self.df['x'] - self.df['x'].min()) / self.df['x'].max()
        #self.df['y'] = self.df['y'] / self.df['y'].max()
        print(self.df)
        self.teta_0 = None
        self.teta_1 = None

    def estimate_price(self, teta_0, teta_1):
        self.df['estimate_price'] = (self.df['x'] * teta_1) + teta_0

    def new_teta_0(self):
        result = (self.df['y'] - self.df['estimate_price']).mean()
        #print(result)
        return result

    def new_teta_1(self):
        result = ((self.df['y'] - self.df['estimate_price']) * self.df['x']).mean()
        #print(result)
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
        teta_0 = self.teta_0 / self.std
        teta_1 = -1 * ((self.mean * self.teta_0) / self.std) + self.teta_1
        result = {'teta_0': teta_0, 'teta_1': teta_1}
        with open(os.path.join(folder, filename), 'w') as file:
            file.write(json.dumps(result))
        plt.scatter(self.df['x'], self.df['y'])
        plt.plot(self.df['x'], (self.df['x'] * teta_1) + teta_0, color='red')
        plt.show()


if __name__ == '__main__':
    regression = LinearRegression(data_filename, folder=data_folder)
    regression.searching_coefficients()
    regression.save_coefficients(filename=coefficients_filename, folder=data_folder)
