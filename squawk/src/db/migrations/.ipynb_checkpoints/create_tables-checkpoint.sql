DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS venue_categories;

CREATE TABLE IF NOT EXISTS venues (
  id serial PRIMARY KEY,
  foursquare_id VARCHAR(255) UNIQUE,
  name VARCHAR(255) NOT NULL,
  price INTEGER,
  rating DECIMAL,
  likes BIGINT,
menu_url VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS venues_price_index ON venues (price);


CREATE TABLE IF NOT EXISTS categories (
  id serial PRIMARY KEY,
  name VARCHAR(255) UNIQUE
);


