import googlemaps
import math
import pickle
import json 

#google maps api client
gmaps = None

api_key = 'AIzaSyAzjqg2bJWGhGBMscWHFLhPsh8skXtWGaE'
fake_api_key = 'AIzaSyA6oPLQHpx8aih4qJJyLqVT1xixoqGktBy'

street_to_location_map = {}

my_house = (44.798025, 20.534188)
republic_square = (44.815944, 20.460199)

def init_googlemaps_client(api_key):
    
    global gmaps
    gmaps = googlemaps.Client(api_key)

    
def distance(loc1, loc2):
    
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
    
    location_dict = geocode_result[0]['geometry']['location']
    
    latitude = location_dict['lat']
    longitude = location_dict['lng']

    return (latitude, longitude)
    
    
def build_street_to_location_map():
    
    global street_to_location_map
    
    
    
init_googlemaps_client(api_key)

    

