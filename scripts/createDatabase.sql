CREATE TABLE restaurants (
  id SERIAL PRIMARY KEY,
  place_id VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  place_details JSON,
  url VARCHAR(255),
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL
);

CREATE TABLE photos (
  id SERIAL PRIMARY KEY,
  place_id VARCHAR(255) NOT NULL,
  url VARCHAR(255),
  photo_reference VARCHAR(255),
  FOREIGN KEY (place_id) REFERENCES restaurants(place_id)
);