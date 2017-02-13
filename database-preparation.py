from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import pandas as pd
import re

_data_path = r'cene kuca i stanova.csv' 

dataframe = pd.read_csv(_data_path)

spisak_ulica = []

log = ''


def uporedi_dve_ulice(ulica1, ulica2):
    partial_ratio = fuzz.ratio(ulica1, ulica2)
    #token_sort_ratio = fuzz.token_sort_ratio(ulica1, ulica2)
    return partial_ratio
    
    
def ukloni_broj_ulaza(adresa):
    return re.sub('\d+$', '', adresa)
    
def ukloni_razmake(string):
    return string.strip()

def dodaj_razmak_posle_tacke(string):
    return re.sub(r'(.)(\.)(.)', r'\1. \3', string)
    
def to_lowercase(string):
    return string.lower()
    
def ukloni_duple_razmake(string):
    return re.sub(r'(.)( )( )*', r'\1\2', string)
    
def ukloni_kvacice(string):
    res = string
    res = res.replace('ć', 'c')
    res = res.replace('č', 'c')
    res = res.replace('š', 's')
    res = res.replace('ž', 'z')
    res = res.replace('đ', 'dj')
    return res
    

def bul_u_bulevar(string):
    return re.sub(r'(bul\.)|(bul )|(bul .)', r'Bulevar', string)
    
def mapiraj_u_spisak_ulica(ulica):
    
    max_match_percentage = 0
    index = 0
    
    for i, ul in enumerate(spisak_ulica):
        match_percentage = uporedi_dve_ulice(ulica, ul)
        if match_percentage > max_match_percentage:
            max_match_percentage = match_percentage
            index = i
            
    if max_match_percentage > 95:
        global log
        print('Menjam {0} u {1}, podudarni su {2}'.format(ulica, spisak_ulica[index], max_match_percentage))
        log += ('Menjam {0} u {1}, podudarni su {2}\n'.format(ulica, spisak_ulica[index], max_match_percentage))
        return spisak_ulica[index]
    else:
        print('Nema podudarnih ulica, max poklapanje {0} dodajem {1} u spisak'.format(max_match_percentage, ulica))
        spisak_ulica.append(ulica)
        return ulica
        
    
def obradi_dataframe(df):
    df['Ulica'] = df['Ulica'].apply(ukloni_broj_ulaza)
    df['Ulica'] = df['Ulica'].apply(ukloni_razmake)
    df['Ulica'] = df['Ulica'].apply(dodaj_razmak_posle_tacke)
    df['Ulica'] = df['Ulica'].apply(to_lowercase)
    df['Ulica'] = df['Ulica'].apply(ukloni_duple_razmake) 
    df['Ulica'] = df['Ulica'].apply(ukloni_kvacice) 
    df['Ulica'] = df['Ulica'].apply(bul_u_bulevar)
    df['Ulica'] = df['Ulica'].apply(mapiraj_u_spisak_ulica)    
    return df

dataframe = dataframe.sort_values(by='Ulica', ascending=False)

#pre obrade: 4716 jedinstvenih imena ulica    
dataframe['Ulica'].describe()

dataframe = obradi_dataframe(dataframe)

#posle obrade: 2822
dataframe['Ulica'].describe()

with open('log.txt', 'rb+') as f:
    f.write(log)

    



