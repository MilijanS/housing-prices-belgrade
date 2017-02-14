from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import pandas as pd
import re
import housing_crawler
import json

_data_path = r'baza jsona.pickle' 


dataframe = None
baza_jsona = None
spisak_ulica = []

atributi = ['Grad', 'Opstina', 'Naselje', 'Ulica', 'Tip', 'Kvadratura', 'Broj soba',
            'Grejanje', 'Sprat', 'Ukupna spratnost', 'Cena']
            

log = ''

def ucitaj_bazu_jsona(filename):
    global baza_jsona
    baza_jsona = housing_crawler.unpickle_json_array(filename)


def ucitaj_csv(filename):
    dataframe = pd.read_csv(filename)
    
def napravi_dataframe():
    
    global dataframe
   
    niz = []
    
    for json_serialized in baza_jsona:
        
        try:
        
            json_instance = json.loads(json_serialized)
            json_instance = json_instance['OtherFields']
        
            grad = json_instance['grad_s']
            opstina = json_instance['lokacija_s']
            naselje = json_instance['mikrolokacija_s']
            ulica = json_instance['ulica_t']
            tip = json_instance['tip_nekretnine_s']
            kvadratura = json_instance['kvadratura_d']
            broj_soba = json_instance['broj_soba_s']
            #gradnja = json_instance['tip_objekta_s'] #pravi problem
            #stanje = json_instance['stanje_objekta_s'] #pravi problem
            grejanje = json_instance['grejanje_s']
            sprat = json_instance['sprat_s']
            ukupna_spratnost = json_instance['sprat_od_s']
            cena = json_instance['cena_d']
        
            niz.append((grad, opstina, naselje, ulica, tip, kvadratura,
                        broj_soba, grejanje, sprat, ukupna_spratnost, cena))
        
            
            print('Nekretnina u {} dodata u dataframe'.format(ulica))
        except Exception as e:
            print('Exception:', e)
        finally:
            pass
        
    dataframe = pd.DataFrame(niz, columns=atributi)
        
    print('Dataframe loaded')
        
        
def uporedi_dve_ulice(ulica1, ulica2):
    partial_ratio = fuzz.ratio(ulica1, ulica2)
    #token_sort_ratio = fuzz.token_sort_ratio(ulica1, ulica2)
    return partial_ratio
    
    
def ukloni_broj_ulaza(adresa):
    return re.sub(r'(\d+.)$', '', adresa)
    
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
            
    if max_match_percentage > 90:
        global log
        print('Menjam {0} u {1}, podudarni su {2}'.format(ulica, spisak_ulica[index], max_match_percentage))
        log += ('Menjam {0} u {1}, podudarni su {2}\n'.format(ulica, spisak_ulica[index], max_match_percentage))
        return spisak_ulica[index]
    else:
        print('Nema podudarnih ulica, max poklapanje {0} dodajem {1} u spisak'.format(max_match_percentage, ulica))
        log += 'Nema podudarnih ulica, max poklapanje {0} dodajem {1} u spisak\n'.format(max_match_percentage, ulica)
        spisak_ulica.append(ulica)
        return ulica
        
def ukloni_rec_broj(string):
    return re.sub(r' broj ', r' ', string)      

        
def obradi_dataframe(df):
    df['Ulica'] = df['Ulica'].apply(ukloni_broj_ulaza)
    df['Ulica'] = df['Ulica'].apply(ukloni_razmake)
    df['Ulica'] = df['Ulica'].apply(dodaj_razmak_posle_tacke)
    df['Ulica'] = df['Ulica'].apply(to_lowercase)
    df['Ulica'] = df['Ulica'].apply(ukloni_duple_razmake) 
    df['Ulica'] = df['Ulica'].apply(ukloni_kvacice) 
    df['Ulica'] = df['Ulica'].apply(bul_u_bulevar)
    df['Ulica'] = df['Ulica'].apply(ukloni_rec_broj)
    df['Ulica'] = df['Ulica'].apply(mapiraj_u_spisak_ulica)    
    
    #uklanjanje redova u kojima ulica nema vrednost
    df = df[df['Ulica'] != '']
    return df
    

def glavna_obrada():
    
    global dataframe    
    
    ucitaj_bazu_jsona(_data_path)
    napravi_dataframe()
    
    dataframe = dataframe.sort_values(by='Ulica')

    #pre obrade: 4716 jedinstvenih imena ulica    
    dataframe['Ulica'].describe()

    dataframe = obradi_dataframe(dataframe)

    # posle obrade: 1178 jedinstvenih imena ulica
    dataframe['Ulica'].describe()

    with open('log - pretraga imena ulica.txt', 'w') as f:
        f.write(log)
        
    dataframe.to_csv('stanovi 11.2.2017. - konsolidovana imena ulica.csv', encoding='utf-8')
    
#glavna_obrada()