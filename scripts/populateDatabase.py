import requests
import psycopg2
import numpy as np
import time
from dotenv import load_dotenv
import os

load_dotenv()

# Set up grid search parameters
beaverton_lat = 45.4871
beaverton_lng = -122.8037
grid_size = 0.25

# Create a list of locations to search
latitudes = np.arange(beaverton_lat - 0.5, beaverton_lat + 0.5, grid_size)
longitudes = np.arange(beaverton_lng - 0.5, beaverton_lng + 0.5, grid_size)

locations = []
for lat in latitudes:
    for lng in longitudes:
        locations.append((lat, lng))

print(locations)
print(len(locations))

# Connect to the Postgres database
try:
    conn = psycopg2.connect(
        host=os.environ.get('PG_HOST'),
        port=os.environ.get('PG_PORT'),
        database=os.environ.get('PG_DATABASE'),
        user=os.environ.get('PG_USERNAME'),
        password=os.environ.get('PG_PASSWORD')
    )
    cur = conn.cursor()
except:
    print("Unable to connect to the database")

cur.execute(
    "CREATE TABLE restaurant();"
)
conn.commit()