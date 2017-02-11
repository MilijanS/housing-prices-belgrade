from urllib.request import urlopen
import random
from bs4 import BeautifulSoup
import re
import pandas as pd



atributi = ['Grad', 'Opstina', 'Naselje', 'Ulica', 'Tip', 'Kvadratura', 'Broj soba', 'Cena']

baza = pd.DataFrame(columns=atributi)

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
for i in range(0, 1100):
            
    url = r'https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd?cena_d_from=5000&cena_d_unit=4&page=' + str(i)

    page = urlopen(url)

    soup = BeautifulSoup(page, 'lxml')
    
    # mydivs sadrzi 20 razlicitih stanova
    mydivs = soup.findAll('div', { 'class' : 'col-md-12 col-sm-12 col-xs-12 col-lg-12'})
    
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
        
            broj_soba = float(broj_soba)
            
            if kvadratura == broj_soba:
                continue
            else:
                baza.loc[len(baza)]=[grad, opstina, naselje, ulica, tip_nekretnine, kvadratura, broj_soba, cena]        
            
        except:
            pass
                
print(baza)
baza.to_csv('cene stanova.csv', encoding='utf-8')

        

        
        
        
        
        
        
        
        
    