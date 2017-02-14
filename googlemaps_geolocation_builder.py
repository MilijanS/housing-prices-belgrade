import googlemaps
import math
import pickle
import json 
import pandas as pd
import numpy as np

#google maps api client
gmaps = None

api_key = 'AIzaSyCC0HVAHlQLHP-6hL9MUscGQyTzD9JJ0bA'
fake_api_key = 'AIzaSyA6oPLQHpx8aih4qJJyLqVT1xixoqGktBy'

input_dataset_path = r'stanovi 11.2.2017. - konsolidovana imena ulica.csv'

street_to_location_map = {}

df = None


my_house = (44.798025, 20.534188)
republic_square = (44.815944, 20.460199)

def init_googlemaps_client(api_key):
    
    global gmaps
    gmaps = googlemaps.Client(api_key)

    
def calculate_distance(loc1, loc2):
    
    y1, x1 = loc1
    y2, x2 = loc2
    
    lat_dif = abs(y1 - y2)
    long_dif = abs(x1 - x2)
    
    diagonal = math.sqrt(lat_dif**2 + long_dif**2)
    
    dst = diagonal * 81.04777696114823
    
    print('Distance equals {0}km'.format(dst))    
    return dst
    

def pickle_street_to_location_map():
    pass
    
def get_location_from_street_name(street_name):
        
    geocode_result = gmaps.geocode(street_name)
    
    if len(geocode_result) == 0:
        return None
    
    location_dict = geocode_result[0]['geometry']['location']
    
    latitude = location_dict['lat']
    longitude = location_dict['lng']

    return (latitude, longitude)
    
    
def build_street_to_location_map():
    
    
    street_to_location_list = []
    
    df = pd.read_csv(input_dataset_path)
    
    try:
        
        for ulica in df['Ulica'].unique():
    
            location = get_location_from_street_name(ulica + 'Beograd')
            
            if location == None:
                
                location = (0.0, 0.0)
                distance = -1.0
                street_to_location_list.append((ulica, location, distance))                                 
                
                continue
        
            distance = calculate_distance(location, republic_square)
        
            print(ulica, location)
        
            street_to_location_list.append((ulica, location, distance))
            
    except Exception as e:
            print(e)
            print(ulica, location, distance)
        
    finally:
            pass
                

    columns = ['Ulica', 'Koordinate', 'Od centra']

    street_names_location = pd.DataFrame(street_to_location_list, columns=columns)
    
    street_names_location.to_csv('street names geocoded.csv', encoding='utf-8')   
    
    
def fill_missing_distances(df):
    
    df['Od centra'] = df['Od centra'].replace(-1, np.nan)
    
    df['Od centra'] = df2['Od centra'].fillna(df2['Od centra'].mean())
    
    
def merge_apartment_with_location_dataframes(apartment_df, location_df):
    
    niz = []
    
    for ulica in apartment_df['Ulica']:
        distance = df2[df2['Ulica']==ulica]['Od centra']
        location = df2[df2['Ulica']==ulica]['Lokacija']
        niz.append(distance)
        
    location_df['Od centra'] = niz    
        
    return location_df    
    


#init_googlemaps_client(api_key)

    

