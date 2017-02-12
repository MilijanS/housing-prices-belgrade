from urllib.request import urlopen
import random
from bs4 import BeautifulSoup
import html5lib
import re
import pandas as pd
import concurrent.futures

atributi = ['Grad', 'Opstina', 'Naselje', 'Ulica', 'Tip', 'Kvadratura', 'Broj soba', 'Cena']

parser = 'lxml'


baza = pd.DataFrame(columns=atributi)

halo_oglasi_stanovi_beograd = r'https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd?cena_d_from=5000&cena_d_unit=4'
halo_oglasi_kuce_beograd = r'https://www.halooglasi.com/nekretnine/prodaja-kuca/beograd?cena_d_from=4000&cena_d_unit=4'

br_strana_stanovi = 1000
br_strana_kuce = 100

class Nekretnina:
    
    def __init__(self, grad, opstina, naselje, ulica, tip_nekretnine, kvadratura, broj_soba, cena):
        self.grad = grad
        self.opstina = opstina
        self.naselje = naselje
        self.ulica = ulica
        self.tip_nekretnine = tip_nekretnine
        self.kvadratura = kvadratura
        self.broj_soba = broj_soba
        self.cena = cena
        
    def __init__(self):
        pass

    def __repr__(self):
        res = """Grad: {0}\n'
        Opština: {1}\n
        Naselje: {2}\n
        Ulica: {3}\n
        Tip nekretnine: {4}\n
        Kvadratura: {5}\n 
        Broj soba: {6}\n
        Cena: {7}\n
        
        """.format(self.grad, self.opstina, self.naselje, self.ulica, self.tip_nekretnine, 
                   self.kvadratura, self.broj_soba, self.cena)
        return res
                
def dodaj_nekretninu_u_dataframe(df):
    pass



#1125
def process_single_page(web_page, page_index):
    
    print("Obradjujem stranicu {0}".format(page_index))
    
    url = web_page + r'&page=' + str(page_index)

    page = urlopen(url)

    soup = BeautifulSoup(page, parser)
    
    # mydivs sadrzi 20 razlicitih stanova
    mydivs = soup.findAll('div', { 'class' : 'col-md-12 col-sm-12 col-xs-12 col-lg-12'})
    
    print('Na stranici je pronadjeno {0} nekretnina'.format(len(mydivs)))
    # odradi 20 stanova
    for div in mydivs:
        try:
        
            # string price izgleda ovako '47.000\xa0€'
            string_price = div.find("span").string
            string_price = string_price.replace('\xa0€','')
            string_price = string_price.replace('.', '')
        
            cena = int(string_price)
        
            info_divs = div.find('div', { 'class' : 'col-md-6 col-sm-5 col-xs-6 col-lg-6 sm-margin'})
        
            info = info_divs.findAll('li')
        
            grad = info[0].string.replace('\xa0', '')
            opstina = info[1].string.replace('\xa0', '')
            opstina = opstina.replace('Opština ', '')
            
            naselje = info[2].string.replace('\xa0', '')
            
            ulica = str(info[3].string).replace('\xa0', '')
            
            tip_nekretnine = info[4].text
            tip_nekretnine = re.sub(r'((\n)|(\r)|(\t))+', r'', tip_nekretnine)
            tip_nekretnine = re.sub(r'\xa0.*', '', tip_nekretnine)
        
            kvadratura = info[5].text
            kvadratura = re.sub(r'((\n)|(\r)|(\t))+', r'', kvadratura)
            kvadratura = re.sub(r',\d*', '', kvadratura)
            kvadratura = re.sub(r'\xa0.+', '', kvadratura)
            kvadratura = float(kvadratura)
        
            broj_soba = info[-1].text
            broj_soba = re.sub(r'((\n)|(\r)|(\t))*', r'', broj_soba)
            broj_soba = re.sub('\xa0.*', '', broj_soba)
            
            if kvadratura < 10 and type(tip_nekretnine)==float:
                kvadratura, broj_soba = broj_soba, kvadratura
        
                        
            print(grad, opstina, naselje, ulica, tip_nekretnine, kvadratura, broj_soba, cena)
            
            if kvadratura == broj_soba:
                print('Kvadratura == broj soba')
                continue
            if ulica == 'None':
                print('Nema informacije o ulici')
                continue

            print('Ubacujem u bazu nekretninu u {0}'.format(ulica))
            baza.loc[len(baza)]=[grad, opstina, naselje, ulica, tip_nekretnine, kvadratura, broj_soba, cena]   
  
    
            
        except Exception as e:
            print(e) 
        finally:
            pass
        
    print('Ubacio nekretnine sa stranice {0}'.format(page_index))    
                

def process_website_pages(web_page, start_page, end_page):
    
    try:
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:            
            future_to_i = {executor.submit(process_single_page, web_page, page_index): page_index for page_index in range(start_page, end_page)}
            
    finally:
        
        print("End.\n")
        print(baza)
       
def prikupi_cene_stanova_i_kuca_u_beogradu():
    
    process_website_pages(web_page=halo_oglasi_kuce_beograd, start_page=1, end_page=2)
      
    """for i in range(0, 2):
        process_website_pages(web_page=halo_oglasi_stanovi_beograd, start_page=i*100 + 1, end_page=(i+1)*100)"""
            
    #baza.to_csv('cene kuca i stanova 11.02.2017. v2.csv', encoding='utf-8')
