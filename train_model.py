import os
import json
import pandas as pd
from config import learning_rate, iters_num


df = pd.read_csv(os.path.join('data', 'data.csv'))
df = df.rename(columns={'km': 'x', 'price': 'y'})

df.x = (df['x'] - df['x'].mean()) / df['x'].std()


print(df)


def estimate_price(df, teta_0, teta_1):
    df['estimate_price'] = (df['x'] * teta_1) + teta_0
    return df

def new_teta_0(df):
    result = (df['y'] - df['estimate_price']).mean()
    return result

def new_teta_1(df):
    result = ((df['y'] - df['estimate_price']) * df['x']).mean()
    return result

def searching_coefficients(df):
    teta_1 = 0
    teta_0 = 0
    for epoch in range(iters_num):
        df = estimate_price(df, teta_0, teta_1)
        teta_0 += new_teta_0(df)
        teta_1 += new_teta_1(df)
    return teta_0, teta_1

result = searching_coefficients(df)
result = {'teta_0': result[0], 'teta_1': result[1]}
with open(os.path.join('data', 'coefficients.json'), 'w') as file:
    file.write(json.dumps(result))
