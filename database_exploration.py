from sklearn.cross_validation import KFold
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
import numpy as np

import pandas as pd

df = pd.read_csv('stanovi.csv')

df['Grad'] = df['Grad'].astype('category')
df['Opstina'] = df['Opstina'].astype('category')
df['Naselje'] = df['Naselje'].astype('category')
df['Ulica'] = df['Ulica'].astype('category')
df['Tip'] = df['Tip'].astype('category')
df['Broj soba'] = df['Broj soba'].astype('category')
df['Grejanje'] = df['Grejanje'].astype('category')
df['Sprat'] = df['Sprat'].astype('category')


linreg = LinearRegression()



linreg.fit(x,y)