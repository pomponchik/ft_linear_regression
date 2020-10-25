import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
from config import data_folder, coefficients_filename, data_filename


def error(text):
    full_message = f'ERROR: {text}.'
    print(full_message)
    exit(1)

def get_coefficients():
    full_filename = os.path.join(data_folder, coefficients_filename)
    if os.path.exists(full_filename) and os.path.isfile(full_filename):
        with open(full_filename, 'r') as file:
            file = file.read()
        try:
            data = json.loads(file)
            return data['teta_0'], data['teta_1']
        except:
            error(f'format of the file "{full_filename}" is incorrect (this must be json contains dict with 2 keys: "teta_0" and "teta_1", all them is floats or ints)')
    error(f'the "{full_filename}" file with coefficients is not exists')

def predict(teta_0, teta_1, number):
    result = teta_0 + teta_1 * number
    return result

def show(teta_0, teta_1, number, result):
    df = pd.read_csv(os.path.join(data_folder, data_filename)).rename(columns={'km': 'x', 'price': 'y'})
    plt.scatter(df['x'], df['y'], zorder=0)
    plt.plot(df['x'], (df['x'] * teta_1) + teta_0, color='red', zorder=1)
    plt.scatter([number], [result], color='yellow', zorder=2)
    plt.show()

def main():
    number = input('Enter mileage (km): ')
    try:
        number = float(number)
    except ValueError:
        error('the mileage must be a number')
    teta_0, teta_1 = get_coefficients()
    result = predict(teta_0, teta_1, number)
    print(f'Price of the car is {result}')
    if '--show' in sys.argv:
        show(teta_0, teta_1, number, result)

if __name__ == '__main__':
    main()
