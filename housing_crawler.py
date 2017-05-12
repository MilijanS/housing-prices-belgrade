from urllib.request import urlopen
import random
from bs4 import BeautifulSoup
import html5lib
import re
import pandas as pd
import concurrent.futures
import json
import pickle

atributi = ['Grad', 'Opstina', 'Naselje', 'Ulica', 'Tip', 'Kvadratura', 'Broj soba', 'Cena']

parser = 'lxml'

string_json = ''

dataframe = pd.DataFrame(columns=atributi)
baza = []
baza_jsona = []

halo_oglasi = r'https://www.halooglasi.com'
halo_oglasi_stanovi_beograd = r'https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd?cena_d_from=5000&cena_d_unit=4'
halo_oglasi_kuce_beograd = r'https://www.halooglasi.com/nekretnine/prodaja-kuca/beograd?cena_d_from=4000&cena_d_unit=4'

br_strana_stanovi = 1000
br_strana_kuce = 100

    
def get_jsons_from_page(web_page, page_index):
    
    print("Obradjujem stranicu {0}".format(page_index))
    
    url = web_page + r'&page=' + str(page_index)

    page = urlopen(url)

    soup = BeautifulSoup(page, parser)
    
    # mydivs sadrzi 20 razlicitih stanova
    mydivs = soup.findAll('div', { 'class' : 'col-md-12 col-sm-12 col-xs-12 col-lg-12'})
    
    # obradi 20 nekretnina
    for i, div in enumerate(mydivs):
        try:
            
            stranica_nekretnine = div.find('a')
            stranica_nekretnine = stranica_nekretnine.get('href')
            
            url_nekretnine_string = halo_oglasi + stranica_nekretnine
            url_nekretnine = urlopen(url_nekretnine_string)
            soup_nekretnine = BeautifulSoup(url_nekretnine, parser)
            
            scripts = soup_nekretnine.find_all('script')
            raw_json = scripts[16].text
            json_string = re.findall(r'(QuidditaEnvironment.CurrentClassified=)(.*)(;.)(for \(var i in QuidditaEnvironment)', raw_json)[0]
            jjson = json_string[1]

            string_json = jjson
            
            baza_jsona.append(jjson)  
            
            jsonucitan = json.loads(string_json)
            print(jsonucitan['OtherFields']['ulica_t'])
                            
        except Exception as e:
            print(e) 
        finally:
            pass
        
    print('Ubacio nekretnine sa stranice {0}'.format(page_index))    
                
    
    
def process_website_pages(web_page, start_page, end_page):
    
    try:
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:            
            future_to_i = {executor.submit(process_single_page, web_page, page_index): page_index for page_index in range(start_page, end_page + 1)}
    except Exception as e:
        print(e)
    finally:
        print("Obradio sve stranice.\n")
        
        
def get_multiple_jsons(web_page, start_page, end_page):
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:            
            future_to_i = {executor.submit(get_jsons_from_page, web_page, page_index): page_index for page_index in range(start_page, end_page + 1)}
    except Exception as e:
        print(e)
    finally:
        print("Obradio sve stranice.\n")
        
       
def prikupi_cene_stanova_i_kuca_u_beogradu():
    
    process_website_pages(web_page=halo_oglasi_kuce_beograd, start_page=1, end_page=120)
    
    process_website_pages(web_page=halo_oglasi_stanovi_beograd, start_page=1, end_page=1100)
    
    dataframe = pd.DataFrame(baza, columns=atributi)
    
    
def eksportuj_kao_csv(filename='Cene kuca i stanova'):
    
    dataframe.to_csv(filename, encoding='utf-8')
    
def pickle_json_array(filename, json_baza):
        
    pickle.dump(json_baza, open(filename, 'wb'))

def unpickle_json_array(filename):
    return pickle.load(open(filename, 'rb'))
    
get_multiple_jsons(halo_oglasi_stanovi_beograd, 1, 120)
get_multiple_jsons(halo_oglasi_stanovi_beograd, 1, 1100)

dataframe = pd.DataFrame(baza_jsona, columns=atributi)
eksportuj_kao_csv('nova baza stanova i kuca.csv')