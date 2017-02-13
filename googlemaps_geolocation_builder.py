import googlemaps

api_key = 'AIzaSyA6oPLQHpx8aih4qJJyLqVT1xixoqGktBY'
fake_api_key = 'AIzaSyA6oPLQHpx8aih4qJJyLqVT1xixoqGktBy'

gmaps = googlemaps.Client(fake_api_key)

def init_googlemaps_client():
    gmaps = googlemaps.Client(api_key)
    
def get_location_from_street_name(street_name):
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    

