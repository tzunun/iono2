from math import cos, asin, sqrt
import csv

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def nearest_city(cities_data, epicenter):
    return min(cities_data, key=lambda city: distance(epicenter['latitude'], epicenter['longitude'], city['latitude'], city['longitude']))

def get_cities_data():
    cities = []
    file_name = 'csv_files/world_cities_data.csv'
    
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            cities.append({'city': row[0], 'country': row[1], 'latitude': float(row[2]), 'longitude': float(row[3])})
    
    return cities

# epicenter is a dictionary such as: {'latitude': 20.99223, 'longitude': 23.9002344} and this function returns a dictionary
def epicenter_nearest_city(epicenter):
    cities_data = get_cities_data()
    return nearest_city(cities_data, epicenter)

# Testing the script
epicenter = {'latitude':5.8993 , 'longitude': 129.9209 }
print(epicenter_nearest_city(epicenter))
