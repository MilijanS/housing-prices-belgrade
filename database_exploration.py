from sklearn.cross_validation import KFold
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
import numpy as np
from sklearn.utils import shuffle

import pandas as pd

linreg = LinearRegression()

df = pd.read_csv('stanovi 11.2.csv', encoding='utf-8')
df = df.drop('Unnamed: 0', axis=1)
df = df.drop('Unnamed: 0.1', axis=1)
df = shuffle(df)


df['Grad'] = df['Grad'].astype('category')
df['Opstina'] = df['Opstina'].astype('category')
df['Naselje'] = df['Naselje'].astype('category')
df['Ulica'] = df['Ulica'].astype('category')
df['Tip'] = df['Tip'].astype('category')
df['Broj soba'] = df['Broj soba'].astype('category')
df['Grejanje'] = df['Grejanje'].astype('category')
df['Sprat'] = df['Sprat'].astype('category')

df = df[['Opstina', 'Naselje', 'Ulica', 'Kvadratura', 'Broj soba', 'Grejanje', 'Sprat', 'Ukupna spratnost', 'Od centra', 'Cena']]

train = df[0:6085]
train_x = train.drop('Cena', axis=1)
train_y = train['Cena']

print('Test apartmani:\n', test)
sacuvani_test = test
test = df[6085:].drop('Cena', axis=1)


train_x = pd.get_dummies(train_x)
test_dummies = pd.get_dummies(test)

linreg.fit(train_x, train_y)

"""
opstina = 'Zvezdara'
naselje = 'Karaburma'
ulica = 'marijane gregoran'
kvadratura = 56
broj_soba = '2.5'
grejanje = 'CG'
sprat = '1'
ukupna_spratnost = 3

od_centra = df[df['Ulica']==ulica]
od_centra = od_centra['Od centra'].at[od_centra.index[0]]

test_apartment = [opstina, naselje, ulica, kvadratura, broj_soba, grejanje, sprat, ukupna_spratnost, od_centra]
"""

prediction = linreg.predict(test_dummies)
print('Rezultati:\n {0}'.format(prediction))


#print(prediction)
