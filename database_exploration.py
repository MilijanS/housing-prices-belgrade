from sklearn.cross_validation import KFold
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
import numpy as np

import pandas as pd

df = pd.read_csv('stanovi 11.2.csv', encoding='utf-8')
df = df.drop('Unnamed: 0', axis=1)
df = df.drop('Unnamed: 0.1', axis=1)

df['Grad'] = df['Grad'].astype('category')
df['Opstina'] = df['Opstina'].astype('category')
df['Naselje'] = df['Naselje'].astype('category')
df['Ulica'] = df['Ulica'].astype('category')
df['Tip'] = df['Tip'].astype('category')
df['Broj soba'] = df['Broj soba'].astype('category')
df['Grejanje'] = df['Grejanje'].astype('category')
df['Sprat'] = df['Sprat'].astype('category')


linreg = LinearRegression()

x = df[['Opstina', 'Naselje', 'Ulica', 'Tip', 'Kvadratura', 'Broj soba', 'Grejanje', 'Sprat', 'Ukupna spratnost', 'Od centra']]
x = pd.get_dummies(x)

y = df['Cena']

linreg.fit(x,y)