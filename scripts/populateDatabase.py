import requests
import json
import psycopg2
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.environ.get('PG_HOST'),
    port=os.environ.get('PG_PORT'),
    database=os.environ.get('PG_DATABASE'),
    user=os.environ.get('PG_USERNAME'),
    password=os.environ.get('PG_PASSWORD')
)

cur = conn.cursor()

beaverton_lat = 45.4871
beaverton_lng = -122.8037
grid_size = 0.25

# Create a list of locations to search
latitudes = np.arange(beaverton_lat - 0.5, beaverton_lat + 0.5, grid_size)
longitudes = np.arange(beaverton_lng - 0.5, beaverton_lng + 0.5, grid_size)

search_locations = []
for lat in latitudes:
    for lng in longitudes:
        search_locations.append((lat, lng))

def insert_restaurant(place_id, name, place_details, url, lat, lng):
    print (f"inserting {name}")
    cur.execute("INSERT INTO restaurants (place_id, name, place_details, url, latitude, longitude) VALUES (%s, %s, %s, %s, %f, %f);", (place_id, name, json.dumps(place_details), url, lat, lng))
    conn.commit()

def insert_photo(place_id, url, photo_reference):
    cur.execute("INSERT INTO photos (place_id, url, photo_reference) VALUES (%s, %s, %s);", (place_id, url, photo_reference))
    conn.commit()

def get_places(lat, lng, next_page_token):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=10000&type=restaurant&key={api_key}"
    if next_page_token:
        url += f"&pagetoken={next_page_token}"
    response = requests.get(url)
    time.sleep(.01)
    data = response.json()
    next_page_token = data.get('next_page_token')
    for place_data in data['results']:
        place_id = place_data['place_id']
        name = place_data['name']
        cur.execute("SELECT * FROM restaurants WHERE place_id = %s", (place_id,))
            id_check = cur.fetchone()
            if id_check:
                print(f"Place with place_id={place_id} already exists in the database. Skipping...")
                continue

        place_details = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}").json()['result']
        time.sleep(.01)
        photos = place_details.get('photos')
        if photos:
            print(f"getting photos for {name}")
            for photo in photos:
                photo_url = requests.get(f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={photo['width']}&photoreference={photo['photo_reference']}&key={api_key}").content
                time.sleep(.01)
                insert_photo(place_id, photo_url, photo['photo_reference'])
        insert_restaurant(place_id, name, place_details, place_details.get('url'), lat, lng)

    if (next_page_token):
        get_places(lat, lng, next_page_token)

for lat, lng in search_locations:
    print(lat,lng)

cur.close()
conn.close()