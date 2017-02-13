from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import pandas as pd
import re

_data_path = r'cene kuca i stanova.csv' 

dataframe = pd.read_csv(_data_path)


def uporedi_dve_ulice(ulica1, ulica2):
    return fuzz.partial_ratio(ulica1, ulica2)
    
def ukloni_broj_ulaza(adresa):
    re.sub('\d+$', '', adresa)
    
def ukloni_razmake(string):
    string.strip()

